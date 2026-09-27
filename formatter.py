#!/usr/bin/env python3
"""Prettify code: real formatters when available, LLM fallback otherwise."""
import argparse
import json
import shutil
import subprocess
import sys
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:14b"

# Extensions prettier (via npx, no install needed) can already handle.
PRETTIER_EXTS = {
    ".js", ".jsx", ".ts", ".tsx", ".json", ".css", ".scss", ".less",
    ".html", ".vue", ".md", ".markdown", ".yaml", ".yml", ".graphql",
}


def detect_language(filename):
    """Return the file extension (lowercase, with dot), or '' if none."""
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[1].lower()


def format_with_rustfmt(code):
    if not shutil.which("rustfmt"):
        return None
    result = subprocess.run(
        ["rustfmt", "--emit=stdout", "--quiet"],
        input=code, capture_output=True, text=True,
    )
    return result.stdout if result.returncode == 0 else None


def format_with_prettier(code, ext):
    if not shutil.which("npx"):
        return None
    result = subprocess.run(
        ["npx", "--yes", "prettier", "--stdin-filepath", f"file{ext}"],
        input=code, capture_output=True, text=True,
    )
    return result.stdout if result.returncode == 0 else None


def strip_code_fence(text):
    """Strip a single markdown code fence wrapping the whole response, if present."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines) + "\n"
    return text


def format_with_llm(code, ext):
    lang_hint = ext.lstrip(".") or "code"
    prompt = (
        f"Reformat the following {lang_hint} code to follow standard style "
        "conventions. Do not change logic, behavior, names, or comments -- "
        "only whitespace, indentation, and line breaks. "
        "Output ONLY the reformatted code, no explanation, no markdown fences.\n\n"
        f"{code}"
    )
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0},
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.load(resp)
    except Exception as e:
        raise RuntimeError(
            f"Ollama request failed ({e}). Is `ollama serve` running?"
        ) from e
    return strip_code_fence(data["response"])


def prettify(code, ext):
    """Real formatter first (deterministic, never changes logic); LLM only as fallback."""
    if ext == ".rs":
        out = format_with_rustfmt(code)
        if out is not None:
            return out
    if ext in PRETTIER_EXTS:
        out = format_with_prettier(code, ext)
        if out is not None:
            return out
    return format_with_llm(code, ext)


def main():
    parser = argparse.ArgumentParser(description="Prettify badly formatted code.")
    parser.add_argument("file", nargs="?", help="file to format (default: stdin)")
    parser.add_argument("-i", "--in-place", action="store_true", help="edit file in place")
    parser.add_argument("--lang", help="extension hint when reading from stdin, e.g. py")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            code = f.read()
        ext = detect_language(args.file)
    else:
        code = sys.stdin.read()
        ext = ("." + args.lang.lstrip(".")) if args.lang else ""

    result = prettify(code, ext)

    if args.in_place:
        if not args.file:
            sys.exit("error: --in-place requires a file argument")
        with open(args.file, "w") as f:
            f.write(result)
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
