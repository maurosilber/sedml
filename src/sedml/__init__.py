from pathlib import Path
from typing import Callable

from . import l1v1, l1v2, l1v3, l1v4, xml

readers: dict[tuple[str, str], Callable] = {
    ("1", "1"): l1v1.SEDML.from_xml_tree,
    ("1", "2"): l1v2.SEDML.from_xml_tree,
    ("1", "3"): l1v3.SEDML.from_xml_tree,
    ("1", "4"): l1v4.SEDML.from_xml_tree,
}


def read(file: Path):
    xml_tree = xml.fromstring(file.read_bytes())
    level = xml_tree.attrib["level"]
    version = xml_tree.attrib["version"]
    try:
        reader = readers[level, version]
    except KeyError:
        raise TypeError(
            f"reader for SED-ML level {level} version {version} not implemented"
        )
    else:
        return reader(xml_tree)
