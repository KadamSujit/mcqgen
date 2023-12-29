import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#loading json file
json_filepath=r'F:\Python_Classes\NLP_alldata\GenerativeAI\Day006_Project_MCQGenerator\mcqgen\Response.json'
with open(json_filepath, 'r') as file:
    RESPONSE_JSON=json.load(file)

#creating a title for the app
st.title("MCQ Creator Application with LangChain 🦜️🔗")

#creating a form using st.form
with st.form("user_inputs"):
    #file upload
    uploaded_files = st.file_uploader("Upload a PDF or txt file")

    #input fields
    #MCQ counts
    mcq_count = st.number_input("No of MCQs", min_value=3, max_value=50)

    #subject
    subject=st.text_input("Insert Subjectt", max_chars=20)

    #quiz tone
    tone=st.text_input("Complexity level of questions", max_chars=20, placeholder="Simple")

    #add Button
    button=st.form_submit_button("Create MCQs")

    # check if the button is clicked and all the fields have input

    if button and uploaded_files is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_files)
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                         "text": text,
                         "number": mcq_count,
                         "subject": subject,
                         "tone":tone,
                         "response_json":json.dumps(RESPONSE_JSON)   
                        }
                    )
                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")

                if isinstance(response, dict):
                    #Extract the quiz data from the response
                    quiz= response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)

