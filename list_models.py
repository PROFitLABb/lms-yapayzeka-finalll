import os
import google.generativeai as genai

# API key'i ayarla
os.environ["GEMINI_API_KEY"] = "AIzaSyAzIHgEQ9nQ_5QeIzF5G1NfmGD8aVxaG6I"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Mevcut Gemini Modelleri:")
print("=" * 60)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
except Exception as e:
    print(f"Hata: {e}")
