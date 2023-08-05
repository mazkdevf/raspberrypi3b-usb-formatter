## Kiitokset Artulle!

import os

for filename in os.listdir("/sys/block/"):
    if filename.startswith("sd"):
        stream = os.popen("udevadm info -p /sys/block/" + filename + " --query=env")
        output = stream.read().split();
        for l in output:
            if l.find("DEVPATH=")>=0:
                print(l)
