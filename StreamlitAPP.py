#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import NLP_modeling
from NLP_modeling import df

def main():

    st.title("Coffee Recommender")
    st.markdown("---")

    blend_list = df['blend'].unique()
    blend = st.selectbox('Step 1: Select your Favorite Coffee Blend', blend_list)
    company_list = df.loc[df['blend'] == blend, 'company'].unique()
    company = st.selectbox('Step 2: Select the company that sells your Coffee Blend ', company_list)

    compute = st.button("Recommend me five coffee blends")
    if compute:
        filtered_df, input_df = NLP_modeling.results(blend,'blend',df)
    
     #filtered_df, input_df = results('House Blend','blend',df)
     # Set page layout to wide
         # Card section
        st.title("YOUR RECOMMENDATIONS")
    
        for index, row in filtered_df.iterrows():


            col1, col2 = st.columns(2)
                
            with col1:
                st.write(f"Blend: {row['blend']}")
                st.write(f"Company: {row['company']}")
                st.write(f"Location: {row['roaster_location']}")
                st.write(f"Date Writtem: {row['review_date']}")
                
            with col2:
                    
                st.write(f"Rating: {row['rating']}")
                st.write(f"Roast Level: {row['roast_level']}")
                st.write(f"Agtron: {row['agtron_1']}/{row['agtron_2']}")
                st.write(f"Price per 100 grams: {row['price_per__100grams']}")

            st.info(f"{row['notes_1']}")
            st.info(f"{row['notes_2']}")
            st.info(f"{row['notes_3']}")

            st.write("---")  # Add a horizontal line between cards

    # # Banner section
    # banner_image = "banner.jpg"  # Replace with your banner image path or URL
    # st.image(banner_image, use_column_width=True)

    
    
if __name__ == '__main__':
    main()


# In[ ]:




