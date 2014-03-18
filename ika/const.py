transfrom = {
    "'(": "quote",
    "`(": "quasiquote",
    ",@(": "unquote-splicing",
    ',(': "unquote",
    "#(": "vector",
}

from .struct import Pair
TEMP = Pair(None)  # a temp pair, simpily program struct.
