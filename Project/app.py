import streamlit as st
from database import *
from model import *

db = Init()
embedding_model = init_emb()


if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button


st.title('Product management system')

selection = st.sidebar.radio("Please choose functions", options= ["Search", "Add", "Edit", "Remove"])


if selection == "Search":

    search_selection = st.selectbox("Please choose search option",options = ["Product ID", "Image"])

    if search_selection == "Product ID":
        product_id = st.text_input('Product ID', value=None)
        if st.button('Submit'):
            if product_id is None:
                st.error('Please type Product ID')
            else:
                exist = Exist(db, product_id)
                if exist == True:
                    result = Get(db,product_id)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(result['image'], width = 150)
                    with col2:
                        st.text('Product ID: ' + result['product_id'])
                        st.text('Category: ' + result['category'])
                else:
                    st.error('Could not find product with this ID')


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


if selection == "Add":

    input_img = Get_image()
    product_id = st.text_input('Product ID', value = None)
    category = st.text_input('Category', value = None)

    if st.button('Submit'):
        if input_img is None:
            st.error('Please select image')
        if product_id is None:
            st.error('Please type Product ID')
        if category is None:
            st.error('Please type Category')
        exist = Exist(db, product_id)
        if exist == True:
            st.error('There is a existed product with same ID')
        else:
            Add_product(db, input_img, product_id, category, embedding_model)
            st.success('Add product successfully')

if selection == "Edit":

    product_id = st.text_input('Product ID', value = None)

    st.button('Check', on_click=click_button)
    if st.session_state.button:
        if product_id is None:
            st.error('Please type Product ID')
        else:
            exist = Exist(db,product_id)
            if exist == False:
                st.error('Could not find product with this ID')
            else:
                result = Get(db, product_id)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(result['image'], width=150)
                with col2:
                    st.text('Product ID: ' + result['product_id'])
                    st.text('Category: ' + result['category'])
                st.text('Leave the field blank if no change is needed')
                input_img = Get_image()
                category = st.text_input('Category', value=None)
                if st.button('Update'):
                    Update(db, product_id, input_img, category, embedding_model)
                    st.success('Edit product successfully')



if selection == "Remove":

    product_id = st.text_input('Product ID', value=None)
    st.button('Check', on_click=click_button)
    if st.session_state.button:
        if product_id is None:
            st.error('Please type ID')
        else:
            exist = Exist(db,product_id)
            if exist == False:
                st.error('Could not find product with this ID')
            else:
                result = Get(db, product_id)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(result['image'], width=150)
                with col2:
                    st.text('Product ID: ' + result['product_id'])
                    st.text('Category: ' + result['category'])
                if st.button('Delete'):
                    Delete(db, product_id)
                    st.success('Delete product successfully')