from mergexp import *

# Create a network topology object.
net = Network('gate', addressing==ipv4, routing==static)

# Create all nodes.
plant,r,p1,p2,p3 = [net.node(name, image=="2204", proc.cores>=4, memory.capacity>=gb(8)) for name in ['plant', 'r', 'p1', 'p2', 'p3']]

# Create a newtork links
plcs = [p1, p2, p3]
for p in plcs:
  net.connect([r, p])
  net.connect([plant, p])

experiment(net)
