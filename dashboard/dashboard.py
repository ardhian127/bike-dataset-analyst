import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_number

# Set custom theme for Seaborn
sns.set(style='whitegrid')

def create_monthly_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Ensure 'dateday' is in datetime format
    dataframe['dateday'] = pd.to_datetime(dataframe['dateday'])
    
    # Resample the dataframe by month
    monthly_dataframe = dataframe.resample(rule="M", on="dateday").agg({
        'grand_total': 'sum'
    }).reset_index()  # Reset index to avoid DatetimeIndex issues
    return monthly_dataframe

def create_seasons_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    seasons_cycle = dataframe.groupby(by='season', as_index=False).agg({
        'grand_total': 'sum'
    })
    return seasons_cycle

# Load all bike rental databases
all_database = pd.read_csv("dashboard/all_database.csv")

# Page Header
with st.container():
    st.write('<style>div.stButton > button {font-size: 30px;}</style>', unsafe_allow_html=True)
    st.title('All Bike Rental Databases')

# SEASONAL RENTALS
seasons_dataframe = create_seasons_dataframe(all_database)
st.subheader('Number of bike rentals based on seasons:')


# Seasonal Rentals Plot
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(data=seasons_dataframe, x="season", y="grand_total", marker="o", color="blue", ax=ax)
ax.set_title("Number of Bikes Rented by Season", fontsize=20)
ax.set_xlabel("Season", fontsize=16)
ax.set_ylabel("Grand Total of Rentals", fontsize=16)

# Calculate peak and low values
max_value = seasons_dataframe["grand_total"].max()
min_value = seasons_dataframe["grand_total"].min()

max_season = seasons_dataframe.loc[seasons_dataframe["grand_total"].idxmax(), "season"]
min_season = seasons_dataframe.loc[seasons_dataframe["grand_total"].idxmin(), "season"]

# Annotate peak value
ax.annotate(f"Peak: {max_value}",
            xy=(max_season, max_value),
            xytext=(max_season, max_value + 500),  # Adjust as needed for better visibility
            arrowprops=dict(facecolor='green', shrink=0.05),
            fontsize=12, color="green")

# Annotate low value
ax.annotate(f"Low: {min_value}",
            xy=(min_season, min_value),
            xytext=(min_season, min_value - 500),  # Adjust as needed for better visibility
            arrowprops=dict(facecolor='red', shrink=0.05),
            fontsize=12, color="red")

st.pyplot(fig)



# Seasonal Rentals Explanation
button_label = ("Number of bike rentals based on seasons explanation")
if st.button(button_label):
  st.write(
        """
As depicted in the preceding chart, the Fall season exhibits the highest rental volume, followed closely by Summer. Conversely, Winter and Spring tend to experience lower rental rates, presumably due to unfavorable weather conditions.
        """
    )

# BIKE RENTAL TRENDS
monthly_dataframe = create_monthly_dataframe(all_database)

# Bike Rental Trends Plot
st.subheader("Bicycle rental service during the 2011-2012 period:")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
    monthly_dataframe["dateday"],
    monthly_dataframe["grand_total"],
    color="#1E90FF",
    marker='o'
)
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_title("Bike Rental Trends (2011-2012)", fontsize=18)
ax.set_xlabel("Date", fontsize=14)
ax.set_ylabel("Total Rentals", fontsize=14)
ax.fill_between(monthly_dataframe["dateday"], monthly_dataframe["grand_total"], color="#ADD8E6", alpha=0.3)

# Highlight peak and low points with annotations for monthly trends
max_value = monthly_dataframe["grand_total"].max()
max_date = monthly_dataframe.loc[monthly_dataframe["grand_total"].idxmax(), "dateday"]
min_value = monthly_dataframe["grand_total"].min()
min_date = monthly_dataframe.loc[monthly_dataframe["grand_total"].idxmin(), "dateday"]

ax.annotate(f"Peak: {max_value}",
            xy=(max_date, max_value),
            xytext=(max_date, max_value + 1000),
            arrowprops=dict(facecolor='green', shrink=0.05),
            fontsize=12, color="green")

ax.annotate(f"Low: {min_value}",
            xy=(min_date, min_value),
            xytext=(min_date, min_value - 1000),
            arrowprops=dict(facecolor='red', shrink=0.05),
            fontsize=12, color="red")

st.pyplot(fig)

# Rental Trends Explanation
button_label = "Bicycle rental service during the 2011-2012 period explanation"
if st.button(button_label):
    st.write("""
Data analysis reveals a clear seasonal pattern in bike rental numbers during the 2011-2012 period. There was a significant increase in bike rental demand from mid-2011 to early 2012, indicating a peak season likely influenced by external factors such as favorable weather conditions or special events. The substantial monthly fluctuations suggest that bike rental demand is sensitive to seasonal factors and current events. However, the sharp decline after peaking in early 2012 indicates that other factors, such as changing seasons or alternative recreational activities, may have influenced a decrease in public interest in bike rentals.
        """)
