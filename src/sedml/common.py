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

    return BeforeValidator(parser)


BOOL = Annotated[bool, PlainSerializer(lambda x: "true" if x else "false")]
INT = Annotated[int, try_types(int)]
FLOAT = Annotated[float, try_types(float)]


# letter ::= ’a’..’z’,’A’..’Z’ digit ::= ’0’..’9’ idChar ::= letter | digit | ’ ’ SId ::= ( letter | ’ ’ ) idChar*
