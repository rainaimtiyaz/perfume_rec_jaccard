import streamlit as st
import pandas as pd
from perfume_recommender import PerfumeRecommender
from perfume_recommender_cosine import PerfumeRecommenderCosine

# Custom CSS untuk styling
st.markdown("""
    <style>
        .st-emotion-cache-1qrv4ga, 
        .st-emotion-cache-1qrv4ga:hover,
        .st-emotion-cache-1qrv4ga:active,
        .st-emotion-cache-1qrv4ga:focus {
            color: black !important;
        }

        .st-emotion-cache-1qrv4ga:hover {
            font-weight: bold !important;
        }

        .st-emotion-cache-1qrv4ga[aria-expanded="true"] {
            font-weight: bold !important;
            color: black !important;
        }

        .stButton>button {
            background-color: #1E90FF;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0066CC;
            color: white !important;
        }
        .stButton>button:active {
            background-color: #004080;
            color: white !important;
        }

        .st-emotion-cache-5rimss.e1nzilvr5 {
            margin-bottom: 1rem;
        }
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 300px;
            background-color: #555;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -150px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 14px;
            font-weight: normal;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
""", unsafe_allow_html=True)

recommender_jaccard = PerfumeRecommender('perfume_dataset_final.csv')
recommender_cosine = PerfumeRecommenderCosine('perfume_dataset_final_cosine.csv')

st.title('Aromaku: Sistem Rekomendasi Parfum')

st.markdown("""
Temukan parfum yang sesuai untuk Anda berdasarkan preferensi pribadi! ✨
""")

col_guide, col_data = st.columns(2)

with col_guide:
    with st.expander("📖 Panduan Penggunaan", expanded=True):
        st.markdown("""
        1. Pilih gender parfum yang diinginkan
        2. Pilih waktu penggunaan
        3. Deskripsikan parfum yang Anda cari (Penulisan notes gunakan bahasa Inggris)
        4. Tulis pengecualian aroma (Jika tidak ada silakan isi dengan '-')
        5. Klik "Dapatkan Rekomendasi"
        """)

with col_data:
    with st.expander("📊 Tentang Dataset", expanded=True):
        st.markdown(f"""
        - Total Parfum: {len(recommender_jaccard.df)}
        - Parfum Wanita: {len(recommender_jaccard.df[recommender_jaccard.df['Gender'] == 'wanita'])}
        - Parfum Pria: {len(recommender_jaccard.df[recommender_jaccard.df['Gender'] == 'pria'])}
        - Parfum Unisex: {len(recommender_jaccard.df[recommender_jaccard.df['Gender'] == 'unisex'])}
        """)

st.markdown("""
<div class="tooltip">
    <h3>🔍 Pilih Metode Similarity</h3>
    <span class="tooltiptext">
        - Jaccard: Melihat berapa banyak keyword yang benar-benar sama antara input user dengan master data<br>
        - Cosine: Melihat seberapa mirip kecenderungan keyword antara input user dengan master data, meskipun tidak semua keyword sama
    </span>
</div>
""", unsafe_allow_html=True)

similarity_method = st.radio(
    "Metode mana yang ingin Anda gunakan untuk menghitung kemiripan parfum?",
    options=["Jaccard", "Cosine"],
    horizontal=True
)

# Form input
st.markdown("### 🔍 Masukkan Preferensi Anda")
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox(
        "Untuk siapa parfum ini? 👩🏻‍🤝‍👨🏽",
        options=['wanita', 'pria', 'unisex']
    )

with col2:
    time_usage = st.selectbox(
        "Waktu penggunaan parfum ⏱️",
        options=['siang', 'malam', 'siang dan malam']
    )

description = st.text_input(
    "Deskripsi aroma yang diinginkan ✍️",
    placeholder="Contoh: Saya ingin parfum lokal yang beraroma fruity"
)

exclusions = st.text_input(
    "Pengecualian Aroma 🚫",
    placeholder="Contoh: Jangan ada wangi vanilla"
)

if st.button("Dapatkan Rekomendasi"):
    if not description:
        st.warning("⚠️ Silakan deskripsikan parfum yang Anda inginkan")
    else:
        with st.spinner('🔍 Mencari rekomendasi terbaik untuk Anda...'):
            if similarity_method == "Jaccard":
                recommender = recommender_jaccard
                similarity_label = "Skor kesamaan Jaccard"

                recommendations = recommender.get_recommendations(
                gender=gender,
                time_usage=time_usage,
                description=description,
                exclusions=exclusions
                )

                if recommendations is None or recommendations.empty:
                    st.error("Maaf, tidak ditemukan rekomendasi yang sesuai 😞")
                else:
                    st.success("🎉 Berikut rekomendasi parfum untuk Anda:")
                    
                    for idx, row in recommendations.iterrows():
                        with st.expander(f"✨️{row['Brand']} - {row['Perfume Name']} ({similarity_label}: {row['similarity']:.4f})"):
                            st.markdown(f"""
                            - **Gender:** {row['Gender'].capitalize()}
                            - **Rating:** {row['Rating']}
                            - **Waktu Penggunaan:** {row['Time Usage'].capitalize()}
                            - **Olfactory Family:** {row['Olfactory Family']}
                            - **Top Notes:** {row['Top Notes']}
                            - **Middle Notes:** {row['Middle Notes']}
                            - **Base Notes:** {row['Base Notes']}
                            - **Negara:** {row['Negara']}
                            """)

            elif similarity_method == "Cosine":
                recommender = recommender_cosine
                similarity_label = "Skor kesamaan Cosine"
 
                recommendations = recommender.recommend(
                gender=gender,
                time_usage=time_usage,
                description=description,
                exclusion=exclusions
                )

                if recommendations is None or recommendations.empty:
                    st.error("Maaf, tidak ditemukan rekomendasi yang sesuai 😞")
                else:
                    st.success("🎉 Berikut rekomendasi parfum untuk Anda:")
                    
                    for idx, row in recommendations.iterrows():
                        with st.expander(f"✨️{row['Brand']} - {row['Perfume Name']} ({similarity_label}: {row['similarity']:.4f})"):
                            st.markdown(f"""
                            - **Gender:** {row['Gender'].capitalize()}
                            - **Rating:** {row['Rating']}
                            - **Waktu Penggunaan:** {row['Time Usage'].capitalize()}
                            - **Olfactory Family:** {row['Olfactory Family']}
                            - **Top Notes:** {row['Top Notes']}
                            - **Middle Notes:** {row['Middle Notes']}
                            - **Base Notes:** {row['Base Notes']}
                            - **Negara:** {row['Negara']}
                            """)
