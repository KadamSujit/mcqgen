import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=''
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
        except Exception as e:
            raise Exception('Error reading the PDF file')
    
    elif file.endswith(".txt"):
        with open(file, 'r') as file:
            txt_data=file.read()
        return txt_data
    
    else:
        raise Exception(
            "Unsupported file format. Only .pdf and .txt files are supported"
        )
    
def get_table_data(quiz_str):
    try:
        # convert the quix from str to a dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]

        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                f"{option}->{option_value}" for option, option_value in value["options"].items()
                    ]
            )
            correct=value["correct"]
            quiz_table_data.append({"MCQ":mcq, "Choices": options, "Correct":correct})
        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
