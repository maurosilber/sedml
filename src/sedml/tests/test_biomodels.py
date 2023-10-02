from pathlib import Path
from typing import Iterator

import biomodels
from biomodels.common import cache_path
from pytest import mark

from .common import load_and_compare


def yield_sedml(f) -> Iterator[Path]:
    omex = biomodels.get_omex(f)
    for p in omex:
        if str(p).endswith(".sedml"):
            yield p


@mark.parametrize("file", sorted(p.stem for p in (cache_path / "omex").iterdir()))
def test_roundtrip(file):
    for p in yield_sedml(file):
        load_and_compare(p.read_bytes())
