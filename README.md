<h1 align="center">detrack</h1>

<p align="center">
  <strong>Strip tracking parameters from URLs. Deterministically. Zero dependencies.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT">
  <img src="https://img.shields.io/badge/dependencies-none-brightgreen.svg" alt="no dependencies">
</p>

## Install

```bash
pip install detrack
```

## Quick start

```python
import detrack

url = "https://example.com/post?utm_source=twitter&q=python&fbclid=123"
result = detrack.clean(url)

print(result.url)
# "https://example.com/post?q=python"

print(result.removed_params)
# {"utm_source": "twitter", "fbclid": "123"}

print(result.cleaned_params)
# {"q": "python"}
```

## Why detrack?

Other URL cleaners do too much (host remapping, site-specific rules, semantic rewriting), while `detrack` does one thing and does it well: remove tracking parameters. 

This makes `detrack` predictable, testable, and trivial to integrate.

## Examples

### Basic

```python
>>> detrack.clean("https://example.com?utm_source=twitter&q=python")
DetrackResult(url="https://example.com?q=python", cleaned_params={"q": "python"},
              removed_params={"utm_source": "twitter"})
```

### Multiple trackers stripped

```python
>>> detrack.clean("https://example.com?a=1&utm_source=x&b=2&fbclid=y&c=3")
DetrackResult(url="https://example.com?a=1&b=2&c=3",
              cleaned_params={"a": "1", "b": "2", "c": "3"},
              removed_params={"utm_source": "x", "fbclid": "y"})
```

### All params stripped (query removed entirely)

```python
>>> detrack.clean("https://example.com?utm_source=x&fbclid=y")
DetrackResult(url="https://example.com",
              cleaned_params={},
              removed_params={"utm_source": "x", "fbclid": "y"})
```

### Custom patterns

```python
>>> detrack.clean("https://example.com?session=abc123&page=1", patterns=["session"])
DetrackResult(url="https://example.com?page=1",
              cleaned_params={"page": "1"},
              removed_params={"session": "abc123"})
```

### Query string only

```python
>>> detrack.clean_query("a=1&utm_source=x&b=2")
"a=1&b=2"

>>> detrack.clean_query("utm_source=x&fbclid=y")
""
```

## API

### `detrack.clean(url, patterns=None)`

Strip tracking parameters from a full URL.

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | Any URL string |
| `patterns` | `list[str] \| None` | Optional param names to strip (defaults to `DEFAULT_PATTERNS`) |

**Returns:** [`DetrackResult`](#detrackresult) -> dataclass with cleaned URL and metadata.

**Raises:** Nothing -> pure function, no exceptions.
Malformed URLs pass through unchanged. Invalid patterns are ignored.

---

### `detrack.clean_query(query, patterns=None)`

Strip tracking parameters from a query string only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | URL query string, e.g. `"a=1&utm_source=x&b=2"` |
| `patterns` | `list[str] \| None` | Optional param names to strip |

**Returns:** `str` -> cleaned query string (empty string if all params stripped).

---

### `detrack.DEFAULT_PATTERNS`

```python
frozenset[str]  # 60+ common tracking parameters
```

Covers UTM parameters, social tracking (`fbclid`, `ref`, `si`), marketing IDs
(`gclid`, `msclkid`, `wbraid`), analytics (`_ga`, `_gl`), cache busters
(`cb`, `rand`, `timestamp`), session IDs (`sid`, `phpsessid`), and redirect
params. Pass a custom `patterns` list to `clean()` to override.

---

### `DetrackResult`

```python
@dataclass
class DetrackResult:
    url: str                       # Cleaned URL
    parsed_url: SplitResult        # urllib.parse result (for further processing)
    cleaned_params: dict[str, str] # Parameters that remain
    removed_params: dict[str, str] # Stripped parameters + their original values
```

`removed_params` preserves the original values so you can log what was stripped
for analytics, debugging, or compliance.

## Features

- **60+ default patterns**: UTM, social, marketing, analytics, cache busters, session, redirect
- **Case-insensitive matching**: `UTM_SOURCE`, `Utm_Source`, and `utm_source` are all stripped
- **Zero dependencies**: uses only `urllib.parse` from the Python standard library
- **Deterministic**: same input always yields the same output, across all systems
- **Pure functions**: no state, no I/O, no random numbers, no exceptions
- **Metadata returned**: `removed_params` tells you exactly what was stripped and its original value

---

See MIT [LICENSE](LICENSE).