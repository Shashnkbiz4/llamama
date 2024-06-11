import json
from django.shortcuts import render
from langchain_community.document_loaders import PyMuPDFLoader
from django.conf import settings
from django.http import JsonResponse
import os
import re
import replicate
import logging
# from llama_instruct import clean_text, llama_instruct
logger = logging.getLogger(__name__)
# Create your views here.
def dashboard(request):
    return render(request, 'index.html')

def clean_text(text):
    sequence_pattern = re.compile(r'(\d)\n(\d\n)+')
    cleaned_text = re.sub(sequence_pattern, '', text)
    lines = [line.strip() for line in cleaned_text.split('\n') if line.strip()]
    cleaned_text = '\n'.join(lines)
    return cleaned_text





def extract_data_from_response(response):
    """Extract pdf_type and client_id from the Llama response text."""
    try:
        # Search for the JSON-like object within the response
        match = re.search(r'{[^}]+}', response)
        if match:
            json_response = match.group()
            logger.debug(f"json_response: {json_response}")
            response_data = json.loads(json_response)
            pdf_type = response_data.get("pdf_type", "")
            client_id = response_data.get("client_id", "")
            year = response_data.get("year", "")
            logger.debug(f"Extracted pdf_type: {pdf_type}")
            logger.debug(f"Extracted client_id: {client_id}")
            logger.debug(f"Extracted year: {year}")
            return pdf_type, client_id, year
        else:
            logger.error("Could not find JSON-like object in response")
            return None, None, None
    except Exception as e:
        logger.error(f"Error extracting data: {e}")
        return None, None, None






def upload(request):
    print("inside upload")
    if request.method == 'POST':
        print("insideeee post ")
        if request.FILES.get('file'):
            print("inside file")
            pdf_file = request.FILES['file']
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', pdf_file.name)
            print("pdf_file>>>>>>>>>>>>>>>>>>>>>>",pdf_file)
            print("file_path>>>>>>>>>>>>>>>>>>>>>>",file_path)
            # Ensure the media directory and pdfs subdirectory exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            # Load and clean the PDF text
            loader = PyMuPDFLoader(file_path)
            data = loader.load()
            structured_text = [page.page_content for page in data]
            combined_text = '\n'.join(structured_text)
            cleaned_text = clean_text(combined_text)
            print(cleaned_text)
            # Process the text (for now, just printing it)
            llama_response = llama_instruct(cleaned_text)
            print(llama_response)
            # Extract JSON data from llama_responsepdf_type, client_id = extract_data_from_response(llama_response)
            pdf_type, client_id, year = extract_data_from_response(llama_response)

                
            if pdf_type and client_id:
                return JsonResponse({'pdf_type': pdf_type, 'client_id': client_id, 'year': year})
            else:
                return JsonResponse({'error': 'Could not extract data from response'}, status=500)
        else:
            return render(request, 'upload.html')
    else:
        return render(request, 'upload.html')
    


#working





def llama_instruct(pdf_data):
    response_text = ""
    for event in replicate.stream("meta/meta-llama-3-8b-instruct",
        input={
        "top_k": 0,
        "top_p": 0.95,
        "prompt": f'''Pdf: ```{pdf_data}```
        Above I have provided you the text extracted from a PDF document. Your tasks are:

        1. Classify whether the PDF is a 'tax_pdf' or 'other_pdf'.
        2. Extract the 'client_id' based on the following instructions:

        Instructions:

        1. If the keywords "tax invoice" or "tax" are present in the document text, identify the document type as "tax document" by printing "document_type: tax document".
        2. Look for any sequence of numbers in the format "12345678 9012 3456.000" within the document text. Consider the last number with a decimal point (e.g., 3456.000) as the client ID. For example, in the sequence "12345678 9012 3456.000", consider "3456.000" as the client ID.
        3. Ensure the client ID is preceded by two sets of numbers. For example:
            - "15110328 798931 1303.000" - here, "1303.000" is the client ID.
            - "2021.03020 MCDERMOTT, BRADLEY 1303.001" - here, "1303.001" is NOT the client ID because it does not follow the correct sequence.
            - "12344566 323212 2323.323" - here, "2323.323" is the client ID.
        4. Print the client ID in the format "client_uid: <extracted_number>".
        5. If this type of Date is present **/**/**** Extract the year from the for example <Date ► 03/07/2022> in the document. If the date is found extract the year from that "year: <extracted_year>" and append that in the below json , 
        5. If neither of the above conditions are met, do not print anything.

        Output the results in JSON format:
        6.Document Type: <value> \n\nI want the output in json format: ```{{"pdf_type": "<type of pdf>","client_id": "<client_id>", "year": "<year>"}}```''',
        "max_tokens": 512,
        "temperature": 0.7,
        "system_prompt": "You are a helpful assistant",
        "length_penalty": 1,
        "max_new_tokens": 512,
        "stop_sequences": "<|end_of_text|>,<|eot_id|>",
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "presence_penalty": 0,
        "log_performance_metrics": False
        },
        ):
        response_text += str(event)
    return response_text

# Function to clean the text




def file_upload(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        for uploaded_file in uploaded_files:
            with open(os.path.join('uploads', uploaded_file.name), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        return JsonResponse({'message': 'Files uploaded successfully'})
    return render(request, 'ultiuploads.html')