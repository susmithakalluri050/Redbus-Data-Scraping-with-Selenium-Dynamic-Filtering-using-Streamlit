import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu
import datetime

# Streamlit page layout
st.set_page_config(page_title="Redbus", layout="wide")
st.title("Redbus User Application")
st.image('D:\Capstone projects\Redbus\generic_banner_Ind.png', use_column_width=True)

# Sidebar options
with st.sidebar:
    st.title("🚍 Travel Filter")
    state = st.selectbox("Select State", ["Telangana", "Andhra Pradesh", "Kerala", "Rajasthan", "Himachal", "South Bengal", "Assam", "Chandigarh", "Punjab", "Bihar"])
    bus_type = st.radio("Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    fare_range = st.radio("Price Range", ("50-1000", "1000-2000", "2000 and above"))
    start_time = st.time_input("Select Time",value=None)
    seats = st.selectbox("Seat Availability", ("0-10", "10-20", "20-30", "30 and above"))
    min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=(3.0,5.0),step=0.5)


# Loading data 
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df["Route_name"].tolist()

# Load routes for each state
lists_t = load_data("df_T.csv")   # Telangana
lists_a = load_data("df_A.csv")   # Andhra Pradesh
lists_k = load_data("df_KERALA.csv")  # Kerala
lists_r = load_data("df_Rsrtc.csv")  # Rajasthan
lists_sb = load_data("df_SBSTC.csv")  # South Bengal
lists_h = load_data("df_HRTC.csv")  # Himachal
lists_as = load_data("df_ASTC.csv")  # Assam
lists_c = load_data("df_C.csv")  # Chandigarh
lists_p = load_data("df_P.csv")  # Punjab
lists_b = load_data("df_B.csv")  # Bihar

# State-wise route selection
if state == "Telangana":
    route = st.selectbox("List of Routes", lists_t)
elif state == "Andhra Pradesh":
    route = st.selectbox("List of Routes", lists_a)
elif state == "Kerala":
    route = st.selectbox("List of Routes", lists_k)
elif state == "Rajasthan":
    route = st.selectbox("List of Routes", lists_r)
elif state == "South Bengal":
    route = st.selectbox("List of Routes", lists_sb)
elif state == "Himachal":
    route = st.selectbox("List of Routes", lists_h)
elif state == "Assam":
    route = st.selectbox("List of Routes", lists_as)
elif state == "Chandigarh":
    route = st.selectbox("List of Routes", lists_c)
elif state == "Punjab":
    route = st.selectbox("List of Routes", lists_p)
elif state == "Bihar":
    route = st.selectbox("List of Routes", lists_b)

# Global function for filtering bus data
def type_and_fare_seat(bus_type, fare_range, seat_availability):
    conn = mysql.connector.connect(host="localhost", user="root", password="susmitha@050", database="RED_BUS")
    my_cursor = conn.cursor()

    # Define fare range
    if fare_range == "50-1000":
        fare_min, fare_max = 50, 1000
    elif fare_range == "1000-2000":
        fare_min, fare_max = 1000, 2000
    else:
        fare_min, fare_max = 2000, 100000  

    # Define bus type condition
    if bus_type == "Sleeper":
        bus_type_condition = "Bus_type LIKE '%Sleeper%'"
    elif bus_type == "Semi-Sleeper":
        bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper%'"
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

    # Query to filter bus data
    query = f'''
        SELECT * FROM bus_details 
        WHERE Price BETWEEN {fare_min} AND {fare_max}
        AND Route_name = "{route}"
        AND {bus_type_condition} AND Start_time >= '{start_time}'
        AND {seat_condition}
        AND Ratings BETWEEN {min_rating[0]} and {min_rating[1]}
        ORDER BY Ratings DESC,Price, Start_time DESC
    '''
    my_cursor.execute(query)
    out = my_cursor.fetchall()
    conn.close()

    # Convert the output to a DataFrame
    df = pd.DataFrame(out, columns=[
        "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
        "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
    ])
    return df

# Display filtered results based on selected filters
df_result = type_and_fare_seat(bus_type, fare_range, seats)
st.dataframe(df_result)
