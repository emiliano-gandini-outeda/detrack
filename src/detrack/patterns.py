DEFAULT_PATTERNS = frozenset({
    # UTM
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_cid", "utm_reader", "utm_viz", "utm_pubreferrer",
    "utm_nooverride",
    # Social
    "fbclid", "ref", "source", "si", "sns", "social", "origin",
    # Marketing / Ad
    "gclid", "gclsrc", "dclid", "msclkid", "wbraid", "gbraid",
    "mc_cid", "mc_eid", "trk", "vero_conv", "vero_id",
    "email", "recipient", "campaign_id", "newsletter", "mbid",
    # Analytics
    "_ga", "_gl", "_ke", "_hsenc",
    # Cache busters
    "_", "cb", "cache", "nocache", "rand", "random", "r", "ts", "_t",
    "timestamp",
    # Session / visit
    "session_id", "sid", "phpsessid", "jsessionid", "view_id", "visit_id",
    # Redirect
    "redirect_to", "return_to", "next", "continue",
    # Misc / platform-specific
    "yclid", "igshid", "_openstat", "oft_id", "wt_mc", "mtm_source",
    "mtm_medium", "mtm_campaign", "mtm_keyword", "mtm_content",
})
