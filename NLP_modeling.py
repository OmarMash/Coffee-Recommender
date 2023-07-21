#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[94]:


df=pd.read_csv('cleaned_coffee_reviews.csv')


# In[57]:


df['notes_1'] = df['notes_1'].fillna('')


# In[58]:


feature_1 = df['notes_1']
vectorizer = TfidfVectorizer()
feature_1_vector = vectorizer.fit_transform(feature_1)
similarity = cosine_similarity(feature_1_vector)


# In[86]:


def get_5_most_similar(input_index,input_indexes):
    similarity_score = similarity[input_index]
    df_similarity = pd.DataFrame({'Index': range(len(similarity_score)), 'Similarity': similarity_score})
    for index in input_indexes:
        df_similarity = df_similarity.drop(index)
    df_similarity = df_similarity.sort_values(by='Similarity', ascending=False)
    top5 = df_similarity[:5]
    return top5


# In[135]:


def get_5_most_similar_overall(input, input_type, df):
    overall_df = pd.DataFrame()
    input_indexes = df[df[input_type] == input].index
    for index in input_indexes:
        top5_df = get_5_most_similar(index,input_indexes)
        overall_df = pd.concat([overall_df, top5_df])
    if len(overall_df)>5:
        overall_df = overall_df.sort_values(by='Similarity', ascending=False)
        overall_df = overall_df[:5]
    return overall_df, input_indexes


# In[150]:


def results(input, input_type, df):
    results_df= pd.DataFrame()
    top5_indexes, input_indexes = get_5_most_similar_overall(input,input_type,df)
    filtered_df = df.loc[top5_indexes.index]
    input_df = df.loc[input_indexes]
    return filtered_df, input_df

