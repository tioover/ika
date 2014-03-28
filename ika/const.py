import re


base_scm = "./scm/base.scm"

float_pattern = re.compile('\d+\.\d+$')


quote = {
    "'": "quote",
    "`": "quasiquote",
    ",@": "unquote-splicing",
    ',': "unquote",
}

lex_replace = {
    "#(": ["(", "vector"],
}


token_patterns = [
    "()",
    "(",
    ")",
]
token_patterns.extend(quote.keys())
token_patterns.extend(lex_replace.keys())
token_patterns = list(map(re.escape, token_patterns))  # escape for re.
token_patterns.extend(  # complex re expr, can't escape.
    [
        r'"(\\"|[^"])*"',  # string
        r'[^(\)|"|;|\s)]+',  # name
    ]
)

remove_pattern = r"^\s+|^;.*"
