"""
swat-s1 plc6.py
"""

from minicps.devices import PLC
from utils import PLC6_DATA, STATE, PLC6_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M, LIT_301_M, FIT_201_THRESH

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
PLC6_ADDR = IP['plc6']
PLANT_ADDR = IP['plant']

FIT601_6 = ('FIT601', 6)
P601_6 = ('P601', 6)
P602_6 = ('P602', 6)
P603_6 = ('P603', 6)

# no interlocks

# SPHINX_SWAT_TUTORIAL PLC6 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatPLC6(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc6 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc6 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc6 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            st = time.time()
            
            # From plant
            fit601 = self.receive(FIT601_6, PLANT_ADDR)
            p601 = self.receive(P601_6,PLANT_ADDR)
            p602 = self.receive(P602_6,PLANT_ADDR)
            p603 = self.receive(P603_6,PLANT_ADDR)


            if not fit601:
                print "DEBUG PLC6: can't get fit601 from plant"
                time.sleep(1)
                continue
                
            fit601 = float(fit601[0][0])
            p601 = int(p601[0][0])
            p602 = int(p602[0][0])
            p603 = int(p603[0][0])
            
            print "DEBUG PLC6 - get fit601: %f" % fit601
             
            self.send(FIT601_6, fit601, PLC6_ADDR)
            self.send(P601_6, p601, PLC6_ADDR)
            self.send(P602_6, p602, PLC6_ADDR)
            self.send(P603_6, p603, PLC6_ADDR)
            
            elapsed = time.time() - st
            print "Finished sending everything in ", str(elapsed), " seconds."

            count += 1
            if elapsed < PLC_PERIOD_SEC:
                time.sleep(PLC_PERIOD_SEC)

        print 'DEBUG swat plc6 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc6 = SwatPLC6(
        name='plc6',
        state=STATE,
        protocol=PLC6_PROTOCOL,
        memory=PLC6_DATA,
        disk=PLC6_DATA)
