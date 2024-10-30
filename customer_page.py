# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 20:09:11 2024

@author: ASUS
"""
import streamlit as st
import json

# Menü öğelerini JSON dosyasından yükleme fonksiyonu
def load_menu():
    try:
        with open("menu.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Müşteri sayfası başlığı
st.title("Menü")

# Menü öğeleri
menu_items = load_menu()

# Kategorileri al
categories = list(set(item["Kategori"] for item in menu_items))  # Kategorileri oluştur
categories.insert(0, "Tümü")  # "Tümü" seçeneğini ekle

# Kategori butonları (yan yana)
num_columns = min(len(categories), 3)  # Kolon sayısını sınırlı tut
columns = st.columns(num_columns)  # Kategori sayısına göre kolon oluştur

# Butonları kolonlara yerleştir
for i, category in enumerate(categories):
    with columns[i % num_columns]:  # Kolon sayısına göre yerleştir
        if st.button(category):
            st.session_state.selected_category = category  # Seçilen kategoriyi state'de sakla

# Menü öğeleri boş değilse listeleme
if menu_items:
    selected_category = st.session_state.get("selected_category", "Tümü")  # Seçilen kategoriyi al, varsayılan "Tümü"

    if selected_category == "Tümü":
        st.subheader("Tüm Ürünler")  # Tüm ürünler başlığı
        category_items = menu_items  # Tüm öğeleri al
    else:
        st.subheader(selected_category)  # Seçilen kategori başlığı
        category_items = [item for item in menu_items if item["Kategori"] == selected_category]  # Seçilen kategori öğeleri

    # Ürünleri listele
    for item in category_items:
        # İki sütun oluştur
        col1, col2 = st.columns([1, 2])  # İlk sütun 1 birim, ikinci sütun 2 birim genişliğinde

        with col1:
            st.image(item["Görsel"].encode("ISO-8859-1"), use_column_width='auto', width=150)  # Resim sol sütunda

        with col2:
            st.write(f"**{item['Ad']}**")
            st.write(item["Açıklama"])
            st.write(f"**Fiyat: {item['Fiyat']} TL**")
            st.write("---")
else:
    st.warning("Menüde şu an ürün bulunmamaktadır.")

