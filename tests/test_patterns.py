from detrack import DEFAULT_PATTERNS


def test_default_patterns_count() -> None:
    assert len(DEFAULT_PATTERNS) >= 60, (
        f"DEFAULT_PATTERNS has {len(DEFAULT_PATTERNS)} items, expected >= 60"
    )


def test_utm_params_present() -> None:
    utm = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
           "utm_id", "utm_cid", "utm_reader", "utm_viz", "utm_pubreferrer",
           "utm_nooverride"}
    assert utm.issubset(DEFAULT_PATTERNS), (
        f"Missing UTM params: {utm - DEFAULT_PATTERNS}"
    )


def test_social_params_present() -> None:
    social = {"fbclid", "ref", "source", "si", "sns", "social", "origin"}
    assert social.issubset(DEFAULT_PATTERNS), (
        f"Missing social params: {social - DEFAULT_PATTERNS}"
    )


def test_marketing_params_present() -> None:
    marketing = {"gclid", "gclsrc", "dclid", "msclkid", "wbraid", "gbraid",
                 "mc_cid", "mc_eid", "trk", "vero_conv", "vero_id",
                 "email", "recipient", "campaign_id", "newsletter", "mbid"}
    assert marketing.issubset(DEFAULT_PATTERNS), (
        f"Missing marketing params: {marketing - DEFAULT_PATTERNS}"
    )


def test_analytics_params_present() -> None:
    analytics = {"_ga", "_gl", "_ke", "_hsenc"}
    assert analytics.issubset(DEFAULT_PATTERNS), (
        f"Missing analytics params: {analytics - DEFAULT_PATTERNS}"
    )


def test_cache_busters_present() -> None:
    cache = {"_", "cb", "cache", "nocache", "rand", "random", "r", "ts", "_t",
             "timestamp"}
    assert cache.issubset(DEFAULT_PATTERNS), (
        f"Missing cache buster params: {cache - DEFAULT_PATTERNS}"
    )


def test_session_params_present() -> None:
    session = {"session_id", "sid", "phpsessid", "jsessionid", "view_id", "visit_id"}
    assert session.issubset(DEFAULT_PATTERNS), (
        f"Missing session params: {session - DEFAULT_PATTERNS}"
    )


def test_redirect_params_present() -> None:
    redirect = {"redirect_to", "return_to", "next", "continue"}
    assert redirect.issubset(DEFAULT_PATTERNS), (
        f"Missing redirect params: {redirect - DEFAULT_PATTERNS}"
    )
