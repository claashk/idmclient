from modbusclient.asyncio import ApiWrapper

from ..api import DEFAULT_API


class Client(ApiWrapper):
    """Asynchronous client to access and control IDM heat pumps

    Arguments:
        host (str): IPv4 address of the heat pump Modbus interface
        api (dict): API definition. Defaults to `idmclient.api.DEFAULT_API`
        unit (int): Unit ID. Defaults to 1.
        **kwargs: Keyword arguments passed verbatim to
            parent (:class:`modbusclient.asyncio.ApiWrapper`)

    Attributes:
        unit (int): Unit ID used in Modbus communication
        settings (dict): Settings dictionary with message as key and respective
          setting as value. When used in a context manager, all settings in this
          dictionary will be restored upon exit.
    """
    def __init__(self, host=None, api=DEFAULT_API, unit=1, **kwargs):
        super().__init__(api=api, host=host, unit=unit, **kwargs)
