import xml.etree.ElementTree as gfg
import datetime
from rest_framework import serializers
from io import BytesIO
from ..parsers.cdata_parser import cdata_parser
from ..types.skroutz_cdata_fields import skroutz_cdata_fields
from ..types.skroutz_required_fields import skroutz_required_fields


class XmlGeneratorSerializer(serializers.Serializer):
    @classmethod
    def for_api(validated_data):
        return validated_data

    @classmethod
    def validate_product_for_skroutz(self, product):
        for required_field in skroutz_required_fields:
            if product.get(required_field) is None:
                print(
                    'Skipping product with id %s due to missing required fields: [%s]',
                    product.get('id', 'undefined'),
                    required_field,
                )
                return False

        return True

    @classmethod
    def for_xml(self, products=[], categories={}, site_url=''):
        """Generates an xml based on -> https://developer.skroutz.gr/el/feedspec/#xml"""

        root = gfg.Element("mywebstore")

        # generate current date
        created_at = gfg.Element("created_at")
        created_at.text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        root.append(created_at)

        tree = gfg.ElementTree(root)

        products_element = gfg.Element('products')
        root.append(products_element)

        # convert Model to Skroutz Key
        products = [vars(prod) for prod in products]
        skroutz_products = []

        for product in products:
            category_object = categories.get(product.get('category', {}).category_id, {})
            # Probably all this logic with link must be moved into sanitizer
            # Link must be refactored since it is heavily depended on Prestashop Settings.
            category_name = category_object.get('name', '')
            category_slug = category_object.get('slug', '')
            product_slug = product.get('slug', '')
            link = ''
            if product_slug and category_slug and site_url:
                link = f'{site_url}/{category_slug}/{product_slug}'

            skroutz_product = {
                'id': str(product.get('product_id')),
                'name': product.get('name'),
                'link': link,  # fix this from prestashop API
                'image': product.get('image'),
                'additionalimage': product.get('additionalimage'),
                'category': category_name,
                'price_with_vat': product.get('wholesale_price'),
                'vat': product.get('vat'),
                'manufacturer': product.get('manufacturer'),
                'mpn': product.get('mpn', 'M7652C'),  # fix this from prestashop API,
                'ean': product.get('ean13'),
                'instock': product.get('in_stock'),
                'availability': str(
                    product.get('availability', 'Παραδοση 1 εως 3 ημερε')
                ),  # fix this from Sanitizer
                'size': product.get('size'),
                'weight': product.get('weight'),
                'color': product.get('color'),  # maybe make it array based on skroutz
                'description': product.get('description'),
                'quantity': product.get('quantity'),
            }
            if self.validate_product_for_skroutz(skroutz_product):
                skroutz_products.append(skroutz_product)

        for product in skroutz_products:
            product_element = gfg.Element('product')

            for key, value in product.items():
                if not value:
                    continue

                child = gfg.Element(key)
                if key in skroutz_cdata_fields:
                    child.text = cdata_parser(value)
                else:
                    child.text = value
                product_element.append(child)

            products_element.append(product_element)

        # for developing purposes in order to view your xml we use the below lines
        f = BytesIO()
        tree.write(f, encoding='utf-8', xml_declaration=True)

        return f.getvalue()
