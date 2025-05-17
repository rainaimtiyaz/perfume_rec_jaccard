import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
class PerfumeRecommenderCosine:
    def __init__(self, data):
        if isinstance(data, str):
            self.df = pd.read_csv(data)
        else:
            self.df = data.copy()
 
        self.df['Negara'] = self.df['Negara'].str.lower()
        self.country_list = self.df['Negara'].dropna().unique().tolist()
        self.vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(', '))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Combined_Features'])
        self.keywords = self._extract_all_keywords()
 
    def _extract_all_keywords(self):
        all_keywords = set()
        for text in self.df['Combined_Features']:
            all_keywords.update(text.split(', '))
        return {kw.lower() for kw in all_keywords}
 
    def _preprocess_text(self, text):
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()
 
    def _extract_keywords_from_text(self, text):
        text = self._preprocess_text(text)
        if 'lokal' in text or 'indo' in text:
            text += ' indonesia'
        matched = [kw for kw in self.keywords if kw in text]
        return matched
 
    def _extract_country_from_text(self, text):
        text = self._preprocess_text(text)
        for country in self.country_list:
            if country in text:
                return country
        return None
 
    def _extract_rating_filter(self, text):
        rating_filter = None
        rating_above = re.search(r'rating\w*\s*(?:di\s*)?(?:atas|lebih\s*dari|>)\s*([\d.]+)', text)
        rating_below = re.search(r'rating\w*\s*(?:di\s*)?(?:bawah|kurang\s*dari|<)\s*([\d.]+)', text)
 
        if rating_above:
            rating_filter = {'type': 'above', 'value': float(rating_above.group(1))}
        elif rating_below:
            rating_filter = {'type': 'below', 'value': float(rating_below.group(1))}
 
        return rating_filter
 
    def recommend(self, gender, time_usage, description, exclusion='', top_n=3):
        include_kw = self._extract_keywords_from_text(description)
        exclude_kw = self._extract_keywords_from_text(exclusion)
        country_filter = self._extract_country_from_text(description)
        rating_filter = self._extract_rating_filter(description)
        is_local = 'indonesia' in include_kw
 
        df_filtered = self.df[
            (self.df['Gender'].str.lower() == gender.lower()) &
            (self.df['Time Usage'].str.lower() == time_usage.lower())
        ].copy()
 
        if country_filter:
            df_filtered = df_filtered[df_filtered['Negara'].str.contains(country_filter)]
        elif is_local:
            df_filtered = df_filtered[df_filtered['Negara'].str.contains('indonesia')]
            include_kw = [kw for kw in include_kw if kw != 'indonesia']
 
        if rating_filter:
            if rating_filter['type'] == 'above':
                df_filtered = df_filtered[df_filtered['Rating'] >= rating_filter['value']]
            elif rating_filter['type'] == 'below':
                df_filtered = df_filtered[df_filtered['Rating'] <= rating_filter['value']]
 
        if df_filtered.empty or not include_kw:
            return None
 
        user_text = ', '.join(include_kw)
        user_vec = self.vectorizer.transform([user_text])
        tfidf_filtered = self.vectorizer.transform(df_filtered['Combined_Features'])
        similarities = cosine_similarity(user_vec, tfidf_filtered).flatten()
        df_filtered['similarity'] = similarities
 
        if exclude_kw:
            for word in exclude_kw:
                pattern = rf'\b{re.escape(word)}\b'
                df_filtered = df_filtered[~df_filtered['Combined_Features'].str.contains(pattern, case=False, na=False)]
 
        if df_filtered.empty:
            return None
 
        recommendations = df_filtered.sort_values(by='similarity', ascending=False).head(top_n)
 
        # return recommendations[[
        #     'Brand', 'Perfume Name', 'Negara', 'Gender', 'Time Usage',
        #     'CombinedNotes', 'Olfactory Family', 'Rating', 'similarity'
        # ]]
    
        return recommendations.head(top_n) if not recommendations.empty else None