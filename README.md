# Article notes with imread

A small, working example for turning one public web article into a Markdown research note while keeping its source. It contains a Python script, a manual reading workflow, and checks for incomplete extraction.

Maintained for [imread](https://imread.org/). This is an affiliated example, not an independent product review. The script uses imread's public extraction API and is not a local HTML parser.

## Save your first note

You need Python 3.9 or later. The script uses only Python's standard library; there are no packages to install and no API key to configure.

Download this repository, open a terminal in its folder, and run:

```sh
python save_article.py "https://paulgraham.com/greatwork.html" "notes/great-work.md"
```

Replace the URL with an article you are allowed to access. On Windows, `py` may be the Python launcher available on your machine. Use `python3` if that is your installation's command.

The script makes one request and saves a new UTF-8 Markdown file. It keeps:

- the source URL you requested;
- a UTC retrieval time;
- a SHA-256 fingerprint of the extracted response;
- a separate space for your own notes;
- the extracted article, including the source attribution returned by the service.

It refuses to overwrite an existing file. Give a new filename when you want to compare another retrieval. The `notes/` folder is ignored by Git so downloaded articles are not accidentally included in a repository commit.

The fingerprint identifies the exact response you saved. It does not prove that the extraction is accurate, that the publisher has not changed the page, or that you have permission to republish it.

## Check the result before using it

Open the original page and your note together. Check the title, an early paragraph, a late paragraph, and every passage you plan to quote. If the article has a table, code block, caption, or correction notice, compare that part too.

Do not invent missing authors or publication dates. Add them to your own source record only after checking the publisher's page. Keep your commentary under **My notes**, separate from the extracted text.

For a workflow without Python, follow [the browser guide](browser-workflow.md). The same source checks apply when copying into a note-taking app.

## What the example handles

The caller URL-encodes the source address, checks HTTP errors and response type, and stops on an empty or oversized response. It also refuses to label a response with imread's continuation marker as a complete note. It makes no automatic retries or background requests.

The [API documentation](https://imread.org/docs/api) explains plain text, JSON, bounded parts, errors, rate limits, and the MCP interface. For very long articles, use its returned continuation offset rather than guessing where the next part starts. This small example deliberately saves a complete Markdown response in one request.

## Limits and privacy

- This fetches a public page through a remote service. Do not put private URLs, access tokens, or confidential documents into the request.
- Login-required, blocked, or heavily JavaScript-dependent pages can fail. The example does not bypass access restrictions.
- A clean extraction can still omit meaning-bearing material. Compare it with the original before quoting or summarizing.
- The service is free and has operational limits; it is not an uptime guarantee. Respect `429` responses rather than adding rapid retries.
- imread's optional listening and translation features may send text to additional providers. This script only calls article extraction. Read the current [privacy information](https://imread.org/privacy).
- Downloading for research does not grant republication rights. This repository contains no copy of the example essay.

## Verification

On 2026-11-01, the published script was run against the public essay used above. It saved a complete Markdown note with source metadata. A second run to the same path was rejected without overwriting the note. An invalid URL was rejected before a request, and an HTTP error did not create a note. See [verification notes](verification.md) for the observed results and limits.
