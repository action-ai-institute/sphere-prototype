#!/bin/bash
set -e
sudo -v
# These variables are for ACTION deployment, and don't apply to most other cases
#GLOBAL_COMM_PASSWORD=$(sudo cat ../vpc-unics-esperanza/inventory.ini | grep global_action_password | cut -d'=' -f2 | cut -d'"' -f2)  # Set your global communication password
GLOBAL_COMM_PASSWORD=passowrd
GLOBAL_COMM_IP="global.$USER.action-ai.institute"
LOCAL_ACTION_PASSWORD="defauilt_password"
LOCAL_ACTION_SERVER="10.5.0.20"

# For ACTION, we need an OPENAI_API_KEY, but in other cases we don't need it
# export OPENAI_API_KEY=$(cat ../.env | grep OPENAI_API_KEY= | cut -d"=" -f2 )
export OPENAI_API_KEY=fakey

# Function to use the inventory file and pass these variables to the action playbooks
function ansible_exec() {
    ansible-playbook -i inventory.ini $1 \
        --extra-var "global_comm_password=$GLOBAL_COMM_PASSWORD" \
        --extra-var "global_comm_ip=$GLOBAL_COMM_IP" \
        --extra-var "local_action_password=$LOCAL_ACTION_PASSWORD" \
        --extra-var "local_action_server_ip=$LOCAL_ACTION_SERVER"
}

ansible_exec ansible/configure-ics.yml
ansible_exec ansible/run-swat-sim.yml

# ACTION specific playbooks not yet included
#ansible_exec ansible/s00_sphere_init.yml
#ansible_exec ../inf/ansible/70_action_server.yml
#ansible_exec ansible/s10_aganets.yml
