import numpy as np  # Số
import pandas as pd # Data wrangling, Data Frame.
import streamlit as st
#import urllib.request # 
#Eimport shutil
#import tempfile
#import altair as alt
import pyodbc
#from keyboard import press

#### ---------------------------------####
st.title('Samples')
#-------------Input Section -------------------------

# Model_input = st.text_input('Model', 'Input Model Here!!!')
# st.write('Model is: ', Model_input)
# st.button ('Check')

#-------------Connection Section-------------------


# def conn_server():
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=vnmsrv601.dl.net\Siplace_2008R2EX;DATABASE=MobileDB;UID=Sa;PWD=Siplace.1')
#     model ='890003434'
# st.write(conn,"Connection OK")   


Model_input =st.text_input('Model Input','Input model here !!!')
if Model_input != '':
    sql=f"SELECT top 5 * FROM LabelcodeFruPP where Model ='{Model_input}'"
    # st.write(sql)
    df=pd.read_sql(sql,conn)
    if len(df) > 0:        
        st.write(st.subheader('Result as below: '),df)
        # Hiển thị Characteristic.
        c= df.loc[0, 'Des']
        st.write(c)
        st.write(type(c))
    else:
        st.write('No data')
else:
    st.write('Model is not setup')
#    
    
    
    
    
    
    