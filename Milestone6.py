from os import mkdir
from urllib.request import urlretrieve
from zipfile import ZipFile
import os
import pandas as pd

import streamlit as st
st.title('Step 1: Provide Milestone 2 Input File')
# url = st.text_input('Enter URL of Test Data', '')
#st.write('The url you entered is', url)

with st.form(key='my_form'):
    urlinput = st.text_input(label='Enter URL of Test Data')
    submit_button = st.form_submit_button(label='Submit')

if urlinput != '':
    url = urlinput
    csvname = url[-16:-9]
    inputFile = "./DownloadedFile.zip"
    outputDir = "DownloadedFile"
    # put zip file in local directory -- this takes a while.. file is big
    urlretrieve(url, inputFile)
    # unzip contents into output folder -- this takes a while.. file is big
    with ZipFile(inputFile) as zipObj:
        zipObj.extractall(outputDir)
    # Extract pic names in the folder
    file_list = os.listdir("./DownloadedFile")
    file_list.sort()
    # remove .jpg
    new_list = [s.replace(".jpg", "") for s in file_list]

    # input csv
    # read the csv file (put 'r' before the path string to address any special characters in the path, such as '\'). Don't forget to put the file name at the end of the path + ".csv"
    CustomerList = pd.read_csv("./liveCustomerList.csv")
    CustomerList['firstName'] = CustomerList['firstName'].str.upper()
    CustomerList['lastName'] = CustomerList['lastName'].str.upper()
    FraudList = pd.read_csv("./liveFraudList.csv")
    FraudList["fraudster"] = '1'

    # change custID list to Dataframe
    custID = pd.DataFrame(new_list, columns=['custID'])
    # change datatype
    custID['custID'] = custID['custID'].astype(int)

    # left join table custID and customerlist
    custIDname = pd.merge(custID, CustomerList, on='custID', how='left')
    custIDnameFraud = pd.merge(custIDname, FraudList, on=[
        'firstName', 'lastName'], how='left')
    custIDnameFraud['fraudster'] = custIDnameFraud['fraudster'].fillna(0)

    # FraudTestOnput.csv
    output = custIDnameFraud[['custID', 'fraudster']]

    @st.cache
    def convert_df_to_csv(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')


else:
    st.text('Please enter url above and click the Submit button')


# # Download and unzip url

# # specifiying url of zip file
# #url = "https://www.dropbox.com/s/0n0u003pk5avp95/321529.zip?dl=1"
# csvname = url[-15:-9]
# inputFile = "./DownloadedFile.zip"
# outputDir = "DownloadedFile"
# # put zip file in local directory -- this takes a while.. file is big
# urlretrieve(url, inputFile)
# # unzip contents into output folder -- this takes a while.. file is big
# with ZipFile(inputFile) as zipObj:
#     zipObj.extractall(outputDir)

# # Extract pic names in the folder
# file_list = os.listdir("./DownloadedFile")
# file_list.sort()
# # remove .jpg
# new_list = [s.replace(".jpg", "") for s in file_list]

# # input csv
# # read the csv file (put 'r' before the path string to address any special characters in the path, such as '\'). Don't forget to put the file name at the end of the path + ".csv"
# CustomerList = pd.read_csv("./liveCustomerList.csv")
# CustomerList['firstName'] = CustomerList['firstName'].str.upper()
# CustomerList['lastName'] = CustomerList['lastName'].str.upper()
# FraudList = pd.read_csv("./liveFraudList.csv")
# FraudList["fraudster"] = '1'

# # change custID list to Dataframe
# custID = pd.DataFrame(new_list, columns=['custID'])
# # change datatype
# custID['custID'] = custID['custID'].astype(int)

# # left join table custID and customerlist
# custIDname = pd.merge(custID, CustomerList, on='custID', how='left')
# custIDnameFraud = pd.merge(custIDname, FraudList, on=[
#                            'firstName', 'lastName'], how='left')
# custIDnameFraud['fraudster'] = custIDnameFraud['fraudster'].fillna(0)

# # FraudTestOnput.csv
# output = custIDnameFraud[['custID', 'fraudster']]


# @st.cache
# def convert_df_to_csv(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv(index=False).encode('utf-8')


if urlinput != '':
    st.title('Step 2: Download Fraudster Detection Result')
    # st.text('Step 2: Download Fraudster Detection Result')
    st.download_button(
        label='Download',
        data=convert_df_to_csv(output),
        file_name=csvname+'.csv',
        mime='text/csv',)
    st.text('Now download the csv file')
else:
    st.text('')
