from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data
import json
import PyPDF2

#logging.info("hi, here I start my execution")

filepath = r'F:\Python_Classes\NLP_alldata\GenerativeAI\Day006_Project_MCQGenerator\mcqgen\TravelInsurance.pdf'
#text = read_file(file=filepath)
#print(text)

json_filepath=r'F:\Python_Classes\NLP_alldata\GenerativeAI\Day006_Project_MCQGenerator\mcqgen\Response.json'
with open(json_filepath, 'r') as file:
    RESPONSE_JSON=json.load(file)
#print(RESPONSE_JSON)



pdf_reader=PyPDF2.PdfReader(filepath)
text=''
for page in pdf_reader.pages:
    text+=page.extract_text()
print(text)