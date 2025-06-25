"""
swat-s1 utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores
values as strings.

Actuator tags are redundant, we will use only the XXX_XXX_OPEN tag ignoring
the XXX_XXX_CLOSE with the following convention:
    - 0 = error
    - 1 = off
    - 2 = on

sqlite uses float keyword and cpppo use REAL keyword.
"""
'''
from minicps.utils import build_debug_logger

swat = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')
'''

# physical process {{{1
# SPHINX_SWAT_TUTORIAL PROCESS UTILS(
GRAVITATION = 9.81             # m.s^-2
TANK_DIAMETER = 1.38           # m
TANK_SECTION = 1.5             # m^2
PUMP_FLOWRATE_IN = 2.55        # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 2.45       # m^3/h spec say btw 2.2 and 2.4

# periods in msec
# R/W = Read or Write
T_PLC_R = 100E-3
T_PLC_W = 100E-3

T_PP_R = 200E-3
T_PP_W = 200E-3
T_HMI_R = 100E-3

# ImageTk
DISPLAYED_SAMPLES = 14

# Control logic thresholds
LIT_101_MM = {  # raw water tank mm
    'LL': 250.0,
    'L': 500.0,
    'H': 800.0,
    'HH': 1200.0,
}
LIT_101_M = {  # raw water tank m
    'LL': 0.250,
    'L': 0.500,
    'H': 0.800,
    'HH': 1.200,
}

LIT_301_MM = {  # ultrafiltration tank mm
    'LL': 250.0,
    'L': 800.0,
    'H': 1000.0,
    'HH': 1200.0,
}
LIT_301_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.800,
    'H': 1.000,
    'HH': 1.200,
}

TANK_HEIGHT = 1.600  # m

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.20  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

RWT_INIT_LEVEL = 0.500  # l

# m^3 / h
FIT_201_THRESH = 1.00
# SPHINX_SWAT_TUTORIAL PROCESS UTILS)

# topo {{{1
IP = {
    'plc1': '10.0.0.1',
    'plc2': '10.0.1.1',
    'plc3': '10.0.2.1',
    'plc4': '10.0.3.1',
    'plc5': '10.0.4.1',
    'plc6': '10.0.5.1',
    'scada':'10.0.0.1',
    'plant':'plant',
    'attacker': '10.0.0.4',
}

NETMASK = '/24'

MAC = {
    'plc1': '00:1D:9C:C7:B0:70',
    'plc2': '00:1D:9C:C8:BC:46',
    'plc3': '00:1D:9C:C8:BD:F2',
    'plc4': '00:1D:9C:C7:FA:2C',
    'plc5': '00:1D:9C:C8:BC:2F',
    'plc6': '00:1D:9C:C7:FA:2D',
    'attacker': 'AA:AA:AA:AA:AA:AA',
}


# others
# TODO
PLC1_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC2_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC3_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC4_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC5_DATA = {
    'TODO': 'TODO',
}
# TODO
PLC6_DATA = {
    'TODO': 'TODO',
}


# SPHINX_SWAT_TUTORIAL PLC1 UTILS(
PLC1_ADDR = IP['plc1']
PLC1_TAGS = (
    ('FIT101', 1, 'REAL'),
    ('MV101', 1, 'INT'),
    ('LIT101', 1, 'REAL'),
    ('P101', 1, 'INT'),
    # interlocks does NOT go to the statedb
    ('FIT201', 1, 'REAL'),
    ('MV201', 1, 'INT'),
    ('LIT301', 1, 'REAL'),
)
PLC1_SERVER = {
    'address': PLC1_ADDR,
    'tags': PLC1_TAGS
}
PLC1_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC1_SERVER
}
# SPHINX_SWAT_TUTORIAL PLC1 UTILS)

PLC2_ADDR = IP['plc2']
PLC2_TAGS = (
    ('FIT201', 2, 'REAL'),
    ('MV201', 2, 'INT'),
    ('AIT201', 2, 'REAL'),
    ('AIT202', 2, 'REAL'),
    ('AIT203', 2, 'REAL'),
    ('CT201', 2, 'REAL'), # Chem tank NaCl
    ('CT202', 2, 'REAL'), # Chem tank HCl
    ('CT203', 2, 'REAL'), # Chem tank NaOCl
    ('P201', 2, 'INT'),   # Pump tank NaCl
    ('P202', 2, 'INT'),   # Pump tank NaCl
    ('P203', 2, 'INT'),   # Pump tank HCl
    ('P204', 2, 'INT'),   # Pump tank HCl
    ('P205', 2, 'INT'),   # Pump tank NaOCl
    ('P206', 2, 'INT'),   # Pump tank NaOCl
    # no interlocks
)
PLC2_SERVER = {
    'address': PLC2_ADDR,
    'tags': PLC2_TAGS
}
PLC2_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC2_SERVER
}

PLC3_ADDR = IP['plc3']
PLC3_TAGS = (
    ('LIT301', 3, 'REAL'),
    ('DPIT301', 3, 'REAL'),
    ('LIT301', 3, 'REAL'),
    ('FIT301', 3, 'REAL'),
    ('MV301', 3, 'INT'),
    ('MV302', 3, 'INT'),
    ('MV303', 3, 'INT'),
    ('MV304', 3, 'INT'),
    ('P301', 3, 'INT'),
    ('P302', 3, 'INT'),
    # no interlocks
)
PLC3_SERVER = {
    'address': PLC3_ADDR,
    'tags': PLC3_TAGS
}
PLC3_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC3_SERVER
}

PLC4_ADDR = IP['plc4']
PLC4_TAGS = (
    ('AIT401', 4, 'REAL'),
    ('AIT402', 4, 'REAL'),
    ('FIT401', 4, 'REAL'),
    ('LIT401', 4, 'REAL'),
    ('P401', 4, 'INT'),
    ('P402', 4, 'INT'),
    ('P403', 4, 'INT'),
    ('P404', 4, 'INT'),
    ('UV401', 4, 'INT'),
    # no interlocks
)
PLC4_SERVER = {
    'address': PLC4_ADDR,
    'tags': PLC4_TAGS
}
PLC4_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC4_SERVER
}

PLC5_ADDR = IP['plc5']
PLC5_TAGS = (
    ('AIT501', 5, 'REAL'),
    ('AIT502', 5, 'REAL'),
    ('AIT503', 5, 'REAL'),
    ('AIT504', 5, 'REAL'),
    ('FIT501', 5, 'REAL'),
    ('FIT502', 5, 'REAL'),
    ('FIT503', 5, 'REAL'),
    ('FIT504', 5, 'REAL'),
    ('P501', 5, 'INT'),
    ('P502', 5, 'INT'),
    ('PIT501', 5, 'REAL'),
    ('PIT502', 5, 'REAL'),
    ('PIT503', 5, 'REAL'),
    # no interlocks
)
PLC5_SERVER = {
    'address': PLC5_ADDR,
    'tags': PLC5_TAGS
}
PLC5_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC5_SERVER
}

PLC6_ADDR = IP['plc6']
PLC6_TAGS = (
    ('FIT601', 6, 'REAL'),
    ('P601', 6, 'INT'),
    ('P602', 6, 'INT'),
    ('P603', 6, 'INT'),
    # no interlocks
)
PLC6_SERVER = {
    'address': PLC6_ADDR,
    'tags': PLC6_TAGS
}
PLC6_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC6_SERVER
}

PLANT_ADDR = IP['plant']
# The plant will have all the tags since it will report sensor values and update state.
PLANT_TAGS = (
    ('LIT101', 1, 'REAL'),
    ('P101',1,'REAL'),
    ('MV101',1,'REAL'),
    ('LIT301',3,'REAL'),
    ('FIT201',2,'REAL'),
    ('FIT101',1,'REAL'),
    ('FIT201', 2, 'REAL'),
    ('MV201', 2, 'INT'),
    ('AIT201', 2, 'REAL'),
    ('AIT202', 2, 'REAL'),
    ('AIT203', 2, 'REAL'),
    
    ('CT201', 2, 'REAL'), # Chem tank NaCl
    ('CT202', 2, 'REAL'), # Chem tank HCl
    ('CT203', 2, 'REAL'), # Chem tank NaOCl
    ('P201', 2, 'INT'),   # Pump tank NaCl
    ('P202', 2, 'INT'),   # Pump tank NaCl
    ('P203', 2, 'INT'),   # Pump tank HCl
    ('P204', 2, 'INT'),   # Pump tank HCl
    ('P205', 2, 'INT'),   # Pump tank NaOCl
    ('P206', 2, 'INT'),   # Pump tank NaOCl
    ('DPIT301', 3, 'REAL'),
    ('FIT301', 3, 'REAL'),
    ('MV301', 3, 'INT'),
    ('MV302', 3, 'INT'),
    ('MV303', 3, 'INT'),
    ('MV304', 3, 'INT'),
    ('P301', 3, 'INT'),
    ('P302', 3, 'INT'),
    ('AIT401', 4, 'REAL'),
    ('AIT402', 4, 'REAL'),
    ('FIT401', 4, 'REAL'),
    ('LIT401', 4, 'REAL'),
    ('P401', 4, 'INT'),
    ('P402', 4, 'INT'),
    ('P403', 4, 'INT'),
    ('P404', 4, 'INT'),
    ('UV401', 4, 'INT'),
    ('AIT501', 5, 'REAL'),
    ('AIT502', 5, 'REAL'),
    ('AIT503', 5, 'REAL'),
    ('AIT504', 5, 'REAL'),
    ('FIT501', 5, 'REAL'),
    ('FIT502', 5, 'REAL'),
    ('FIT503', 5, 'REAL'),
    ('FIT504', 5, 'REAL'),
    ('P501', 5, 'INT'),
    ('P502', 5, 'INT'),
    ('PIT501', 5, 'REAL'),
    ('PIT502', 5, 'REAL'),
    ('PIT503', 5, 'REAL'),
    ('FIT601', 6, 'REAL'),
    ('P601', 6, 'INT'),
    ('P602', 6, 'INT'),
    ('P603', 6, 'INT'),
    # no interlocks
)
PLANT_SERVER = {
    'address': PLANT_ADDR,
    'tags': PLANT_TAGS
}
PLANT_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLANT_SERVER
}

# state {{{1
# SPHINX_SWAT_TUTORIAL STATE(
PATH = 'swat_s1_db.sqlite'
NAME = 'swat_s1'

STATE = {
    'name': NAME,
    'path': PATH
}
# SPHINX_SWAT_TUTORIAL STATE)

SCHEMA = """
CREATE TABLE swat_s1 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO swat_s1 VALUES ('FIT101',   1, '2.55');
    INSERT INTO swat_s1 VALUES ('MV101',    1, '0');
    INSERT INTO swat_s1 VALUES ('LIT101',   1, '0.500');
    INSERT INTO swat_s1 VALUES ('P101',     1, '1');

    INSERT INTO swat_s1 VALUES ('FIT201',   2, '2.45');
    INSERT INTO swat_s1 VALUES ('MV201',    2, '0');

    INSERT INTO swat_s1 VALUES ('LIT301',   3, '0.500');
"""
REAL_DATA_PATH = './real-swat-data/SWaT_Dataset_Normal_v1.csv'
