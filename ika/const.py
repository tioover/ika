import re

quote = {
    "'": "quote",
    "`": "quasiquote",
    ",@": "unquote-splicing",
    ',': "unquote",
}


replace = {
    "#(": ["(", "vector"],
}


token_patterns = [
    "()",
    "(",
    ")",
]
token_patterns.extend(quote.keys())
token_patterns.extend(replace.keys())
token_patterns = list(map(re.escape, token_patterns))  # escape for re.
token_patterns.extend(  # complex re expr, can't escape.
    [
        r'"(\\"|[^"])*"',  # string
        r'[^(\)|"|;|\s)]+',  # name
    ]
)

remove_pattern = r"^\s+|^;.*"
