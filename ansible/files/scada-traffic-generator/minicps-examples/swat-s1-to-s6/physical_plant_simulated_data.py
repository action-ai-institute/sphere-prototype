#!/usr/bin/env python3
from __future__ import print_function
import sys
import json
from collections import OrderedDict
import re
import os

sys.path.append("../../simutils")
from simutils import PLCState, get_swat_data_from_file, find_multiexecution_discrepancies  # noqa

# Boolean variable that determines if we are writing the closed loop
# or open loop values to the tick file
closed_loop = True

progname = sys.argv[1]
tick = int(sys.argv[2])
current_pid = int(sys.argv[3])
start_tick = int(sys.argv[4])

# Typical FR ~ 2.5-2.6
fr_error_threshold = 2.55
fr_conversion_constant = 0.186428

# Error thresholds:
lit_error_threshold = 5.5  # Defined by SWaT invariance checker
lit_check_interval_tick = 6  # Defined by SWaT invariance checker

flow_rate_error_threshold = 0.01  # Should be less than 0.01 after
fit_check_interval_tick = 25  # 25 seconds

actuator_error_threshold = 0.001  # Actuators (valves/pumps) should be checked every cycle
actuator_check_interval_tick = 1

discrepancy_check_interval = 50
# Create a PLC state variable
plc_state = PLCState(
    start_tick = start_tick, current_tick=tick, progname=progname, current_pid=current_pid)


# Retrieves the values from either the estimated
def get_sensor_val(val):
    try:
        if val in est_sensors_names.keys():
            return sensor_vals[val]
        else:
            return swatdata[val]
    except:
        print("ERROR: Invalid sensor name: {}").format(val)
        sys.exit(1)


##################################################
# physical model functions
##################################################
# Used to store the open and closed loop flow rate values
def flow_rate(fit, actuators):
    global closed_loop_vals
    global open_loop_vals
    # We first need to iterate through all the actuators (valves/pumps)
    # to see if they are open or closed:
    actuator_val_cum = 1
    for actuator in actuators.split(","):
        # The stored values are going to be 2 (open), 1 (closed), or 0 (closing).
        # We translate this to binary values 1 (open) or 0 (closed)
        actuator_val = int(get_sensor_val(actuator.strip()))
        actuator_val_cum = actuator_val_cum * actuator_val

    # closed loop estimation
    closed_loop_vals[fit] = float(swatdata[fit]) * actuator_val_cum

    # open loop estimation
    if fit in est_sensors_names.keys():
        open_loop_vals[fit] = float(sensor_vals[fit]) * actuator_val_cum


# Used to store the closed and open loop values of the water tank
# estimation.
def water_tank(tank, flowrates):
    global closed_loop_vals
    global open_loop_vals
    flow_toks = flowrates.split(',')
    if len(flow_toks) != 2:
        print("Water tanks should have 2 args: inflow,outflow")
        sys.exit(1)
    # tmp = get_sensor_val(flow_toks[0])
    inflow = float(get_sensor_val(flow_toks[0]))
    outflow = float(get_sensor_val(flow_toks[1]))
    prev_closed = float(swatdata[tank])

    # State estimation translation of Sridhar's code :
    closed_loop_vals[
        tank] = prev_closed + (inflow - outflow) * fr_conversion_constant

    if tank in est_sensors_names.keys():
        prev_open = float(sensor_vals[tank])
        open_loop_vals[
            tank] = prev_open + (inflow - outflow) * fr_conversion_constant


# Used to  store the valve values. Because this is an actuator, we need
# to only use the estimated values based on what the PLC code wrote.
def valve(v, blank):
    global closed_loop_vals
    global open_loop_vals
    closed_loop_vals[v] = int(sensor_vals[v])
    open_loop_vals[v] = int(sensor_vals[v])


# Used to  store the pump values. Because this is an actuator, we need
# to only use the estimated values based on what the PLC code wrote.
def pump(p, blank):
    global closed_loop_vals
    global open_loop_vals
    closed_loop_vals[p] = int(sensor_vals[p])
    open_loop_vals[p] = int(sensor_vals[p])


# These are the sensors we will be estimating. All other values will be
# provided by the SWaT data set. Pass the function and respective args.
# The first arg will be the name of the sensor, the second will be
# the enumerated parameters for a function separated by  commas
est_sensors_names = OrderedDict(
    ##################################################
    # Values that are estimated that ARE written to by our PLC code.
    # This is for the current configuration where the LLVM
    # MATIEC  dumps the variables in a particular order
    [
        ("LIT101", [water_tank, "LIT101", "FIT101,FIT201"]),
        ("LIT301", [water_tank, "LIT301", "FIT201,FIT301"]),  # TankeLevel2
        ("FIT201", [flow_rate, "FIT201", "MV201,P101"]),  # Flowrate21
        ("MV101", [valve, "MV101", ""]),  # Valve_1
        ("MV201", [valve, "MV201", ""]),  # Valve 2
       # ("MV301", [valve, "MV301", ""]),  
        #("MV302", [valve, "MV302", ""]), 
       # ("MV303", [valve, "MV303", ""]),  
        #("MV304", [valve, "MV304", ""]), 
        ("P101", [pump, "P101", ""]),  # Pump1
        ("P102", [pump, "P102", ""]), 
        #("P302", [pump, "P302", ""]), 
        #("P402", [pump, "P402", ""]),  
        ("P403", [pump, "P403", ""]),   
        ("P404", [pump, "P404", ""]), 
        #("UV401", [valve, "UV401", ""]),
        #("P401", [pump, "P401", ""]),   
        ("P502", [pump, "P502", ""]), 
        ##################################################
        # Values that are estimated but aren't written to by our PLC code.
        # This is for the current configuration where the LLVM
        # MATIEC  dumps the variables in a particular order
        ("FIT101", [flow_rate, "FIT101", "MV101"]),
        ("FIT301", [flow_rate, "FIT301", "P301"]),
        ("FIT401", [flow_rate, "FIT401", "P401"])
        
        
    ])

# Dicts to store closed/open loop estimations of each value
closed_loop_vals = {}
open_loop_vals = {}

# Variables to store previously estimated values:
sensor_vals = {}

# Dict to store variable tick values for those variables that aren't
# being estimated
swatdata = {}


# Retrieves estimated data for a particular tick
def get_est_data_from_file(t):
    # vals = {}
    # for val in est_sensors_names.keys():
    #     vals[val] = plc_state[val]
    
    return PLCState(start_tick = start_tick,current_tick=t, progname=progname, current_pid=current_pid)


# Write swat data to file (used on initialization):
def write_swat_data_to_file(t):
    for val in est_sensors_names.keys():
        plc_state[val] = swatdata[val]
    plc_state.save_current_tick()


# Write estimated data to file:
# def write_est_data_to_file(t):
# plc_state = PLCState(
#     current_tick=t, progname=progname, current_pid=current_pid)
def write_est_data_to_file():

    for val in est_sensors_names.keys():
        if closed_loop:
            V = closed_loop_vals[val]
        else:
            V = open_loop_vals[val]

        plc_state[val] = V

    plc_state.save_current_tick()


# Returns the average error of a sensor value for a given interval:
def get_avg_error(sensor, interval):
    average_error = 0
    for i in range(0, interval):
        
        est_vals = get_est_data_from_file(tick - interval + i)
        swat_vals = get_swat_data_from_file(tick - interval + i,
                                            est_sensors_names)
        
        average_error = average_error + float(
            abs(float(est_vals[sensor]) - float(swat_vals[sensor]))) / float(
                interval)
    return average_error


def write_error_to_file(sensor, tick, error):
    print("Detected deviation in {} of {} at tick {}, writing to file...".
          format(sensor, error, tick))
    if not os.path.exists("errors"):
        os.makedirs("errors/")
    fpath = "errors/{}.{}.error".format(sensor, tick)
    with open(fpath, "w+") as f:
        print(
            "Var: {}; Deviation: {}; Tick: {}\n".format(sensor, error, tick),
            file=f)


# Check errors against threshold if the error check interval for a sensor
# has lapsed:
def check_errors():
    if (tick-start_tick) > 0:
        if (tick-start_tick) % actuator_check_interval_tick == 0:
            for val in est_sensors_names.keys():
                # check for valve or pump values:
                if bool(re.search(r'^P|MV|UV[0-9]*?', val)):
                    error = get_avg_error(val, actuator_check_interval_tick)
                    if error > actuator_error_threshold:
                        write_error_to_file(val, tick, error)

        if (tick-start_tick) % lit_check_interval_tick == 0:
            for val in est_sensors_names.keys():
                # check for LIT values:
                if bool(re.search(r'^LIT[0-9]*?', val)):
                    error = get_avg_error(val, lit_check_interval_tick)
                    if error > lit_error_threshold:
                        write_error_to_file(val, tick, error)

        if (tick-start_tick) % fit_check_interval_tick == 0:
            for val in est_sensors_names.keys():
                # check for FIT values:
                if bool(re.search(r'^FIT[0-9]*?', val)):
                    error = get_avg_error(val, fit_check_interval_tick)
                    if error > fr_error_threshold:
                        write_error_to_file(val, tick, error)
       # if (tick-start_tick) % discrepancy_check_interval == 0:
           # print("Looking for discrepancies...")
           # find_multiexecution_discrepancies(tick-discrepancy_check_interval)


def update_estimation_values():
    # Call the mapped update function for each sensor:
    for val in est_sensors_names.keys():
        est_sensors_names[val][0](est_sensors_names[val][1],
                                  est_sensors_names[val][2])

        # print ("{} Closed: {}\n".format(val,closed_loop_vals[val]))
        # print ("{} Open: {}\n".format(val,open_loop_vals[val]))


    # Initialize data sets for this tick
def initialize_data_sets(t):
    global swatdata
    global sensor_vals
    # Retrieve the swat data for this tick
    swatdata = get_swat_data_from_file(t, est_sensors_names)
    print ("***Current tick: {}, start= {}".format(tick,start_tick))
    # special case: for tick 0, we need to provide the data
    if t == start_tick  and current_pid == 0:
        print ("Writing swat file: ")
        write_swat_data_to_file(t)

    # Retrieve the sensor vals from the the file for this tick:
    # TODO: "t" or "tick" correct?
    sensor_vals = get_est_data_from_file(t)
    #print(sensor_vals)


if __name__ == "__main__":

    #print("simulate prog={}, tick={}, write={}"
#          .format(progname, tick, current_pid))

    initialize_data_sets(tick)

    update_estimation_values()

    #check_errors()
    # actual simulation now
    #print("==>")
    '''
    if closed_loop:
        print("Closed Loop Values:\n")
        for val in closed_loop_vals:
            print("EST: {} = {}\nSWAT: {} = {}\n".format(
                val, closed_loop_vals[val], val, swatdata[val]))
    else:
        #print("Open Loop Values:\n")
        for val in open_loop_vals:
            print("{} = {}\n".format(val, open_loop_vals[val]))
    '''
    # write_est_data_to_file(tick)
    write_est_data_to_file()
    '''
    # Get valve/pump values:
    out_vals["MV101"] = int(get_sensor_val("MV101"))
    out_vals["MV201"] = int(get_sensor_val("MV101"))
    out_vals["P101"] = int(get_sensor_val("P101"))

    # Convert the valve value
    MV101 = 1 if out_vals["MV101"] == 2 else 0
    MV201 = 1 if out_vals["MV201"] == 2 else 0
    P101 = 1 if out_vals["P101"] == 2 else 0


    #Open Loop estimation:
    out_vals["FIT101"] = flow_rate_est * MV101
    out_vals["FIT201"] = flow_rate_est * MV201 * P101
    out_vals["LIT101"] = float(get_sensor_val("LIT101")) + (out_vals["FIT101"]  - out_vals["FIT201"]) * fr_conversion_constant
    #out_vals["LIT301"]  = float(get_sensor_val("LIT101")) + out_vals["FIT201"] * fr_conversion_constant-get_sensor_val(
    out_vals["LIT301"] = float(get_sensor_val("LIT301"))

    if out_vals["LIT101"] < 0:
        out_vals["LIT101"] = 0
    if out_vals["LIT301"]< 0:
        out_vals["LIT301"] = 0
    for val in out_vals:
      print("{} = {}\n".format(val,out_vals[val]))

    #print("""LIT101   = {}
    #LIT301   = {}
    #FIT201 = {}
    #MV101       = {}
    #P101        = {}
    #MV201       = {}
    #""".format(LIT101_out, LIT301_out, FIT201_out, MV101, P101, MV201))

    # write variables back to file
    fpath = "tick/{}.{}.{}.in".format(progname, tick, write)
    '''
    '''
    with open(fpath, "w") as out_file:
        vals = []
        for name in est_sensors_names.keys():
          vals.append(str(out_vals[name]))# = [LIT101_out, LIT301_out, FIT201_out, MV101, P101, MV201]
        #vals = map(str, vals)
        print("\n".join(vals), file=out_file)
    '''
"""
SWaT sub1 physical process

RawWaterTank has an inflow pipe and outflow pipe, both are modeled according
to the equation of continuity from the domain of hydraulics
(pressurized liquids) and a drain orefice modeled using the Bernoulli's
principle (for the trajectories).
"""


from minicps.devices import Tank

from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_HEIGHT, TANK_SECTION, TANK_DIAMETER
from utils import LIT_101_M, RWT_INIT_LEVEL , IP
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS, PP_SAMPLES, PLANT_PROTOCOL

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

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(MV101, 1)
        #self.send(MV101, 1, PLC1_ADDR)
        self.set(P101, 0)
        #self.send(P101, 0, PLC1_ADDR)
        self.level = self.set(LIT101, 0.300)
        self.send(LIT101,self.level, PLANT_ADDR)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

        # test underflow
        # self.set(MV101, 0)
        # self.set(P101, 1)
        # self.level = self.set(LIT101, 0.500)

    def main_loop(self):

        count = 0
        while(count <= PP_SAMPLES):

            new_level = self.level

            # compute water volume
            water_volume = self.section * new_level

            # inflows volumes
            
            mv101 = self.receive(MV101,PLC1_ADDR)
            print 'DEBUG plant received mv101: ',str(mv101)
            if mv101: 
                mv101 = int(mv101[0][0])
                self.set(MV101,mv101)
            else:
                mv101 = self.get(MV101)
            if int(mv101) == 1:
                self.set(FIT101, PUMP_FLOWRATE_IN)
                self.send(FIT101,PUMP_FLOWRATE_IN,PLANT_ADDR)
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank inflow: ", inflow
                water_volume += inflow
            else:
                self.set(FIT101, 0.00)
                self.send(FIT101, 0.00, PLANT_ADDR)

            # outflows volumes
            p101 = int(self.receive(P101,PLC1_ADDR)[0][0])
            if int(p101) == 1:
                self.set(FIT201, PUMP_FLOWRATE_OUT)
                self.send(FIT201,PUMP_FLOWRATE_OUT,PLANT_ADDR)
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                # print "DEBUG RawWaterTank outflow: ", outflow
                water_volume -= outflow
            else:
                self.set(FIT201, 0.00)
                self.send(FIT201,0.00,PLANT_ADDR)

            # compute new water_level
            new_level = water_volume / self.section

            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            print "DEBUG new_level: %.5f \t delta: %.5f" % (
                new_level, new_level - self.level)
            self.level = self.set(LIT101, new_level)
            self.send(LIT101, new_level, PLANT_ADDR)
            # 988 sec starting from 0.500 m
            if new_level >= LIT_101_M['HH']:
                print 'DEBUG RawWaterTank above HH count: ', count
                break

            # 367 sec starting from 0.500 m
            elif new_level <= LIT_101_M['LL']:
                print 'DEBUG RawWaterTank below LL count: ', count
                break

            count += 1
            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    rwt = RawWaterTank(
        name='rwt',
        state=STATE,
        protocol=PLANT_PROTOCOL,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )
