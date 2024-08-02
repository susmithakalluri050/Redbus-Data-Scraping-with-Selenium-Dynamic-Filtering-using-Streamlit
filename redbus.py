# importing libraries
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
import time

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










#setting up streamlit page
slt.set_page_config(layout="wide")

web=option_menu(menu_title="🚌OnlineBus",
                options=["Home","📍States and Routes"],
                icons=["house","info-circle"],
                orientation="horizontal"
                )
# Home page setting
if web=="Home":
    slt.image("redBus-Logo.jpg",width=200)
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    slt.subheader(":blue[Domain:]  Transportation")
    slt.subheader(":blue[Objective:] ")
    slt.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
    slt.subheader(":blue[Overview:]") 
    slt.markdown("Selenium: Selenium is a tool used for automating web browsers. It is commonly used for web scraping, which involves extracting data from websites. Selenium allows you to simulate human interactions with a web page, such as clicking buttons, filling out forms, and navigating through pages, to collect the desired data...")
    slt.markdown('''Pandas: Use the powerful Pandas library to transform the dataset from CSV format into a structured dataframe.
                    Pandas helps data manipulation, cleaning, and preprocessing, ensuring that data was ready for analysis.''')
    slt.markdown('''MySQL: With help of SQL to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                    and the data was efficiently inserted into relevant tables for storage and retrieval.''')
    slt.markdown("Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.")
    slt.subheader(":blue[Skill-take:]")
    slt.markdown("Selenium, Python, Pandas, MySQL,mysql-connector-python, Streamlit.")
    slt.subheader(":blue[Developed-by:]  KALLURI SUSMITHA")

# States and Routes page setting
if web == "📍States and Routes":
    S = slt.selectbox("Lists of States", [ "Telangana", "Adhra Pradesh", "Kerala", "Rajastan","Himachal",
                                          "South Bengal","Assam", "Chandigarh", "Punjab", "Bihar"])
    
    col1,col2=slt.columns(2)
    with col1:
        select_type = slt.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = slt.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    TIME=slt.time_input("select the time")

    # telangana bus fare filtering
    if S == "Telangana":
        T = slt.selectbox("List of routes",lists_t)

        def type_and_fare(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{T}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare(select_type, select_fare)
        slt.dataframe(df_result)

    # Adhra Pradesh bus fare filtering
    if S=="Adhra Pradesh":
        A=slt.selectbox("list of routes",lists_a)

        def type_and_fare_A(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_A(select_type, select_fare)
        slt.dataframe(df_result)
          

    # kerala bus fare filtering
    if S=="Kerala":
        K=slt.selectbox("list of routes",lists_k)

        def type_and_fare_K(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{K}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_K(select_type, select_fare)
        slt.dataframe(df_result)

    # RAJASTHAN bus fare filtering
    if S=="Rajasthan":
        R=slt.selectbox("list of routes",lists_r)

        def type_and_fare_R(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{R}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_R(select_type, select_fare)
        slt.dataframe(df_result)  

    # South Bengal bus fare filtering       
    if S=="South Bengal":
        SB=slt.selectbox("list of rotes",lists_sb)

        def type_and_fare_SB(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{SB}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_SB(select_type, select_fare)
        slt.dataframe(df_result)
    
    # Himachal bus fare filtering
    if S=="Himachal":
        H=slt.selectbox("list of rotes",lists_h)

        def type_and_fare_H(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{H}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_H(select_type, select_fare)
        slt.dataframe(df_result)


    # Assam bus fare filtering
    if S=="Assam":
        AS=slt.selectbox("list of rotes",lists_as)

        def type_and_fare_AS(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{AS}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_AS(select_type, select_fare)
        slt.dataframe(df_result)

    # Chandigarh bus fare filtering
    if S=="Chandigarh":
        C=slt.selectbox("list of rotes",lists_c)

        def type_and_fare_C(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{C}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_C(select_type, select_fare)
        slt.dataframe(df_result)

    # Punjab bus fare filtering
    if S=="Punjab":
        P=slt.selectbox("list of rotes",lists_p)

        def type_and_fare_P(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{P}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_P(select_type, select_fare)
        slt.dataframe(df_result)

  # Bihar bus fare filtering
    if S=="Bihar":
        B=slt.selectbox("list of rotes",lists_b)

        def type_and_fare_B(bus_type, fare_range):
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

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{B}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
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

        df_result = type_and_fare_B(select_type, select_fare)
        slt.dataframe(df_result)



