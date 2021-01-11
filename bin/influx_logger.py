#!/usr/bin/env python3
import logging, sys

from modbusclient import iter_payloads

from vzclient.asyncio import InfluxLogger as LoggerBase

from idmclient.asyncio import Client
from idmclient.api import MESSAGE_BY_ADDRESS as API
from idmclient.api import DEFAULT_PRECISION


class InfluxLogger(LoggerBase):
    def __init__(self):
        super().__init__(logger=logging.getLogger(),
                         description="Log IDM modbus data to Influx DB")
        self.third_party_libs.append("modbusclient")

    def iter_channels(self, driver, channels):
        """Iterate over all channels for a specific driver

        Arguments:
            driver (str): Driver name.
            channels (iterable): Iterable of channels

        Yield:
        """
        api = self.get_modbus_api(driver)
        yield from iter_payloads(messages=channels, api=api, key_type=int)

    def get_modbus_api(self, driver):
        """Get Modbus API definition for a driver

        Needs to be implemented by derived class

        Arguments:
            driver (str): Driver name

        Return:
            dict: Modbus API definition
        """
        if driver == "modbus.idm":
            return API
        raise ValueError(f"Unknown driver: '{driver}'")

    def get_client(self, driver):
        if driver == "modbus.idm":
            return Client
        raise ValueError(f"Unknown driver: '{driver}'")

    def get_precision(self, driver, channel):
        """Get default precision for a channel depending on the driver

        Arguments:
            driver (str): Driver
            channel: Channel information. Type depends on driver.

        Return:
            int: Default channel precision
        """
        sensor_type = self.get_sensor_type(driver, channel)
        return DEFAULT_PRECISION.get(sensor_type, None)


InfluxLogger.default_config.update({
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
        "buffer_size": 100000,
        "max_buffer_age": 30,
        "max_retries": 5
    },
    "logs": ["*"]
})



if __name__ == '__main__':
    tool = InfluxLogger()
    sys.exit(tool.run())
