import os
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print("=" * 50)
print("ENV Dosyası Test Sonuçları:")
print("=" * 50)
print(f"GEMINI_API_KEY: {'✓ Bulundu' if gemini_key else '✗ Bulunamadı'}")
if gemini_key:
    print(f"  İlk 10 karakter: {gemini_key[:10]}...")
print(f"GROQ_API_KEY: {'✓ Bulundu' if groq_key else '✗ Bulunamadı'}")
print("=" * 50)
