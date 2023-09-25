import biomodels
from biomodels.common import cache_path
from pytest import mark

from .. import read
from ..xml import fromstring
from .common import compare_xml


def yield_sedml(f):
    omex = biomodels.get_omex(f)
    for p in omex:
        if str(p).endswith(".sedml"):
            yield p


@mark.parametrize("file", [p.stem for p in (cache_path / "omex").iterdir()])
def test_roundtrip(file):
    for p in yield_sedml(file):
        direct = fromstring(p.read_bytes())
        round_trip = fromstring(read(p).to_xml(skip_empty=True))
        assert compare_xml(direct, round_trip)
