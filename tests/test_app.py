import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, highlight  # noqa: E402
from helpers import lines, sentences, substrings  # noqa: E402


def test_helpers():
    assert sorted(lines("a\nb\nc", "b\nc\nd")) == ["b", "c"]
    assert sentences("Hi there. Bye now!", "Bye now! Ok.") == ["Bye now!"]
    assert sorted(substrings("abcd", "bcde", 2)) == ["bc", "cd"]
    assert substrings("ab", "ab", 0) == []


def test_highlight_escapes_html():
    assert highlight("<b>x</b>", ["x"]) == "&lt;b&gt;<span>x</span>&lt;/b&gt;"


def _post(**form):
    data = {"file1": (io.BytesIO(b"hello world"), "a.txt"),
            "file2": (io.BytesIO(b"world peace"), "b.txt"), **form}
    return app.test_client().post("/compare", data=data, content_type="multipart/form-data")


def test_compare_routes():
    assert app.test_client().get("/").status_code == 200
    assert _post(algorithm="substrings", length="3").status_code == 200
    assert _post(algorithm="lines").status_code == 200
    assert _post(algorithm="sentences").status_code == 200
    assert _post(algorithm="substrings", length="abc").status_code == 400
    assert _post(algorithm="nope").status_code == 400
