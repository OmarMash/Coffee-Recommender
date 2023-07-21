#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# In[10]:


# if already have a web scraped file please load with -
reviews_df = pd.read_csv('all_coffee_reviews.csv')
# if not must set reviews_df as empty by -
# reviews_df = pd.DataFrame()


# In[8]:


def insert_all_reviews_from_the_pg(reviews_in_pg_html, reviews_df, new_record_count):
    break_value  = 0
    for review in reviews_in_pg_html:
        location = origin = roast_level = agtron = price = review_date = aroma = acidity = body = None
        flavor = aftertaste = with_milk = notes_1 = notes_2 = notes_3 = None
        rating = company = blend = None

        review_text = review.get_text()
        link =review.find_all('a', href=True)
        link =link[0]['href']

        try:
            if link in reviews_df['url'].values:
                print("dataframe has been updated")
                break_value = 1
                break
        except:
            pass
    
        review_url =link
        review_response = requests.get(review_url ,headers = {'User-agent': 'Omar Mash'})
        review_html = review_response.content
        review_soup = BeautifulSoup(review_html, 'html.parser')

        try:location = review_soup.find("td", string = "Roaster Location:").find_next_sibling('td').text.strip()
        except:pass
        try:origin = review_soup.find("td", string = "Coffee Origin:").find_next_sibling('td').text.strip() 
        except:pass
        try:roast_level= review_soup.find("td", string = "Roast Level:").find_next_sibling('td').text.strip()
        except:pass
        try:agtron= review_soup.find("td", string = "Agtron:").find_next_sibling('td').text.strip()
        except:pass
        try:price = review_soup.find("td", string = "Est. Price:").find_next_sibling('td').text.strip()
        except:pass
        try:review_date = review_soup.find("td", string = "Review Date:").find_next_sibling('td').text.strip()
        except:pass
        try:aroma = review_soup.find("td", string = "Aroma:").find_next_sibling('td').text.strip()
        except:pass
            
        try:
            try:acidity = review_soup.find("td", string = "Acidity:").find_next_sibling('td').text.strip()
            except:pass
            acidity = review_soup.find("td", string = "Acidity/Structure:").find_next_sibling('td').text.strip()
        except:pass
            
        try:body = review_soup.find("td", string = "Body:").find_next_sibling('td').text.strip()
        except:pass
        try:flavor = review_soup.find("td", string = "Flavor:").find_next_sibling('td').text.strip()
        except:pass
        try:aftertaste = review_soup.find("td", string = "Aftertaste:").find_next_sibling('td').text.strip()
        except:pass
        try:with_milk = review_soup.find("td", string = "With Milk:").find_next_sibling('td').text.strip()

        except:pass
    
        notes_1 = review_soup.find("h2").find_next_sibling('p')
        notes_2 = notes_1.find_next_sibling('p')
        notes_3 = notes_2.find_next_sibling('p')
    
        rating = review_soup.find('span', attrs={"class": "review-template-rating"}).text.strip()
        company = review_soup.find('p', attrs={"class": "review-roaster"}).text.strip()
        blend = review_soup.find('h1', attrs={"class": "review-title"}).text.strip()
    
        row_data = {'blend': blend, 'url': review_url, 'company': company, 'review_date': review_date,
                    'roaster_location': location, 'origin': origin,'rating': rating, 'roast_level': roast_level,
                    'agtron': agtron, 'price': price,'aroma': aroma, 'acidity': acidity,
                    'body': body, 'flavor': flavor, 'aftertaste': aftertaste, 'with_milk': with_milk,
                    'notes_1': notes_1.text.strip(),'notes_2': notes_2.text.strip(), 'notes_3': notes_3.text.strip()}
    
        reviews_df = pd.concat([reviews_df, pd.DataFrame([row_data])], ignore_index=True)
        new_record_count +=1
    return reviews_df, break_value, new_record_count


# In[4]:


### to retrieve max page number, which will allow us to iterate the scrape for all pages dynamically
url = 'https://www.coffeereview.com/review/page/'
response = requests.get(url + '1' + '/',headers = {'User-agent': 'Omar Mash'})
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
page_count_wrapper = soup.find('li', class_='pagination-omission').find_next_sibling('li')
page_count_text = page_count_wrapper.a.text.strip()
pg_count = re.search(r'\d+', page_count_text).group()
pg_count = int(pg_count)


# In[11]:


url = 'https://www.coffeereview.com/review/page/'
new_record_count = 0
print('begin scraping')
for page in range(1,pg_count+1,1):
    response = requests.get(url + str(page) + '/',headers = {'User-agent': 'Omar Mash'})
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    reviews_in_pg_html = soup.find_all('p', class_='review-roaster')
    reviews_df,break_value,new_record_count = insert_all_reviews_from_the_pg(reviews_in_pg_html,reviews_df,new_record_count)
    if break_value == 1:
        break
        
print('done scraping')
print(f'scraped {page} pages')
print(f"{new_record_count} new record(s)")


# In[16]:


reviews_df.to_csv('all_coffee_reviews.csv', index=False)


# In[ ]:




