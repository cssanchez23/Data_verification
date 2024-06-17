#Author Christian Sanchez
"""Purpose of this script is to check qc metrics to ensure that a project passes QC"""
import os
from os import path
from operator import itemgetter
import pandas as pd
import subprocess
import sys 

# Will take two arguemnts 
#qc link 
qc = sys.arg[1]

qc_list = qc.split('/')[3:8]
x = "/"
qc_s3 = x.join(qc_list)

os.system("aws s3 cp s3://{}/data/QC_Overview.txt . ".format(qc_s3))
os.system("aws s3 cp s3://{}/data/Project_QC_Depths.csv . ".format(qc_s3))
os.system("aws s3 cp s3://{}/data/metrics.csv . ".format(qc_s3))
qc_depths = "Project_QC_Depths.csv"

if path.exists("Project_QC_Depths.csv") == True:
    pass
else:
    print ("Project QC depths not found")
    
if path.exists("QC_Overview.txt") == True:
    pass
else:
    print ("QC Overview missing")
    
    
df = pd.read_csv("Project_QC_Depths.csv")

pos_controls = df[df.S_C == '+']
neg_controls = df[df.S_C == '-']
samples_df = df[df.S_C == 'samples']
average_depth = samples_df["depth_raw"].mean()
ten_percent_depth = average_depth/10
neg_above_ten = neg_controls[neg_controls.depth_raw > ten_percent_depth]
pos_above_ten = pos_controls[pos_controls.depth_raw < ten_percent_depth]


project  = subprocess.check_output("cat QC_Overview.txt | grep 'Project ID:'| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()


mean_qc_depth  = subprocess.check_output("cat QC_Overview.txt | grep 'Mean Depth QC-passes'| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()
min_depth  = subprocess.check_output("cat QC_Overview.txt | grep 'Minimum Depth (Quote)'| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()
samp_num  = subprocess.check_output("cat QC_Overview.txt | grep 'Total Sample Number'| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()
per_qc_pass  = subprocess.check_output("cat QC_Overview.txt | grep 'Percent of QC-passes'| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()
lib_prep_reads_pass = subprocess.check_output("cat QC_Overview.txt | grep 'reads passing'| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()

failed  = subprocess.check_output("cat QC_Overview.txt | grep 'failed'| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()
no_reads  = subprocess.check_output("cat QC_Overview.txt | grep 'generate '| cut -d':' -f2 | cut -d' ' -f2",shell=True).decode('utf-8').strip()


print ("Mean QC-Passing Sample Depth: {}".format(mean_qc_depth))
print ("Minimum: {}".format(min_depth))
print ("Percent Reads above Minimum Depth: {}".format(per_qc_pass))
if len(pos_above_ten.index) > 0:
    print ("Positive controls BELOW ten percent of mean depth:")
    print (pos_above_ten["sample_id"])
else:
    print ("Positive controls pass")
print ("-----------")
if len(neg_above_ten.index) > 0:
    print ("Negatives controls ABOVE ten percent of mean depth:")
    print (neg_above_ten["sample_id"])
else:
    print ("Negative controls pass")
print ("% Library Prep reads post-qc: {}".format(lib_prep_reads_pass))
print ("Mean QC-Passi\ng Sample Depth: {}".format(mean_qc_depth))
print ("Mean QC-Passing Sample Depth: {}".format(mean_qc_depth))



