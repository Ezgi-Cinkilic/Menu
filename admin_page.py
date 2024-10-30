# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 20:08:51 2024

@author: ASUS
"""
import streamlit as st
import json

# Menü öğelerini saklamak için JSON dosyasına yazma fonksiyonu
def save_menu(menu_items):
    with open("menu.json", "w") as f:
        json.dump(menu_items, f)

# Menü öğelerini JSON dosyasından yükleme fonksiyonu
def load_menu():
    try:
        with open("menu.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Kategoriler
categories = ["İçecek", "Burger", "Pizza", "Makarna"]

# Streamlit uygulama başlatma
st.title("Admin Sayfası - Menü Ekleme")

# Menü öğeleri listesi
menu_items = load_menu()

# Ürün ekleme alanları
ad = st.text_input("Ürün Adı")
fiyat = st.number_input("Fiyat", min_value=0, step=1, format="%d")
aciklama = st.text_area("Açıklama")
gorsel = st.file_uploader("Görsel Yükle", type=["jpg", "png", "jpeg"])
kategori = st.selectbox("Kategori Seçin", categories)  # Kategori seçimi

# Menüye ekleme butonu
if st.button("Menüye Ekle"):
    if any(item['Ad'].lower() == ad.lower() for item in menu_items):
            st.error("Bu ürün adı zaten mevcut. Lütfen farklı bir ad girin.")
    else:
        if ad and aciklama and gorsel:
            new_item = {
                "Ad": ad,
                "Fiyat": fiyat,
                "Açıklama": aciklama,
                "Görsel": gorsel.getvalue().decode("ISO-8859-1"),  # Görseli string olarak kaydet
                "Kategori": kategori  # Kategori bilgisi ekleniyor
            }
            menu_items.append(new_item)
            save_menu(menu_items)  # Menü dosyasını güncelle
            st.success("Ürün menüye eklendi!")
    
            # Girdi alanlarını temizle
            ad = ""
            fiyat = 0
            aciklama = ""
            gorsel = None
            kategori = categories[0]  # İlk kategoriyi seç
        else:
            st.error("Lütfen tüm alanları doldurunuz.")

# Mevcut menü öğelerini listeleme
st.subheader("Mevcut Menü")
for i, item in enumerate(menu_items):
    # Ürün bilgilerini gösterme
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(item["Görsel"].encode("ISO-8859-1"), use_column_width=True, width=100)
    with col2:
        st.write(f"**{item['Ad']}** - {item['Fiyat']} TL")
        st.write(item["Açıklama"])
        st.write(f"**Kategori:** {item['Kategori']}")

        # Düzenleme durumu
        if f"editing_{i}" not in st.session_state:
            st.session_state[f"editing_{i}"] = False

        # Düzenleme butonu
        if st.button("📝 Düzenle", key=f"edit_{i}"):  # Her butona benzersiz bir anahtar veriyoruz
            st.session_state[f"editing_{i}"] = True  # Düzenleme modunu aç

        # Düzenleme alanları
        if st.session_state[f"editing_{i}"]:
            new_fiyat = st.number_input("Yeni Fiyat", value=item['Fiyat'], min_value=0, step=1)
            new_aciklama = st.text_area("Yeni Açıklama", value=item['Açıklama'])

            if st.button("Değişiklikleri Kaydet", key=f"save_{i}"):
                item['Fiyat'] = new_fiyat
                item['Açıklama'] = new_aciklama
                save_menu(menu_items)  # Menü dosyasını güncelle
                st.success(f"{item['Ad']} başarıyla güncellendi!")
                st.session_state[f"editing_{i}"] = False  # Düzenleme modunu kapat
                st.stop()  # Uygulamayı durdur ve yenile

            if st.button("İptal", key=f"cancel_{i}"):
                st.session_state[f"editing_{i}"] = False  # Düzenlemeyi iptal et

        # Silme butonu (çöp kutusu)
        if not st.session_state[f"editing_{i}"]:  # Düzenleme modunda değilse silme butonunu göster
            if st.button("🗑️", key=f"delete_{i}"):  # Her butona benzersiz bir anahtar veriyoruz
                menu_items.pop(i)  # Ürünü listeden sil
                save_menu(menu_items)  # Menü dosyasını güncelle
                st.success(f"{item['Ad']} başarıyla silindi!")
                st.stop()  # Uygulamayı durdur ve yenile
                

    st.write("---")

