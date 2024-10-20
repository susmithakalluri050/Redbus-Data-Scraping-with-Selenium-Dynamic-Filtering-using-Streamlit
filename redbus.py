import streamlit as st
import pandas as pd
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
import datetime


# Telangana bus
lists_t=[]
df_t=pd.read_csv("df_T.csv")
for i,r in df_t.iterrows():
    lists_t.append(r["Route_name"])

# Andhra pradesh bus
lists_a=[]
df_a=pd.read_csv("df_A.csv")
for i,r in df_a.iterrows():
    lists_a.append(r["Route_name"])


# Kerala bus
lists_k=[]
df_k=pd.read_csv("df_KERALA.csv")
for i,r in df_k.iterrows():
    lists_k.append(r["Route_name"])


# Rajasthan bus
lists_r=[]
df_r=pd.read_csv("df_Rsrtc.csv")
for i,r in df_r.iterrows():
    lists_r.append(r["Route_name"])


# South Bengal bus
lists_sb=[]
df_sb=pd.read_csv("df_SBSTC.csv")
for i,r in df_sb.iterrows():
    lists_sb.append(r["Route_name"])


# Himachal bus
lists_h=[]
df_h=pd.read_csv("df_HRTC.csv")
for i,r in df_h.iterrows():
    lists_h.append(r["Route_name"])


# Assam bus
lists_as=[]
df_as=pd.read_csv("df_ASTC.csv")
for i,r in df_as.iterrows():
    lists_as.append(r["Route_name"])



# CHANDIGARH bus
lists_c=[]
df_c=pd.read_csv("df_C.csv")
for i,r in df_c.iterrows():
    lists_c.append(r["Route_name"])


# punjab bus
lists_p=[]
df_p=pd.read_csv("df_P.csv")
for i,r in df_p.iterrows():
    lists_p.append(r["Route_name"])


# Bihar bus
lists_b=[]
df_b=pd.read_csv("df_B.csv")
for i,r in df_b.iterrows():
    lists_b.append(r["Route_name"])

#page layout
st.set_page_config(page_title="Redbus", layout="wide")

#setting streamlit page
st.title("Redbus User Application")
st.image('D:\Capstone projects\Redbus\generic_banner_Ind.png',use_column_width=True)
with st.sidebar:
    st.title("🚍 Travel Filter")
    S = st.selectbox("Select State", [ "Telangana", "Andhra Pradesh", "Kerala", "Rajasthan", "Himachal", "South Bengal", "Assam", "Chandigarh", "Punjab", "Bihar"])
    select_type = st.radio("Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Price Range", ("50-1000", "1000-2000", "2000 and above"))
    t = st.time_input("Select Time",value=None)
    seats = st.selectbox("Seat Availability",("0-10","10-20","20-30","30 and above"))
    min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=3.0, step=0.5)  # Slider for rating


 # telangana bus fare filtering
if S == "Telangana":
    T = st.selectbox("List of Routes",lists_t)

    def type_and_fare(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
        
         # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{T}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID","Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare(select_type, select_fare,seats)
    st.dataframe(df_result)

# Adhra Pradesh bus fare filtering
if S=="Andhra Pradesh":
    A=st.selectbox("List of Routes",lists_a)

    def type_and_fare_A(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"
         
        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{A}"
            AND {bus_type_condition} AND Start_time>='{t}'
            And {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_A(select_type, select_fare,seats)
    st.dataframe(df_result)
        

# kerala bus fare filtering
if S=="Kerala":
    K=st.selectbox("List of Routes",lists_k)

    def type_and_fare_K(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{K}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_K(select_type, select_fare,seats)
    st.dataframe(df_result)

# RAJASTHAN bus fare filtering
if S=="Rajasthan":
    R=st.selectbox("List of Routes",lists_r)

    def type_and_fare_R(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{R}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_R(select_type, select_fare,seats)
    st.dataframe(df_result)  

# South Bengal bus fare filtering       
if S=="South Bengal":
    SB=st.selectbox("List of Routes",lists_sb)

    def type_and_fare_SB(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{SB}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_SB(select_type, select_fare,seats)
    st.dataframe(df_result)

# Himachal bus fare filtering
if S=="Himachal":
    H=st.selectbox("List of Routes",lists_h)

    def type_and_fare_H(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{H}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_H(select_type, select_fare,seats)
    st.dataframe(df_result)


# Assam bus fare filtering
if S=="Assam":
    AS=st.selectbox("List of Routes",lists_as)

    def type_and_fare_AS(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{AS}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_AS(select_type, select_fare,seats)
    slt.dataframe(df_result)

# Chandigarh bus fare filtering
if S=="Chandigarh":
    C=slt.selectbox("List of Routes",lists_c)

    def type_and_fare_C(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{C}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_C(select_type, select_fare,seats)
    st.dataframe(df_result)

# Punjab bus fare filtering
if S=="Punjab":
    P=st.selectbox("List of Routes",lists_p)

    def type_and_fare_P(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{P}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time  DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_P(select_type, select_fare,seats)
    st.dataframe(df_result)

# Bihar bus fare filtering
if S=="Bihar":
    B=st.selectbox("List of Routes",lists_b)

    def type_and_fare_B(bus_type, fare_range,seat_availability):
        conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
        my_cursor = conn.cursor()
        # Define fare range based on selection
        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  

        # Define bus type condition
        if bus_type == "sleeper":
            bus_type_condition = "Bus_type LIKE '%Sleeper%'"
        elif bus_type == "semi-sleeper":
            bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
             # Define seat availability condition
        if seat_availability == "0-10":
            seat_condition = "Seats_Available BETWEEN 0 AND 10"
        elif seat_availability == "10-20":
            seat_condition = "Seats_Available BETWEEN 11 AND 20"
        elif seat_availability == "20-30":
            seat_condition = "Seats_Available BETWEEN 21 AND 30"
        else:  
            seat_condition = "Seats_Available >= 30"

        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{B}"
            AND {bus_type_condition} AND Start_time>='{t}'
            AND {seat_condition}
            AND Ratings >= {min_rating}
            ORDER BY Price and Start_time DESC
        '''
        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])
        return df

    df_result = type_and_fare_B(select_type, select_fare,seats)
    st.dataframe(df_result)

