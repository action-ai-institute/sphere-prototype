"""
swat-s1 plc6.py
"""

from minicps.devices import PLC
from utils import PLC4_DATA, STATE, PLC4_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M, LIT_301_M, FIT_201_THRESH

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
PLC4_ADDR = IP['plc4']
PLC5_ADDR = IP['plc5']
PLANT_ADDR = IP['plant']


AIT401_4 = ('AIT401', 4)
AIT402_4 = ('AIT402', 4)
FIT401_4 = ('FIT401', 4)
LIT401_4 = ('LIT401', 4)
P401_4 = ('P401', 4)
P402_4 = ('P402', 4)
P403_4 = ('P403', 4)
P404_4 = ('P404', 4)
UV401_4 = ('UV401', 4)

# interlocks to be received from plc5 and plc2
P501_4 = ('P501', 4)  # to be sent
P501_5 = ('P501', 5)  # to be received
P502_4 = ('P502', 4)  # to be sent
P502_5 = ('P502', 5)  # to be received
P205_4 = ('P205', 4)  # to be sent
P205_2 = ('P205', 2)  # to be received
P206_4 = ('P206', 4)  # to be sent
P206_2 = ('P206', 2)  # to be received
# SPHINX_SWAT_TUTORIAL PLC4 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatPLC4(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc4 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc4 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc4 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            st = time.time()
            # From plant
            ait401 = self.receive(AIT401_4, PLANT_ADDR)
            ait402 = self.receive(AIT402_4,PLANT_ADDR)
            fit401 = self.receive(FIT401_4,PLANT_ADDR)
            lit401 = self.receive(LIT401_4,PLANT_ADDR)
            p401 = self.receive(P401_4, PLANT_ADDR)
            p402 = self.receive(P402_4, PLANT_ADDR)
            p403 = self.receive(P403_4, PLANT_ADDR)
            p404 = self.receive(P404_4, PLANT_ADDR)
            uv401 = self.receive(UV401_4, PLANT_ADDR)
            
            # From interlocks
            p501 = self.receive(P501_5, PLC5_ADDR)
            p502 = self.receive(P502_5, PLC5_ADDR)
            p205 = self.receive(P205_2, PLC2_ADDR)
            p206 = self.receive(P206_2, PLC2_ADDR)

            if not ait401:
                print "DEBUG PLC4: can't get ait401 from plant"
                time.sleep(1)
                continue
            ait401 = float(ait401[0][0])
            ait402 = float(ait402[0][0])
            fit401 = float(fit401[0][0])
            lit401 = float(lit401[0][0])
            p401 = int(p401[0][0])
            p402 = int(p402[0][0])
            p403 = int(p403[0][0])
            p404 = int(p404[0][0])
            uv401 = int(uv401[0][0])
            p501 = int(p501[0][0])
            p502 = int(p502[0][0])
            p205 = int(p205[0][0])
            p206 = int(p206[0][0])
            
            print "DEBUG PLC4 - get lit401: %f" % lit401  
            
            self.send(AIT401_4, ait401, PLC4_ADDR)
            self.send(AIT402_4, ait402, PLC4_ADDR)
            self.send(FIT401_4, fit401, PLC4_ADDR)
            self.send(LIT401_4, lit401, PLC4_ADDR)
            self.send(P401_4, p401, PLC4_ADDR)
            self.send(P402_4, p402, PLC4_ADDR)
            self.send(P403_4, p403, PLC4_ADDR)
            self.send(P404_4, p404, PLC4_ADDR)
            self.send(UV401_4, uv401, PLC4_ADDR)
            self.send(P501_4, p501, PLC4_ADDR)
            self.send(P502_4, p502, PLC4_ADDR)
            self.send(P205_4, p205, PLC4_ADDR)
            self.send(P206_4, p206, PLC4_ADDR)
            elapsed = time.time() - st
            print "Finished sending everything in ", str(elapsed), " seconds."

            count += 1
            if elapsed < PLC_PERIOD_SEC:
                time.sleep(PLC_PERIOD_SEC)

        print 'DEBUG swat plc4 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc6 = SwatPLC4(
        name='plc4',
        state=STATE,
        protocol=PLC4_PROTOCOL,
        memory=PLC4_DATA,
        disk=PLC4_DATA)
