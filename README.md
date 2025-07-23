# Automated deployment onto SPHERE
This is a prototype deployment of a water plant simulation on the SPHERE testbed, capable to communicate via the GATE action server.

## Pre-requisites
1. Request the SWaT dataset from [iTrust, Centre for Research in Cyber Security](https://itrust.sutd.edu.sg/itrust-labs_datasets/), save it as `SWaT_Dataset_Normal_v1.csv` put it inside of the folder `ansible/files/scada-traffic-generator/minicps-examples/swat-s1-to-s6/real-swat-data/`.
2. Get the `mrg` [tool from sphere](https://mergetb.gitlab.io/testbeds/sphere/sphere-docs/docs/experimentation/getting-started/#account-creation-through-the-cli).
3. `mrg login <username>`

## Usage:
1. Initialize and activate the experiment: `bash up.sh`
2. Confure the deployed nodes and start the services: `bash ansible.sh`
3. Explore the experiment and network, over [the web interface](https://launch.sphere-testbed.net/).

For example:
- Continue exploring over an `ssh` session. You can reach any of the nodes in the experiment by name: `ssh -F ssh_config plant`.
- Once you are on an experiment machine, inspect SWaT the traffic as it passes through the experiment network: `sudo tcpdump -i eth2 'port 44818'`.

## Troubleshooting:
If you are logged into an experiment machine and are having problems inspecting traffic, check on the status of the service: `sudo systemctl status plant`

# Cleanup:
1. `bash down.sh`

<small>This was developed as part of the compelling demo for the year 2 site visit for the [NSF Action Institute](https://github.com/action-ai-institute) to prototype a collaboration with [SPHERE](https://sphere-project.net/).</small>
