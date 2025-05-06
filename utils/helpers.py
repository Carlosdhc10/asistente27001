# utils/helpers.py

from difflib import SequenceMatcher

def evaluar_respuesta(respuesta_modelo, respuesta_usuario):
    ratio = SequenceMatcher(None, respuesta_modelo.lower(), respuesta_usuario.lower()).ratio()
    porcentaje = round(ratio * 100, 2)

    if porcentaje > 85:
        recomendacion = "✅ Excelente, tu respuesta está muy alineada con las mejores prácticas ISO 27000."
    elif porcentaje > 60:
        recomendacion = "🟡 Buena respuesta, pero puedes mejorar detallando más controles o justificando decisiones."
    else:
        recomendacion = "🔴 Tu respuesta necesita mejoras. Revisa los controles aplicables al caso con más detalle."

    return porcentaje, recomendacion
