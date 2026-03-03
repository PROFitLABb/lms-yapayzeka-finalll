import os
from dotenv import load_dotenv

print("Mevcut dizin:", os.getcwd())
print(".env dosyası var mı?", os.path.exists(".env"))
print()

# .env dosyasını oku
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
        print("=== .env Dosya İçeriği ===")
        print(repr(content))
        print()

# dotenv yükle
result = load_dotenv()
print("load_dotenv() sonucu:", result)
print()

# Tüm environment variables
print("=== Environment Variables ===")
for key in ["GEMINI_API_KEY", "GROQ_API_KEY"]:
    value = os.getenv(key)
    print(f"{key}: {value[:20] + '...' if value else 'None'}")
