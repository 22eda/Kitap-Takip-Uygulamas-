import streamlit as st
import pandas as pd
import os

# 📁 Kayıt dosyasının adı
dosya_adi = "kitaplar.csv"

# 📥 Daha önce kayıt varsa oku, yoksa boş tablo oluştur
def kitaplari_yukle():
    if os.path.exists(dosya_adi):
        return pd.read_csv(dosya_adi)
    else:
        return pd.DataFrame(columns=["Kitap Adı", "Yazar", "Sayfa", "Tarih", "Puan", "Yorum", "Durum"])

# 💾 Yeni kitap ekle ve kaydet
def kitap_kaydet(yeni_veri):
    df = kitaplari_yukle()
    df = pd.concat([df, pd.DataFrame([yeni_veri])], ignore_index=True)
    df.to_csv(dosya_adi, index=False)

# 🗑️ Kitap sil
def kitap_sil(indeks):
    df = kitaplari_yukle()
    if 0 <= indeks < len(df):
        silinen = df.loc[indeks, "Kitap Adı"]
        df = df.drop(indeks).reset_index(drop=True)
        df.to_csv(dosya_adi, index=False)
        st.success(f"'{silinen}' kitabı silindi.")
    else:
        st.error("Geçersiz seçim!")

# 🎨 Uygulama Arayüzü
st.title("📚 Kitap Takip Uygulaması")

# Yan panel: Kitap ekleme
st.sidebar.header("➕ Yeni Kitap Ekle")

kitap_adi = st.sidebar.text_input("Kitap Adı")
yazar = st.sidebar.text_input("Yazar")
sayfa = st.sidebar.number_input("Sayfa Sayısı", min_value=1, step=1)
tarih = st.sidebar.date_input("Okuma Tarihi")
puan = st.sidebar.slider("Puan", 1, 10)
yorum = st.sidebar.text_area("Yorum")
durum = st.sidebar.selectbox("Okuma Durumu", ["Okundu", "Okunacak", "Yarıda Kaldı"])

if st.sidebar.button("📥 Kaydet"):
    if kitap_adi.strip() == "" or yazar.strip() == "":
        st.sidebar.error("Kitap adı ve yazar boş olamaz!")
    else:
        yeni_kitap = {
            "Kitap Adı": kitap_adi,
            "Yazar": yazar,
            "Sayfa": sayfa,
            "Tarih": tarih,
            "Puan": puan,
            "Yorum": yorum,
            "Durum": durum
        }
        kitap_kaydet(yeni_kitap)
        st.sidebar.success("✅ Kitap başarıyla kaydedildi!")

# Kitapları yükle
kitaplar = kitaplari_yukle()

# Filtreleme seçenekleri
st.subheader("🔍 Kitapları Filtrele / Ara")

with st.form("filter_form"):
    filtre_durum = st.selectbox("Duruma göre filtrele", options=["Hepsi"] + ["Okundu", "Okunacak", "Yarıda Kaldı"])
    filtre_yazar = st.text_input("Yazar ara")
    filtre_kitap = st.text_input("Kitap adı ara")
    filtre_puan_min, filtre_puan_max = st.slider("Puan aralığı", 1, 10, (1, 10))
    filtre_submit = st.form_submit_button("Filtrele")

if filtre_submit:
    df_filtre = kitaplar.copy()
    if filtre_durum != "Hepsi":
        df_filtre = df_filtre[df_filtre["Durum"] == filtre_durum]
    if filtre_yazar.strip() != "":
        df_filtre = df_filtre[df_filtre["Yazar"].str.contains(filtre_yazar, case=False, na=False)]
    if filtre_kitap.strip() != "":
        df_filtre = df_filtre[df_filtre["Kitap Adı"].str.contains(filtre_kitap, case=False, na=False)]
    df_filtre = df_filtre[(df_filtre["Puan"] >= filtre_puan_min) & (df_filtre["Puan"] <= filtre_puan_max)]
else:
    df_filtre = kitaplar.copy()

# Kitapları göster
st.subheader("📖 Kitap Listesi")

if df_filtre.empty:
    st.info("Filtreleme sonucunda hiç kitap bulunamadı.")
else:
    # Kitapları tablo olarak göster
    st.dataframe(df_filtre.reset_index(drop=True))

    # Silme işlemi için seçim
    secilen_index = st.number_input("Silmek istediğin kitabın satır numarasını gir (0’dan başlar)", min_value=0, max_value=len(df_filtre)-1, step=1)

    if st.button("🗑️ Seçilen Kitabı Sil"):
        # Silme için orijinal DataFrame’de index bul
        orijinal_index = df_filtre.index[secilen_index]
        kitap_sil(orijinal_index)
        st.rerun()  # Sayfayı yenile

# İstatistikler
st.subheader("📊 İstatistikler")
toplam_kitap = len(kitaplar)
toplam_sayfa = kitaplar["Sayfa"].sum() if toplam_kitap > 0 else 0
ortalama_puan = kitaplar["Puan"].mean() if toplam_kitap > 0 else 0
st.write(f"Toplam kitap sayısı: **{toplam_kitap}**")
st.write(f"Toplam okunan sayfa sayısı: **{toplam_sayfa}**")
st.write(f"Ortalama puan: **{ortalama_puan:.2f}**")
