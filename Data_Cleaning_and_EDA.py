#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re


# In[2]:


df = pd.read_csv('all_coffee_reviews.csv')


# In[3]:


df['rating'] = df['rating'].replace('NR',np.nan )


# In[4]:


df['origin'] = df['origin'].replace('Not disclosed.',np.nan )


# In[5]:


df['origin'] = df['origin'].replace('Blend',np.nan )


# In[6]:


split_agtron = df["agtron"].str.split("/", expand=True)


# In[7]:


df["agtron_1"] = split_agtron[0]
df["agtron_2"] = split_agtron[1]


# In[8]:


df = df.drop(["agtron"], axis=1)


# In[9]:


df['agtron_1'] = df['agtron_1'].replace(['','NA','na','0','g'],np.nan)
df['agtron_2'] = df['agtron_2'].replace(['','NA','na','0','wb'],np.nan)


# In[10]:


df['agtron_1'] = df['agtron_1'].astype(float)
df['agtron_2'] = df['agtron_2'].astype(float)
df.loc[df['agtron_1'] > 100, 'agtron_1'] = np.nan
df.loc[df['agtron_2'] > 100, 'agtron_2'] = np.nan


# In[11]:


df['aroma'] = df['aroma'].replace('NR',np.nan )
df['aroma'] = df['aroma'].astype(float)
df['rating'] = df['rating'].astype(float)
df['acidity'] = df['acidity'].replace(['na','Moderate','Low','Very Low','NR'],np.nan )
df['acidity'] = df['acidity'].astype(float)
df['body'] = df['body'].replace('NR',np.nan )
df['body'] = df['body'].astype(float)
df['flavor'] = df['flavor'].replace('NR',np.nan )
df['flavor'] = df['flavor'].astype(float)
df['aftertaste'] = df['aftertaste'].astype(float)
df['with_milk'] = df['with_milk'].str.extract(r'(\d+)').astype(float)
df['with_milk'] = df['with_milk'].astype(float)
df['review_date'] = pd.to_datetime(df['review_date'], format='%B %Y')


# In[12]:


df['price'] = df['price'].replace(['Not Available','Not available.'],np.nan)


# In[13]:


df["price"].isna().sum()
## alot of cleaning left to do with price


# In[14]:


currencies = df['price'].str.extract(r'([^\d\s]+)')
currencies[0].unique()


# In[15]:


df['price'] = df['price'].replace(to_replace=r'\s*\([^)]*\)', value='', regex=True)
df['price'] = df['price'].replace(['NA','Not disclosed.',"See review note","See website for more information"],np.nan)
df.loc[df['price'].str.contains("fluid", case=False, na=False), 'price'] = np.nan


# In[16]:


df['price'] = df['price'].replace(to_replace=r'\b(?:ounces|ounce|onces|ouncues|oz)\b', value='ounces', regex=True)
df['price'] = df['price'].replace(to_replace=r'\b(?:g|grams|gram)\b', value='grams', regex=True)


# In[17]:


df['price'] = df['price'].replace(to_replace=r'\b(?:sachet)\b', value='5 grams', regex=True)


# In[18]:


for word in ['boxed','single','capsules','ml','can','cans','cups','caps','pods','Vue','Discs',';','bottle','liquid','sticks']:
    df.loc[df['price'].str.contains(word, case=False, na=False), 'price'] = np.nan


# In[19]:


df['price'] = df['price'].replace(to_replace=r'\b(?:kilogram|Kilogram|kilo|Kilo|kg)\b', value='Kg', regex=True)
df['price'] = df['price'].replace(to_replace=r'\b(?:pound|pounds|Pounds|Pound)\b', value='Lbs', regex=True)
df['price'] = df['price'].replace(to_replace=r'\b(?:US)\b', value='USD', regex=True)
df['price'] = df['price'].replace(to_replace=r'\b(?:for)\b', value='/', regex=True)


# In[20]:


df['price'][~df['price'].str.contains("/", na=False)& df['price'].notnull()] = np.nan
df['price'] = df['price'].replace(to_replace=r'#', value='$', regex=True)


# In[21]:


df['price'] = df['price'].replace(to_replace=r'(?<!\d)\.(?!\d)|[^\w\s./¥£€]', value='', regex=True)
df['price'] = df['price'].replace(to_replace=r'Price', value='', regex=True)


# In[22]:


split_price = df["price"].str.split("/", expand=True)
df["raw_price"] = split_price[0]
df["quantity"] = split_price[1]


# In[23]:


df['raw_price'] = df['raw_price'].replace(to_replace=r'\b(?:E)\b|€|Euros', value='EUR', regex=True)
df['raw_price'] = df['raw_price'].replace(to_replace=r'£', value='Pound ', regex=True)
df['raw_price'] = df['raw_price'].replace(to_replace=r'\bNT(?!\D)|NT |TWD', value='NTD', regex=True)
df['raw_price'] = df['raw_price'].replace(to_replace=r'\b(?:HK)\b', value='HKD', regex=True)
df['raw_price'] = df['raw_price'].replace(to_replace=r'\b(?:RMB)\b|¥', value='CNY', regex=True)
df['raw_price'] = df['raw_price'].replace(to_replace=r'\b(?:USD)\b', value='', regex=True)
df['raw_price'] = df['raw_price'].replace(to_replace=r'\b(?:HK)\b', value='HKD', regex=True)
df['raw_price'] = df['raw_price'].replace(to_replace=r'pesos', value='MXN', regex=True)


# In[24]:


def standardize_price(value):
    if pd.isna(value):
        return value

    if re.match(r'^\d+(\.\d+)?$', str(value)):
        return float(value)  # If the value consists of only numbers, return it as is

    currency_values = {
        'NTD': 0.32,
        'AED': 0.27,
        'KRW': 0.00079,
        'HKD': 0.13,
        'Pound': 1.31,
        'CAD': 0.76,
        'RM': 0.22,
        'CNY': 0.14,
        'MXN': 0.060, 
        'EUR': 1.12,
        'LAK': 0.000052, 
        'IDR': 0.000067, 
        'AUD': 0.68, 
        'THB': 0.029, 
        'GTQ':0.000040
    }

    # Extract the currency code and amount using a regular expression pattern
    match = re.match(r'^(?:([A-Za-z]+)?\s*(\d+(\.\d+)?)\s*([A-Za-z]+)?)|((?<=Pound)\s*(\d+(\.\d+)?)\s*([A-Z]+)?)$', str(value))
    if match:
        currency = match.group(1) or match.group(4)
        amount = float(match.group(2) or match.group(5))

        if currency and currency in currency_values:
            conversion_rate = currency_values[currency]
            return amount * conversion_rate  

    return value  # Return original value if no conversion is applied

df['raw_price'] = df['raw_price'].str.replace(r'^(?:([A-Za-z]+)?\s*(\d+(\.\d+)?)\s*([A-Za-z]+)?)|((?<=Pound)\s*(\d+(\.\d+)?)\s*([A-Z]+)?)$', lambda m: str(standardize_price(m.group(0))), regex=True)
df['raw_price'] = df['raw_price'].astype(float)


# In[25]:


df['quantity'] = df['quantity'].replace(to_replace=r'(\d+)([a-zA-Z]+)', value=r'\1 \2', regex=True)


# In[26]:


df['quantity'] = df['quantity'].str.strip()
df['quantity'] = df['quantity'].replace(to_replace=r'\b(?:g)\b', value='grams', regex=True)

for word in ['grams', 'Lbs', 'Kg','ounces']:
    df.loc[df["quantity"].str.contains(word, na=False), "quantity_units"] = word
    df['quantity']= df['quantity'].str.split(word, n=1).str[0].str.strip()


# In[27]:


pattern = r'(\w+) (\d+(\.\d+)?)'

def multiply_values(row):
    value = row['quantity']
    if pd.isna(value) or not isinstance(value, str):
        return value  # Return original value for missing or non-string values

    match = re.match(pattern, value)
    if match:
        word = match.group(1)
        number = float(match.group(2))
        if word == 'eight':
            return number * 8
        elif word == 'six':
            return number * 6
    return value  # Return original value if pattern doesn't match or word is not 'eight' or 'six'

df['quantity'] = df.apply(multiply_values, axis=1)
df['quantity'] = df['quantity'].replace('8 18','144')
df['quantity'] = df['quantity'].replace('','1').astype(float)


# In[28]:


measurement_conversion = {
    'grams': 0.035274,
    'Lbs': 16,
    'Kg': 35.274,
    'ounces': 1
}
df['#_of_ounces'] = df.apply(lambda row: row['quantity'] * measurement_conversion.get(row['quantity_units'], 1) if pd.notnull(row['quantity_units']) else np.nan, axis=1)
df['price_per__100grams'] = np.where(
    df['#_of_ounces'].notnull(), 
    round(((df['raw_price'] / df['#_of_ounces'])*3.5),2), 
    np.nan 
)


# In[29]:


df['origin'] = df['origin'].replace(to_replace=r'Not', value=np.nan, regex=True)


# In[30]:


df = df.drop(['raw_price', 'quantity','quantity_units','#_of_ounces','price'], axis=1)


# In[31]:


df.to_csv('cleaned_coffee_reviews.csv', index=False)


# In[32]:


# IDK why url column python in python is not correct 
#df = df.drop(['URL'], axis=1)


# In[ ]:





# In[ ]:




