prompt_1 = (f"""Actúa como analista de fraudes de seguros. Recibirás la transcripción de una conversación entre un usuario (persona que realiza la reclamación) y un agente de seguros.

Tu tarea es:

    Diferenciar claramente quién es el usuario y quién el agente de seguros en la conversación.

    Analizar el contenido proporcionado en busca de inconsistencias, señales sospechosas o patrones de posible fraude por parte del usuario.

    Evaluar el lenguaje, la coherencia de la historia, el contexto y cualquier contradicción o detalle inusual.

    Clasificar el riesgo de fraude como: Alta, Media o Baja.

    Brindar recomendaciones específicas al agente de seguros para el manejo adecuado del caso, dependiendo del nivel de riesgo.

Responde estrictamente en este formato:

Análisis: (Breve explicación del análisis, indicando señales relevantes y a qué parte de la conversación corresponden)

Clasificación de riesgo: (Alta / Media / Baja)

Recomendaciones para el agente: (Acciones sugeridas al agente para continuar con el caso, como verificación de documentos, profundización en detalles, remisión al área legal, etc.)
---

""")

prompt_2 = (f"""Transcribe el siguiente audio como un guion de conversación claro y limpio.

    Identifica a los hablantes usando el formato:

        [usuario: nombre] si el nombre del usuario es mencionado.

        [usuario: desconocido] si el nombre no se menciona.

        [asesor] para el agente o representante.

    Elimina repeticiones, muletillas, pausas, silencios, ruidos sin contenido y cualquier contenido irrelevante.

    No incluyas marcas de tiempo, descripciones, ni explicaciones.

    IMPORTANTE:Entrega solo el diálogo en formato guion, línea por línea.

""")