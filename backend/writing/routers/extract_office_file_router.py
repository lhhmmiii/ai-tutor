from fastapi import APIRouter, HTTPException, UploadFile, Depends

from writing.services.extract_office_file_service import OfficeFile
from writing.schemas.text_extractor_schema import TextExtractor
from writing.helpers.jwt_token_helper import validate_token

extract_office_file_router = APIRouter(tags=["OfficeFile"])


# CREATE
@extract_office_file_router.post("/office_file/", dependencies=[Depends(validate_token)])
async def extract_text_from_office_file(
    file: UploadFile, user_id: str = ""
) -> list[TextExtractor]:
    file_name = file.filename
    office_file_instance = OfficeFile()
    if office_file_instance.supports_file_type(file_name):
        texts = await office_file_instance.extract_text(file)
        docs = office_file_instance.create_docs(texts, file_name, user_id)
        response = []
        for doc in docs:
            response.append(
                TextExtractor(id=doc.id_, text=doc.text, metadata=doc.extra_info)
            )
        return response
    else:
        raise HTTPException(status_code=415, detail="Error file type")
