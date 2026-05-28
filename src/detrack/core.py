from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.parse import SplitResult

from detrack.patterns import DEFAULT_PATTERNS


@dataclass
class DetrackResult:
    url: str
    parsed_url: SplitResult
    cleaned_params: dict[str, str]
    removed_params: dict[str, str]


def _filter_pairs(
    query: str,
    patterns: list[str] | None = None,
) -> tuple[list[tuple[str, str]], dict[str, str]]:
    patterns_set = frozenset(p.lower() for p in (patterns or list(DEFAULT_PATTERNS)))
    pairs = parse_qsl(query, keep_blank_values=True)
    cleaned: list[tuple[str, str]] = []
    removed: dict[str, str] = {}
    for key, val in pairs:
        if key.lower() in patterns_set:
            removed[key] = val
        else:
            cleaned.append((key, val))
    return cleaned, removed


def clean_query(query: str, patterns: list[str] | None = None) -> str:
    cleaned, _ = _filter_pairs(query, patterns)
    return urlencode(cleaned, doseq=True)


def clean(url: str, patterns: list[str] | None = None) -> DetrackResult:
    try:
        parsed = urlsplit(url)
        if not parsed.query:
            return DetrackResult(
                url=url,
                parsed_url=parsed,
                cleaned_params={},
                removed_params={},
            )
        cleaned_pairs, removed = _filter_pairs(parsed.query, patterns)
        cleaned_qs = urlencode(cleaned_pairs, doseq=True)
        cleaned_dict = dict(cleaned_pairs)
        new_url = urlunsplit((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            cleaned_qs,
            parsed.fragment,
        ))
        return DetrackResult(
            url=new_url,
            parsed_url=parsed,
            cleaned_params=cleaned_dict,
            removed_params=removed,
        )
    except Exception:
        return DetrackResult(
            url=url,
            parsed_url=urlsplit(""),
            cleaned_params={},
            removed_params=[],
        )
