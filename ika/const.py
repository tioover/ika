quote = {
    "'": "quote",
    "`": "quasiquote",
    ",@": "unquote-splicing",
    ',': "unquote",
}


replace = {
    "#(": ["(", "vector"],
}

token_str = list(quote.keys())
token_str.extend(replace.keys())
