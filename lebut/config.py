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


class _GH_REPO:
    URL = "https://github.com/obestwalter/obestwalter.github.io"
    CONTENT = f"{URL}/lektor-sources/content"
    ARTICLES = f"{CONTENT}/{NAME.ARTICLES}"
    ISSUES = f"{URL}/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc"
    LICENSE = f"{CONTENT}/LICENSE"


class _GL_REPO:
    URL = "https://gitlab.com/obestwalter/tmp_website_private"
    SOURCE = f"{URL}/tree/lektor-sources"
    CONTENT = f"{SOURCE}/content"
    ARTICLES = f"{CONTENT}/{NAME.ARTICLES}"
    ISSUES = f"{URL}/issues"
    LICENSE = f"{CONTENT}/LICENSE"


REPO = _GH_REPO


class LEBUT:
    REPO = REPO
    URL = URL
