from pathlib import Path

from pytest import mark

from .. import read
from ..xml import fromstring
from .common import compare_xml

root = Path("src/sedml/tests/sed-ml/specification")


def yield_sedml_files():
    for file in root.rglob("*.xml"):
        if "<sedML" in file.read_text():
            yield str(file.relative_to(root))


@mark.parametrize("file", list(yield_sedml_files()))
def test_roundtrip(file):
    path = root / file
    direct = fromstring(path.read_bytes())
    round_trip = fromstring(read(path).to_xml(skip_empty=True))
    assert compare_xml(direct, round_trip)
