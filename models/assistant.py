import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from openai import OpenAI
from utils.helpers import evaluar_respuesta  # Ya está importada

# Cargar variables de entorno
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Inicializar clientes
client_openai = OpenAI(api_key=OPENAI_API_KEY)
hf_model_id = "HuggingFaceH4/zephyr-7b-beta"
hf_client = InferenceClient(model=hf_model_id, token=HUGGINGFACE_API_TOKEN)

def responder_con_openai(pregunta):
    try:
        respuesta = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en normas ISO 27000."},
                {"role": "user", "content": pregunta}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI] Error: {str(e)}"

def responder_con_huggingface(pregunta):
    try:
        prompt = f"Eres un experto en normas ISO 27000. Responde con precisión:\nUsuario: {pregunta}\nAsistente:"
        respuesta = hf_client.text_generation(prompt, max_new_tokens=500, temperature=0.3)
        return respuesta.strip()
    except Exception as e:
        return f"[Hugging Face] Error: {str(e)}"

def responder_pregunta(pregunta, modelo, contexto, respuesta_usuario=None):
    entrada = f"{contexto}\n\nPregunta: {pregunta}"
    
    if modelo == "OpenAI GPT-3.5":
        respuesta_modelo = responder_con_openai(entrada)
    elif modelo == "Hugging Face Zephyr":
        respuesta_modelo = responder_con_huggingface(entrada)
    else:
        return "Modelo no reconocido."

    if respuesta_usuario:
        porcentaje, recomendacion = evaluar_respuesta(respuesta_modelo, respuesta_usuario)
        return respuesta_modelo, porcentaje, recomendacion

    return respuesta_modelo

def comparar_respuestas(respuesta_asistente, respuesta_usuario):
    """
    Compara las respuestas del asistente y la del usuario.
    Devuelve un porcentaje de coincidencia y una recomendación.
    """
    # Aquí se puede utilizar alguna lógica más avanzada para comparar las respuestas.
    # Para este ejemplo, compararemos simplemente si las respuestas son iguales.
    if respuesta_asistente.strip().lower() == respuesta_usuario.strip().lower():
        return 100, "Respuesta correcta"
    else:
        return 50, "La respuesta podría mejorarse. Revisa la norma ISO 27000 para más detalles."
