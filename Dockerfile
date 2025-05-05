# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia todos los archivos al contenedor
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usa Gradio
EXPOSE 7860

# Establece la variable de entorno para producción (opcional)
ENV GRADIO_ALLOW_FLAGGING="never"

# Comando por defecto para ejecutar tu aplicación
CMD ["python", "main.py"]
