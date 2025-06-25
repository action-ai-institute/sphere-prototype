
"""
swat-s1 plc3
"""

from minicps.devices import PLC
from utils import PLC3_DATA, STATE, PLC3_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
PLC4_ADDR = IP['plc4']
PLANT_ADDR = IP['plant']

DPIT301_3 = ('DPIT301', 3)
LIT301_3 = ('LIT301', 3)
FIT301_3 = ('FIT301', 3)
MV301_3 = ('MV301', 3)
MV302_3 = ('MV302', 3)
MV303_3 = ('MV303', 3)
MV304_3 = ('MV304', 3)
P301_3 = ('P301', 3)
P302_3 = ('P302', 3)
# interlocks to be received from plc4
LIT401_3 = ('LIT401', 3)  # to be sent
LIT401_4 = ('LIT401', 4)  # to be received

class SwatPLC3(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc3 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc3 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

        print 'DEBUG: swat-s1 plc3 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            st = time.time()
            # From plant
            lit301 = self.receive(LIT301_3, PLANT_ADDR)
            dpit301 = self.receive(DPIT301_3,PLANT_ADDR)
            fit301 = self.receive(FIT301_3,PLANT_ADDR)
            mv301 = self.receive(MV301_3,PLANT_ADDR)
            mv302 = self.receive(MV302_3, PLANT_ADDR)
            mv303 = self.receive(MV303_3, PLANT_ADDR)
            mv304 = self.receive(MV304_3, PLANT_ADDR)
            p301 = self.receive(P301_3, PLANT_ADDR)
            p302 = self.receive(P302_3, PLANT_ADDR)
            
            # from PLC4
            lit401 = self.receive(LIT401_4, PLC4_ADDR)
            
            if not lit301:
                print "DEBUG PLC3: can't get lit301 from plant"
                time.sleep(1)
                continue
            lit301 = float(lit301[0][0])
            lit401 = float(lit401[0][0])
            dpit301 = float(dpit301[0][0])
            fit301 = float(fit301[0][0])
            mv301 = int(mv301[0][0])
            mv302 = int(mv302[0][0])
            mv303 = int(mv303[0][0])
            mv304 = int(mv304[0][0])
            p301 = int(p301[0][0])
            p302 = int(p302[0][0])
            print "DEBUG PLC3 - get lit301: %f" % lit301
             
            self.send(LIT301_3, lit301, PLC3_ADDR)
            self.send(LIT401_3, lit401, PLC3_ADDR)
            self.send(DPIT301_3, dpit301, PLC3_ADDR)
            self.send(FIT301_3, fit301, PLC3_ADDR)
            self.send(MV301_3, mv301, PLC3_ADDR)
            self.send(MV302_3, mv302, PLC3_ADDR)
            self.send(MV303_3, mv303, PLC3_ADDR)
            self.send(MV304_3, mv304, PLC3_ADDR)
            self.send(P301_3, p301, PLC3_ADDR)
            self.send(P302_3, p302, PLC3_ADDR)
            
            elapsed = time.time() - st
            print "Finished sending everything in ", str(elapsed), " seconds."

            count += 1
            if elapsed < PLC_PERIOD_SEC:
                time.sleep(PLC_PERIOD_SEC)
            

        print 'DEBUG swat plc3 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc3 = SwatPLC3(
        name='plc3',
        state=STATE,
        protocol=PLC3_PROTOCOL,
        memory=PLC3_DATA,
        disk=PLC3_DATA)
