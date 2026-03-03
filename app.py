import os
import time

import streamlit as st
from dotenv import load_dotenv

from ai_service import analyze_text
from database import get_history, init_db, save_analysis, get_statistics, search_history
from models import TextRequest
import pandas as pd
from datetime import datetime


# .env dosyasını yüklemeyi dene (Lokaldeysen çalışır)
load_dotenv()

# Manuel API key ayarı (geçici çözüm)
if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "AIzaSyAzIHgEQ9nQ_5QeIzF5G1NfmGD8aVxaG6I"


def get_api_key(key_name: str) -> str | None:
    """
    Önce .env dosyasını kontrol eder, bulamazsa
    Streamlit Secrets (Bulut) sistemine bakar.
    """
    # Önce sistem ortam değişkenlerine bak (.env burayı doldurur)
    api_key = os.getenv(key_name)

    # Eğer orada yoksa (Deploy ortamındaysak) Streamlit Secrets'a bak
    if not api_key and key_name in st.secrets:
        api_key = st.secrets[key_name]

    return api_key


if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0


def check_rate_limit(interval_seconds: int = 10) -> bool:
    """
    Kullanıcının isteklerini basitçe sınırlamak için zaman kontrolü.
    Varsayılan olarak 10 saniyede bir istek yapılmasına izin verir.
    """
    current_time = time.time()
    if current_time - st.session_state.last_request_time < interval_seconds:
        return False
    st.session_state.last_request_time = current_time
    return True


# 1. Başlangıç Ayarları
st.set_page_config(page_title="AI Destekli LMS", page_icon="🎓")

# Uygulama açıldığında veritabanı tablolarını oluştur (Eğer yoksa)
init_db()

st.title("🎓 AI Destekli LMS Analiz Paneli")
st.markdown(
    """
Bu sistem, öğrenci geri bildirimlerini **Doğal Dil İşleme (NLP)** kullanarak analiz eder.
Eğitmenlere ders kalitesini artırmak için yapay zeka tabanlı içgörüler sunar.
"""
)
st.markdown("---")

# 2. Yan Menü (Sekme Mantığı)
menu = st.sidebar.selectbox("Menü", ["Dashboard", "Analiz Yap", "Geçmiş Analizler"])

# Dashboard Sayfası
if menu == "Dashboard":
    st.subheader("📊 Genel İstatistikler")
    
    stats = get_statistics()
    
    # İstatistik Kartları
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Analiz", stats["total"])
    
    with col2:
        st.metric("Pozitif", stats["positive"], delta=f"{stats['positive']} adet")
    
    with col3:
        st.metric("Negatif", stats["negative"], delta=f"-{stats['negative']} adet", delta_color="inverse")
    
    with col4:
        st.metric("Nötr", stats["neutral"])
    
    # Grafik
    if stats["total"] > 0:
        st.markdown("---")
        st.subheader("📈 Duygu Dağılımı")
        
        chart_data = pd.DataFrame({
            "Duygu": ["Pozitif", "Negatif", "Nötr"],
            "Sayı": [stats["positive"], stats["negative"], stats["neutral"]]
        })
        
        st.bar_chart(chart_data.set_index("Duygu"))
        
        # Pasta grafik için
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("**Yüzdelik Dağılım:**")
            if stats["total"] > 0:
                pos_pct = (stats["positive"] / stats["total"]) * 100
                neg_pct = (stats["negative"] / stats["total"]) * 100
                neu_pct = (stats["neutral"] / stats["total"]) * 100
                
                st.progress(pos_pct / 100, text=f"Pozitif: %{pos_pct:.1f}")
                st.progress(neg_pct / 100, text=f"Negatif: %{neg_pct:.1f}")
                st.progress(neu_pct / 100, text=f"Nötr: %{neu_pct:.1f}")

elif menu == "Analiz Yap":
    st.subheader("📝 Yeni Analiz")

    # Kullanıcı Girdileri
    user_name = st.text_input("Kullanıcı Adınız", value="Öğrenci")
    feedback_text = st.text_area("Analiz edilecek geri bildirimi girin:", height=150)
    provider = st.selectbox("AI Modeli", ["gemini", "groq"])

    if st.button("AI Analizini Başlat"):
        if feedback_text:
            with st.spinner("Yapay zeka analiz ediyor..."):
                try:
                    # Basit rate limit kontrolü
                    if not check_rate_limit():
                        st.warning("Lütfen yeni bir istek göndermeden önce birkaç saniye bekleyin.")
                    else:
                        # A. Veri Doğrulama (Models kullanımı)
                        request_data = TextRequest(
                            text=feedback_text, provider=provider
                        )

                        # B. AI Servis Çağrısı
                        response = analyze_text(
                            request_data.text, request_data.provider
                        )

                    if "error" in response:
                        st.error(response["error"])
                    else:
                        # C. Sonuçları Ekranda Göster
                        st.success("Analiz Tamamlandı!")
                        st.subheader("📊 AI Analiz Sonucu")
                        st.info(response["analysis"])
                        st.caption(f"Kaynak: {response['source']}")

                        # D. Veritabanına Kaydet (Database kullanımı)
                        save_analysis(
                            user_name=user_name,
                            text=feedback_text,
                            result=response["analysis"],
                            provider=response["source"],
                        )
                        st.toast("Veritabanına kaydedildi!")

                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen bir metin girin.")

elif menu == "Geçmiş Analizler":
    st.subheader("📜 Analiz Geçmişi")
    
    # Filtreleme ve Arama
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Ara (metin, kullanıcı, sonuç)", "")
    
    with col2:
        start_date = st.date_input("Başlangıç Tarihi", value=None)
    
    with col3:
        end_date = st.date_input("Bitiş Tarihi", value=None)
    
    # Arama yap
    if search_term or start_date or end_date:
        history = search_history(
            search_term=search_term,
            start_date=start_date.strftime("%Y-%m-%d") if start_date else None,
            end_date=end_date.strftime("%Y-%m-%d") if end_date else None
        )
    else:
        history = get_history()
    
    # CSV Export Butonu
    if history:
        # DataFrame oluştur
        df_data = []
        for row in history:
            df_data.append({
                "Kullanıcı": row["user_name"],
                "Tarih": row["created_at"],
                "Orijinal Metin": row["original_text"],
                "AI Analizi": row["ai_result"],
                "Model": row["provider"]
            })
        
        df = pd.DataFrame(df_data)
        
        # CSV indirme butonu
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 CSV Olarak İndir",
            data=csv,
            file_name=f"analiz_gecmisi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.info(f"Toplam {len(history)} kayıt bulundu")
    
    if not history:
        st.write("Henüz bir analiz kaydı bulunamadı.")
    else:
        for row in history:
            with st.expander(f"📌 {row['user_name']} - {row['created_at']}"):
                st.write(f"**Orijinal Metin:** {row['original_text']}")
                st.write(f"**AI Analizi:** {row['ai_result']}")
                st.caption(f"Model: {row['provider']}")

st.markdown("---")
st.caption("LMS AI Final Project v2.0 - Enhanced Edition")

 

