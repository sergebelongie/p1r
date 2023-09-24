import plotly.express as px
import requests
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

KEYWORD_URL = (
    "https://raw.githubusercontent.com/sergebelongie/p1r/main/data/member_keywords.yml"
)
LOCAL = True

if not LOCAL:
    response = requests.get(KEYWORD_URL)
    keywords = yaml.safe_load(response.text)
else:
    with open("data/member_keywords.yml", "r") as f:
        keywords = yaml.safe_load(f)

researcher_names = list(keywords.keys())
texts = list(keywords.values())

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
tfidf_matrix = vectorizer.fit_transform(texts)

# t-SNE Visualization
tsne = TSNE(n_components=2, random_state=0)
tsne_results = tsne.fit_transform(tfidf_matrix.toarray())

# Create an interactive plot using plotly
fig = px.scatter(x=tsne_results[:, 0], y=tsne_results[:, 1], text=researcher_names)
fig.update_traces(textposition="top center")
fig.update_layout(title_text="t-SNE visualization of researchers", showlegend=False)
fig.show()
