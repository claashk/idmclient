import asyncio
from modbusclient.asyncio import ComponentBase
from vzclient.asyncio import VzLoggerCodec
from vzclient import Power
from ..api import MESSAGE_BY_ADDRESS


PV_MESSAGE = MESSAGE_BY_ADDRESS[74]


class Controller(ComponentBase):
    """Autobahn Component relaying current PV output to IDM heat pump

    The controller derives from

    Arguments:
        client (:class:`modbusclient.asyncio.ApiWrapper`): API wrapper. Passed
            verbatim to parent :class:`modbusclient.asyncio.ComponentBase`.
        wamp_host (str): URL of Autobahn / WAMP router to connect to. Passed
            verbatim to parent :class:`modbusclient.asyncio.ComponentBase`
        wamp_realm (str): WAMP realm to connect to. Passed verbatim to
            parent :class:`modbusclient.asyncio.ComponentBase`.
        channel (str): Name of channel used to receive current PV output
        message (Payload): Modbus message used to send PV information to
            heat pump.
        with_timestamp (bool): Indicates, whether PV messages contain a timestamp
           or not. Passed verbatim to :class:`vzclient.asyncio.VzLoggerCodec`.
           Defaults to ``False``.
    """
    def __init__(self,
                 client,
                 wamp_host,
                 wamp_realm,
                 channel='vzlogger.data.chn1.agg',
                 message=PV_MESSAGE,
                 with_timestamp=False):
        super().__init__(transports=wamp_host, realm=wamp_realm, client=client)
        self._channel = channel
        self._message = message
        self._with_timestamp = with_timestamp
        self._power = Power()

    async def _join(self, session, details):
        """Coroutine invoked on each join by Autobahn

        Arguments:
            session (:class:`autobahn.wamp.protocol.ApplicationSession`):
                Application session.
            details (dict): Dictionary with details.
        """
        await super()._join(session, details)
        codec = VzLoggerCodec(with_timestamp=self._with_timestamp)
        self.session.set_payload_codec(codec)
        await self._session.subscribe(self.update_pv_power, self._channel)

    async def update_pv_power(self, reading=-1., uri="", timestamp=None):
        """Update available PV Power

         The keyword arguments are defined in VzLoggerCodec and are extracted
         there from the MQTT messages sent by vzlogger.
         """
        self.debug(f"2.8.0 update: reading={reading}, timestamp={timestamp}")

        p = self._power(reading, timestamp)

        if timestamp is None:
            self.debug("Set missing timestamp to {timestamp} s",
                       timestamp=self._power.timestamp)

        if p is not None:
            try:
                async with self._client:
                    pwr = await self._client.set(self._message, p)
                    self.info(f"Set available PV power to {pwr} kW")
            except OSError as ex:
                self.error(f"While setting PV power: {ex}")

    async def _leave(self, session, reason):
        """Coroutine invoked on each leave by Autobahn"""
        self._client.disconnect()
        await super()._leave(session, reason)


class Monitor(ComponentBase):
    """This is just a stub that does nothing yet."""

    def __init__(self, client, wamp_host, wamp_realm):
        super().__init__(transports=wamp_host, realm=wamp_realm, client=client)
        self._monitor_active = False

    async def _join(self, session, details):
        """

        Arguments:
            session (:class:`autobahn.wamp.protocol.ApplicationSession`):
                Application session.
            details (dict): Dictionary with details.

        """
        await super()._join(session, details)
        self._monitor_active = True
        asyncio.ensure_future(self.monitor())

    async def monitor(self):
        while self._monitor_active:
            self.info("Invoked monitoring")
            await asyncio.sleep(5.)

    async def _leave(self, session, reason):
        self._monitor_active = False
        await super()._leave(session, reason)
