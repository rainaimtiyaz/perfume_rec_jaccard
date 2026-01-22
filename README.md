# Personalized Perfume Recommendation System
> **Undergraduate Thesis: Personalized Perfume Recommendations Based on User Descriptions Using Cosine and Jaccard Similarity**

## Project Background
Memilih parfum secara online merupakan tantangan karena keterbatasan indra penciuman digital. Proyek skripsi ini mengembangkan sistem rekomendasi **Content-Based Filtering** yang mampu menerjemahkan deskripsi keinginan pengguna (misal: "wangi jasmine fresh dan lavender") menjadi rekomendasi produk yang akurat.

Penelitian ini memfokuskan pada perbandingan efektivitas dua metode *similarity* dalam memproses deskripsi teks berbahasa Indonesia untuk menghasilkan rekomendasi yang paling relevan.

---

## Technical Workflow & Methodology

### 1. Indonesian NLP Preprocessing
Sistem menggunakan **Sastrawi** untuk pemrosesan teks Bahasa Indonesia yang optimal:
* **Tokenization & Cleaning:** Menghapus karakter khusus dan angka.
* **Stopword Removal:** Menghapus kata umum serta kata spesifik domain yang tidak memberikan nilai unik (misal: "parfum", "aroma").
* **Feature Extraction:** Menggunakan **TF-IDF Vectorizer** untuk mengubah deskripsi tekstual menjadi representasi numerik.

### 2. Similarity Methods Comparison
Sistem ini mengimplementasikan dua pendekatan berbeda untuk menghitung kemiripan:

* **Jaccard Similarity (`perfume_recommender.py`):** Berfokus pada irisan kata kunci (*sets of tokens*) antara input pengguna dan deskripsi parfum. Metode ini cenderung efektif untuk pencocokan kata kunci yang spesifik.
* **Cosine Similarity (`perfume_recommender_cosine.py`):** Mengukur sudut antar vektor TF-IDF. Metode ini lebih berfokus pada kemiripan konteks dan frekuensi kata dalam deskripsi.

---

## Model Evaluation (Comparison)
Berdasarkan pengujian mendalam yang dilakukan pada `dataset_prep.ipynb`, berikut adalah hasil perbandingan performa kedua metode:

| Metric | Jaccard Similarity (Selected) | Cosine Similarity |
| :--- | :---: | :---: |
| **Recall@3** | **~0.889** | ~0.778 |
| **Precision@3** | **~0.889** | ~0.778 |
| **nDCG@3** | ~0.897 | **1** |
| **Catalog Coverage** | ~0.0004 | ~0.0004 |

> **Key Finding:** Meskipun kedua metode memberikan hasil yang baik, **Jaccard Similarity** dipilih sebagai mesin utama sistem ini. Jaccard memberikan skor **Recall** yang lebih tinggi, yang berarti sistem lebih mampu menemukan hampir semua item relevan dan menampilkannya di urutan teratas (ranking lebih akurat).

---

## Limitations & Notes
Penting untuk diperhatikan bahwa sistem ini memiliki batasan terkait **bahasa pada dataset**:

* **English-Based Scent Keywords:** Meskipun sistem diprogram untuk memproses struktur kalimat Bahasa Indonesia, dataset utama (*aroma/notes*) masih menggunakan terminologi **Bahasa Inggris**.
* **Keyword Matching:** Pengguna disarankan menggunakan istilah aroma dalam Bahasa Inggris untuk mendapatkan hasil maksimal.
    * **Efektif:** *"Parfum wangi **apple** yang **fresh** dan **fruity**"* (Sistem berhasil mencocokkan ketiga kata kunci).
    * **Kurang Efektif:** *"Parfum wangi **apel** yang **segar** dan **fruity**"* (Sistem mungkin hanya mendeteksi *"fruity"*, karena gagal mengenali *"apel"* sebagai *"apple"* atau *"segar"* sebagai *"fresh"*).
      
---

## Main Features
* **Natural Language Query:** Mendukung input deskripsi bebas dalam Bahasa Indonesia.
* **Dual Engine Support:** Tersedia skrip terpisah untuk pengujian dengan Cosine maupun Jaccard.
* **Smart Attribute Filtering:** Memungkinkan filter berdasarkan Gender, Waktu Penggunaan (Day/Night), dan pengecualian (*Exclusions*) tertentu.
* **Rating Integration:** Mempertimbangkan rating produk dalam proses pemeringkatan (namun tetap mengutamakan kecocokan keyword).
