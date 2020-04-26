import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st


url = 'https://github.com/rakesh-choudhury/Dataset/raw/master/YouTube.csv'

df = pd.read_csv(url,sep=",")


selection = st.selectbox('Select the category', df.Category.unique())
nation = st.selectbox('Select the Country', df.Country.unique())
df = df[(df['Category'] == selection)&(df['Country'] == nation)]
st.title('Trend Metrics of Different Youtube Channels')
opt = st.multiselect('Select Channel', df.channel_title.unique().tolist(), default=[df.iloc[1]['channel_title']])

dr_noz = df[df['channel_title'].isin(opt)]

dr_noz['publish_time'] =  pd.to_datetime(dr_noz['publish_time'])

dr_noz['publish_time'] = dr_noz['publish_time'].dt.date

dr_noz['publish_time'] = pd.DatetimeIndex(dr_noz['publish_time']).month
dn1 = dr_noz.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'video_id', 'trending_date', 'title', 'Category', 'tags', 'comment_count', 'thumbnail_link', 'comments_disabled',
                  'ratings_disabled', 'video_error_or_removed', 'Country', 'tags_clean'], axis = 'columns')
#dn1 = dn1.groupby(['publish_time']).mean()
dn1 = dn1.groupby(['publish_time', 'channel_title']).mean()

# Scaling the columns

scaler = MinMaxScaler()

scaler.fit(dn1[['views']])
dn1['views'] = scaler.transform(dn1[['views']])

scaler.fit(dn1[['like_percentage']])
dn1['like_percentage'] = scaler.transform(dn1[['like_percentage']])

# Trend_metric formula

t_m = dn1["views"] + dn1["like_percentage"] + dn1["popular"] + dn1["sent_score"]

dn1['Trend_Metric'] = t_m

dn2 = dn1.reset_index()


# Scaled_ROi column added
n = dn2.index
roi_year = dn2['Trend_Metric'] * 0.9 ** n
dn2['Scaled_ROI'] = roi_year

roi = dn2.groupby('channel_title').sum()

fig = go.Figure()
for i in dn2.channel_title.unique():
  dn3 = dn2[dn2['channel_title']==i]
  x = dn3.publish_time
  y = dn3.Trend_Metric
  fig.add_trace(go.Scatter(x=x, y=y, name=i))



fig.update_layout(
    title="Trend of Channels",
    xaxis_title="Month",
    yaxis_title="Trend_Score",)

st.plotly_chart(fig)
st.markdown('## Return on investment for different channels')
labels = roi.index.values
values = roi.Scaled_ROI

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
st.plotly_chart(fig)