from modbusclient import Payload
from .data_types import FLOAT, WORD

#from https://beyer-tom.de/blog/2019/01/heatpump-idm-terra-ml-complete-hgl-modbus-adresses/
#
# 01 	1000 	3E8 	FLOAT 	Außentemperatur 	°C
# 02 	1002 	3EA 	FLOAT 	Wärmepumpen Vorlauftemperatur 	°C
# 03 	1004 	3EC 	FLOAT 	HGL Vorlauftemperatur 	°C
# 04 	1006 	3EE 	FLOAT 	Wärmequellenaustrittstemperatur 	°C
# 05 	1008 	3F0 	FLOAT 	Wärmepumpen Rücklauftemperatur / Wärmespeichertemperatur 	°C
# 06 	1010 	3F2 	FLOAT 	Kältespeichertemperatur 	°C
# 07 	1012 	3F4 	FLOAT 	Trinkwassererwärmertemperatur 	°C
# 08 	1014 	3F6 	FLOAT 	Frischwasserzapftemperatur 	°C
# 09 	1016 	3F8 	FLOAT 	Heizkreis A Vorlauftemperatur 	°C
# 10 	1018 	3FA 	FLOAT 	Heizkreis B Vorlauftemperatur 	°C
# 11 	1020 	3FC 	FLOAT 	Heizkreis C Vorlauftemperatur 	°C
# 12 	1022 	3FE 	FLOAT 	Heizkreis D Vorlauftemperatur 	°C
# 13 	1024 	400 	FLOAT 	Heizkreis E Vorlauftemperatur 	°C
# 14 	1026 	402 	FLOAT 	Heizkreis F Vorlauftemperatur 	°C
# 15 	1028 	404 	FLOAT 	Heizkreis G Vorlauftemperatur 	°C
# 16 	1030 	406 	FLOAT 	Heizkreis A Raumgerät 	°C
# 17 	1032 	408 	FLOAT 	Heizkreis B Raumgerät 	°C
# 18 	1034 	40A 	FLOAT 	Heizkreis C Raumgerät 	°C
# 19 	1036 	40C 	FLOAT 	Heizkreis D Raumgerät 	°C
# 20 	1038 	40E 	FLOAT 	Heizkreis E Raumgerät 	°C
# 21 	1040 	410 	FLOAT 	Heizkreis F Raumgerät 	°C
# 22 	1042 	412 	FLOAT 	Heizkreis G Raumgerät 	°C
# 23 	1044 	414 	FLOAT 	Heissgastemperatur 	°C
# 24 	1046 	416 	FLOAT 	Feuchtesensor 	% r.F.
# 25 	1048 	418 	FLOAT 	Luftansaugtemperatur 	°C
# 26 	1050 	41A 	FLOAT 	Luftwärmetauschertemperatur 	°C
# 27 	1052 	41C 	FLOAT 	Solar Kollektortemperatur 	°C
# 28 	1054 	41E 	FLOAT 	Solar Ladetemperatur 	°C
# 29 	1056 	420 	FLOAT 	Solar Kollektorrücklauftemperatur 	°C
# 30 	1058 	422 	FLOAT 	Solar Wärmequellenreferenztemperatur / Pooltemperatur 	°C
# 31 	1060 	424 	FLOAT 	Gemittelte Aussentemperatur 	°C
# 32 	1062 	426 	FLOAT 	Wärmequelleneintritsstemperatur 	°C
# 33 	1064 	428 	FLOAT 	IDM Systemkühlung - Ladefühler Kühlen 	°C
# 34 	1066 	42A 	FLOAT 	IDM Systemkühlung - Rückkühlfühler 	°C
# 35 	1068 	42C 	FLOAT 	Wärmemenge Wärmepumpenvorlauf (bei Navigator 1.0) 	kW
# 36 	1070 	42E 	FLOAT 	Wärmemenge HGL-Vorlauf (bei Navigator 1.0) 	kW
# 37 	1072 	430 	FLOAT 	Wärmemenge Momentanleistung 	kW
# 38 	1074 	432 	FLOAT 	Wärmemenge Solar 	kW
# 39 	1076 	434 	FLOAT 	Wärmemenge gesamt (bei Navigator 1.0) 	kWh
# 40 	1078 	436 	FLOAT 	Wärmemenge Heizen gesamt 	kWh
# 41 	1080 	438 	FLOAT 	Wärmemenge HGL gesamt (bei Navigator 1.0) 	kWh
# 42 	1082 	43A 	FLOAT 	Wärmemenge Kühlen gesamt 	kWh
# 43 	1084 	43C 	FLOAT 	Wärmemenge Solar gesamt 	kWh
# 44 	1086 	43E 	FLOAT 	Summe Durchflussmengenzähler Grundwasserpumpe (bei TERRA SW Max mit Navigator 1.7)
# 45 	1088 	440 	FLOAT 	Betriebsstundenzähler Wärmequellenpumpe (bei Grundwasseranlagen)
# 46 	1500 	5DC 	UCHAR 	Aktuelle Störungsnummer
# 47 	1501 	5DD 	UCHAR 	Betriebsart Wärmepumpe (0=AUS / 1=Heizen / 2=Kühlen / 4=Vorrang / 8=Abtauen)
# 48 	1502 	5DE 	UCHAR 	Status Heizkreis A
# 49 	1503 	5DF 	UCHAR 	Status Heizkreis A (kein Heizkreis B bei Navigator 1.7)
# 50 	1504 	5E0 	UCHAR 	Status Heizkreis C
# 51 	1505 	5E1 	UCHAR 	Status Heizkreis D
# 52 	1506 	5E2 	UCHAR 	Status Heizkreis E
# 53 	1507 	5E3 	UCHAR 	Status Heizkreis F
# 54 	1508 	5E4 	UCHAR 	Status Heizkreis G
# 55 	1509 	5D5 	UCHAR 	Status Verdichter 1 (0=Aus / 1=Ein)
# 56 	1510 	5D6 	UCHAR 	Status Verdichter 2
# 57 	1511 	5E7 	UCHAR 	Status Verdichter 3
# 58 	1512 	5E8 	UCHAR 	Status Verdichter 4
# 59 	1513 	5E9 	UCHAR 	Status Ladepumpe (0=Aus / 1=Betrieb / 2=Störung)
# 60 	1514 	5EA 	UCHAR 	Status Wärmequellenpumpe
# 61 	1515 	5EB 	UCHAR 	Status Zwischenkreispumpe
# 62 	1516 	5EC 	UCHAR 	Status ISC Kältespeicherpumpe
# 63 	1517 	5ED 	UCHAR 	Status ISC Rückkühlpumpe
# 64 	1518 	5EE 	UCHAR 	Anzahl laufende Verdichterstufen Heizen gesamt
# 65 	1519 	5EF 	UCHAR 	Anzahl laufende Verdichterstufen Kühlen gesamt
# 66 	1520 	5F0 	UCHAR 	Anzahl laufende Verdichterstufen Vorrang gesamt
# 67 	1521 	5F1 	UCHAR 	Betriebsart Kaskade
# 68 	1522 	5F2 	UCHAR 	Betriebsart Solar
# 69 	1523 	5F3 	UCHAR 	Smart Grid Status
# 70 	1524 	5F4 	UCHAR 	IDM Systemkühlung (ISC) Modus

MESSAGES = [
    Payload(FLOAT, 74, name="Available PV Power", units="kW", mode='rw'),
    Payload(FLOAT, 1000, name="Outside Air Temperature", units="°C"),
    Payload(FLOAT, 1002, name="Mean Outside Air Temperature", units="°C"),
    Payload(FLOAT, 1008, name="Heat Store Temperature", units="°C"),
    Payload(FLOAT, 1012, name="Tap Water Heater Bottom Temperature", units="°C"),
    Payload(FLOAT, 1014, name="Tap Water Heater Top Temperature", units="°C"),
    Payload(FLOAT, 1030, name="Tap Water Temperature", units="°C"),
    Payload(FLOAT, 1050, name="Heat Pump Flow Temperature", units="°C"),
    Payload(FLOAT, 1052, name="Heat Pump Return Temperature", units="°C"),
    Payload(FLOAT, 1054, name="HGL Flow Temperature", units="°C"),
    Payload(FLOAT, 1056, name="Heat Source Inlet Temperature", units="°C"),  # n.a
    Payload(FLOAT, 1058, name="Heat Source Outlet Temperature", units="°C"), # n.a
    Payload(FLOAT, 1060, name="Air Inlet Temperature", units="°C"),
    Payload(FLOAT, 1062, name="Air Heat Exchanger Temperature", units="°C"), # n.a.
    Payload(FLOAT, 1064, name="Air Inlet Temperature 2", units="°C"),
    Payload(WORD,  1112, name="Tap Water / Heater Switch", units="1"),
    Payload(FLOAT, 1350, name="Heating Circuit A Flow Temperature", units="°C"),
    Payload(FLOAT, 1364, name="Heating Circuit A Room Temperature", units="°C"),
    Payload(FLOAT, 1378, name="Heating Circuit A Temperature Setpoint", units="°C"),
    Payload(FLOAT, 1392, name="Relative Humidity Sensor", units="%"),
    Payload(WORD,  1498, name="Heating Circuit A Mode", units="1"),
    Payload(FLOAT, 1750, name="Heater Heat Supply", units="kWh"),
    Payload(FLOAT, 1752, name="Cooler Heat Supply", units="kWh"),
    Payload(FLOAT, 1754, name="Tap Water Heat Supply", units="kWh"),
    Payload(FLOAT, 1756, name="De-ice Heat Supply", units="kWh"),
    Payload(FLOAT, 1790, name="Current Power Consumption", units="kW"),
    Payload(FLOAT, 1792, name="Current Solar Power Production", units="kW"),
    Payload(FLOAT, 4122, name="Current Power Consumption", units="kW")
]

MESSAGE_BY_ADDRESS = {m.address: m for m in MESSAGES}
MESSAGE_BY_NAME = {m.name: m for m in MESSAGES}

MESSAGE_BY_FUNC_NAME = {key : MESSAGE_BY_ADDRESS[val] for key,val in [
    ("pv_output", 74),
    ("outside_air_temp", 1000),
    ("mean_outside_air_temp", 1002),
    ("heat_store_temp", 1008),
    ("bottom_tap_water_heater_temp", 1012),
    ("top_tap_water_heater_temp", 1014),
    ("tap_water_temp", 1030),
    ("power_cosumption", 4122)
]}

DEFAULT_API = MESSAGE_BY_NAME

