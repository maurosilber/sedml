from xml.etree.ElementTree import Element

from ..common import bool_parser, try_types

float_bool_str = try_types(float, bool_parser, str)


def compare_xml(x: Element, y: Element) -> bool:
    """Compare two XML trees."""
    assert x.tag == y.tag
    x_keys = set(xi for xi in x.attrib.keys())
    y_keys = set(yi for yi in y.attrib.keys())
    diff: set[str] = set.symmetric_difference(x_keys, y_keys)
    diff = {x for x in diff if not x.startswith("{")}
    assert len(diff) == 0, diff

    for k, xv in x.attrib.items():
        yv = y.attrib[k]
        assert float_bool_str(xv) == float_bool_str(yv), (k, xv, yv)

    x_elements = sorted(x, key=lambda x: x.tag)
    y_elements = sorted(y, key=lambda x: x.tag)
    assert all(map(compare_xml, x_elements, y_elements))
    return True
