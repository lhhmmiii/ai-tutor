from fastapi import APIRouter, HTTPException, UploadFile, Depends

from writing.services.extract_table_file_service import TableFile
from writing.schemas.text_extractor_schema import TextExtractor
from writing.helpers.jwt_token_helper import validate_token 

extract_table_file_router = APIRouter(tags=["TableFile"])


# CREATE
@extract_table_file_router.post("/table_file", dependencies=[Depends(validate_token)])
async def extract_text_from_table_file(
    file: UploadFile, user_id: str = "", is_header: bool = False
) -> list[TextExtractor]:
    file_name = file.filename
    table_file_instance = TableFile(is_header=is_header)
    if table_file_instance.supports_file_type(file_name):
        texts, sheet_names = await table_file_instance.extract_text(file=file)
        docs = table_file_instance.create_docs(texts, file_name, sheet_names, user_id)
        response = []
        for doc in docs:
            response.append(
                TextExtractor(id=doc.id_, text=doc.text, metadata=doc.extra_info)
            )
        return response
    else:
        raise HTTPException(status_code=415, detail="Error file type")
