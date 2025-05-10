from fastapi import APIRouter, HTTPException, UploadFile, Depends   

from writing.services.extract_html_file_service import HtmlFile
from writing.schemas.text_extractor_schema import TextExtractor
from writing.helpers.jwt_token_helper import validate_token

extract_html_file_router = APIRouter(tags=["HtmlFile"])


@extract_html_file_router.post("/HTML/extract_text", dependencies=[Depends(validate_token)])
async def extract_text_from_html(
    file: UploadFile | None = None, url: str = None, user_id: str = None
) -> list[TextExtractor]:
    file_name = file.filename if file else ""
    html_file_instance = HtmlFile()
    if html_file_instance.supports_file_type(file_name=file_name, url=url):
        texts = await html_file_instance.extract_text(file=file, url=url)
        docs = html_file_instance.create_docs(
            texts=texts, file_name=file_name, url=url, user_id=user_id
        )
        response = []
        for doc in docs:
            response.append(
                TextExtractor(id=doc.id_, text=doc.text, metadata=doc.extra_info)
            )
        return response
    else:
        raise HTTPException(status_code=415, detail="Error file type")
