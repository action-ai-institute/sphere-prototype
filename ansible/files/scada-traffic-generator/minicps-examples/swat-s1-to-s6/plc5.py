"""
swat-s1 plc6.py
"""

from minicps.devices import PLC
from utils import PLC5_DATA, STATE, PLC5_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M, LIT_301_M, FIT_201_THRESH

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
PLC4_ADDR = IP['plc4']
PLC5_ADDR = IP['plc5']
PLANT_ADDR = IP['plant']


AIT501_5 = ('AIT501', 5)
AIT502_5 = ('AIT502', 5)
AIT503_5 = ('AIT503', 5)
AIT504_5 = ('AIT504', 5)
FIT501_5 = ('FIT501', 5)
FIT502_5 = ('FIT502', 5)
FIT503_5 = ('FIT503', 5)
FIT504_5 = ('FIT504', 5)
P501_5 = ('P501', 5)
P502_5 = ('P502', 5)
PIT501_5 = ('PIT501', 5)
PIT502_5 = ('PIT502', 5)
PIT503_5 = ('PIT503', 5)

# interlocks to be received from plc4
P401_5 = ('P401', 5)  # to be sent
P401_4 = ('P401', 4)  # to be received
P402_5 = ('P402', 5)  # to be sent
P402_4 = ('P402', 4)  # to be received

# SPHINX_SWAT_TUTORIAL PLC5 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatPLC5(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc6 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc4 main loop.

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
            ait501 = self.receive(AIT501_5, PLANT_ADDR)
            ait502 = self.receive(AIT502_5,PLANT_ADDR)
            ait503 = self.receive(AIT503_5, PLANT_ADDR)
            ait504 = self.receive(AIT504_5,PLANT_ADDR)
            fit501 = self.receive(FIT501_5,PLANT_ADDR)
            fit502 = self.receive(FIT502_5,PLANT_ADDR)
            fit503 = self.receive(FIT503_5,PLANT_ADDR)
            fit504 = self.receive(FIT504_5,PLANT_ADDR)
            p501 = self.receive(P501_5,PLANT_ADDR)
            p502 = self.receive(P502_5,PLANT_ADDR)
            pit501 = self.receive(PIT501_5, PLANT_ADDR)
            pit502 = self.receive(PIT502_5, PLANT_ADDR)
            pit503 = self.receive(PIT503_5, PLANT_ADDR)
                        
            # From interlocks
            p401 = self.receive(P401_4, PLC4_ADDR)
            p402 = self.receive(P402_4, PLC4_ADDR)

            if not ait501:
                print "DEBUG PLC5: can't get ait501 from plant"
                time.sleep(1)
                continue
                
            ait501 = float(ait501[0][0])
            ait502 = float(ait502[0][0])
            ait503 = float(ait503[0][0])
            ait504 = float(ait504[0][0])
            fit501 = float(fit501[0][0])
            fit502 = float(fit502[0][0])
            fit503 = float(fit503[0][0])
            fit504 = float(fit504[0][0])
            p501 = int(p501[0][0])
            p502 = int(p502[0][0])
            pit501 = float(pit501[0][0])
            pit502 = float(pit502[0][0])
            pit503 = float(pit503[0][0])
            p401 = int(p401[0][0])
            p402 = int(p402[0][0])
            
            print "DEBUG PLC5 - get ait501: %f" % ait501  
            
            self.send(AIT501_5, ait501, PLC5_ADDR)
            self.send(AIT502_5, ait502, PLC5_ADDR)
            self.send(AIT503_5, ait503, PLC5_ADDR)
            self.send(AIT504_5, ait504, PLC5_ADDR)
            self.send(FIT501_5, fit501, PLC5_ADDR)
            self.send(FIT502_5, fit502, PLC5_ADDR)
            self.send(FIT503_5, fit503, PLC5_ADDR)
            self.send(FIT504_5, fit504, PLC5_ADDR)
            self.send(P501_5, p501, PLC5_ADDR)
            self.send(P502_5, p502, PLC5_ADDR)
            self.send(PIT501_5, pit501, PLC5_ADDR)
            self.send(PIT502_5, pit502, PLC5_ADDR)
            self.send(PIT503_5, pit503, PLC5_ADDR)
            self.send(P401_5, p401, PLC5_ADDR)
            self.send(P402_5, p402, PLC5_ADDR)
            
            elapsed = time.time() - st
            print "Finished sending everything in ", str(elapsed), " seconds."

            
            if elapsed < PLC_PERIOD_SEC:
                time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat plc6 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc6 = SwatPLC5(
        name='plc5',
        state=STATE,
        protocol=PLC5_PROTOCOL,
        memory=PLC5_DATA,
        disk=PLC5_DATA)
