import streamlit as st
import pandas as pd 

st.title('Amazon Analytics')

# Button to show the dataframe
show_button = st.button('Show Data')

# Reading the data only once using a cached function
@st.cache_resource
def load_data():
    df = pd.read_csv('Superstore.csv', encoding='latin-1')
    df['year'] = pd.to_datetime(df['Order Date'],format='mixed').dt.year
    return df

df = load_data()

if show_button:
    st.dataframe(df)

# Function to get top n categories based on profit
def top(category, n):
    df = load_data()
    result = df.groupby(category).agg(
        highest_profit=('Profit', 'sum')
    ).sort_values('highest_profit', ascending=False).head(n)
    return result

st.header('Top N Category Profit')

cat = st.text_input('Enter the Category you want:')
topn = int(st.number_input('Top N', min_value=1, step=1))

calculate_top = st.button('Calculate Top N')
if calculate_top:
    var = top(cat, topn)
    st.dataframe(var)
    # Plotting the bar chart
    st.bar_chart(var)

st.header('Yearly Profit')

# Function to calculate total profit for a specified year
def yearly(year):
    df = load_data()
    return df.loc[df['year'] == year]['Profit'].sum(),df.loc[df['year'] == year]['Sales'].sum()

year = int(st.number_input('Enter Year', value=2020))
calculate_yearly = st.button('Calculate Yearly Profit')
if calculate_yearly:
    total_profit,total_sales = yearly(year)
    # Displaying the total profit as a metric
    st.metric(label=f"Total Profit for {year}", value=f"${total_profit:.2f}")
    st.metric(label=f"Total Sale for {year}", value=f"${total_sales:.2f}")
