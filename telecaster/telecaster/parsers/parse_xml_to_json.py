def parse_xml_to_json(xml):
    response = {}
    for child in list(xml):
        if len(list(child)) > 0:
            response[child.tag] = parse_xml_to_json(child)
        else:
            response[child.tag] = child.text or ''

    return response


def parse_prestashop_xml_products(xml):
    response = {}

    for child in list(xml):
        if len(list(child)) > 0:
            response[child.attrib.get('id')] = parse_prestashop_xml_products(child)
        else:
            response[child.attrib.get('id')] = child.attrib

    return response
