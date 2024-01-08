from flask import request
from app.services.qdrant_service import connect_qdrant, search_in_qdrant
from app.config import Config
from app.utils import generate_response, get_prompt, validate_prompt, string_not_null


def handle_faq_response(all=False):
    if (request.method == "GET"):
        return handle_get_response() if not all else handle_get_all_response()
    if (request.method == "POST"):
        return handle_post_response()
    return generate_response("Método no permitido", "error", 405)


def handle_get_all_response():
    qdrant_client = connect_qdrant()
    if qdrant_client is None:
        return generate_response(
            "No se ha podido conectar al cliente de Qdrant", "error", 500
        )
    try:
        records = qdrant_client.scroll(
            collection_name=Config.COLLECTION_NAME_FAQ, limit=1000
        )[0]
        response = []
        for doc in records:
            response.append({
                "question": doc.payload["document"],
                "answer": doc.payload["answer"],
                "category": doc.payload["category"],
                "courses_id": doc.payload["courses_id"]
            })
        return generate_response(response, "ok", 200)
    except Exception as e:
        print(e)
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_get_response():
    prompt = get_prompt(request)
    prompt_validation = validate_prompt(prompt)
    if (prompt_validation is not True):
        return prompt_validation
    qdrant_client = connect_qdrant()
    if qdrant_client is None:
        return generate_response(
            "No se ha podido conectar al cliente de Qdrant", "error", 500
        )
    try:
        search_result = search_in_qdrant(
            prompt, Config.COLLECTION_NAME_FAQ, qdrant_client)
        return handle_faq_result(search_result)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_post_response():
    question = request.form["question"]
    answer = request.form["answer"]
    category = request.form["category"]
    courses_id = request.form.getlist("courses_id")

    if (not string_not_null(question)):
        return generate_response("La pregunta es obligatoria", "error", 400)
    if (not string_not_null(answer)):
        return generate_response("La respuesta es obligatoria", "error", 400)
    if (not string_not_null(category)):
        return generate_response("La categoría es obligatoria", "error", 400)

    qdrant_client = connect_qdrant()
    if qdrant_client is None:
        return generate_response(
            "No se ha podido conectar al cliente de Qdrant", "error", 500
        )
    md = {
        "answer": answer,
        "category": category,
        "courses_id": courses_id
    }
    text = question.strip()

    try:
        qdrant_client.add(Config.COLLECTION_NAME_FAQ,
                          documents=[text], metadata=[md])
        return generate_response("Pregunta agregada correctamente", "ok", 200)
    except Exception as e:
        return generate_response("Algo salió mal en el servidor", "error", 500)


def handle_faq_result(search_result):
    return (
        process_successful_search(search_result)
        if isinstance(search_result, list)
        else search_result
    )


def process_successful_search(search_result):
    score = search_result[0].score
    if score < Config.SCORE_THRESHOLD:
        return generate_response("No se han encontrado resultados", "error", 404)
    return generate_response(search_result[0].metadata["answer"], "ok", 200, score)
