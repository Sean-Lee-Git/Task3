from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "index.html",
    "app.html",
    "requirements.txt",
    ".gitignore",
    ".github/workflows/deploy-huggingface.yml",
]
REQUIRED_APP_TEXT = [
    "getUserMedia",
    "AudioContext",
    "createAnalyser",
    "Export CSV",
    "How it works",
    "Microphone permission was denied",
]


class AppHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = 0
        self.canvases = 0
        self.buttons = 0

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.scripts += 1
        elif tag == "canvas":
            self.canvases += 1
        elif tag == "button":
            self.buttons += 1


def assert_required_files_exist() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).exists()]
    if missing:
        raise AssertionError(f"Missing required files: {', '.join(missing)}")


def assert_readme_front_matter() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = ["sdk: static", "app_file: index.html", "Live Space URL", "Data and model"]
    missing = [text for text in required if text not in readme]
    if missing:
        raise AssertionError(f"README is missing: {', '.join(missing)}")


def assert_app_contains_required_features() -> None:
    app = (ROOT / "index.html").read_text(encoding="utf-8")
    missing = [text for text in REQUIRED_APP_TEXT if text not in app]
    if missing:
        raise AssertionError(f"index.html is missing: {', '.join(missing)}")

    parser = AppHtmlParser()
    parser.feed(app)
    if parser.scripts < 1 or parser.canvases < 1 or parser.buttons < 4:
        raise AssertionError("index.html must include script, canvas, and interactive controls")


def main() -> None:
    assert_required_files_exist()
    assert_readme_front_matter()
    assert_app_contains_required_features()
    print("Static app verification passed.")


if __name__ == "__main__":
    main()