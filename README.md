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
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install black           # optional, for real Python formatting
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

## Test

```bash
python3 test_formatter.py
```
