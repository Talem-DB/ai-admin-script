def save_online_pdf(pdf_url):

    # Folder where you want to save the PDF
    save_folder = "source"

    # Ensure the folder exists
    os.makedirs(save_folder, exist_ok=True)

    # Extract filename from URL
    file_name = os.path.join(save_folder, pdf_url.split("/")[-1])

    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(file_name, "wb") as pdf_file:
            for chunk in response.iter_content(1024):
                pdf_file.write(chunk)
        return f"./helper/sources/{file_name}.pdf"
    else:
        return "Failed to download PDF"