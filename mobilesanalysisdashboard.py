import pandas as pd
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(r"C:\Users\DELL\Desktop\DataScience_Project\final_cleaned.csv")

# Converting all the ram column values into GB (gigabytes)
data['RAM'] = data['RAM'] / 1000
data['RAM'] = data['RAM'].round(2)

#Making new column of price range
labels = ['Rs.10000 and Below','Rs.10000 - Rs.20000','Rs.20000 - Rs.30000','Rs.30000 - Rs.40000','Rs.40000 - Rs.50000','Rs.50000 - Rs.60000','Rs.60000 - Rs.70000','Rs.70000 - Rs.80000','Rs.80000 - Rs.90000','Rs.90000 - Rs.100000','Rs.100000 And Above']
bins = [0,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,500000]
data['PriceRange'] = pd.cut(data['Price'],bins= bins,labels=labels)

# Streamlit
st.set_page_config(page_title="Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")



# Sidebar
st.sidebar.header("Please Filter Here:")

brand = st.sidebar.multiselect("Select the Brand:",
                               options=data["brand"].unique())

PriceRange = st.sidebar.multiselect("Select the Price Range:",
                               options=data["PriceRange"].unique())

st.sidebar.markdown("---")

#Creating Buttons for graphs 
def chipsetdistributiongraph():
    d3 = (data.groupby('Chipset')['brand'].count().sort_values(ascending=False).head(15)).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(d3['Chipset'], d3['brand'], color='cyan')
    ax.set_xlabel('Chipset')
    ax.set_ylabel('No. of brands')
    ax.set_title('Chipset Distribution as per the brands')
    ax.set_xticks(range(len(d3['Chipset'])))
    ax.set_xticklabels(d3['Chipset'], rotation=90)
    for i in bars:
        value = i.get_height()
        ax.text(i.get_x() + i.get_width() / 2, value + 0.05, round(value, 2), ha='center', va='top')
    st.pyplot(fig)

def screensizedistribution():
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.histplot(data=data, x='Screen Size', multiple='stack', kde=True, ax=ax)
    ax.set_title('Distribution of Screen Sizes by Brand')
    ax.set_xlabel('Screen Size (inches)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

if 'show_chipset_graph' not in st.session_state:
    st.session_state.show_chipset_graph = False
if 'show_screen_size_histogram' not in st.session_state:
    st.session_state.show_screen_size_histogram = False

#
st.sidebar.markdown("## Chipset Graph")
chipset_col1, chipset_col2 = st.sidebar.columns(2)
if chipset_col1.button('Show Chipset Graph'):
    st.session_state.show_chipset_graph = True
if chipset_col2.button('Hide Chipset Graph'):
    st.session_state.show_chipset_graph = False

#
st.sidebar.markdown("## Screen Size Graph")
screensize_col1, screensize_col2 = st.sidebar.columns(2)
if screensize_col1.button('Show Screen Size Histogram'):
    st.session_state.show_screen_size_histogram = True
if screensize_col2.button('Hide Screen Size Histogram'):
    st.session_state.show_screen_size_histogram = False

if st.session_state.show_chipset_graph:
    chipsetdistributiongraph()
if st.session_state.show_screen_size_histogram:
    screensizedistribution()



# Filter the data based on selections
query = []
if brand:
    query.append(f"brand in @brand")
if PriceRange:
    query.append(f"PriceRange in @PriceRange")
#if RAM:
#    query.append(f"RAM in @RAM")

query_string = " & ".join(query)

if query_string:
    df_selection = data.query(query_string)
else:
    df_selection = data


# Main Page
st.title(":bar_chart: Mobiles Dashboard")
#st.markdown("##")

# Top KPIs
total_mobiles = int(df_selection.shape[0])

average_ratings = round(df_selection['Rating'].mean(), 1)
if average_ratings >=0:
    average_ratings = average_ratings
elif average_ratings == np.nan:
    average_ratings = 0
elif average_ratings == 'nan':
    average_ratings = 0



#creating columns
left_column, right_column = st.columns(2,vertical_alignment='top')
with left_column:
    st.subheader("Total count of mobiles :")
    st.subheader(total_mobiles)
with right_column:
    st.subheader("Average rating :")
    st.subheader(f"{average_ratings}")

#
st.dataframe(df_selection[['brand','Name','Price','Rating','RAM','Chipset','Display Type']],height=350) 
st.markdown("---")




