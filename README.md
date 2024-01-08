## Instalación

1. **Clonar el Repositorio:**

   ```bash
   git clone https://github.com/JordiBustos/chatbot-videos.git
   cd chatbot-videos

   ```

2. python -m venv venv

   - source venv/bin/activate en unix o macos
   - .\venv\Scripts\activate en windows

3. pip install -r requirements.txt

4. Configurar variables de entorno QDRANT_KEY (apikey) y QDRANT_ENDPOINT (endpoint del cluster)

5. run "python main.py"

## Endpoint de Consulta query

### Descripción

El endpoint `/query` permite a los usuarios realizar una consulta en una base de datos vectorial, específicamente un clúster de Qdrant. Los usuarios proporcionan un mensaje en la solicitud, y el sistema genera una respuesta basada en los resultados de la consulta.

### Endpoint

- **Método:** GET
- **URL:** `health`

Chequear que el servicio está corriendo correctamente

### Endpoint

- **Método:** GET
- **URL:** `api/v1/query`

### Solicitud

- **Tipo de contenido:** `application/json`

#### Argumentos

| Nombre | Tipo   | Descripción                                         |
| ------ | ------ | --------------------------------------------------- |
| prompt | string | El mensaje generado por el usuario para la consulta |

#### Ejemplo

```javascript
var requestOptions = {
  method: "GET",
  redirect: "follow",
};

fetch(
  'http://127.0.0.1:5000/query?prompt="Cómo podemos escribir archivos?"',
  requestOptions
)
  .then((response) => response.text())
  .then((result) => console.log(result))
  .catch((error) => console.log("error", error));
```

```json
{
  "prompt": "Qué se puede hacer para manejar errores en tiempo de ejecución?"
}
```

```json
{
  "prompt": "Cómo podemos escribir archivos?"
}
```

```json
{
  "prompt": "Cómo puedo usar los bloques try y except para el manejo de errores?"
}
```

```json
{
  "prompt": "Qué son las variables globales y las locales?"
}
```

```json
{
  "prompt": "Cuál es la diferencia entre una variable global y una local?"
}
```

```json
{
  "prompt": "Qué son los argumentos variables, *args y **kwargs?"
}
```

## Respuesta

La API devuelve una respuesta JSON basada en los resultados de la consulta.

### Respuesta Exitosa

- Código de Estado: 200 OK

```json
{
  "status": "ok",
  "answer": "https://www.youtube.com/watch?v=identificador_del_video&t=tiempo_en_segundos",
  "score": "es un float del 0 al 1 representando la confianza en la respuesta"
}
```

- Si hubo un error

```json
{
  "status": "error",
  "message": "Error message"
}
```

## Endpoint de Consulta faq

### Endpoint

- **Métodos:** GET, POST
- **URL:** `api/v1/faq`

### Solicitud

- **Tipo de contenido:** `application/json`

Si la consulta es a través del método GET se debe proporcionar el argumento prompt de manera obligatoria, similar al query.
En cambio si es a través del método POST se debe proporcionar:
Si es en postman realizar a través de form-data en el body.

```json
{
    "question": "string",
    "answer": "string",
    "category": "string <admin, tech>",
    "courses_id": ["list of string"]
}
```

## Ejemplos

A pesar de usar palabras diferentes los siguientes dos prompts otorgan el mismo resultado

```json
{
  "prompt": "Cómo entrar en la plataforma"
}
```

```json
{
  "prompt": "Cómo puedo ingresar a la página"
}
```

## Notas

- El parámetro prompt es obligatorio en el cuerpo de la solicitud y debe contener alguna letra.
- Una respuesta exitosa incluye un enlace de video generado.
- Si no se encuentran resultados para el mensaje dado, se devuelve un error 404.
- Los errores internos del servidor se indican con una respuesta de error 500.
