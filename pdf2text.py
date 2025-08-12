import PyPDF2
import os


def pdf_parser(path):
    with open(path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or "" 
    return text


# Convert PDFs to text 
if __name__ == "__main__":
    input_pdf_folder = "input/inputpdf"
    input_txt_folder = "input/inputtxt"

    os.makedirs(input_txt_folder, exist_ok=True)

    for filename in os.listdir(input_pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_pdf_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(input_txt_folder, txt_filename)

            print(f"Converting {filename} to text...")

            try:
                text = pdf_parser(pdf_path)
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Saved text to {txt_path}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")