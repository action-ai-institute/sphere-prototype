echo "Creating new experiment"
mrg new experiment gate.$USER 'Gate Dev' || true
echo "Creating new xdc"
mrg new xdc x0.$USER || true
echo "pushing the network model"
REV=$(mrg push ./model.py gate.$USER | cut -d':' -f2 | cut -d' ' -f2 | head -n 1)
echo "$REV"
echo "realizing the experiment"
mrg realize test.gate.$USER revision $REV
echo "Here are the realizations:"
mrg list realizations

mrg mat test.gate.$USER

mrg xdc attach x0.$USER test.gate.$USER

cat > ssh_config <<EOF
Host *
   StrictHostKeyChecking no
   UserKnownHostsFile=/dev/null
   User $USER
Host jump
    HostName jump.sphere-testbed.net
    Port 2022
    User $USER
    IdentityFile ~/.ssh/merge_key

Host x0-$USER
    HostName x0-$USER
    User $USER
    IdentityFile ~/.ssh/merge_key
    ProxyJump jump

Host plant
    HostName plant
    User $USER
    IdentityFile ~/.ssh/merge_key
    ProxyJump x0-$USER

Host action
    HostName action
    User $USER
    IdentityFile ~/.ssh/merge_key
    ProxyJump x0-$USER

Host p2
    HostName p2
    User $USER
    IdentityFile ~/.ssh/merge_key
    ProxyJump x0-$USER
EOF

PWD=$(pwd)

cat > inventory.ini <<EOF
[all:vars]
ansible_ssh_common_args="-F ${PWD}/ssh_config"
[private_hosts]
action_server ansible_host=action ansible_user=$USER
r ansible_host=r ansible_user=$USER
p2 ansible_host=p2 ansible_user=$USER
plant ansible_host=plant ansible_user=$USER
EOF
