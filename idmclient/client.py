from modbusclient import ApiWrapper

from .api import DEFAULT_API


class Client(ApiWrapper):
    """Client to access and control SMA units

    Arguments:
        host (str): IPv4 address of the unit
        port (int): Modbus port. Defaults to 502.
        timeout (float): Connection timeout
        unit (int): Unit ID. Defaults to 3.

    Attributes:
        unit (int): Unit ID used in Modbus communication
    """
    def __init__(self, host="", api=DEFAULT_API, unit=1, **kwargs):
        super().__init__(api=api, host=host, unit=unit, **kwargs)
