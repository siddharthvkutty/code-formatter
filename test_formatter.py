#!/usr/bin/env python3
"""Self-check for formatter.py -- run with `python3 test_formatter.py`."""
import formatter as fmt


def test_detect_language():
    assert fmt.detect_language("main.rs") == ".rs"
    assert fmt.detect_language("README") == ""
    assert fmt.detect_language("a.b.py") == ".py"
    assert fmt.detect_language("Dockerfile") == ""


def test_strip_code_fence():
    assert fmt.strip_code_fence("```python\nx = 1\n```") == "x = 1\n"
    assert fmt.strip_code_fence("x = 1") == "x = 1"
    assert fmt.strip_code_fence("```\ny=2\n```\n") == "y=2\n"


def test_prettify_dispatch_order():
    fmt.format_with_rustfmt = lambda code: "RUSTFMT\n"
    fmt.format_with_black = lambda code: "BLACK\n"
    fmt.format_with_prettier = lambda code, ext: "PRETTIER\n"
    fmt.format_with_llm = lambda code, ext: "LLM\n"
    assert fmt.prettify("code", ".rs") == "RUSTFMT\n"

    fmt.format_with_rustfmt = lambda code: None
    assert fmt.prettify("code", ".py") == "BLACK\n"

    fmt.format_with_black = lambda code: None
    assert fmt.prettify("code", ".js") == "PRETTIER\n"

    fmt.format_with_prettier = lambda code, ext: None
    assert fmt.prettify("code", ".go") == "LLM\n"


if __name__ == "__main__":
    test_detect_language()
    test_strip_code_fence()
    test_prettify_dispatch_order()
    print("all tests passed")
