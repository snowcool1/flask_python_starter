import numpy as np  # Số
import pandas as pd # Data wrangling, Data Frame.
import streamlit as st
import pyodbc
# import os.path
# from os import path
# import sys
# from cmd import Cmd
import subprocess
import os 
from subprocess import Popen

#### ---------------------------------####
st.title('Samples')
#-------------Input Section -------------------------

Model_input =st.text_input('Model Input','Input model here !!!')

#-------------Connection Section-------------------


# def conn_server():
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=vnmsrv601.dl.net\Siplace_2008R2EX;DATABASE=MobileDB;UID=Sa;PWD=Siplace.1')
sql=f"SELECT top 5 * FROM LabelcodeFruPP where Model ='{Model_input}'"
#st.write(sql)
df=pd.read_sql(sql,conn)
#     model ='890003434'
#st.write(conn,"Connection OK")   

if Model_input != '':
    if  len(df) > 0:        
        st.write('Result as below: ',df)               
    else:
        st.write('Model is not setup')
else:
    st.write('Please fill model here !!!')
    
# ----------- Showing Characteristic----------------------
# c= '111' + '.btw'
Label_name= df.loc [0, 'Characteristic'] 
c=str(Label_name + '.btw')
c=c.replace(" ","")
st.write(c)
btw = os.path.isfile(f"//vnmsrv601/DevelopSoftware/T01-Print Label/FRUlabel/" + c)
st.write(btw)

#Change dir to correct app path
rootfolder="C:/Program Files (x86)/Seagull/BarTender Suite/BarTender"
assert os.path.isdir(rootfolder)
os.chdir(rootfolder)
#Prepare path
appname=fr'bartend.exe'
btwfile=fr"D:\FRUlabel\ + {c}"  ##d \ slash forward for window

if (btw == True):
    #Run All wwith argument
    subprocess.Popen([appname,btwfile,"/P","/X"])
    st.write('In nhé')
else:
    st.write('The label is not setup')
#     subprocess.call(["taskkill /IM bartend.exe /F", "bartend.exe /x /F=D:\FRUlabel\104.btw /P"])
             





    
    
    
    
    
    