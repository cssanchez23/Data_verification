import argparse
import pandas as pd
import sys


parser = argparse.ArgumentParser()
parser.add_argument('--project','-p',type=str, required=True)
parser.add_argument('--scf','-s',type=str,required=True)
parser.add_argument('--sheet','-e',type=str,required=True)
args = parser.parse_args()

#TODO pull sample number from project spec to check it matches number of samples in SS

df = pd.read_excel(args.scf,sheet_name="SCF - Standard",engine='openpyxl')
df_ss = pd.read_csv(args.sheet,header=None)

def value_pull(metric):
    
    for row in range(df.shape[0]): 

        for col in range(df.shape[1]):

            if df.iat[row,col] == metric:
                row_start = row
                break

    df_tmp = df.loc[row_start:]
    df_tmp.columns = df_tmp.iloc[0]
    df_tmp = df_tmp.drop(df_tmp.index[0])
    tmp = df_tmp[metric].iat[0]
    return tmp

def ss_pull(df):
    df= df.iloc[(df.loc[df[0]=='[Data]'].index[0]+1):, :].reset_index(drop = True)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df_c = df.copy()
    df = df.drop_duplicates(subset='Sample_Project', keep="first")
    df_proj = df.loc[df["Sample_Project"] == args.project]
    global platform
    global r_host
    global host
    global pooled
    global mean_depth
    global low_depth
    global cut_depth
    platform  = df_proj["Platform"].iat[0]
    r_host = df_proj["Remove_Host"].iat[0]
    host = df_proj["Host"].iat[0]
    pooled = df_proj["Pooled_Sample_Name"].duplicated().any()
    if "Mean_Depth_{}".format(platform) in df.columns:
        mean_depth = df_proj["Mean_Depth_{}".format(platform)].iat[0]
        low_depth = df_proj["Lowest_Depth_{}".format(platform)].iat[0]
        cut_depth = df_proj["Low_Depth_Cutoff_{}".format(platform)].iat[0]
    else: 
        print ("Depth information is not in SampleSheet!!!")
        mean_depth = "NA"
        low_depth = "NA"
        cut_depth = "NA"
        pass
    df_c = df_c.drop_duplicates(subset="Pooled_Sample_Name", keep="first")
    df_c = df_c.loc[df_c["Sample_Project"] == args.project]
    samples_only = df_c["Pooled_Sample_Name"]
    samples_only = [x for x in samples_only if not 'DIV' in x]
    global ss_sample_count
    ss_sample_count = len(samples_only)
    

#df_t = df.transpose()
#df_t.columns = df_t.iloc[0]
#df_t = df_t.drop(df_t.index[0])
#df_t['Sample Number (total)']
#df_t = df_t.drop(df_t.index[0])
#df_t['Sample Number (total)']
#samp_spec = df_t['Sample Number (total)']
#project_s_samp = samp_spec[0]

annotation = value_pull("Library Prep 1")
cust_annotation = value_pull("Annotation 1")
depth_t = value_pull("Target Depth 1")
depth_spec = value_pull("Depth Specifications")
h_removal = value_pull("Host Removal? If so what kind?")
ss_pull(df_ss)

print ("Are there pooled Samples? {}".format(pooled))
print ("Remove Host correct: PS {},SS {} {}".format(h_removal,r_host,host))
print ("Platform: PS {} - {},SS {}".format(annotation,cust_annotation,platform))
print ("Specs in SS Target :{} Low {} : percent {}".format(mean_depth,low_depth,cut_depth))
print ("Specs in Project Spec: Target {}, Percent {} ".format(depth_t,depth_spec))
print ("-----------------------")
print ("Number of samples in SampleSheet: {}".format(ss_sample_count))

