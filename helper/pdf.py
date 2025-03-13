import os
import requests

def save_online_pdf(pdf_url):
    print(f"Attempting to download from: {pdf_url}")  # Debug the URL passed

    if not pdf_url.startswith(('http://', 'https://')):
        return "Invalid URL provided. URL should start with http:// or https://"

    save_folder = "sources"
    os.makedirs(save_folder, exist_ok=True)

    file_name = os.path.join(save_folder, pdf_url.split("/")[-1])

    try:
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            with open(file_name, "wb") as pdf_file:
                for chunk in response.iter_content(1024):
                    pdf_file.write(chunk)
            return f"../source/{file_name}"
        else:
            return "Failed to download PDF"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
