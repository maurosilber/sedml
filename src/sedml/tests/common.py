from xml.etree.ElementTree import Element


def compare_xml(x: Element, y: Element) -> bool:
    """Compare two XML trees."""
    assert x.tag == y.tag
    x_keys = set(xi for xi in x.attrib.keys())
    y_keys = set(yi for yi in y.attrib.keys())
    assert x_keys == y_keys, set.symmetric_difference(x_keys, y_keys)

    for k, xv in x.attrib.items():
        yv = y.attrib[k]
        try:
            assert float(xv) == float(yv)
        except ValueError:
            assert xv == yv

    x_elements = sorted(x, key=lambda x: x.tag)
    y_elements = sorted(y, key=lambda x: x.tag)
    assert all(map(compare_xml, x_elements, y_elements))
    return True
