import streamlit as st
from database import *
from model import *

db = Init()
embedding_model = init_emb()


st.title('Product management system')


#selection = st.selectbox("Please choose functions", ["Find", "Add", "Edit", "Remove"])

selection = st.sidebar.radio("Please choose functions", options= ["Search", "Add", "Edit", "Remove"])


if selection == "Search":

    search_selection = st.selectbox("Please choose search option",options = ["ID", "Text", "Image"])

    if search_selection == "ID":
        tbc = 1
        ## Call the exist-check function

    if selection == "Text":
        tbc = 1
        ##To be update

    if search_selection == "Image":
        input_img = Get_image()

        if st.button('Submit'):
            if input_img is None:
                st.error('Please select image')
            else:
                for img in pipeline(db, embedding_model, input_img, 20):
                    st.image(img, width = 250)


if selection == "Add":

    input_img = Get_image(get_dir = True)
    img_id = st.text_input('Img_id', value = None)
    category = st.text_input('Category', value = None)

    if st.button('Submit'):
        if input_img is None:
            st.error('Please select image')
        if img_id is None:
            st.error('Please type ID')
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

    img_id = st.text_input('Img_id', value = None)

    if st.button('Check'):
        if img_id is None:
            st.error('Please type ID')
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

    img_id = st.text_input('Img_id', value=None)
    if st.button('Check'):
        if img_id is None:
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