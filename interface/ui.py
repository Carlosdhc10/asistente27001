import gradio as gr
import os
from models.assistant import responder_pregunta, comparar_respuestas
from data.cases import user_cases

def launch_ui(server_name="127.0.0.1", server_port=int(os.getenv("PORT", 7860))):  # Cambiado 0.0.0.0 a 127.0.0.1
    with gr.Blocks() as demo:
        gr.Markdown("# 🛡️ Asistente ISO 27000 — Casos de Usuario")

        with gr.Row():
            modelo = gr.Radio(["OpenAI GPT-3.5", "Hugging Face Zephyr"], label="Modelo", value="Hugging Face Zephyr")
            caso_dropdown = gr.Dropdown(list(user_cases.keys()), label="Selecciona un caso de estudio")

        caso_texto = gr.Textbox(label="Descripción del caso", lines=5, interactive=False, show_copy_button=True)

        pregunta = gr.Textbox(label="Haz tu pregunta", placeholder="Ej: ¿Qué controles aplicarías en este caso?", lines=3)
        respuesta_asistente = gr.Textbox(label="Respuesta del asistente", lines=10, interactive=False)

        gr.Markdown("### ✍️ Tu Respuesta")
        respuesta_usuario = gr.Textbox(label="Tu respuesta", lines=5, placeholder="Escribe tu respuesta aquí...")

        gr.Markdown("### ✅ Evaluación")
        porcentaje = gr.Textbox(label="Porcentaje de acierto", interactive=False)
        recomendacion = gr.Textbox(label="Recomendación del asistente", lines=5, interactive=False)

        archivo_descarga = gr.File(label="Descargar evaluación")

        def mostrar_descripcion(caso_seleccionado):
            return user_cases.get(caso_seleccionado, "")

        def responder_y_guardar(pregunta, modelo, caso):
            contexto = user_cases.get(caso, "")
            respuesta = responder_pregunta(pregunta, modelo, contexto)
            return respuesta

        def evaluar_respuesta(pregunta, modelo, caso, respuesta_usuario):
            contexto = user_cases.get(caso, "")
            respuesta_asistente = responder_pregunta(pregunta, modelo, contexto, respuesta_usuario)

            # Desempacamos la respuesta
            respuesta, porcentaje_eval, recomendacion_eval = respuesta_asistente

            # Guardar como archivo
            path = "evaluacion.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write("📘 Descripción del caso:\n")
                f.write(contexto + "\n\n")
                f.write("🧠 Respuesta del asistente:\n")
                f.write(respuesta + "\n\n")
                f.write("👤 Tu respuesta:\n")
                f.write(respuesta_usuario + "\n\n")
                f.write(f"✅ Porcentaje de acierto: {porcentaje_eval}\n")
                f.write("🛠️ Recomendación:\n")
                f.write(recomendacion_eval + "\n")

            return respuesta, porcentaje_eval, recomendacion_eval, path

        caso_dropdown.change(fn=mostrar_descripcion, inputs=caso_dropdown, outputs=caso_texto)
        gr.Button("Comparar y evaluar").click(
            fn=evaluar_respuesta,
            inputs=[pregunta, modelo, caso_dropdown, respuesta_usuario],
            outputs=[respuesta_asistente, porcentaje, recomendacion, archivo_descarga]
        )

    demo.launch(server_name=server_name, server_port=server_port)  # Se mantiene 127.0.0.1 o el puerto por defecto
