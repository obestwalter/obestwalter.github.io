from pathlib import Path


class NAME:
    ARTICLES = "articles"
    CONTENTS = "contents.lr"
    DRAFT = "__draft__"


class PATH:
    HERE: Path = Path(__file__).parent
    PROJECT: Path = HERE.parent
    OUTPUT: Path = PROJECT.parent / "build"
    DRAFTS: Path = PROJECT / "drafts"
    CONTENT: Path = PROJECT / "content"
    ARTICLES: Path = CONTENT / "articles"


class URL:
    WEBSITE = "https://oliver.bestwalter.de"
    WEBSITE_ARTICLES = f"{WEBSITE}/{NAME.ARTICLES}"
    REPO = "https://github.com/obestwalter/obestwalter.github.io"
    REPO_CONTENT = f"{REPO}/lektor-sources/content"
    REPO_ARTICLES = f"{REPO_CONTENT}/{NAME.ARTICLES}"
