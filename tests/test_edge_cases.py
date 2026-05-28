from detrack import clean, clean_query


def test_case_insensitivity_utm() -> None:
    for url in [
        "https://example.com?utm_source=x&q=1",
        "https://example.com?UTM_SOURCE=x&q=1",
        "https://example.com?Utm_Source=x&q=1",
        "https://example.com?utm_SOURCE=x&q=1",
    ]:
        result = clean(url)
        assert result.url == "https://example.com?q=1", f"Failed for {url}"
        assert "utm_source" in result.removed_params or "UTM_SOURCE" in result.removed_params or "Utm_Source" in result.removed_params or "utm_SOURCE" in result.removed_params


def test_case_insensitivity_fbclid() -> None:
    for url in [
        "https://example.com?fbclid=x&q=1",
        "https://example.com?FBCLID=x&q=1",
        "https://example.com?Fbclid=x&q=1",
    ]:
        result = clean(url)
        assert result.url == "https://example.com?q=1", f"Failed for {url}"


def test_empty_values_preserved_for_non_tracking() -> None:
    result = clean("https://example.com?a=&b=2")
    assert result.url == "https://example.com?a=&b=2"
    assert result.removed_params == {}


def test_empty_values_removed_for_tracking() -> None:
    result = clean("https://example.com?utm_source=&b=2")
    assert result.url == "https://example.com?b=2"
    assert result.removed_params == {"utm_source": ""}


def test_duplicate_params_all_removed() -> None:
    result = clean("https://example.com?utm_source=x&utm_source=y&a=1")
    assert result.url == "https://example.com?a=1"
    assert result.removed_params == {"utm_source": "y"}


def test_url_without_scheme() -> None:
    result = clean("//example.com/page?utm_source=x")
    assert "utm_source" not in result.url


def test_url_with_port() -> None:
    result = clean("https://example.com:8080/page?utm_source=x&q=1")
    assert result.url == "https://example.com:8080/page?q=1"


def test_url_with_auth() -> None:
    result = clean("https://user:pass@example.com/page?utm_source=x&q=1")
    assert result.url == "https://user:pass@example.com/page?q=1"


def test_only_tracking_params_different_cases() -> None:
    result = clean("https://example.com?UTM_CAMPAIGN=spring&utm_medium=email&q=1")
    assert result.url == "https://example.com?q=1"


def test_no_changes_with_no_tracking() -> None:
    url = "https://example.com/search?q=python&page=2"
    result = clean(url)
    assert result.url == url
    assert result.cleaned_params == {"q": "python", "page": "2"}
    assert result.removed_params == {}


def test_query_only_function_with_mixed() -> None:
    assert clean_query("a=1&utm_source=x&b=2") == "a=1&b=2"


def test_query_only_all_tracking() -> None:
    assert clean_query("utm_source=x&fbclid=y") == ""


def test_query_only_empty() -> None:
    assert clean_query("") == ""


def test_query_only_no_tracking() -> None:
    assert clean_query("a=1&b=2") == "a=1&b=2"
