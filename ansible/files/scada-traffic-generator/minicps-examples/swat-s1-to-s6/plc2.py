
"""
swat-s1 plc2
"""

from minicps.devices import PLC
from utils import PLC2_DATA, STATE, PLC2_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
PLANT_ADDR = IP['plant']

AIT201_2 = ('AIT201', 2)
AIT202_2 = ('AIT202', 2)
AIT203_2 = ('AIT203', 2)
FIT201_2 = ('FIT201', 2)
MV201_2 = ('MV201', 2)
CT201_2 = ('CT201', 2) # Chem tank NaCl
CT202_2 = ('CT202', 2) # Chem tank HCl
CT203_2 = ('CT203', 2) # Chem tank NaOCl
P201_2 = ('P201', 2)   # Pump tank NaCl
P202_2 = ('P202', 2)   # Pump tank NaCl
P203_2 = ('P203', 2)   # Pump tank HCl
P204_2 = ('P204', 2)   # Pump tank HCl
P205_2 = ('P205', 2)   # Pump tank NaOCl
P206_2 = ('P206', 2)   # Pump tank NaOCl
# interlocks to be received from 

class SwatPLC2(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc2 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - read flow level sensors #2
            - update interal enip server
        """

        print 'DEBUG: swat-s1 plc2 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            st = time.time()
            fit201 = self.receive(FIT201_2, PLANT_ADDR)
            ait201 = self.receive(AIT201_2,PLANT_ADDR)
            ait202 = self.receive(AIT202_2,PLANT_ADDR)
            ait203 = self.receive(AIT203_2,PLANT_ADDR)
            ct201 = self.receive(CT201_2, PLANT_ADDR)
            ct202 = self.receive(CT202_2, PLANT_ADDR)
            ct203 = self.receive(CT203_2, PLANT_ADDR)
            # print "DEBUG PLC2 - get fit201: ", str(fit201)
            if not fit201:
                print "DEBUG PLC2: can't get fit201 from plant"
                time.sleep(1)
                continue
            fit201 = float(fit201[0][0])
            ait201 = float(ait201[0][0])
            ait202 = float(ait202[0][0])
            ait203 = float(ait203[0][0])
            ct201 = float(ct201[0][0])
            ct202 = float(ct202[0][0])
            ct203 = float(ct203[0][0])
            self.send(FIT201_2, fit201, PLC2_ADDR)
            self.send(AIT201_2, ait201, PLC2_ADDR)
            self.send(AIT202_2, ait202, PLC2_ADDR)
            self.send(AIT203_2, ait203, PLC2_ADDR)
            self.send(CT201_2, ct201, PLC2_ADDR)
            self.send(CT202_2, ct202, PLC2_ADDR)
            self.send(CT203_2, ct203, PLC2_ADDR)
            # fit201 = self.receive(FIT201_2, PLC2_ADDR)
            # print "DEBUG PLC2 - receive fit201: ", fit201
            
            elapsed = time.time() - st
            print "Finished sending everything in ", str(elapsed), " seconds."

            count += 1
            if elapsed < PLC_PERIOD_SEC:
                time.sleep(PLC_PERIOD_SEC)
        

        print 'DEBUG swat plc2 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = SwatPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)
