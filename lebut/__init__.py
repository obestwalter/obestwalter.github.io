from pathlib import Path


class PATH:
    HERE: Path = Path(__file__).parent
    PROJECT: Path = HERE.parent
    OUTPUT: Path = PROJECT.parent / "website_build"
    DRAFTS: Path = PROJECT / "drafts"
    ARTICLES: Path = PROJECT / "content" / "articles"
