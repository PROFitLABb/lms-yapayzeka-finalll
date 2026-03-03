# 🎓 AI Destekli LMS Analiz Paneli

Öğrenci geri bildirimlerini yapay zeka ile analiz eden, eğitmenlere ders kalitesini artırmak için içgörüler sunan bir Learning Management System (LMS) uygulaması.

## ✨ Özellikler

- 🤖 **Çoklu AI Desteği**: Google Gemini ve Groq (Llama 3) modelleri
- 📊 **Dashboard**: Gerçek zamanlı istatistikler ve duygu dağılımı grafikleri
- 🔍 **Gelişmiş Filtreleme**: Tarih ve metin bazlı arama
- 📥 **CSV Export**: Tüm analizleri CSV formatında indirme
- 💾 **Veritabanı**: SQLite ile kalıcı veri saklama
- 📈 **Duygu Analizi**: Pozitif, negatif ve nötr duygu tespiti
- ⚡ **Rate Limiting**: API kullanımını optimize eden istek sınırlama

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- pip

### Adımlar

1. Repoyu klonlayın:
```bash
git clone https://github.com/[kullanici-adi]/ai-lms-analysis.git
cd ai-lms-analysis
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyasını oluşturun ve API anahtarlarınızı ekleyin:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### API Anahtarları Nasıl Alınır?

**Google Gemini API:**
1. [Google AI Studio](https://aistudio.google.com/app/apikey) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşan anahtarı kopyalayın

**Groq API (Opsiyonel):**
1. [Groq Console](https://console.groq.com/) adresine gidin
2. Hesap oluşturun
3. API Keys bölümünden yeni bir anahtar oluşturun

## 💻 Kullanım

### Streamlit Uygulamasını Başlatma

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılacaktır.

### FastAPI Backend (Opsiyonel)

API endpoint'lerini kullanmak isterseniz:

```bash
uvicorn api:app --reload --port 8000
```

API dokümantasyonu: `http://localhost:8000/docs`

## 📁 Proje Yapısı

```
.
├── app.py                 # Ana Streamlit uygulaması
├── api.py                 # FastAPI backend
├── ai_service.py          # AI model entegrasyonları
├── database.py            # SQLite veritabanı işlemleri
├── models.py              # Pydantic veri modelleri
├── requirements.txt       # Python bağımlılıkları
├── .env                   # API anahtarları (git'e eklenmez)
├── lms.db                 # SQLite veritabanı
└── README.md             # Proje dokümantasyonu
```

## 🎯 Kullanım Senaryoları

### 1. Dashboard
- Toplam analiz sayısını görüntüleme
- Pozitif/negatif/nötr duygu dağılımı
- Görsel grafikler ve istatistikler

### 2. Analiz Yap
- Öğrenci geri bildirimini girin
- AI modelini seçin (Gemini veya Groq)
- Analiz sonuçlarını görüntüleyin
- Otomatik veritabanına kaydetme

### 3. Geçmiş Analizler
- Tüm geçmiş analizleri görüntüleme
- Metin, kullanıcı veya tarih bazlı filtreleme
- CSV formatında dışa aktarma

## 🛠️ Teknolojiler

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI Models**: Google Gemini 2.5 Flash, Groq Llama 3
- **Database**: SQLite
- **Data Processing**: Pandas
- **Validation**: Pydantic

## 📊 Veritabanı Şeması

### feedback_analysis
| Alan | Tip | Açıklama |
|------|-----|----------|
| id | INTEGER | Primary Key |
| user_name | TEXT | Kullanıcı adı |
| original_text | TEXT | Orijinal geri bildirim |
| ai_result | TEXT | AI analiz sonucu |
| provider | TEXT | Kullanılan AI modeli |
| created_at | TIMESTAMP | Oluşturulma tarihi |

## 🔒 Güvenlik

- API anahtarları `.env` dosyasında saklanır
- `.env` dosyası `.gitignore`'a eklenmelidir
- Rate limiting ile API kötüye kullanımı önlenir

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

[Adınız] - Final Projesi

## 🙏 Teşekkürler

- Google Gemini API
- Groq Cloud
- Streamlit Community

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
