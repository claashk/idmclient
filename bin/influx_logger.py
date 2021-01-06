#!/usr/bin/env python3
import logging, asyncio, sys, argparse
from copy import deepcopy
import yaml

from vzclient import Service
from vzclient.asyncio import InfluxHub, log_modbus

from idmclient.asyncio import Client
from idmclient.api import MESSAGE_BY_ADDRESS as API
from idmclient.api import find_by_name, DEFAULT_PRECISION


logger = logging.getLogger("influx_logger.py")

CLIENTS = {"modbus.idm": (Client, API)}

DEFAULT_CONFIG = {
    "defaults": {
        "sampling_interval": 30,
        "interpolate": True,
        "max_gap": 7200,
        "precision": "auto",
        "measurement": "volkszaehler",
        "tags": {
            "title": "auto",
            "type": "auto",
            "unit": "auto",
            "uuid": "auto"
        },
        "field_name": "value",
        "source": {
            "driver": 'modbus.idm',
            "host": "192.168.10.1",
            "device_id": "idm-aero-ilm-12346.home"
        }
    },
    "destination": {
        "driver": 'influx',
        "host": "192.168.10.1",
        "bucket": "volkszaehler",
        "org": "volkszaehler",
        "secret": "",
        "buffer_size": 1000000,
        "max_buffer_age": 30,
        "max_retries": 5
    },
    "logs": ["*"]
}


def parse_yaml(path):
    """Parse yaml configuration file

    Arguments:
        path (str): Path to config file

    Return:
        tuple: Three dictionaries containing default options, default source
        options and
    """
    cfg = deepcopy(DEFAULT_CONFIG)

    with open(path) as cfg_file:
        yaml_cfg = yaml.load(cfg_file, Loader=yaml.SafeLoader)

    defaults = cfg.pop('defaults', dict())
    yaml_defaults = yaml_cfg.pop('defaults', dict())

    src = defaults.pop("source", dict())
    src.update(yaml_defaults.pop("source", dict()))

    defaults.update(yaml_defaults)

    dest = cfg.pop('destination', dict())
    dest.update(yaml_cfg.pop("destination", dict()))

    logs = yaml_cfg.pop("logs", cfg.pop('logs', ['*']))

    log_streams = []
    for i, log in enumerate(logs, 1):
        log_cfg = deepcopy(defaults)
        log_src = deepcopy(src)
        if isinstance(log, dict):
            log_src.update(log.pop('source', dict()))
            log_cfg.update(log)
            message = log_cfg.pop('address', None)
            name = log_cfg.pop('name', None)
        else:
            try:
                message = int(log)
                name = None
            except ValueError:
                message = None
                name = str(log)

        driver = log_src.get('driver', None)
        if driver not in CLIENTS.keys():
            raise ValueError(f"In log {i}: Invalid driver: '{driver}'")
        client, api = CLIENTS[driver]

        log_cfg.update(log_src)

        if message is None and name is None:
            logger.warning(f"In log {i}: Found neither address nor name. "
                           "Ignoring this log")
            continue

        if message is not None:
            if name is not None:
                logger.warning(f"In log {i}: Found address and name: Ignoring "
                               "name")
            messages = [api[message]]
        else:
            messages = list(find_by_name(name))

        for msg in messages:
            log_stream = deepcopy(log_cfg)
            log_stream['message'] = int(msg.address)
            if log_stream.get('precision', 'auto') == 'auto':
                precision = DEFAULT_PRECISION.get(msg.sensor_type, None)
                log_stream['precision'] = precision
            max_gap = log_stream.pop("max_gap", None)
            if max_gap and int(max_gap) > 0:
                log_stream['max_gap'] = int(max_gap)
            logger.debug(f"Found config for {msg.name} ({msg.address})")
            log_streams.append(log_stream)

    assert not cfg

    return dest, log_streams


def configure(args=None):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
                 description="Log IDM modbus data to Influx DB")

    parser.add_argument("--logfile", "-l",
                        help="Path to logfile. If not specified, log goes to "
                             "stderr")

    parser.add_argument("--verbose", "-v",
                        help="Set verbose mode. Use more often to increase log "
                        "level",
                        action='count', default=0)

    parser.add_argument("path",
                        help="Path to yaml configuration file",
                        nargs=1)

    config = parser.parse_args(args)

    if config.verbose == 0:
        log_level = logging.WARNING
        lib_log_level = logging.WARNING
    elif config.verbose == 1:
        log_level = logging.INFO
        lib_log_level = logging.WARNING
    elif config.verbose == 2:
        log_level = logging.DEBUG
        lib_log_level = logging.INFO
    else:
        log_level = logging.DEBUG
        lib_log_level = logging.DEBUG

    if config.logfile:
        logging.basicConfig(level=log_level, filename=config.logfile)
    else:
        logging.basicConfig(level=log_level)

    logging.getLogger("modbusclient").setLevel(lib_log_level)

    return parse_yaml(config.path[0])


async def main():
    dest, logs = configure()

    dest_driver = dest.pop('driver')
    if dest_driver != "influx":
        raise ValueError(f"Invalid destination driver {dest_driver}")

    buffer_size = dest.pop('buffer_size', 1000000)
    max_buffer_age = int(1000 * dest.pop('max_buffer_age'))
    max_retries = int(dest.pop('max_retries'))
    hub = InfluxHub(buffer_size=buffer_size,
                    max_buffer_age=max_buffer_age,
                    max_retries=max_retries)

    with Service() as service:
        hub.connect_writer(**dest)
        for log in logs:
            client, api = CLIENTS[log.pop('driver')]
            log_modbus(hub, client=client, api=api, **log)

        while service.run:
            await asyncio.sleep(3)
    await hub.stop()
    return


if __name__ == '__main__':
    exitCode = 1
    try:
        loop = asyncio.get_event_loop()
        # loop.set_debug(True)
        loop.run_until_complete(main())
        loop.close()
        exitCode = 0
    except Exception as ex:
        logger.exception(f"{ex}")
    except SystemExit as ex:
        exitCode = ex.code
    except:
        logger.exception("Unknown error")

    state = "successfully"
    if exitCode:
        state = "abnormally"
    logger.error("Program terminated %s\n", state)
    sys.exit(exitCode)

