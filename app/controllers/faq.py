from typing import Tuple, Union
from flask import request
from app.middlewares.faq import extract_and_validate_post_data
from app.services.qdrant_service import connect_qdrant, search_in_qdrant
from app.config import Config
from app.utils import (
    generate_response,
    get_prompt,
    validate_prompt,
    retrieve_faq,
    process_successful_search,
    generate_faq_dict,
)
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client import QdrantClient


def handle_faq_response(all: bool = False) -> dict:
    qdrant_client, err = connect_qdrant()
    if err:
        return qdrant_client
    if request.method == "GET":
        return (
            handle_get_response(qdrant_client)
            if not all
            else handle_get_all_response(qdrant_client)
        )
    if request.method == "POST":
        return handle_post_response(qdrant_client)
    return generate_response("Método no permitido", "error", 405)


def handle_get_all_response(qdrant_client: QdrantClient) -> dict:
    try:
        records: list = qdrant_client.scroll(
            collection_name=Config.COLLECTION_NAME_FAQ, limit=1000
        )[0]
        response: list[dict] = [
            generate_faq_dict(doc.payload, doc.id) for doc in records
        ]
        return generate_response(response, "ok", 200)
    except UnexpectedResponse as ur:
        return generate_response(f"{ur}", "error", 404)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_get_response(qdrant_client: QdrantClient):
    prompt: str = get_prompt(request)
    prompt_validation: Union[bool, Tuple[any, float]] = validate_prompt(prompt)
    if prompt_validation is not True:
        return prompt_validation
    try:
        search_result: Union[list, str] = search_in_qdrant(
            prompt, Config.COLLECTION_NAME_FAQ, qdrant_client
        )
        return handle_faq_result(search_result)
    except UnexpectedResponse as ur:
        return generate_response(f"{ur}", "error", 404)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_post_response(qdrant_client: QdrantClient):
    result = extract_and_validate_post_data(request)

    if not result[0]:
        text, md = result[1], result[2]
        try:
            qdrant_client.add(
                Config.COLLECTION_NAME_FAQ, documents=[text], metadata=[md]
            )
            return generate_response("Pregunta agregada correctamente", "ok", 200)
        except UnexpectedResponse as e:
            return generate_response(f"{e}", "error", 400)
        except Exception as e:
            return generate_response("Algo salió mal en el servidor", "error", 500)
    else:
        return result[1]


def handle_faq_result(search_result):
    return (
        process_successful_search(search_result)
        if isinstance(search_result, list)
        else search_result
    )


def update_or_delete_faq(faq_id: str):
    conn, err = connect_qdrant()
    if err:
        return conn
    qdrant_client: QdrantClient = conn
    if request.method == "PUT":
        return handle_update_response(faq_id, qdrant_client)
    if request.method == "DELETE":
        return handle_faq_delete_response(faq_id, qdrant_client)

    return generate_response("Método no permitido", "error", 405)


def handle_update_response(faq_id: str, qdrant_client: QdrantClient):
    result = extract_and_validate_post_data(request)
    if not result[0]:
        try:
            qdrant_client.overwrite_payload(
                Config.COLLECTION_NAME_FAQ,
                {
                    "document": result[1],
                    "answer": result[2]["answer"],
                    "category": result[2]["category"],
                    "courses_id": result[2]["courses_id"],
                },
                points=[faq_id],
            )
        except:
            pass
    return result[1]


def handle_faq_delete_response(faq_id: str, qdrant_client: QdrantClient):
    faq, err = retrieve_faq(qdrant_client, faq_id)
    if err:
        return faq

    if len(faq) == 0:
        return generate_response("La pregunta no existe", "error", 404)

    try:
        qdrant_client.delete(Config.COLLECTION_NAME_FAQ, [faq_id])
        return generate_response("Pregunta eliminada correctamente", "ok", 200)
    except UnexpectedResponse as e:
        return generate_response(f"{e}", "error", 400)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def get_faq_by_id(faq_id: str):
    qdrant_client, err = connect_qdrant()
    if err:
        return qdrant_client

    faq, err = retrieve_faq(qdrant_client, faq_id)
    if err:
        return faq
    if len(faq) == 0:
        return generate_response("La pregunta no existe", "error", 404)
    return generate_response(
        generate_faq_dict(faq[0].payload, faq[0].id),
        "ok",
        200,
    )
