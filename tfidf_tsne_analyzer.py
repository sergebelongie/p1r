import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import plotly.express as px

# GitHub API endpoint to list files in the 'profiles' directory of your repo
api_url = "https://api.github.com/repos/sergebelongie/p1r/contents/profiles"

response = requests.get(api_url)

texts = []
researcher_names = []

if response.status_code == 200:
    files = response.json()
    txt_files = [file['name'] for file in files if file['name'].endswith('.txt')]
    
    # Base URL for the raw content of files in the GitHub repository
    base_url = "https://raw.githubusercontent.com/sergebelongie/p1r/main/profiles/"
    
    for file_name in txt_files:
        file_response = requests.get(base_url + file_name)
        
        if file_response.status_code == 200:
            content = file_response.text
            texts.append(content)
            researcher_names.append(file_name.replace(".txt", "").replace("_", " "))
        else:
            print(f"Failed to fetch data for {file_name}")

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    # t-SNE Visualization
    tsne = TSNE(n_components=2, random_state=0)
    tsne_results = tsne.fit_transform(tfidf_matrix.toarray())

    # Create an interactive plot using plotly
    fig = px.scatter(x=tsne_results[:, 0], y=tsne_results[:, 1], text=researcher_names)
    fig.update_traces(textposition='top center')
    fig.update_layout(title_text="t-SNE visualization of researchers", showlegend=False)
    fig.show()
else:
    print("Failed to fetch file list from GitHub.")
