import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
import streamlit as st

import plotly.graph_objects as go
plt.style.use('ggplot')

import seaborn as sns

import plotly

import plotly.graph_objs as go

from plotly.graph_objs import *



url = 'https://github.com/rakesh-choudhury/Dataset/raw/master/YouTube.csv'

df = pd.read_csv(url,sep=",")
youtube = df

###############################################################################

#youtube = pd.read_csv("/content/drive/My Drive/Datasets/Final_YouTube_Dataset/YouTube.csv")
st.title('Youtube Trend Analysis')

st.markdown('### Youtube Dataset')

youtube['trending_date'] = pd.to_datetime(youtube['trending_date'], format='%y.%d.%m') #parsing

youtube["ldratio"] = youtube["likes"] / youtube["dislikes"]

youtube["perc_comment"] = youtube["comment_count"] / youtube["views"]
youtube["perc_reaction"] = (youtube["likes"] + youtube["dislikes"]) / youtube["views"]
st.write(youtube.head())

st.markdown('## Dataset category overview')

labels = list(youtube.Category.value_counts().index.values)
values = list(youtube.Category.value_counts().values)
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
#trace = go.Pie(labels=labels, values=values)
#iplot([trace], filename='basic_pie_chart')
st.plotly_chart(fig)

def distribution_cont(youtube, var):
    plt.hist(youtube[youtube["dislikes"] != 0][var])
    plt.xlabel(f"{var}")
    plt.ylabel("Count")
    plt.title(f"Distribution of Trending Video {var}")
    plt.show()
option = st.selectbox('select type',("views", "likes", "dislikes", "comment_count", "ldratio", "perc_reaction", "perc_comment"))
#for i in ["views", "likes", "dislikes", "comment_count", "ldratio", "perc_reaction", "perc_comment"]:
distribution_cont(youtube, option)
st.pyplot()

contvars = youtube[["views", "likes", "dislikes", "comment_count", "ldratio", "perc_comment", "perc_reaction"]]
corr = contvars.corr()

mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
st.markdown('## Correlation Heatmap')
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.show()
st.pyplot()
Country = st.selectbox('Select Country',(youtube.Country.unique()))

##############################sentiment############################################
cat = st.selectbox('Select Category',(youtube.Category.unique()))
sent_plot = youtube[(youtube['Country']==Country)&(youtube['Category']==cat)].groupby("channel_title").sum().sort_values(by = 'sent_score', ascending = False).head(20)
plt.figure(figsize=(10,5))

fig = go.Figure(
    data=[go.Scatter(x=sent_plot.index.values,y=sent_plot['sent_score'])],
    layout_title_text="Channelwise Top 20 Sentiments"
)
st.plotly_chart(fig)
#Country = st.selectbox('Select Country',(youtube.Country.unique()))
option1 = st.selectbox('Select Type',("channel_title", "Category"))
by_channel = youtube[youtube['Country']==Country].groupby([option1]).size().sort_values(ascending = False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(by_channel.values, by_channel.index.values, palette = "rocket")
plt.title("Top 10 Most Frequent Trending Youtube Stats")
plt.xlabel("Video Count")
plt.show()
st.pyplot()

like_category = youtube[(youtube["dislikes"] != 0)& (youtube['Country']==Country)].groupby(option1).mean().sort_values(by = "ldratio", ascending = False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(like_category["ldratio"], like_category.index.values, palette = "rocket")
plt.title("Top 10 Most Liked Trending Youtube Stats")
plt.xlabel("Average Like to Dislike Ratio")
plt.show()
#st.plotly_chart(fig1)
# st.pyplot(fig1)
st.pyplot()


#cat = st.selectbox('Select Category',(youtube.Category.unique()))

by_channel = youtube[youtube['Category']==cat].groupby(['channel_title']).size().sort_values(ascending = False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(by_channel.values, by_channel.index.values, palette = "rocket")
plt.title("Top 10 Most Frequent Trending Youtube Stats")
plt.xlabel("Video Count")
plt.show()
st.pyplot()

like_category = youtube[(youtube["dislikes"] != 0)& (youtube['Category']==cat)].groupby('channel_title').mean().sort_values(by = "ldratio", ascending = False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(like_category["ldratio"], like_category.index.values, palette = "rocket")
plt.title("Top 10 Most Liked Trending Youtube Stats")
plt.xlabel("Average Like to Dislike Ratio")
plt.show()
st.pyplot()



#######################k-means##############################################
st.title('K-Means Clustering to determine the popularity')
st.markdown('## All videos distribution')
#df = pd.read_csv('YouTube.csv')
le_category = LabelEncoder()
df['pop_per'] = df['views']
inputs = df[['like_percentage', 'pop_per']]
inputs['category_n'] = le_category.fit_transform(inputs['like_percentage'])
inputs['pop_per_n'] = df['pop_per']
del inputs['pop_per']
inputs_n = inputs.drop(['category_n'], axis = 'columns')
plt.scatter(inputs_n['pop_per_n'], inputs_n['like_percentage'])
st.pyplot()

km = KMeans(n_clusters=3)
inputs_n = inputs_n.dropna()
inputs_n['pop_per_n'] = inputs_n['pop_per_n'].replace(np.nan, 0)
y_predicted = km.fit_predict(inputs_n[['like_percentage', 'pop_per_n']])
inputs_n['cluster'] = y_predicted
inputs_n1 = inputs_n[inputs_n.cluster==0]
inputs_n2 = inputs_n[inputs_n.cluster==1]
inputs_n3 = inputs_n[inputs_n.cluster==2]
st.markdown('## k means cluster popularity "Part 1"')
plt.scatter(inputs_n1['pop_per_n'], inputs_n1['like_percentage'], color='green')
plt.scatter(inputs_n2['pop_per_n'], inputs_n2['like_percentage'], color='red')
plt.scatter(inputs_n3['pop_per_n'], inputs_n3['like_percentage'], color='black')

plt.xlabel('Views')
plt.ylabel('Like Percentage')
plt.legend()
st.pyplot()



scaler = MinMaxScaler()
scaler.fit(inputs_n[['pop_per_n']])
inputs_n['pop_per_n'] = scaler.transform(inputs_n[['pop_per_n']])

scaler.fit(inputs_n[['like_percentage']])
inputs_n['like_percentage'] = scaler.transform(inputs_n[['like_percentage']])

plt.scatter(inputs_n['pop_per_n'],inputs_n['like_percentage'])


km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(inputs_n[['like_percentage', 'pop_per_n']])

inputs_n['cluster'] = y_predicted
inputs_n1 = inputs_n[inputs_n.cluster==0]
inputs_n2 = inputs_n[inputs_n.cluster==1]
inputs_n3 = inputs_n[inputs_n.cluster==2]

st.markdown('## k means cluster popularity "Part 2"')

plt.scatter(inputs_n1['pop_per_n'], inputs_n1['like_percentage'], color='green')
plt.scatter(inputs_n2['pop_per_n'], inputs_n2['like_percentage'], color='red')
plt.scatter(inputs_n3['pop_per_n'], inputs_n3['like_percentage'], color='black')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='p',label='centroid')
plt.xlabel('Views')
plt.ylabel('Like Percentage')
plt.legend()

st.pyplot()