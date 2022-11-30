import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import csv

'''
df = pd.read_csv("/Users/idohyeon/crc_project/data/data1.csv")
df.shape
df.head()
df.tail()
df = df.duplicated(["Roll_hand", "Pitch_hand", "Yaw_hand","Acc_x_hand", "Acc_y_hand", "Acc_z_hand",  "Roll_head", "Pitch_head",  "Yaw_head",  "Acc_x_head", "Acc_y_head", "Acc_z_head"], keep = 'first')
#df = df.drop_duplicates(["Roll_hand", "Pitch_hand", "Yaw_hand","Acc_x_hand", "Acc_y_hand", "Acc_z_hand",  "Roll_head", "Pitch_head",  "Yaw_head",  "Acc_x_head", "Acc_y_head", "Acc_z_head"], keep = False)
'''

'''
lines = set()
outfile = open("/Users/idohyeon/crc_project/data/data1.csv","w")

for line in open("/Users/idohyeon/crc_project/data/data1.csv","r"):
    if line not in lines:
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
'''
with open('/Users/idohyeon/crc_project/data/data1.csv','r') as in_file, open('/Users/idohyeon/crc_project/data/data3.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line not in seen: 
            seen.add(line)
            out_file.write(line)