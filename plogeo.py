import os
import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import mysql.connector
import json
import streamlit as st
from streamlit_option_menu import option_menu
import requests



# GETTING INDIA MAP CO-ORDINATES DATA FROM URL
url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(url)
data1 = json.loads(response.content)


# sql connection 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("use Phonepay_pulse")



# AGGREGATED_INSURANCE DF  
mycursor.execute("select * from AGGREGATED_INSURANCE")
mydb.commit()
Table_1=mycursor.fetchall()
Aggre_Insur=pd.DataFrame(Table_1,columns=[i[0] for i in mycursor.description])
A_I_YR=list(Aggre_Insur["YEAR"].unique())
A_I_QR=list(Aggre_Insur["QUARTER"].unique())
A_I_QR.sort()


# AGGREGATED_TRANSACTION DF
mycursor.execute("select * from AGGREGATED_TRANSACTION")
mydb.commit()
Table_2=mycursor.fetchall()
Aggre_Trans=pd.DataFrame(Table_2,columns=[i[0] for i in mycursor.description])
A_T_YR=list(Aggre_Trans["YEAR"].unique())
A_T_QR=list(Aggre_Trans["QUARTER"].unique())
A_T_QR.sort()


# AGGREGATED_USER DF
mycursor.execute("select * from AGGREGATED_USER")
mydb.commit()
Table_3=mycursor.fetchall()
Aggre_User=pd.DataFrame(Table_3,columns=[i[0] for i in mycursor.description])
A_U_YR=list(Aggre_User["YEAR"].unique())
A_U_QR=list(Aggre_User["QUARTER"].unique())
A_U_QR.sort()



# MAP_INSURANCE DF
mycursor.execute("select * from MAP_INSURANCE")
mydb.commit()
Table_4=mycursor.fetchall()
Map_Insur=pd.DataFrame(Table_4,columns=[i[0] for i in mycursor.description])
M_I_YR=list(Map_Insur["YEAR"].unique())
M_I_QR=list(Map_Insur["QUARTER"].unique())
M_I_QR.sort()

# MAP_TRANSACTION DF
mycursor.execute("select * from MAP_TRANSACTION")
mydb.commit()
Table_5=mycursor.fetchall()
Map_Trans=pd.DataFrame(Table_5,columns=[i[0] for i in mycursor.description])
M_T_YR=list(Map_Trans["YEAR"].unique())
M_T_QR=list(Map_Trans["QUARTER"].unique())
M_T_QR.sort()


# MAP_User DF
mycursor.execute("select * from MAP_USER")
mydb.commit()
Table_6=mycursor.fetchall()
Map_User=pd.DataFrame(Table_6,columns=[i[0] for i in mycursor.description])
M_U_YR=list(Map_User["YEAR"].unique())
M_U_QR=list(Map_User["QUARTER"].unique())
M_U_QR.sort()


# TOP_INSURANCE DF
mycursor.execute("select * from TOP_INSURANCE")
mydb.commit()
Table_7=mycursor.fetchall()
Top_Insur=pd.DataFrame(Table_7,columns=[i[0] for i in mycursor.description])
T_I_YR=list(Top_Insur["YEAR"].unique())
T_I_QR=list(Top_Insur["QUARTER"].unique())
T_I_QR.sort()


# TOP_TRANSACTION DF
mycursor.execute("select * from TOP_TRANSACTION")
mydb.commit()
Table_8=mycursor.fetchall()
Top_Trans=pd.DataFrame(Table_8,columns=[i[0] for i in mycursor.description])
T_T_YR=list(Top_Trans["YEAR"].unique())
T_T_QR=list(Top_Trans["QUARTER"].unique())
T_T_QR.sort()


# TOP_USER DF
mycursor.execute("select * from TOP_USER")
mydb.commit()
Table_9=mycursor.fetchall()
Top_User=pd.DataFrame(Table_9,columns=[i[0] for i in mycursor.description])
T_U_YR=list(Top_User["YEAR"].unique())
T_U_QR=list(Top_User["QUARTER"].unique())
T_U_QR.sort()


##STREAMLIT CODE SPACE
#----------------------------------------------------------------------##

st.set_page_config(layout="wide")

st.title(":rainbow[Phonepe Pulse Data Visualization and Exploration]") 
#colors: blue, green, orange, red, violet, gray/grey, rainbow.

selected = option_menu(None, ["Aggregated Analysis","Map Analysis","Top Analysis"], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0, orientation="horizontal")


# CREATING OPTION MENU FOR Aggregated Analysis
if selected=="Aggregated Analysis":

  Type_1=st.radio("Aggregated",["Insurance", "Transaction", "User"],horizontal=True)

## AGGREGATED_INSURANCE 
  if Type_1=="Insurance":
    col1, col2 = st.columns(2)
    with col1:
      option1 = st.selectbox("Select Year",A_I_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option1)

      A_I_YR2=Aggre_Insur[Aggre_Insur["YEAR"]==option1]
      A_I_QR2=A_I_YR2["QUARTER"].unique()

    with col2:
      option2 = st.selectbox("Select Quarter",A_I_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option2)
  

    if st.button("Display", type="primary"):
      if option1 != None:        
        if option2 != None:
          A_I_M=Aggre_Insur[Aggre_Insur["YEAR"]==option1]
          A_I_M_Q=A_I_M[A_I_M["QUARTER"]==option2].reset_index(drop=True)
            
          fig1=px.choropleth(A_I_M_Q, locations="STATE",hover_data=["TRANSACTION_AMOUNT", "TRANSACTION_COUNT"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig1.update_geos(fitbounds="locations",visible=False)
          fig1.update_layout(title_text = f'Aggregated {Type_1} Analysis [Year : {option1} & Quarter : {option2}]')          
          st.plotly_chart(fig1)    
            
          fig_chart2=px.bar(A_I_M_Q, x="STATE", y="TRANSACTION_AMOUNT",
                            hover_data="TRANSACTION_COUNT",  
                            color="TRANSACTION_NAME", width=1000 , height =800,
                            title = f'Aggregated {Type_1} Analysis [Year : {option1} & Quarter : {option2}]')
          st.plotly_chart(fig_chart2)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")


# AGGREGATED_TRANSACTION 
  if Type_1=="Transaction":
    col3, col4 = st.columns(2)
    with col3:
      option3 = st.selectbox("Select Year",A_T_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option3)

      A_T_YR2=Aggre_Trans[Aggre_Trans["YEAR"]==option3]
      A_T_QR2=A_T_YR2["QUARTER"].unique()

    with col4:
      option4 = st.selectbox("Select Quarter",A_T_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option4)
  

    if st.button("Display", type="primary"):
      if option3 != None:        
        if option4 != None:
          A_T_M=Aggre_Trans[Aggre_Trans["YEAR"]==option3]
          A_T_M_Q=A_T_M[A_T_M["QUARTER"]==option4].reset_index(drop=True)

          gb=A_T_M_Q.groupby("STATE").agg({"TRANSACTION_COUNT" : "sum",	"TRANSACTION_AMOUNT" : "sum"}).reset_index()
      
          fig2=px.choropleth(gb, locations="STATE",hover_data=["TRANSACTION_AMOUNT", "TRANSACTION_COUNT"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", 
                            color='STATE')
          fig2.update_geos(fitbounds="locations",visible=False)
          fig2.update_layout(title_text = f'Aggregated {Type_1} Analysis [Year : {option3} & Quarter : {option4}]')          
          st.plotly_chart(fig2)

          fig_chart3=px.bar(A_T_M_Q, x="STATE", y="TRANSACTION_AMOUNT",
                            hover_data="TRANSACTION_COUNT",  
                            color="TRANSACTION_NAME", width=1000 , height =800,
                            title = f'Aggregated {Type_1} Analysis [Year : {option3} & Quarter : {option4}]')
          st.plotly_chart(fig_chart3)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")


# AGGREGATED_USER
  if Type_1=="User":
    col5, col6 = st.columns(2)
    with col5:
      option5 = st.selectbox("Select Year",A_U_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option5)

      A_U_YR2=Aggre_User[Aggre_User["YEAR"]==option5]
      A_U_QR2=A_U_YR2["QUARTER"].unique()

    with col6:
      option6 = st.selectbox("Select Quarter",A_U_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option6)
  

    if st.button("Display", type="primary"):
      if option5 != None:        
        if option6 != None:
          A_U_M=Aggre_User[Aggre_User["YEAR"]==option5]
          A_U_M_Q=A_U_M[A_U_M["QUARTER"]==option6].reset_index(drop=True)
      
          gb2=A_U_M_Q.groupby("STATE").agg({"TRANSACTION_COUNT" : "sum",	"PERCENTAGE" : "sum"}).reset_index()

                      
          fig3=px.choropleth(gb2, locations="STATE",hover_data=['TRANSACTION_COUNT', 'PERCENTAGE'],geojson=data1,
                            width=1000 , height =800, projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig3.update_geos(fitbounds="locations",visible=False)
          fig3.update_layout(title_text = f'Aggregated {Type_1} Analysis [Year : {option5} & Quarter : {option6}]')          
          st.plotly_chart(fig3)
          
          fig_chart4=px.bar(A_U_M_Q, x="STATE", y="TRANSACTION_COUNT",
                            hover_data="PERCENTAGE",  
                            color="USER_BY_DEVICE", width=1000 , height =800,
                            title = f'Aggregated {Type_1} Analysis by User By Device [Year : {option5} & Quarter : {option6}]')
          st.plotly_chart(fig_chart4)            

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")


# CREATING OPTION MENU FOR Map Analysis
if selected=="Map Analysis":

  Type_2=st.radio("Map",["Insurance", "Transaction", "User"],horizontal=True)

# MAP_INSURANCE
  if Type_2=="Insurance":
    col7, col8 = st.columns(2)
    with col7:
      option7 = st.selectbox("Select Year ",M_I_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option7)

      M_I_YR2=Map_Insur[Map_Insur["YEAR"]==option7]
      M_I_QR2=M_I_YR2["QUARTER"].unique()
      
    with col8:
      option8 = st.selectbox("Select Quarter ",M_I_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option8)
  

    if st.button("Display ", type="primary"):
      if option7 != None:        
        if option8 != None:
          M_I_M=Map_Insur[Map_Insur["YEAR"]==option7]
          M_I_M_Q=M_I_M[M_I_M["QUARTER"]==option8].reset_index(drop=True)

          
          gb3=M_I_M_Q.groupby("STATE").agg({"TRANSACTION_AMOUNT" : "sum",	"TRANSACTION_COUNT" : "sum"}).reset_index()


          fig4=px.choropleth(gb3, locations="STATE",hover_data=["TRANSACTION_AMOUNT", "TRANSACTION_COUNT"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig4.update_geos(fitbounds="locations",visible=False)
          fig4.update_layout(title_text = f'Map {Type_2} Analysis [Year : {option7} & Quarter : {option8}]')          
          st.plotly_chart(fig4)

          fig_chart5=px.bar(M_I_M_Q, x="STATE", y="TRANSACTION_AMOUNT",
                            hover_data="TRANSACTION_COUNT",  
                            color="DISTRICTS", width=1000 , height =800,
                            title = f'Map {Type_2} Analysis by Districts [Year : {option7} & Quarter : {option8}]')
          st.plotly_chart(fig_chart5)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")

# MAP_TRANSACTION
  if Type_2=="Transaction":
    col9, col10 = st.columns(2)
    with col9:
      option9 = st.selectbox("Select Year ",M_T_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option9)

      M_T_YR2=Map_Trans[Map_Trans["YEAR"]==option9]
      M_T_QR2=M_T_YR2["QUARTER"].unique()
    
    with col10:
      option10 = st.selectbox("Select Quarter ",M_T_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option10)
  

    if st.button("Display ", type="primary"):
      if option9 != None:        
        if option10 != None:
          M_T_M=Map_Trans[Map_Trans["YEAR"]==option9]
          M_T_M_Q=M_T_M[M_T_M["QUARTER"]==option10].reset_index(drop=True)

          gb4=M_T_M_Q.groupby("STATE").agg({"TRANSACTION_AMOUNT" : "sum",	"TRANSACTION_COUNT" : "sum"}).reset_index()

          fig5=px.choropleth(gb4, locations="STATE",hover_data=["TRANSACTION_AMOUNT", "TRANSACTION_COUNT"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig5.update_geos(fitbounds="locations",visible=False)
          fig5.update_layout(title_text = f'Map {Type_2} Analysis [Year : {option9} & Quarter : {option10}]')          
          st.plotly_chart(fig5)

          fig_chart6=px.bar(M_T_M_Q, x="STATE", y="TRANSACTION_AMOUNT",
                            hover_data="TRANSACTION_COUNT",  
                            color="DISTRICTS", width=1000 , height =800,
                            title = f'Map {Type_2} Analysis by Districts [Year : {option9} & Quarter : {option10}]')
          st.plotly_chart(fig_chart6)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")      


# MAP_User
  if Type_2=="User":
    col11, col12 = st.columns(2)
    with col11:
      option11 = st.selectbox("Select Year ",M_U_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option11)

      M_U_YR2=Map_User[Map_User["YEAR"]==option11]
      M_U_QR2=M_U_YR2["QUARTER"].unique()
      
    with col12:
      option12 = st.selectbox("Select Quarter ",M_U_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option12)
  

    if st.button("Display ", type="primary"):
      if option11 != None:        
        if option12 != None:
          M_U_M=Map_User[Map_User["YEAR"]==option11]
          M_U_M_Q=M_U_M[M_U_M["QUARTER"]==option12].reset_index(drop=True)

          gb5=M_U_M_Q.groupby("STATE").agg({"REG_USER" : "sum",	"APP_OPENS" : "sum"}).reset_index()

          fig6=px.choropleth(gb5, locations="STATE",hover_data=["REG_USER", "APP_OPENS"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig6.update_geos(fitbounds="locations",visible=False)
          fig6.update_layout(title_text = f'Map {Type_2} Analysis [Year : {option11} & Quarter : {option12}]')          
          st.plotly_chart(fig6)

          fig_chart7=px.bar(M_U_M_Q, x="STATE", y="REG_USER",
                            hover_data="APP_OPENS",  
                            color="DISTRICTS", width=1000 , height =800,
                            title = f'Map {Type_2} Analysis by Districts [Year : {option11} & Quarter : {option12}]')
          st.plotly_chart(fig_chart7)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")    
    


# CREATING OPTION MENU FOR Top Analysis
if selected=="Top Analysis":
  Type_3=st.radio("Top",["Insurance", "Transaction", "User"],horizontal=True)

# TOP_INSURANCE
  if Type_3=="Insurance":
    col13, col14 = st.columns(2)
    with col13:
      option13 = st.selectbox(" Select Year ",T_I_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option13)

      T_I_YR2=Top_Insur[Top_Insur["YEAR"]==option13]
      T_I_QR2=T_I_YR2["QUARTER"].unique()
      
    with col14:
      option14 = st.selectbox(" Select Quarter ",T_I_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option14)
  

    if st.button(" Display ", type="primary"):
      if option13 != None:        
        if option14 != None:
          T_I_M=Top_Insur[Top_Insur["YEAR"]==option13]
          T_I_M_Q=T_I_M[T_I_M["QUARTER"]==option14].reset_index(drop=True)


          gb6=T_I_M_Q.groupby("STATE").agg({"TRANSACTION_AMOUNT" : "sum",	"TRANSACTION_COUNT" : "sum"}).reset_index()

          fig7=px.choropleth(gb6, locations="STATE",hover_data=["TRANSACTION_AMOUNT", "TRANSACTION_COUNT"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig7.update_geos(fitbounds="locations",visible=False)
          fig7.update_layout(title_text = f'Top {Type_3} Analysis [Year : {option13} & Quarter : {option14}]')          
          st.plotly_chart(fig7)

          fig_chart8=px.bar(T_I_M_Q, x="STATE", y="TRANSACTION_AMOUNT",
                            hover_data=["TRANSACTION_COUNT","PINCODES"], width=1000 , height =800, color="PINCODES",
                            title = f'Map {Type_3} Analysis by Districts [Year : {option13} & Quarter : {option14}]')
          st.plotly_chart(fig_chart8)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")


# TOP_TRANSACTION 
  if Type_3=="Transaction":
    col15, col16 = st.columns(2)
    with col15:
      option15 = st.selectbox(" Select Year ",T_T_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option15)

      T_T_YR2=Top_Trans[Top_Trans["YEAR"]==option15]
      T_T_QR2=T_T_YR2["QUARTER"].unique()
      
    with col16:
      option16 = st.selectbox(" Select Quarter ",T_T_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option16)
  

    if st.button(" Display ", type="primary"):
      if option15 != None:        
        if option16 != None:
          T_T_M=Top_Trans[Top_Trans["YEAR"]==option15]
          T_T_M_Q=T_T_M[T_T_M["QUARTER"]==option16].reset_index(drop=True)


          gb7=T_T_M_Q.groupby("STATE").agg({"TRANSACTION_AMOUNT" : "sum",	"TRANSACTION_COUNT" : "sum"}).reset_index()
          
          fig8=px.choropleth(gb7, locations="STATE",hover_data=["TRANSACTION_AMOUNT", "TRANSACTION_COUNT"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig8.update_geos(fitbounds="locations",visible=False)
          fig8.update_layout(title_text = f'Top {Type_3} Analysis [Year : {option15} & Quarter : {option16}]')          
          st.plotly_chart(fig8)

          fig_chart9=px.bar(T_T_M_Q, x="STATE", y="TRANSACTION_AMOUNT",
                            hover_data=["TRANSACTION_COUNT","PINCODES"], width=1000 , height =800, color="PINCODES",
                            title = f'Map {Type_3} Analysis by Districts [Year : {option15} & Quarter : {option16}]')
          st.plotly_chart(fig_chart9)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")       


# TOP_USER 
  if Type_3=="User":
    col17, col18 = st.columns(2)
    with col17:
      option17 = st.selectbox(" Select Year ",T_U_YR,index=None ,placeholder="Choose an option")
      st.write('YEAR', option17)

      T_U_YR2=Top_User[Top_User["YEAR"]==option17]
      T_U_QR2=T_U_YR2["QUARTER"].unique()
      
    with col18:
      option18 = st.selectbox(" Select Quarter ",T_U_QR2,index=None ,placeholder="Choose an option")
      st.write('QUARTER', option18)
  

    if st.button(" Display ", type="primary"):
      if option17 != None:        
        if option18 != None:
          T_U_M=Top_User[Top_User["YEAR"]==option17]
          T_U_M_Q=T_U_M[T_U_M["QUARTER"]==option18].reset_index(drop=True)
          
          gb8=T_U_M_Q.groupby("STATE").agg({"REG_USER" : "sum"}).reset_index()

          fig9=px.choropleth(gb8, locations="STATE",hover_data=["REG_USER"],geojson=data1,
                            width=1000 , height =800,projection="mercator" ,hover_name="STATE" ,featureidkey="properties.ST_NM", color='STATE')
          fig9.update_geos(fitbounds="locations",visible=False)
          fig9.update_layout(title_text = f'Top {Type_3} Analysis [Year : {option17} & Quarter : {option18}]')          
          st.plotly_chart(fig9)

          fig_chart10=px.bar(T_U_M_Q, x="STATE", y="REG_USER",
                            hover_data=["REG_USER","PINCODES"], width=1000 , height =800, color="PINCODES",
                            title = f'Map {Type_3} Analysis by Districts [Year : {option17} & Quarter : {option18}]')
          st.plotly_chart(fig_chart10)

        else:
          st.warning("Select Quarter")
      else:
        st.warning("Select Year")