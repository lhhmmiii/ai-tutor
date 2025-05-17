from fastapi import APIRouter, Request, UploadFile, Depends

from app.schemas.document_qa_schema import Index, QueryRequest, QueryResponse, DocQADeleteResponse  
from app.schemas.text_extractor_schema import TextExtractor
from app.dependencies import get_embed_model, get_index_instance
from app.helpers.jwt_token_helper import validate_token

document_qa_router = APIRouter(tags=["DocumentQA"])


# CREATE
@document_qa_router.post("/document_qa", dependencies=[Depends(validate_token)])
async def create_index_without_document(request: Request) -> Index:
    index_instance = get_index_instance(user_id = '', request = request)
    index = index_instance.create_index_without_document()
    response = Index(index_id=index.index_id, nodes_dict=index.index_struct.nodes_dict)
    return response


@document_qa_router.post("/document_qa/{user_id}", dependencies=[Depends(validate_token)])
async def create_index(
    file: UploadFile | None = None,
    user_id: str = "",
    url: str = "",
    is_header: bool = True,
    request: Request = None,
) -> Index:
    index_instance = get_index_instance(user_id = user_id, request = request)
    index = await index_instance.create_index_with_document(
        file=file, url=url, is_header=is_header
    )
    response = Index(index_id=index.index_id, nodes_dict=index.index_struct.nodes_dict)
    return response


@document_qa_router.post("/document_qa/add_document/{user_id}", dependencies=[Depends(validate_token)])
async def add_document_to_index(
    index_id,
    file: UploadFile | None = None,
    user_id: str = "",
    url: str = "",
    is_header: bool = True,
    request: Request = None,
) -> Index:
    index_instance = get_index_instance(user_id = user_id, request = request)
    embed_model = get_embed_model(request)
    index = index_instance.load_index_by_index_id(index_id=index_id)
    await index_instance.add_nodes_to_index(
        index=index,
        file=file,
        user_id=user_id,
        url=url,
        is_header=is_header,
        embed_model=embed_model,
    )
    index_struct = index.storage_context.index_store.get_index_struct(index_id)
    response = Index(index_id=index.index_id, nodes_dict=index_struct.nodes_dict)
    return response


# READ
@document_qa_router.get("/document_qa/nodes/{index_id}", dependencies=[Depends(validate_token)])
async def get_nodes(index_id, request: Request) -> list[TextExtractor]:
    index_instance = get_index_instance(user_id = '', request = request)
    index = index_instance.load_index_by_index_id(index_id=index_id)
    nodes = index_instance.get_nodes(index)
    response = []
    for node in nodes:
        response.append(
            TextExtractor(id=node.id_, text=node.text, metadata=node.metadata)
        )
    return response


@document_qa_router.get("/document_qa/nodes/{index_id}/{ref_doc_id}", dependencies=[Depends(validate_token)])
async def get_nodes_by_ref_doc_id(
    index_id, ref_doc_id, request: Request
) -> list[TextExtractor]:
    index_instance = get_index_instance(user_id = '', request = request)
    index = index_instance.load_index_by_index_id(index_id=index_id)
    nodes = index_instance.get_nodes_by_ref_doc_id(index, ref_doc_id)
    response = []
    for node in nodes:
        response.append(
            TextExtractor(id=node.id_, text=node.text, metadata=node.metadata)
        )
    return response


@document_qa_router.get("/document_qa/query", dependencies=[Depends(validate_token)])
async def query(input, user_id, request: Request) -> QueryResponse:
    index_instance = get_index_instance(user_id = user_id, request = request)
    index = index_instance.load_index_by_index_id()
    res = index_instance.query(index=index, query_str=input)
    response = QueryResponse(response=res.response, source_nodes=res.source_nodes)
    return response


@document_qa_router.get("/document_qa/query/{ref_doc_id}", dependencies=[Depends(validate_token)])
async def query_by_ref_doc_id(ref_doc_id, input, user_id, request: Request)\
        -> QueryResponse:
    index_instance = get_index_instance(user_id = user_id, request = request)
    index = index_instance.load_index_by_index_id()
    res = index_instance.query_by_ref_doc_id(
        index=index, ref_doc_id=ref_doc_id, query_str=input, user_id=user_id
    )
    response = QueryResponse(response=res.response, source_nodes=res.source_nodes)
    return response


@document_qa_router.get("/document_qa/{index_id}/query/{ref_doc_id}", dependencies=[Depends(validate_token)])
async def query_by_index_id_and_ref_doc_id(
    input, index_id, ref_doc_id, user_id, request: Request
) -> QueryResponse:
    index_instance = get_index_instance(user_id = user_id, request = request)
    index = index_instance.load_index_by_index_id(index_id = index_id)
    res = index_instance.query_by_index_id_and_ref_doc_id(
        index=index, ref_doc_id=ref_doc_id, query_str=input, user_id=user_id
    )
    response = QueryRequest(response=res.response, source_nodes=res.source_nodes)
    return response


# PUT
@document_qa_router.put("/document_qa", dependencies=[Depends(validate_token)])
async def update_document(
    index_id,
    file: UploadFile | None = None,
    user_id: str = "",
    url="",
    is_header=True,
    request: Request = None,
) -> Index:
    index_instance = get_index_instance(user_id = user_id, request = request)
    embed_model = get_embed_model(request)
    index = index_instance.load_index_by_index_id(index_id=index_id)
    index_instance.update_document(index, file, user_id, url, is_header, embed_model)
    index_struct = index.storage_context.index_store.get_index_struct(index_id)
    response = Index(index_id=index.index_id, nodes_dict=index_struct.nodes_dict)
    return response


# DELETE
@document_qa_router.delete("/document_qa/{index_id}", dependencies=[Depends(validate_token)])
async def delete_index_by_index_id(index_id, request: Request) -> DocQADeleteResponse:
    index_instance = get_index_instance(user_id = '', request = request)
    index = index_instance.load_index_by_index_id(index_id=index_id)
    index_instance.delete_index_by_index_id(index, index_id)
    return DocQADeleteResponse(content="Delete successfully")


@document_qa_router.delete("/document_qa/{index_id}/{ref_doc_id}", dependencies=[Depends(validate_token)])
async def delete_index_by_ref_doc_id(index_id, ref_doc_id, request: Request):
    index_instance = get_index_instance(user_id = '', request = request)
    index = index_instance.load_index_by_index_id(index_id=index_id)
    index_instance.delete_index_by_ref_doc_id(index, index_id, ref_doc_id)
    return DocQADeleteResponse(content="Delete successfully")
