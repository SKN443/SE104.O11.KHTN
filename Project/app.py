from PIL import Image
import streamlit as st
from database import *
from model import *

db = Init()
embedding_model = init_emb()

st.title('Product management system')

#col1, col2 = st.columns(2)

#selection = st.selectbox("Please choose functions", ["Find", "Add", "Edit", "Remove"])

selection = st.sidebar.radio("Please choose functions", options= ["Search", "Add", "Edit", "Remove"])


if selection == "Search":

    search_selection = st.selectbox("Please choose search option",options = ["Product ID", "Text", "Image"])

    if search_selection == "Product ID":
        tbc = 1
        ## Call the exist-check function

    if selection == "Text":
        tbc = 1
        ##To be update

    # output.append({
    #     'image': byte2img(dct['image']),
    #     'path': dct['path'],
    #     'product_id': dct['product_id'],
    #     'category': dct['category']
    # })

    if search_selection == "Image":
        input_img = Get_image()

        if st.button('Submit'):
            if input_img is None:
                st.error('Please select image')
            else:
                output = pipeline(db, embedding_model, input_img, 15)
                cols = st.columns(3)
                for col_id in range(len(cols)):
                    with cols[col_id]:
                        for i in range(len(output)):
                            if i % len(cols) == col_id:
                                st.image(output[i]['image'])
                                st.text('Product ID: '+output[i]['product_id'])
                                st.text(output[i]['category'])
                # col1, col2 = st.columns(2)
                # with col1:
                #     for product in output:
                #         st.image(product['image'], width = 175)
                # with col2:
                #     for product in output:
                #         #st.text(product['path'])
                #         st.subheader('ID:')
                #         st.text(product['product_id'])
                #         st.subheader('Category')
                #         st.text(product['category'])



if selection == "Add":

    input_img = Get_image(get_dir = True)
    product_id = st.text_input('Product ID', value = None)
    category = st.text_input('Category', value = None)

    if st.button('Submit'):
        if input_img is None:
            st.error('Please select image')
        if product_id is None:
            st.error('Please type Product ID')
        if category is None:
            st.error('Please type Category')
        exist = False
        ##### Call exist-check function to find duplicate
        if exist == False:
            st.error('There is a existed product with same ID')
        else:
            ###### Call add function
            st.success('Add product successfully')

if selection == "Edit":

    product_id = st.text_input('Product ID', value = None)

    if st.button('Check'):
        if product_id is None:
            st.error('Please type Product ID')
        else:
            ## Call the exist-check function
            exist = True
            if exist == False:
                st.error('Could not find product with this ID')
            else:
                ## Retrieve and show current data
                st.text('Leave the field blank if no change is needed')
                input_img = Get_image(get_dir=True)
                category = st.text_input('Category', value=None)
                ## Call the update function



if selection == "Remove":

    product_id = st.text_input('Product ID', value=None)
    if st.button('Check'):
        if product_id is None:
            st.error('Please type ID')
        else:
            ## Call the exist-check function
            exist = True
            if exist == False:
                st.error('Could not find product with this ID')
            else:
                ## Retrieve and show current data
                if st.button('Delete'):
                    ### Call delete function
                    st.success('Delete product successfully')