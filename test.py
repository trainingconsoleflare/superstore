import streamlit as st
import pandas as pd 

st.title('Amazon Analytics')

# Button to show the dataframe
show_button = st.button('Show Data')

# Reading the data only once using a cached function
@st.cache_resource
def load_data():
    return pd.read_csv('Superstore.csv', encoding='latin-1')

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

calculate = st.button('Calculate')
if calculate:
    var = top(cat, topn)
    st.dataframe(var)
    # Plotting the bar chart
    st.bar_chart(var)
