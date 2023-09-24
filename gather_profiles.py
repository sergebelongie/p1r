import csv
import re
from functools import partial

import yaml
from scholarly import scholarly as sch

AUTHOR_FILE = "data/authors_data.csv"
OUTPUT_FILE = "data/extended_data.yml"
SECTIONS = ["basics", "publications"]
PUB_FIELDS = ["title", "pub_year", "author", "journal", "abstract"]


def schid_from_url(url):
    """Extracts the scholar ID from a URL."""
    match = re.search(r"user=([^&]+)", url)
    return match.group(1) if match else None


def build_ids(author_file):
    """Builds a list of scholar IDs from a CSV file."""
    with open(author_file, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header line
        ids = [schid_from_url(row[-1]) for row in reader]
        return [id for id in ids if id is not None]


def format_pub(pub):
    """Formats a publication for YAML output."""
    author_pub_id = pub["author_pub_id"]
    return (author_pub_id, {field: pub["bib"].get(field, "") for field in PUB_FIELDS})


def format_author(author, pubs):
    """Formats extended author info for YAML output."""
    return {
        author["name"]: {
            "id": author.get("scholar_id", ""),
            "affiliation": author.get("affiliation", ""),
            "interests": author.get("interests", []),
            "publications": pubs,
        }
    }


fill_by_cites = partial(sch.fill, sections=SECTIONS, publication_limit=5)
fill_by_year = partial(sch.fill, sections=SECTIONS, sortby="year", publication_limit=5)
with open(OUTPUT_FILE, "a+") as f:
    for id in build_ids(AUTHOR_FILE):
        author_details = fill_by_cites(sch.search_author_id(id))
        pubs_by_cites = author_details["publications"]
        pubs_by_year = fill_by_year(sch.search_author_id(id))["publications"]

        pubs_by_cites = dict(format_pub(sch.fill(pub)) for pub in pubs_by_cites)
        pubs_by_year = dict(format_pub(sch.fill(pub)) for pub in pubs_by_year)
        pubs = {**pubs_by_cites, **pubs_by_year}  # De-duplicate

        content = format_author(author_details, pubs)
        yaml.safe_dump(content, f, default_style="", allow_unicode=True)
