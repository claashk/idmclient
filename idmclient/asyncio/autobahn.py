import asyncio
from modbusclient.asyncio import ComponentBase
from vzclient.asyncio import VzLoggerCodec
from vzclient import Power
from ..api import MESSAGE_BY_ADDRESS


PV_MESSAGE = MESSAGE_BY_ADDRESS[74]


class Controller(ComponentBase):

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
        """

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
        self.debug("2.8.0 update: reading={reading}, timestamp={timestamp}",
                   reading=reading, timestamp=timestamp)

        p = self._power(reading, timestamp)

        if timestamp is None:
            self.debug("Set missing timestamp to {timestamp} s",
                       timestamp=self._power.timestamp)

        if p is not None:
            try:
                pwr = await self._client.set(self._message, p)
                self.info("Setting available PV power to {power} kW", power=pwr)
            except OSError as ex:
                self.error("While setting PV power: {err}", err=str(ex))

    async def _leave(self, session, reason):
        self._client.disconnect()
        await super()._leave(session, reason)


class Monitor(ComponentBase):

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
