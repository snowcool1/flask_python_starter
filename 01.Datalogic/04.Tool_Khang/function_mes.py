"""
Instruction
CALL DATA FROM SYSTEM 

ACS > acssql(query)
MES > messql(query)
MES > mes_datatype(tablename) eg:. mes_datatype("ZME_KITTING")
DF  > dfsql(query)

"""



def update_os():
    """
    Provide PATH ENV for Oracle running.
    """

    os.environ["PATH"] = "C:\oracle\instantclient_12_2\;"+os.environ["PATH"]
    #print(os.environ["PATH"])
    #os.environ["NLS_LANG"] = ".UTF8"

import os
update_os()
import cx_Oracle
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('oracle://MES_READ:D4ta7061@blqsrv612.dl.net:1521/WPP')
def mesquery(q):

#     df = pd.read_sql("""
#     select owner, table_name, column_name, column_id, num_distinct,last_analyzed from all_tab_columns where OWner='WPPUSER' and last_analyzed is not NULL order by last_analyzed desc
#     """, engine)
    df = pd.read_sql(q, engine)
    return df
messql=mesquery
from pandasql import *
from pandasql import sqldf
def dfquery(q):

    pysqldf = lambda q: sqldf(q, globals())

#     pysqldf("SELECT distinct(table_name) FROM df where table_name like '%kitting%' ").head(10)
    return pysqldf(q)
dfsql=dfquery
def acssql(q):
    import sqlalchemy
    import pandas as pd
    engine = sqlalchemy.create_engine("mssql+pymssql://reports:reports@vnmacsdb:1433/ACS EE")
#     df = pd.read_sql('select top 100 Material  from hts_vi where DescriptionVI is null or HTSCode is null', engine)
    df = pd.read_sql(q, engine)
    return df
acsquery=acssql
# acssql("select top 10 * from testlog")


def mes_datatype(tablename="ZME_KITTING"):
#     print(tablename)
    return sqlmes("""
    SELECT all_tab.owner,
           all_tab.table_name,
           all_tab.column_name,
           all_tab.data_type,
           all_tab.data_length,
           col_com.comments
    FROM   all_tab_columns all_tab
           JOIN all_col_comments col_com
              ON  all_tab.table_name = col_com.table_name
              AND all_tab.owner = col_com.owner
    WHERE  all_tab.table_name = '{}'
    """.format(tablename))
#     dftype

def tracking(sfc, direction="down"):
    field_direction="sfc_bom_bo" if direction=="down" else "inventory_bo"
    table='SFC_ASSY' 
    site=3400
    
    q=("""
        select * from WPPUSER.{}  

            where ROWNUM <100     
             and handle like '{}'
             or {} like '%{}'  
         """.format(table,site,field_direction,sfc))
    df = pd.read_sql(q, engine)

    #sfc_bom_bo top_down and sfc_bom_bo like '%G19NAQILN%' 
    #inventory_bo bot_up
    cols=["sfc_bom_bo","component_bo","inventory_bo","assembled_date","assembled_by_bo","shop_order_bo"]
    return df[cols]
def tracking_multi(sfc_list, direction="down"):
    mylist=sfc_list.split('\n')
    #send list to have list complate
    while '' in mylist:
        mylist.remove('')
        
    # do main here
    dfmain=None
    boolfirstdone=False
    for item in mylist:
        sn=item#row['nam']

    #     print(q)
        df=tracking(sn,"down")

        if len(df) >0 and boolfirstdone==False : #loop1
    #         print("now first row",df)
            boolfirstdone=True
    #         print(sn,"=0")
            dfmain=df
    #         print(dfmain)
        else:
            dfmain=pd.concat([dfmain,df], ignore_index=True)

    return dfmain

#TODO: get all ACS test machine 10 day

def getAllMachineList():
    import sqlalchemy
    import pyodbc
    import pandas as pd
    engine = sqlalchemy.create_engine("mssql+pymssql://reports:reports@vnmacsdb:1433/ACS EE")
    df = pd.read_sql(fr"select distinct workcenter from testlog where test_Date_time >dateadd(dd,-10,getdate())", engine)
#     df.head()
    alllist=df.workcenter.values
#     print(len(alllist))
    return alllist


def grant_access(mylist):
    import subprocess

    # Disconnect anything on M
#     subprocess.call(r'net use m: /del', shell=True)
    for i  in range(len(mylist)):
        print(mylist[i])
        RS="Fail"
        try:
            command= fr'net use "\\{mylist[i]}\C$" stark300 /user:dl\fixture'
#             print(command)
#             !{command}
            subprocess.call(command)
            RS="done fixture"
        except:
            command= fr'net use "\\{mylist[i]}\C$" stark200 /user:dl\acsuser'
#             print(command)
#             !{command}
            subprocess.call(command)
            RS="done acs"
        else:
#             command= fr'net use "\\{mylist[i]}\C$" 6Turtl3$ /user:{mylist[i]}\Administrator'
#             print(command)
#             !{command}
            pass
    return RS

def getHostCommanderlogs(machinepath,loc=0):
    """
    return df and filename last.
    """
    folder=fr'\\{machinepath}\C$\ProgramData\HostCommander\logs'
    import time
    data = []
    # for folder in sorted(os.listdir(dirpath)):
    #     print(folder)
    for file in sorted(os.listdir(""+folder)):
    #     print(file)
        file=folder+"/"+file
    #     print('Access time  :', time.ctime(os.path.getatime(file)))
    #     print('Modified time:', time.ctime(os.path.getmtime(file)))
    #     print('Change time  :', time.ctime(os.path.getctime(file)))
    #     print('Size         :', os.path.getsize(file))
        at=time.ctime(os.path.getatime(file))
        mt=time.ctime(os.path.getmtime(file))
        ct=time.ctime(os.path.getctime(file))
        s=os.path.getsize(file)
        data.append((folder, file,at,mt,ct,s))
    import pandas as pd
    df = pd.DataFrame(data, columns=['Folder', 'File','AccessTime',"ModifiedTime","ChangeTime","FileSize"])
    df['AccessTime']= pd.to_datetime(df['AccessTime'])
    df['ModifiedTime']= pd.to_datetime(df['ModifiedTime'])
    df['ChangeTime']= pd.to_datetime(df['ChangeTime'])
    df.sort_values(by=['ModifiedTime'], ascending=False, inplace=True)
    # print(df.info())
    df.reset_index(inplace=True, drop=True)
    lastfile=df.iloc[loc]['File']
    f=lastfile

    df0=pd.read_table(f, encoding='latin-1')
    df0.time=pd.to_datetime(df0.time)
    df0.sort_values(by=['time'], ascending=True, inplace=True)
    df0.tail(10)
   
    return df0, lastfile
