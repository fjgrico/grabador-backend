import openai
import os

def interpretar_sueno(texto_sueno):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
Eres un experto internacional en interpretación simbólica y espiritual de los sueños, con conocimientos en psicología profunda, tradiciones chamánicas y orientales, culturas ancestrales y simbolismo universal. Interpreta el siguiente sueño de forma detallada y comprensiva.

Sueño del consultante:
"{texto_sueno}"

Analiza el sueño en profundidad desde los siguientes enfoques:
1. 🧠 Freudiana / Inconsciente reprimido: analiza los deseos inconscientes, represiones y mecanismos de defensa.
2. 🧠 Junguiana / Arquetípica: interpreta los arquetipos presentes, símbolos universales y el proceso de individuación.
3. 🖋️ Metafórica / Poética: describe el mensaje del sueño como una metáfora del alma y su lenguaje poético.
4. 🌌 Espiritual / Trascendente: conecta el sueño con una experiencia espiritual, de guía o trascendencia.
5. 🧘 Taoísta / Budista: interpreta el sueño como un mensaje sobre el desapego, la mente, el karma o el flujo del Tao.
6. 🔥 Chamánica: analiza el sueño como un viaje del alma, señal de animales de poder o mensajes del mundo invisible.
7. 🙏 Hindú / Védica: incluye posibles significados según los Vedas, el alma (Atman) y el ciclo del Samsara.
8. 🪶 Nativo Americano (Hopi): analiza los símbolos según esta cosmovisión: visión, equilibrio, naturaleza, ancestrales.
9. 🧊 Tradición Escandinava: interpreta el sueño con elementos del inconsciente nórdico, mitología y símbolos rúnicos.
10. 🌍 Tradición Africana: conecta con símbolos tribales, energías ancestrales, la sabiduría de los sueños y la comunidad.

Asegúrate de mencionar detalles simbólicos o arquetípicos de cualquier objeto, animal, persona, emoción o escenario presente en el sueño. Si hay un elemento concreto (por ejemplo, una puerta, un río, una caída, un fuego, etc.), desarrolla su simbolismo en cada enfoque relevante.

Después de todas las interpretaciones, ofrece una pregunta profunda que ayude al usuario a reflexionar sobre el mensaje del sueño, y finaliza con una pregunta dirigida directamente al consultante que invite a la acción o a la introspección.

Responde con lenguaje humano, emocional y comprensible, pero con autoridad profesional.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un guía experto en interpretación simbólica, ancestral y espiritual de los sueños."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85
    )

    return response.choices[0].message.content.strip()
