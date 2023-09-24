import re
import string

import yaml
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

EXTENDED_FILE = "data/extended_data.yml"
OUTPUT_FILE = "data/member_keywords.yml"

# Initialize a stemmer and the list of stopwords
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))


def filtered_tokens(pub_data):
    """Returns the filtered tokens for a publication, by lowercasing, removing
    punctuation and numbers, tokenising, stemming and avoiding stopwords."""
    text = pub_data.get("title", "") + " " + pub_data.get("abstract", "")
    clean_text = re.sub(f"[{string.punctuation}0-9]", " ", text.lower())
    tokens = word_tokenize(clean_text)
    stems = set([ps.stem(w) for w in tokens if w not in stop_words])
    return " ".join(stems)


def keyword_set(member):
    """Extract stem keywords from all publications for a member."""
    pubs_data = member["publications"].values()
    keywords = [filtered_tokens(pub_data) for pub_data in pubs_data]
    return set(" ".join(keywords).strip().split(" "))


with open(EXTENDED_FILE, "r") as f:
    P1 = yaml.safe_load(f)

keywords = dict((member, " ".join(keyword_set(data))) for member, data in P1.items())

with open(OUTPUT_FILE, "w") as f:
    yaml.safe_dump(keywords, f, default_style="", allow_unicode=True)
