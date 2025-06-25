# Acknowledgement
This research was developed with funding from the Defense Advanced Research Projects Agency
(DARPA). The views, opinions and/or findings expressed are those of the
author and should not be interpreted as representing the official views or
policies of the Department of Defense or the U.S. Government


# SCADA Traffic Generator
The SCADA traffic generator is defined as traffic between industrial control system nodes that uses industrial standard protocols. Currently, the project supports Ethernet over IP (ENIP) and Modbus.

[[_TOC_]]

## Source Code
TODO

## Architecture
TODO

## Configuring the SCADA Traffic Generator Controller
TODO (both controller implementation + documentation)

## Configuring the PLC Nodes
1. Clone the repository within your XDC CLI
2. Run the ansible playbook to configure the ICS with: `ansible-playbook -i ./scada-traffic-generator/testbed/scada-ics.inv ./scada-traffic-generator/testbed/configure-ics.yml`
	* This should install all the dependencies on each node and copy over the repository to each node.
3. Run the ansible playbook to capture network traffic on the router with: `ansible-playbook -i scada-traffic-generator/testbed/scada-ics.inv ./dev/mergetb/xdc/ansible/tcpdump-start.yml -e <experiment_name> --limit r` 
4. Run the ansible playbook to start the ICS simulation with: `ansible-playbook -i ./scada-traffic-generator/testbed/scada-ics.inv ./scada-traffic-generator/testbed/run-swat-sim.yml`
	* TODO: automate end of experiment; we currently have to manually kill the experiments after a certain time using the clean-exp.yml playbook. It should just end for all nodes once the plant node has ingested all samples from the physical file.
5. Run the ansible playbook to stop the tcpdump  traffic on the router with: `ansible-playbook -i scada-traffic-generator/testbed/scada-ics.inv ./dev/mergetb/xdc/ansible/tcpdump-stop.yml --limit r`

