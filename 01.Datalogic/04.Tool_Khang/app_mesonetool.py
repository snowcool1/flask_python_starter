import streamlit as st
import function_mes as mes
import pandas as pd
print()

st.sidebar.title("WORKFLOW")
start=True
if st.sidebar.button("Getting Started") or start==True:
    # TODO: """Do instruction to help pepole understand process"""
    # TODO: 
    st.title("**NO-MES**: **N**ot-**O**nly-**M**es ")
    st.write("* Application provide advanced setup workflow for enginnering to prevent missing setup and aim to setup MES/ACS data just 5 minute as ACSonetool used to.")
    st.write('* Workflow: ')
    
    #TAG """End """

# st.graphviz_chart('''
# digraph g {
# 	rankdir=LR;

# 	node [shape=rpromoter colorscheme=rdbu5 color=1 style=filled fontcolor=3]; Hef1a; TRE; UAS; Hef1aLacOid;
# 	Hef1aLacOid [label="Hef1a-LacOid"];
# 	node [shape=rarrow colorscheme=rdbu5 color=5 style=filled fontcolor=3]; Gal4VP16; LacI; rtTA3; DeltamCherry;
# 	Gal4VP16 [label="Gal4-VP16"];	
# 	product [shape=oval style=filled colorscheme=rdbu5 color=2 label=""];
# 	repression [shape=oval label="LacI repression" fontcolor=black style=dotted];
# 	node [shape=oval style=filled colorscheme=rdbu5 color=4 fontcolor=5];
# 	combination [label="rtTA3 + Doxycycline"];
# 	LacIprotein [label="LacI"];
# 	rtTA3protein [label="rtTA3"];
# 	Gal4VP16protein [label="Gal4-VP16"];
	

# 	subgraph cluster_0 {
# 		colorscheme=rdbu5;
# 		color=3;
# 		node [colorscheme=rdbu5 fontcolor=3];
# 		Hef1a -> Gal4VP16 [arrowhead=none];
# 		Gal4VP16 -> UAS [arrowhead=none];
# 		UAS -> LacI [arrowhead=none];
# 		LacI -> Hef1aLacOid [arrowhead=none];
# 		Hef1aLacOid -> rtTA3 [arrowhead=none];
# 		rtTA3 -> TRE [arrowhead=none];
# 		TRE -> DeltamCherry [arrowhead=none]
# 	}
	
# 	Gal4VP16 -> Gal4VP16protein;
# 	Gal4VP16protein -> UAS;
# 	LacI -> LacIprotein;
# 	LacIprotein -> repression;
# 	repression -> Hef1aLacOid [arrowhead=tee];
# 	IPTG -> repression [arrowhead=tee];
# 	rtTA3 -> rtTA3protein;
# 	rtTA3protein -> combination;
# 	combination -> TRE;
# 	Doxycycline -> combination;
# 	DeltamCherry -> product;
	
	
		
# }

# ''')

    st.graphviz_chart('''
        digraph {
            order -> list_kitting
            order -> model
            model -> BOM_bom_routing
            model -> ROUTING_bom_routing
            model -> SW_is_exist
            SW->SW_LOCATION

            BOM_bom_routing -> sleep
            order -> BOM_PO
            BOM_PO -> LABEL
            BOM_PO -> OPERATION
            order -> SFC
            LABEL -> LABEL_SETUP
            LABEL_SETUP -> LABEL_LOCATION
            LABEL -> OK_SETUP
            LABEL -> WRONG_SETUP
            LABEL -> MISSING_SETUP
        }
    ''')
site=st.sidebar.selectbox("plant",[3400,2600])
report_type=st.sidebar.selectbox("Start with ShopOrder/Material/SFC",["ShopOrder","Material","SFC","ASSY tracking up/down"])


#-------------------------

def track_sfc_to_po(site,sfc):

    table='SFC' 
    df=mes.mesquery("""
            select * from WPPUSER.{0}  

                where ROWNUM <10    
                and site ='{1}'
    --and sfc_router_bo like '%G19NAQMDM%'
    and sfc='{2}'
             """.format(table,site,sfc))

    #sfc_bom_bo top_down
    #inventory_bo bot_up
#     print(df.columns)
#     print(df.head(1).T)
    last_record=df.head(1)
    _shop_order_bo = last_record["shop_order_bo"].values
#     print(_shop_order_bo)
    _shop_order=_shop_order_bo[0].split(",")[1]
#     print(_shop_order)
# print(mes_datatype(table))
#     print(fr"test: sfc_to_po(3400,"G19NAQMDM")")
    return _shop_order
# track_sfc_to_po(3400,"G19NAQMDM")

bool_order=False
#----------------------------------
if report_type =="SFC":
    sfc=st.sidebar.text_input("SFC","G19NAQMDM")
    if st.sidebar.button("track sfc to po"):
        po_sfc=track_sfc_to_po(site,sfc)
        st.sidebar.text("PO: {}".format( po_sfc))
#         report_type ="ShopOrder"
#         bool_order=True
#         po=st.sidebar.text_input("Nhập PO",po_sfc)
        
if report_type =="ShopOrder" :
    
    po = st.sidebar.text_input("Nhập PO","101333846").strip()


#     po=po.split('\n')
#     #send list to have list complate
#     while '' in po:
#         po.remove('')



    #-----------------------

    if st.sidebar.button("CHECK MES"):
        start=False
        st.sidebar.text("---start {}---".format(site))
        st.sidebar.text("ShopOrder: {}".format(po))
        df= mes.mesquery("""
         select * from WPPUSER.ZME_KITTING WHERE 1=1 
                 and SHOP_ORDER_BO LIKE '%{}%'  
                 AND SITE ='3400'
                AND assigned_start_date >= (SYSDATE -3) AND assigned_start_date <= (SYSDATE +3)


                order by assigned_start_date desc

        """.format(po)    )
        def order_status(r):
            return str(r["shop_order_bo"].split(",")[1]) +str( "-deleted" if r['fl_delete'] =="X" else "")

#         df.insert (0, "Order", df.shop_order_bo.apply(lambda r: r.split(",")[1]))
        df.insert (0, "Order", df.apply(order_status, axis=1))

        st.subheader("Step: Check Kitting ,Count order {} , PO#: {}".format(len(df),po))
        st.table(df)
        model=df.item.iloc[0]
        sapwc=df.primary_work_center.iloc[0]
        meswc=df.work_center.iloc[0]
        qty=df.qty_to_build.iloc[0]
    #     st.write("Sap_model: {}".format(model))
        st.sidebar.text("Model :{} ".format(model))
        st.sidebar.text("Qty: {}".format(qty))
        st.sidebar.text("SAP WC: {} ".format(sapwc))
        st.sidebar.text("MES WC: {} ".format(meswc))
        st.sidebar.text("MES delete: {} ".format(df.fl_delete.iloc[0]))
        
        list_allorder=df.shop_order_bo.apply(lambda r: r.split(",")[1]).values
#         myTuple = ["John", "Peter", "Vicky"]
        query="'{}'".format(list_allorder[0])
        for x in list_allorder[1:]:
            query=query + ",'{}'".format(x)
#         query
        #---------------------
        def shop_oder_status(site,po):
            table='SHOP_ORDER' 
            # site=3400
            df=mes.mesquery("""
                        select * from WPPUSER.{0}  

                            where ROWNUM <10    
                           and site='{1}'
                           
                            and shop_order = '{2}'
                            or shop_order in ({3})
                         """.format(table,site,po,query))
            return df
        
        po_status_df=shop_oder_status(site,po)
        "Check SHOP_ORDER Table {}".format(len(po_status_df))
        if len(po_status_df) >0:
            st.table(po_status_df)
            qty_build=po_status_df.qty_to_build.iloc[0]
            qty_done=po_status_df.qty_done.iloc[0]
            qty_released=po_status_df.qty_released.iloc[0]
            qty_released

            st.sidebar.text("qty_released: {}".format(qty_released))
            st.sidebar.text("qty_done: {}".format(qty_done))
        else:
            "in info in shop order"
         #---------------------       

        st.subheader("Step: Check BOM, ROUTING")
        bom_routing_df=mes.mesquery("""
        select * from WPPUSER.ZME_PN_ROUTING WHERE 1=1 and
            site={} and item='{}'
        """.format(site,model)    )
        
        if len(bom_routing_df)>0:
            st.table(bom_routing_df)

            st.sidebar.text("BOM: {} ".format(bom_routing_df["master_bom"].iloc[0]))
            router=bom_routing_df['router'].iloc[0]
            st.sidebar.text("Routing: {} ".format(bom_routing_df['router'].iloc[0]))

            table="ROUTER"
            router_df=mes.mesquery("""
                select * from WPPUSER.{} where site='{}' 
                and router='{}'
                and ROWNUM <= 5
                 """.format(table,site,router))
        #     st.table(router_df[:10])
        else:
            st.sidebar.text("NO ROUTING SETUP *")
            
            
        #-------------------------
        st.subheader("Step: Check TEST SW MES")
        def model_sw(site,model=''):
            table='ZME_TEST_CONFIGURATION' 
            site=3400
            q=("""
                        select * from WPPUSER.{0}  

                            where ROWNUM <10    

            and plant ='{1}'
            and part_number like '%{2}'
                         """.format(table,site,model))
#             df = pd.read_sql(q, engine)
            df=mes.mesquery(q)
            return df
#         model_sw(3400,'GD4130-BK')
        sw_df=model_sw(site,model)
        if len(sw_df)>0:
            sw_df.drop(columns=["row_id"],inplace=True)
            st.table(sw_df)
        else:
            "No-found-SW"
        st.subheader("Step: Check TEST SW ACS for reference") 
        def acs_model_sw(model=''):
            table='tffc_kicker_table' 
            site=3400
            df=mes.acsquery("""
                        select * from [ACS EE].dbo.{0}  

                            where    1=1

             and tffc_kicker_model like '%{1}'
                         """.format(table,model))
        #     df = pd.read_sql(q, engine)
            return df
        sw_df_acs=acs_model_sw(model)
#         acs_model_sw(3400,'GD4130-BK')
        if len(sw_df_acs)>0:
            st.write(sw_df_acs)
        else:
            st.write("no-found-acs-sw")
    
        st.sidebar.text("---end---")
        st.sidebar.text("---follow instruction--->")

    #-----------------------


#----------------------------
def tracking(sfc, direction="down"):
    field_direction="sfc_bom_bo" if direction=="down" else "inventory_bo"
    table='SFC_ASSY' 
    site=3400
    df=mes.mesquery("""
        select * from WPPUSER.{}  

            where ROWNUM <100     
             and handle like '{}'
             or {} like '%{}'  
         """.format(table,site,field_direction,sfc))

    #sfc_bom_bo top_down and sfc_bom_bo like '%G19NAQILN%' 
    #inventory_bo bot_up
    cols=["sfc_bom_bo","component_bo","inventory_bo","assembled_date","assembled_by_bo","shop_order_bo"]
    return df[cols]
if report_type=="ASSY tracking up/down":
    #    -----------------------
    snlist = st.sidebar.text_area('{0}'.format("Nhap serial"), '')

    import pandas as pd

    mylist=snlist.split('\n')
    #send list to have list complate
    while '' in mylist:
        mylist.remove('')
    #st.write('My list',mylist)
    st.write('qty sns',len(mylist))
    
    
    if st.sidebar.button("trackindown"):

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
        print("done")
        st.table(dfmain)
    if (st.sidebar.button("trackingup")):

        dfmain=None
        boolfirstdone=False
        for item in mylist:
            sn=item#row['nam']

        #     print(q)
            df=tracking(sn,"up")

            if len(df) >0 and boolfirstdone==False : #loop1
        #         print("now first row",df)
                boolfirstdone=True
        #         print(sn,"=0")
                dfmain=df
        #         print(dfmain)
            else:
                dfmain=pd.concat([dfmain,df], ignore_index=True)
        print("done")
        st.table(dfmain)


        
#--------------


mylist=mes.getAllMachineList()
machine=None
# TODO: check serial status
try:
    machine=st.selectbox("chon may tinh",mylist)
except:
#     st.selectbox("chon may tinh",mylist)
    pass
st.write("select ",machine)
# TODO: Do grant access
if st.button("grant access"):
    mes.grant_access(machine)
#     fr"done {} machine".format(len(mylist))
    st.write("done grant")
# TODO: View db test
if st.button("view"):
    
    df,fn=mes.getHostCommanderlogs(machine,loc=0)
    st.table(df.tail(10))
# TODO: View HC Log

# TODO: logx

# TODO: SFC Step status + show current flow
