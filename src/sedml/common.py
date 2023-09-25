from typing import Any, Callable

from pydantic import BeforeValidator, PlainSerializer
from typing_extensions import Annotated


def try_types(*types: Callable[[str], Any]):
    def parser(x):
        x = x.strip()
        for f in types:
            try:
                return f(x)
            except Exception:
                pass

    return parser


def bool_parser(x):
    match x:
        case "1" | "true":
            return True
        case "0" | "false":
            return False
        case _:
            raise ValueError(x)


BOOL = Annotated[
    bool,
    BeforeValidator(bool_parser),
    PlainSerializer(lambda x: "true" if x else "false"),
]
INT = Annotated[int, BeforeValidator(try_types(int))]
FLOAT = Annotated[float, BeforeValidator(try_types(float))]
FLOAT_BOOL_STR = Annotated[
    float | bool | str, BeforeValidator(try_types(float, bool_parser, str))
]


# letter ::= ’a’..’z’,’A’..’Z’ digit ::= ’0’..’9’ idChar ::= letter | digit | ’ ’ SId ::= ( letter | ’ ’ ) idChar*
