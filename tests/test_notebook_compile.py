from pathlib import Path

from lebut import ipynb_to_md

HERE: Path = Path(__file__).parent

def test_convert_to_markdown():
    inPath = HERE / "code.ipynb"
    outPath = inPath.with_suffix(".md")
    expectationPath = outPath.with_suffix(".expectation.md")
    if outPath.exists():
        outPath.unlink()
    output = ipynb_to_md.(inPath)
    outPath.write_text(output)
    expectation = expectationPath.read_text().strip()
    assert expectation == output
