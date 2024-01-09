from app.utils import generate_response, string_not_null
from app.types import FaqCategory
from markupsafe import escape


def extract_and_validate_post_data(request):
    question = escape(request.form.get("question"))
    answer = escape(request.form.get("answer"))
    category = escape(request.form.get("category"))
    courses_id = escape(request.form.getlist("courses_id"))

    try:
        FaqCategory(category).name
    except:
        return False, generate_response(
            "La categoría ingresada es inválida", "error", 400
        )
    if not string_not_null(question):
        return False, generate_response("La pregunta es obligatoria", "error", 400)
    if not string_not_null(answer):
        return False, generate_response("La respuesta es obligatoria", "error", 400)
    if not string_not_null(category):
        return False, generate_response("La categoría es obligatoria", "error", 400)

    md = {"answer": answer, "category": category, "courses_id": courses_id}
    text = question.strip()

    return True, text, md
