# Verification notes

Checked on 2026-11-01 with Python and the live extraction endpoint. These are observations from one example, not a benchmark or a promise that every website works.

| Check | Observed result |
| --- | --- |
| Run `save_article.py` with the public essay linked in the README | Exit 0; 67,079 extracted characters; note contains the source URL, retrieval time, response fingerprint, a separate notes section and the article title |
| Run again with the same output filename | Exit 2; existing file unchanged |
| Supply a `file:` address | Exit 2 before an API request; no note created |
| Supply a malformed bracketed URL | Exit 2 with a readable argument error; no note created |
| Request an article on the reserved `example.invalid` domain | Service returned HTTP 422; caller exited 1 and did not create a note |

The downloaded essay was used only for verification and is not included in this repository. The public example contains original instructions and code.

Not covered: every source-page layout, pagination through an entire long document, a strict comparison of every extracted paragraph, load testing, all operating systems/Python versions, translation/audio, and automatic validation of the Markdown guides or `.gitignore`. Read the current API documentation and compare your own result with its original source.
