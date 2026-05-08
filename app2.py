# =========================================
# UNIVERSAL AI TRANSLATOR (200+ LANGUAGES)
# =========================================

# INSTALL REQUIRED LIBRARIES
# Run this in Colab first:
#
# !pip install -q transformers sentencepiece torch gradio langdetect

# =========================================
# IMPORTS
# =========================================

import gradio as gr
from transformers import pipeline
from langdetect import detect

# =========================================
# LOAD TRANSLATION MODEL
# =========================================

translator = pipeline(
    "translation",
    model="facebook/nllb-200-distilled-600M",
    device=-1
)

# =========================================
# LANGUAGE MAPPING
# =========================================

languages = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "French": "fra_Latn",
    "German": "deu_Latn",
    "Spanish": "spa_Latn",
    "Chinese": "zho_Hans",
    "Japanese": "jpn_Jpan",
    "Korean": "kor_Hang",
    "Russian": "rus_Cyrl",
    "Arabic": "arb_Arab",
    "Portuguese": "por_Latn",
    "Bengali": "ben_Beng",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Urdu": "urd_Arab"
}

# =========================================
# LANGUAGE DETECTION
# =========================================

def detect_language(text):

    try:

        detected = detect(text)

        mapping = {
            "en": "English",
            "hi": "Hindi",
            "fr": "French",
            "de": "German",
            "es": "Spanish",
            "zh-cn": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "ar": "Arabic",
            "pt": "Portuguese",
            "bn": "Bengali",
            "ta": "Tamil",
            "te": "Telugu",
            "ur": "Urdu"
        }

        return mapping.get(detected, "Unknown")

    except:

        return "Unknown"

# =========================================
# TRANSLATION FUNCTION
# =========================================

def translate_text(text, source_lang, target_lang):

    try:

        if text.strip() == "":
            return "Please enter text."

        source_code = languages[source_lang]
        target_code = languages[target_lang]

        result = translator(
            text,
            src_lang=source_code,
            tgt_lang=target_code,
            max_length=400
        )

        translated_text = result[0]["translation_text"]

        detected_language = detect_language(text)

        final_output = f"""
Detected Language:
{detected_language}

Translated Text:
{translated_text}
"""

        return final_output

    except Exception as e:

        return f"Translation Error: {str(e)}"

# =========================================
# GRADIO UI
# =========================================

title = "🌍 Universal AI Translator"

description = """
Translate text across 200+ languages using AI.

Features:
✅ AI-powered translation  
✅ Language detection  
✅ Multilingual support  
✅ Real-time translation  
"""

examples = [
    [
        "Hello, how are you?",
        "English",
        "Hindi"
    ],
    [
        "Artificial Intelligence is changing the world.",
        "English",
        "French"
    ],
    [
        "Machine Learning is amazing.",
        "English",
        "German"
    ]
]

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(f"# {title}")

    gr.Markdown(description)

    input_text = gr.Textbox(
        label="Enter Text",
        lines=6,
        placeholder="Type text to translate..."
    )

    with gr.Row():

        source_language = gr.Dropdown(
            choices=list(languages.keys()),
            value="English",
            label="Source Language"
        )

        target_language = gr.Dropdown(
            choices=list(languages.keys()),
            value="Hindi",
            label="Target Language"
        )

    translate_button = gr.Button("🚀 Translate")

    output_text = gr.Textbox(
        label="Translation Output",
        lines=10
    )

    translate_button.click(
        fn=translate_text,
        inputs=[
            input_text,
            source_language,
            target_language
        ],
        outputs=output_text
    )

    gr.Examples(
        examples=examples,
        inputs=[
            input_text,
            source_language,
            target_language
        ]
    )

# =========================================
# LAUNCH APPLICATION
# =========================================

demo.launch(share=True)
