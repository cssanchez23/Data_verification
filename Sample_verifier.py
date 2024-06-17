"""Purpose of theis script is to compare Sample names betweeen the sample submnission 
form and the SampleSheet. This is to ensure all samples are accounted for"""

#Author Christian Sanchez

import argparse
import math
import pandas as pd
import sys

#PROJ = sys.argv[1]
#SUB = sys.argv[2]


parser = argparse.ArgumentParser()
parser.add_argument('--project','-p',type=str, required=True)
parser.add_argument('--SUB','-s',type=str,required=True)





args = parser.parse_args()
#project = PROJ



#PROJ = sys.argv[1]
#PROJ="Seres_Batch248_MQ3487_CLINICAL"
#SUB = sys.argv[2]
#SUB = "Seres_Batch248_Diversigen_PlateSampleSubmissionSheet.xlsx"
samples_submission_list = []

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def process_samplesheet_list(df,proj):
    df= df.iloc[(df.loc[df[0]=='[Data]'].index[0]+1):, :].reset_index(drop = True)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df=df.loc[df['Sample_Project']==proj]
    sample_sheet_l = df["Pooled_Sample_Name"]
    sample_sheet_l = [x for x in sample_sheet_l if not 'DIV' in x]
    return sample_sheet_l

def process_submission_list(sub,plate):
    df_sub=pd.read_excel(sub,sheet_name="Plate {}".format(plate),header=1,engine='openpyxl')
    df_sub.dropna(axis=1,how='all',inplace=True)
    if "Sample ID" in df_sub.columns:
        print ("Plate {} had samples".format(plate))
        df_sub = df_sub.dropna(subset=["Sample ID"])
        submission_sheet_l = df_sub["Sample ID"]
        submission_sheet_l = [x for x in submission_sheet_l if not 'EMPTY' in x]
        samples_submission_list.extend(submission_sheet_l)
    else:
        print ("Nothing was in plate {}".format(plate))
        pass

def process_tube_submission_list(sub):
    #df_sub=pd.read_excel(sub,sheet_name="Sample Submission",header=None)
    #TODO find a way to iterate through plates
    df=pd.read_excel(sub,sheet_name="Sample Submission",header=None)
    df.dropna(axis=1,how='all',inplace=True)
    df= df.iloc[(df.loc[df[1]=='Submission Type'].index[0]):, :].reset_index(drop = True)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df = df.dropna(subset=["Sample ID"])
    submission_sheet_l = df["Sample ID"]
    submission_sheet_l = [x for x in submission_sheet_l if not 'EMPTY' in x]
    samples_submission_list.extend(submission_sheet_l)

def compare_list(ss,other):
    if len(ss) == len(other) :
        print ("There are the Same number of Samples")
    else:
        print ("Below are the differences in list")
        print (Diff(ss,other))
        ss_not_sub= [item for item in ss if item not in other]
        print ("Unique Samples in SampleSheet")
        print (ss_not_sub)
        sub_not_ss= [item for item in other if item not in ss]
        print ("Unique Samples in Submission Form")
        print (sub_not_ss)
        
        
def compare_list1(ss,other):
        print ("Below are the differences in list")
        print (Diff(ss,other))
        ss_not_sub= [item for item in ss if item not in other]
        print ("Unique Samples in SampleSheet")
        print (ss_not_sub)
        sub_not_ss= [item for item in other if item not in ss]
        print ("Unique Samples in Submission Form")
        print (sub_not_ss)
        

df_ss = pd.read_csv("SampleSheet.csv",header=None)
sample_sheet_l = process_samplesheet_list(df_ss,args.project)

if "Tube" in args.SUB:
    print ("Tube Submission form used")
    process_tube_submission_list(args.SUB)
    
elif "Plate" in args.SUB:
    print("Plate Submission form used")
    for i in range(1,9):
        
        process_submission_list(args.SUB,i)
        
else:
    print ("not right format")
    
    
compare_list1(sample_sheet_l,samples_submission_list)
    