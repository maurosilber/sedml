from typing import Any, Callable

from pydantic import BeforeValidator, PlainSerializer
from pydantic_xml import BaseXmlModel
from typing_extensions import Annotated

from .xml import Element


class _BaseSEDML(BaseXmlModel):
    def __repr_str__(self, join_str: str) -> str:
        args = []
        for a, v in self.__repr_args__():
            if v is None:
                continue
            elif a is None:
                args.append(repr(v))
            else:
                args.append(f"{a}={v!r}")
        return join_str.join(args)

    def to_xml(
        self,
        *,
        skip_empty: bool = True,
        **kwargs,
    ) -> str | bytes:
        return super().to_xml(skip_empty=skip_empty, **kwargs)

    def to_xml_tree(self, *, skip_empty: bool = True) -> Element:
        return super().to_xml_tree(skip_empty=skip_empty)


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
