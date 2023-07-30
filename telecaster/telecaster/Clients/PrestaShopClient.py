import xml.etree.ElementTree as ElementTree
import urllib.parse
from .BaseClient import BaseClient
from ..parsers.parse_xml_to_json import parse_xml_to_json


class PrestaShopClient(BaseClient):
    def __init__(self, base_url, token):
        self.token = token
        self.base_url = base_url

    def build_url(self, url, params={}):
        updated_params = {**params, 'ws_key': self.token}
        return f'{self.base_url}/api{url}?{urllib.parse.urlencode(updated_params)}'

    def get_products(self, params={}):
        constructed_params = {
            'display': '[name, id, mpn, id_default_image, id_category_default,price,wholesale_price,manufacturer_name,ean13,delivery_in_stock,additional_shipping_cost,description,quantity, link_rewrite]',
            **params,
        }
        full_url = self.build_url('/products', constructed_params)
        # we need to parse these since the response is in XML
        # check parsers folder for relevant functions/classes
        products = self.get(full_url)

        xml_products = ElementTree.fromstring(products)
        products = list(xml_products)[0]
        result = [parse_xml_to_json(child) for child in products]

        return result

    def get_categories(self, params={}):
        constructed_params = {'display': '[id,name, link_rewrite]', **params}
        full_url = self.build_url('/categories', constructed_params)
        xml_categories_content = self.get(full_url)
        xml_categories = ElementTree.fromstring(xml_categories_content)
        categories = list(xml_categories)[0]
        # result = {}
        # for child in categories:
        #     child_ojb = parse_xml_to_json(child)
        #     result[child_ojb['id']] = child_ojb
        # Alternatively if we wanna convert to Array check use the below
        result = [parse_xml_to_json(child) for child in categories]
        return result
