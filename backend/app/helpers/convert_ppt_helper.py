import os
import shutil

from spire.presentation import FileFormat, Presentation


def save_document_into_temp(document):
    document.file.seek(0)
    upload_dir = "temp_folder"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, document.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)
    return file_path


def delete_document(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        parent_dir = os.path.dirname(file_path)
        if not os.listdir(parent_dir):
            os.rmdir(parent_dir)
    except Exception as e:
        print(f"Error while deleting the file: {e}")


def convert_ppt_to_pptx_stream(document):
    input_path = save_document_into_temp(document)
    output_path = os.path.join("temp_folder", "temp.pptx")
    pre = Presentation()
    pre.LoadFromFile(input_path)
    pre.SaveToFile(output_path, FileFormat.Pptx2010)
    with open(output_path, "rb") as f:
        document_content = f.read()
    delete_document(input_path)
    delete_document(output_path)
    return document_content
