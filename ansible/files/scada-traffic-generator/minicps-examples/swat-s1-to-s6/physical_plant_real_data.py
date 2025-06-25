"""
SWaT sub1 physical process

RawWaterTank has an inflow pipe and outflow pipe, both are modeled according
to the equation of continuity from the domain of hydraulics
(pressurized liquids) and a drain orefice modeled using the Bernoulli's
principle (for the trajectories).
"""


from minicps.devices import Tank

from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT,REAL_DATA_PATH
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL , IP
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES, PLANT_PROTOCOL
import pandas as pd

import sys
import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
PLANT_ADDR = IP['plant']

# Sensor values sent to PLCs
FIT101 = ('FIT101', 1)
MV101 = ('MV101', 1)
LIT101 = ('LIT101', 1)
P101 = ('P101', 1)
P102 = ('P102', 1)
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
DPIT301_3 = ('DPIT301', 3)
LIT301_3 = ('LIT301', 3)
FIT301_3 = ('FIT301', 3)
MV301_3 = ('MV301', 3)
MV302_3 = ('MV302', 3)
MV303_3 = ('MV303', 3)
MV304_3 = ('MV304', 3)
P301_3 = ('P301', 3)
P302_3 = ('P302', 3)
AIT401_4 = ('AIT401', 4)
AIT402_4 = ('AIT402', 4)
FIT401_4 = ('FIT401', 4)
LIT401_4 = ('LIT401', 4)
P401_4 = ('P401', 4)
P402_4 = ('P402', 4)
P403_4 = ('P403', 4)
P404_4 = ('P404', 4)
UV401_4 = ('UV401', 4)
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
FIT601_6 = ('FIT601', 6)
P601_6 = ('P601', 6)
P602_6 = ('P602', 6)
P603_6 = ('P603', 6)

# Interlocks (actuators written by PLC)


# SPHINX_SWAT_TUTORIAL TAGS)


# TODO: implement orefice drain with Bernoulli/Torricelli formula
class RawWaterTank(Tank):

    def pre_loop(self):
        pass
        # SPHINX_SWAT_TUTORIAL STATE INIT(
        #self.set(MV101, 1)
        #self.send(MV101, 1, PLC1_ADDR)
        #self.set(P101, 0)
        #self.send(P101, 0, PLC1_ADDR)
        #self.level = self.set(LIT101, 0.300)
        #self.send(LIT101,self.level, PLANT_ADDR)
        # SPHINX_SWAT_TUTORIAL STATE INIT)
        
        # test underflow
        # self.set(MV101, 0)
        # self.set(P101, 1)
        # self.level = self.set(LIT101, 0.500)

    def main_loop(self):

        count = 0
        chunksize = 1000
        print("Entering main loop")
        reader = pd.read_csv(REAL_DATA_PATH,skiprows=1, iterator=True)
        
        df=reader.get_chunk(chunksize)
        while not df.empty:

            for index, row in df.iterrows():
                
                print "Debug: iterating row: ",index
                st = time.time()
                lit101 = float(row[LIT101[0]])
                mv101 = int(row[MV101[0]])
                fit101 = float(row[FIT101[0]])
                p101 = int(row[P101[0]])
                p102 = int(row[P102[0]])
                ait201 = float(row[AIT201_2[0]])
                ait202 = float(row[AIT202_2[0]])
                ait203 = float(row[AIT203_2[0]])
                fit201 = float(row[FIT201_2[0]])
                mv201 = int(row[MV201_2[0]])
                ct201 = float(200.0) # Not provided by sensor data
                ct202 = float(20.0)  # Not provided by sensor data
                ct203 = float(150.0) # Not provided by sensor data
                p201 = int(row[P201_2[0]])
                p202 = int(row[P202_2[0]])
                p203 = int(row[P203_2[0]])
                p204 = int(row[P204_2[0]])
                p205 = int(row[P205_2[0]])
                p206 = int(row[P206_2[0]])
                dpit301 = float(row[DPIT301_3[0]])
                lit301 = float(row[LIT301_3[0]])
                fit301 = float(row[FIT301_3[0]])
                mv301 = int(row[MV301_3[0]])
                mv302 = int(row[MV302_3[0]])
                mv303 = int(row[MV303_3[0]])
                mv304 = int(row[MV304_3[0]])
                p301 = int(row[P301_3[0]])
                p302 = int(row[P302_3[0]])
                ait401 = float(row[AIT401_4[0]])
                ait402 = float(row[AIT402_4[0]])
                fit401 = float(row[FIT401_4[0]])
                lit401 = float(row[LIT401_4[0]])
                p401 = int(row[P401_4[0]])
                p402 = int(row[P402_4[0]])
                p403 = int(row[P403_4[0]])
                p404 = int(row[P404_4[0]])
                uv401 = int(row[UV401_4[0]])
                ait501 = float(row[AIT501_5[0]])
                ait502 = float(row[AIT502_5[0]])
                ait503= float(row[AIT503_5[0]])
                ait504 = float(row[AIT504_5[0]])
                fit501 = float(row[FIT501_5[0]])
                fit502 = float(row[FIT502_5[0]])
                fit503 = float(row[FIT503_5[0]])
                fit504 = float(row[FIT504_5[0]])
                p501 = int(row[P501_5[0]])
                p502 = int(row[P502_5[0]])
                pit501 = float(row[PIT501_5[0]])
                pit502 = float(row[PIT502_5[0]])
                pit503 = float(row[PIT503_5[0]])
                fit601 = float(row[FIT601_6[0]])
                p601 = int(row[P601_6[0]])
                p602 = int(row[P602_6[0]])
                p603 = int(row[P603_6[0]])
                
                self.send_multiple(
                        (LIT101,MV101,FIT101,P101,AIT201_2,AIT202_2,AIT203_2,FIT201_2,MV201_2,CT201_2,CT202_2,CT203_2, P201_2,P202_2,P203_2,P204_2,P205_2,P206_2,DPIT301_3,LIT301_3,FIT301_3,MV301_3,MV302_3,MV303_3,MV304_3,P301_3,P302_3, AIT401_4, AIT402_4,FIT401_4,LIT401_4,P401_4,P402_4,P403_4,P404_4,UV401_4,AIT501_5,AIT502_5,AIT503_5,AIT504_5,FIT501_5,FIT502_5,FIT503_5,FIT504_5,P501_5,P502_5,PIT501_5,PIT502_5,PIT503_5,FIT601_6,P601_6,P602_6,P603_6),#P102
                   (lit101,mv101,fit101,p101,ait201,  ait202,  ait203,  fit201,  mv201,  ct201,  ct202,  ct203,   p201,  p202,  p203,  p204,  p205,  p206,  dpit301,  lit301,  fit301,  mv301,  mv302,  mv303,  mv304,  p301,  p302,   ait401,   ait402,  fit401,  lit401,  p401,  p402,  p403,  p404,  uv401,  ait501,  ait502,  ait503,  ait504,  fit501,  fit502,  fit503,  fit504, p501,   p502,  pit501,  pit502,  pit503,  fit601,  p601,  p602,  p603),#p102 
                       PLANT_ADDR)
                
                '''
                self.send_multiple((LIT101,MV101,FIT101,), (lit101,mv101,fit101), PLANT_ADDR)
                
                self.send(MV101, mv101, PLANT_ADDR)
                self.send(FIT101, fit101, PLANT_ADDR)
                self.send(P101, p101, PLANT_ADDR) 
                self.send(P102, p102, PLANT_ADDR) 
                self.send(AIT201_2, ait201, PLANT_ADDR) 
                self.send(AIT202_2, ait202, PLANT_ADDR) 
                self.send(AIT203_2, ait203, PLANT_ADDR) 
                self.send(FIT201_2, fit201, PLANT_ADDR) 
                self.send(MV201_2, mv201, PLANT_ADDR) 
                #self.send((CT201_2,CT202_2,CT203_2), (ct201,ct202,ct203), PLANT_ADDR) 
                #self.send(CT202_2, ct202, PLANT_ADDR) 
                #self.send(CT203_2, ct203, PLANT_ADDR) 
                self.send(P201_2, p201, PLANT_ADDR) 
                self.send(P202_2, p202, PLANT_ADDR)
                self.send(P203_2, p203, PLANT_ADDR) 
                self.send(P204_2, p204, PLANT_ADDR) 
                self.send(P205_2, p205, PLANT_ADDR) 
                self.send(P206_2, p206, PLANT_ADDR) 
                self.send(DPIT301_3, dpit301, PLANT_ADDR) 
                self.send(LIT301_3, lit301, PLANT_ADDR) 
                self.send(FIT301_3, fit301, PLANT_ADDR) 
                self.send(MV301_3, mv301, PLANT_ADDR) 
                self.send(MV302_3, mv302, PLANT_ADDR) 
                self.send(MV303_3, mv303, PLANT_ADDR) 
                self.send(MV304_3, mv304, PLANT_ADDR) 
                self.send(P301_3, p301, PLANT_ADDR) 
                self.send(P302_3, p302, PLANT_ADDR) 
                self.send(AIT401_4, ait401, PLANT_ADDR) 
                self.send(AIT402_4, ait402, PLANT_ADDR) 
                self.send(FIT401_4, fit401, PLANT_ADDR) 
                self.send(LIT401_4, lit401, PLANT_ADDR) 
                self.send(P401_4, p401, PLANT_ADDR) 
                self.send(P402_4, p402, PLANT_ADDR) 
                self.send(P403_4, p403, PLANT_ADDR) 
                self.send(P404_4, p404, PLANT_ADDR)
                self.send(UV401_4, uv401, PLANT_ADDR) 
                self.send(AIT501_5, ait501, PLANT_ADDR)
                self.send(AIT502_5, ait502, PLANT_ADDR) 
                self.send(AIT503_5, ait503, PLANT_ADDR)
                self.send(AIT504_5, ait504, PLANT_ADDR) 
                self.send(FIT501_5, fit501, PLANT_ADDR)
                self.send(FIT502_5, fit502, PLANT_ADDR)
                self.send(FIT503_5, fit503, PLANT_ADDR)
                self.send(FIT504_5, fit504, PLANT_ADDR) 
                self.send(P501_5, p501, PLANT_ADDR) 
                self.send(P502_5, p502, PLANT_ADDR) 
                self.send(PIT501_5, pit501, PLANT_ADDR) 
                self.send(PIT502_5, pit502, PLANT_ADDR) 
                self.send(PIT503_5, pit503, PLANT_ADDR) 
                self.send((FIT601_6,P601_6, P602_6,P603_6), (fit601,p601, p602,p603), PLANT_ADDR) 
                #self.send(P601_6, p601, PLANT_ADDR) 
                #self.send(P602_6, p602, PLANT_ADDR) 
                #self.send(P603_6, p603, PLANT_ADDR)
                '''
                elapsed = time.time() - st
                print "Finished sending everything in ", str(elapsed), " seconds."
                
                count += 1
                if elapsed < PP_PERIOD_SEC:
                    time.sleep(PP_PERIOD_SEC)
            df = reader.get_chunk(chunksize)

if __name__ == '__main__':

    rwt = RawWaterTank(
        name='rwt',
        state=STATE,
        protocol=PLANT_PROTOCOL,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )
