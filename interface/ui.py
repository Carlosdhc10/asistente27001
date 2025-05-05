import gradio as gr
import os
from models.assistant import responder_pregunta
from data.cases import user_cases

def launch_ui(server_name="127.0.0.1", server_port=7860):
    with gr.Blocks() as demo:
        gr.Markdown("# 🛡️ Asistente ISO 27000 — Casos de Usuario")

        with gr.Row():
            modelo = gr.Radio(["OpenAI GPT-3.5", "Hugging Face Zephyr"], label="Modelo", value="Hugging Face Zephyr")
            caso_dropdown = gr.Dropdown(list(user_cases.keys()), label="Selecciona un caso de estudio")
        
        caso_texto = gr.Textbox(label="Descripción del caso", lines=5, interactive=False, show_copy_button=True)

        pregunta = gr.Textbox(label="Haz tu pregunta", placeholder="Ej: ¿Qué controles aplicarías en este caso?", lines=3)
        respuesta = gr.Textbox(label="Respuesta del asistente", lines=10, interactive=False)

        def mostrar_descripcion(caso_seleccionado):
            return user_cases.get(caso_seleccionado, "")

        def procesar(pregunta, modelo, caso):
            contexto = user_cases.get(caso, "")
            return responder_pregunta(pregunta, modelo, contexto)

        caso_dropdown.change(fn=mostrar_descripcion, inputs=caso_dropdown, outputs=caso_texto)
        gr.Button("Responder").click(fn=procesar, inputs=[pregunta, modelo, caso_dropdown], outputs=respuesta)

    demo.launch(server_name=server_name, server_port=server_port)
