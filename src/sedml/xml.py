from typing import TYPE_CHECKING

try:
    from lxml.etree import _Element as Element
    from lxml.etree import fromstring  # type: ignore
except ImportError:
    from xml.etree.ElementTree import Element, fromstring


__all__ = [
    "fromstring",
    "Element",
]


if TYPE_CHECKING:

    def fromstring(text: str | bytes, /) -> Element:  # noqa
        ...
