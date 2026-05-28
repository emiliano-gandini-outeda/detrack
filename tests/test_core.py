from detrack import DetrackResult, clean, clean_query


def test_clean_basic() -> None:
    result = clean("https://example.com/post?utm_source=twitter&q=python")
    assert result.url == "https://example.com/post?q=python"
    assert result.cleaned_params == {"q": "python"}
    assert result.removed_params == ["utm_source"]


def test_clean_multiple_trackers() -> None:
    result = clean("https://example.com?a=1&utm_source=x&b=2&fbclid=y&c=3")
    assert result.url == "https://example.com?a=1&b=2&c=3"
    assert result.cleaned_params == {"a": "1", "b": "2", "c": "3"}
    assert sorted(result.removed_params) == sorted(["utm_source", "fbclid"])


def test_clean_all_stripped() -> None:
    result = clean("https://example.com?utm_source=x&fbclid=y")
    assert result.url == "https://example.com"
    assert result.cleaned_params == {}
    assert sorted(result.removed_params) == sorted(["utm_source", "fbclid"])


def test_clean_custom_patterns() -> None:
    result = clean("https://example.com?session=abc123&page=1", patterns=["session"])
    assert result.url == "https://example.com?page=1"
    assert result.cleaned_params == {"page": "1"}
    assert result.removed_params == ["session"]


def test_clean_preserves_fragment() -> None:
    result = clean("https://example.com/page?utm_source=x#section")
    assert result.url == "https://example.com/page#section"
    assert result.removed_params == ["utm_source"]


def test_clean_no_query() -> None:
    result = clean("https://example.com/page")
    assert result.url == "https://example.com/page"
    assert result.cleaned_params == {}
    assert result.removed_params == []


def test_clean_empty_url() -> None:
    result = clean("")
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == []


def test_clean_malformed_url() -> None:
    result = clean("http:///example.com")
    assert result.removed_params == []


def test_clean_query_basic() -> None:
    result = clean_query("a=1&utm_source=x&b=2")
    assert result == "a=1&b=2"


def test_clean_query_all_stripped() -> None:
    result = clean_query("utm_source=x&fbclid=y")
    assert result == ""


def test_clean_query_empty() -> None:
    assert clean_query("") == ""


def test_clean_query_no_trackers() -> None:
    assert clean_query("a=1&b=2") == "a=1&b=2"


def test_clean_query_custom_patterns() -> None:
    result = clean_query("session=abc&page=1", patterns=["session"])
    assert result == "page=1"


def test_detrack_result_fields() -> None:
    result = clean("https://example.com/p?utm_source=x")
    assert isinstance(result, DetrackResult)
    assert hasattr(result, "url")
    assert hasattr(result, "parsed_url")
    assert hasattr(result, "cleaned_params")
    assert hasattr(result, "removed_params")
