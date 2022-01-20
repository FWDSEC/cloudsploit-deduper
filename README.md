The CSV report from CloudSploit can be a bit unruly. The same issue is repeated multiple times if it's found for different **Regions** or **Resources**.

This script looks through each FAILed finding (because those are the ones we care about), and groups together the Regions and Resources into a single cell, so that each issue type is only listed once.