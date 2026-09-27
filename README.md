# code-formatter

A CLI that prettifies code. It prefers real, deterministic formatters
(never changes logic, only style) and only falls back to a local LLM for
languages that have no formatter available.

## How it picks a formatter

| Extension(s) | Formatter | Requires |
|---|---|---|
| `.rs` | [`rustfmt`](https://github.com/rust-lang/rustfmt) | `rustfmt` on `PATH` |
| `.py` | [`black`](https://github.com/psf/black) | `black` on `PATH` (e.g. `pip install black`) |
| `.js` `.jsx` `.ts` `.tsx` `.json` `.css` `.scss` `.less` `.html` `.vue` `.md` `.markdown` `.yaml` `.yml` `.graphql` | [`prettier`](https://prettier.io) via `npx` | `npx`/Node.js |
| anything else | a local LLM | [Ollama](https://ollama.com) running, with a model pulled |

If the real formatter for a language isn't installed, or it rejects the
input (e.g. genuinely broken/unparseable syntax, not just messy
indentation), it falls back to the LLM automatically.

Because the LLM works by regenerating the code rather than rearranging
whitespace, it will often also repair small structural breakage along the
way (an unclosed HTML tag, a missing colon) instead of just erroring out
like a real formatter would. This isn't a guaranteed feature — it's not
verified or deterministic the way `rustfmt`/`black`/`prettier` are, so
don't rely on it as a linter or repair tool, especially with `-i`.

## Requirements

- Python 3
- At least one of `rustfmt`, `black`, or `npx` — only needed for the
  languages they cover; the tool skips straight to the LLM for anything
  missing
- [Ollama](https://ollama.com) running locally (`ollama serve`) with a
  code-capable model pulled, for languages with no dedicated formatter.
  Set `OLLAMA_MODEL` at the top of `formatter.py` to whichever model you
  have (a coding-tuned model, e.g. `qwen2.5-coder`, works best)

## Setup

```bash
git clone <this-repo>
cd code-formatter
pip install -r requirements.txt   # installs black globally
```

## Usage

```bash
# format a file, print result to stdout
python3 formatter.py file.js

# format a file in place (overwrites it)
python3 formatter.py file.py -i

# format code from stdin -- no filename, so pass --lang explicitly
cat messy.go | python3 formatter.py --lang go
```

On macOS/Linux, `formatter.py` is also executable directly (`./formatter.py file.js`).

## scripts/

- `scripts/download_model.sh` — pulls whatever model `formatter.py` is
  configured to use (reads `OLLAMA_MODEL` directly, so it never drifts out
  of sync with the code). Requires Ollama installed.
- `scripts/add_alias.sh` (Linux/macOS) — adds a `format` alias to
  `~/.bashrc` so you can run `format file.py` from anywhere. Safe to
  re-run; it skips if the alias already exists.
- `scripts/add_alias.bat` (Windows) — cmd has no `.bashrc` equivalent, so
  this creates a `format.bat` shim in `scripts/` and adds that folder to
  your user `PATH`. Run once, open a new cmd window, then `format file.py`
  works the same way.

## Test

```bash
python3 test_formatter.py
```
