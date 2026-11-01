#!/usr/bin/env python3
"""Save one public article as a Markdown note with a source record."""

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


API_URL = "https://imread.org/api/extract"
MAX_RESPONSE_BYTES = 8 * 1024 * 1024


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Public HTTP(S) article URL")
    parser.add_argument("output", type=Path, help="New Markdown file; never overwritten")
    args = parser.parse_args()
    try:
        source = urlsplit(args.url)
    except ValueError:
        parser.error("The source URL is malformed.")
    if (
        source.scheme not in {"http", "https"}
        or not source.netloc
        or source.username
        or any(char in args.url for char in "\r\n<>")
    ):
        parser.error("Use a public HTTP(S) URL without embedded credentials.")
    if args.output.exists():
        parser.error(f"Output already exists: {args.output}")

    request = Request(
        API_URL + "?" + urlencode({"url": args.url, "format": "markdown"}),
        headers={"Accept": "text/markdown", "User-Agent": "imread-article-notes/1.0"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            content_type = response.headers.get_content_type()
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as error:
        message = error.read(400).decode("utf-8", errors="replace").strip()
        print(f"Extraction failed (HTTP {error.code}): {message}", file=sys.stderr)
        return 1
    except (URLError, TimeoutError) as error:
        print(f"Could not reach the extraction service: {error}", file=sys.stderr)
        return 1

    if len(raw) > MAX_RESPONSE_BYTES:
        print("Response exceeds this example's 8 MiB limit; no note was saved.", file=sys.stderr)
        return 1
    if content_type not in {"text/markdown", "text/plain"}:
        print(f"Unexpected response type: {content_type}; no note was saved.", file=sys.stderr)
        return 1
    try:
        article = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("The response is not valid UTF-8; no note was saved.", file=sys.stderr)
        return 1
    if not article.strip():
        print("The service returned an empty article; no note was saved.", file=sys.stderr)
        return 1
    if re.search(r"\[The article goes on:.*offset=\d+.*\]\s*$", article, re.DOTALL):
        print("The response is only one part. Follow the API pagination instructions before saving a complete note.", file=sys.stderr)
        return 1

    accessed = datetime.now(timezone.utc).isoformat(timespec="seconds")
    fingerprint = hashlib.sha256(raw).hexdigest()
    note = (
        "# Article note\n\n"
        f"- Source requested: <{args.url}>\n"
        f"- Retrieved (UTC): {accessed}\n"
        "- Extraction service: <https://imread.org/>\n"
        f"- Extracted response SHA-256: `{fingerprint}`\n\n"
        "## My notes\n\n"
        "<!-- Add your analysis here. Check author/date on the original page. -->\n\n"
        "## Extracted article\n\n"
        + article.rstrip()
        + "\n"
    )
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8", newline="\n") as output:
            output.write(note)
    except OSError as error:
        print(f"Could not save the note: {error}", file=sys.stderr)
        return 1
    print(f"Saved {len(article):,} extracted characters to {args.output}")
    print("Compare the result with the source before quoting or summarizing it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
