async def load_file(
    office_file,
    table_file,
    html_file,
    file: None,
    user_id=None,
    url=None,
    is_header=True,
):
    file_name = file.filename if file else ""
    if office_file.supports_file_type(file_name):
        texts = await office_file.extract_text(file)
        docs = office_file.create_docs(texts, file_name, user_id)
        return docs
    elif table_file.supports_file_type(file_name):
        texts, sheet_names = await table_file.extract_text(
            file=file, is_header=is_header
        )
        docs = table_file.create_docs(texts, file_name, sheet_names, user_id)
        return docs
    elif html_file.supports_file_type(file_name=file_name, url=url):
        texts = await html_file.extract_text(file=file, url=url)
        docs = html_file.create_docs(texts=texts, file_name=file_name, user_id=user_id)
        return docs
