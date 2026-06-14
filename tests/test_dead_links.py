import re
from pathlib import Path

LOCAL_MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def test_local_markdown_links_point_to_existing_files() -> None:
    missing_links: list[str] = []
    for markdown_path in _markdown_files():
        for link in LOCAL_MARKDOWN_LINK.findall(
            markdown_path.read_text(encoding="utf-8")
        ):
            target = link.split("#", maxsplit=1)[0]
            if not target or _is_external_link(target):
                continue
            target_path = (markdown_path.parent / target).resolve()
            if not target_path.exists():
                missing_links.append(f"{markdown_path}: {link}")

    assert missing_links == []


def _markdown_files() -> tuple[Path, ...]:
    return tuple(
        path
        for path in Path(".").glob("**/*.md")
        if ".git" not in path.parts
    )


def _is_external_link(link: str) -> bool:
    return link.startswith(("http://", "https://", "mailto:"))
