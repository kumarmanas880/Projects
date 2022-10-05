#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np 
import pandas as pd 
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


my_file="C:/Users/kumar/Downloads/titles.csv"
data= pd.read_csv(my_file,index_col="id")
data.head(5)


# In[4]:


data.columns


# In[5]:


data.shape


# As we can see, there are a few columns that are not necesary to our analysis. We will delete the description, imdb_id, imdb_votes, tmdb_popularity, and seasons columns.

# In[6]:


data.drop(['description','imdb_id','imdb_votes','tmdb_popularity', 'seasons'], axis=1,inplace=True)


# Now let us preview the first 5 rows again.

# In[7]:


data.head(5)


# Next we will check if there are any duplicated or null value rows.

# In[8]:


data.duplicated().sum()


# In[9]:


data.isnull().sum()


# We will drop any rows that have null values in them.

# In[10]:


data.dropna(axis=0,how='any',inplace=True)
data.isnull().sum()


# Let's look at a quick summary of our data, including mean, minimum, and maximum.

# In[11]:


data.describe()


# We are now ready to begin our analysis. 
# 
# We will compare the types of media on Netflix.

# In[12]:


type_count = data.type.value_counts()
type_count.head()


# In[13]:


plt.figure(figsize=(5,5))
type_color = sns.color_palette("pastel")
sns.countplot(data=data, x='type',palette=type_color)
plt.title("Comparison of Movies vs Shows")
plt.show()


# From the graph, we can see that Netflix produces and streams more TV Shows than movies.

# Now, we want to discover the most popular genre of TV shows and movies that is on Netflix.

# In[14]:


genre_count = data.genres.value_counts()
genre_count.head(10)


# When we obtain a count of the genres, it seems that there are some shows and movies that have multiple genres. This is an issue because the multiple genres are contained within the brackets. As a result, we will need to parse the genre column.

# In[15]:


genres = {}

def get_genres(row):
  parsed = (str(row)[1:-1]).split(",")

  for i in range(len(parsed)):
    parsed[i] = parsed[i].strip()
    parsed[i] = parsed[i][1:-1]

  for i in parsed:
    if i not in genres.keys():
      genres[i] = 0
      continue
    genres[i] += 1

  return row
data['genres'] = data['genres'].map(get_genres)
genres


# In[16]:


for genre in genres.items():
    print (genre or 'none')


# 
# To create a graph, we will need to use the list() function for the x and y axis.

# In[17]:


x_axis = list(genres.keys())
y_axis = list(genres.values())

genre_color = sns.color_palette("pastel")
plt.figure(figsize=(25,10))
plt.bar(x_axis,y_axis,color = genre_color)
plt.title("Most Popular Genres")
plt.xlabel("Genre")
plt.ylabel("Count")
plt.show()


# Drama is the leading genre of TV shows and movies in Netflix, with over 1500 titles. Comedy follows right after, but still has less than 1000.

# Next, we want to view the amount of titles that released during each year. Netflix became popularized in 2007, so we will only view the years 2007 - 2022.
# 
# Keep in mind that these titles do not include shows or movies that were released before, they will only be contemporary titles.

# In[18]:


year_count = data.release_year.value_counts()
year_count.head(16)


# In[19]:


plt.figure(figsize=(15,10))
sns.lineplot(data=year_count)
plt.xlim(2007,2022)
plt.xlabel('release year')
plt.ylabel('total amount of releases')
plt.title("Total Amount of Releases Since Netflix's Streaming Services")
plt.show()


# The movies and shows released at the time of 2018 and 2021 were the most popular. Netflix's rise of viewship in 2020 could be the result of the pandemic and lockdown, when people were mandated to stay home.

# We will now view the what type of age certifications TV shows and movies most released.
# 
# The ratings for movies are as followed:
# * G (General Audiences) - All ages admitted
# * PG (Parental Guidance Suggested) - Some material may not be suitable for children
# * PG-13 (Parents Strongly Cautioned) - Some material may be inappropriate for children under 13
# * R (Restricted) - Under 17 requires accompanying parent or adult guardian
# * NC-17 (Adults Only) - No one 17 and under admitted
# 
# The ratings for TV shows are as followed:
# * TV-G (General Audience) - Suitable for all ages
# * TV-Y (All Children) - Designed to be appropriate for all children, including children from ages 2-6
# * TV-Y7 (Directed to Older Children) - Designed for children ages 7 and above
# * TV-PG (Parental Guidance Suggested) - Some material may not be suitable for children
# * TV-14 (Parents Strongly Cautioned) - Some material may not be suitable for children under 14
# * TV-MA (Mature Audiences Only) - Designed only for adults and not suitable for children under 17

# In[20]:


age_ratings = data.age_certification.value_counts()
age_ratings.head(12)


# In[33]:


plt.figure(figsize=(10,10))
sns.countplot(data['age_certification'])
plt.title("Netflix's Age Content Ratings")
plt.show()


# Most TV shows have an age certification of TV-MA while most movies have an age certification of R. This makes sense as Netflix's main demographic is adults or people over the age of 17.

# Let's now view where most of the TV shows and movies are produced from by country.

# In[23]:


countries_count = data.production_countries.value_counts()
countries_count.head(10)


# In[24]:



values = [1275,213,187,137,116,77,54,53,49,46]
labels = ['US','IN','JP','GB','KR','ES','FR','CA','TR','MX']
pie_colors = sns.color_palette('pastel')
plt.pie(values, labels=labels, colors=pie_colors, autopct='%.0f%%', radius=2)
plt.title("Countries Producing the Most Movies and Shows",y=1.50)
plt.show()


# The United States of America produces more than half of the TV shows and movies found on Netflix, followed by India and Japan. As a streaming service company founded in the United States, it is reasonable that the majority of titles would be produced from there.

# Now we will compare based on IMDB Ratings.

# In[25]:


top_10_imdb = data.sort_values(['imdb_score'], ascending=False)[['title','imdb_score','type']].head(10)
top_10_imdb


# In[26]:


top_10_tmdb = data.sort_values(['tmdb_score'], ascending=False)[['title','tmdb_score','type']].head(10)
top_10_tmdb


# The top 10 IMDb titles and top 10 TMDB titles are not close at all! In fact, one of the top 10 titles of TMDB is "Little Baby Bum," a children's animated nursery song program.
# 
# Another thing to note is that the highest rating for a title on IMDb is 9.5, while there are 10 titles with perfect 10.0 ratings on TMDB.

# We will view how IMDb and TMDB scores have changed over time with a movie's or TV show's release.

# In[27]:


year_vs_scores = data.groupby('release_year').agg({'imdb_score':'mean','tmdb_score':'mean'})
year_vs_scores.head()


# In[28]:


plt.figure(figsize=(20,10))
palette = sns.color_palette('pastel')
sns.barplot(x=year_vs_scores.index,y=year_vs_scores['imdb_score'],palette=palette)
plt.title('IMDb Score vs. Years Released')
plt.ylabel('IMDb Ratings (Average)')
plt.xlabel('Released Year')
plt.xticks(rotation=45)
plt.show()


# In[29]:


plt.figure(figsize=(20,10))
sns.barplot(x=year_vs_scores.index,y=year_vs_scores['tmdb_score'],palette=palette)
plt.title('TMDB Score vs. Years Released')
plt.ylabel('TMDB Score(Average)')
plt.xlabel('Released Year')
plt.xticks(rotation=45)
plt.show()


# As we can see from comparing the two graphs, IMDb scores are generally lower than TMDB scores.
# 
# IMDb also is steadily decreasing in their ratings as time goes on, while TMDB ratings have been consistent.

# In[ ]:




