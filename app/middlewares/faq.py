from app.utils import generate_response, string_not_null

def extract_and_validate_post_data(request):
    question = request.form.get("question")
    answer = request.form.get("answer")
    category = request.form.get("category")
    courses_id = request.form.getlist("courses_id")

    if not string_not_null(question):
        return False, generate_response("La pregunta es obligatoria", "error", 400)
    if not string_not_null(answer):
        return False, generate_response("La respuesta es obligatoria", "error", 400)
    if not string_not_null(category):
        return False, generate_response("La categoría es obligatoria", "error", 400)

    md = {"answer": answer, "category": category, "courses_id": courses_id}
    text = question.strip()

    return True, text, md
