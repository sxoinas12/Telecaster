from ..models.ProductModel import ProductModel
from ..models.CategoryModel import CategoryModel


class PrestashopBackOfficeApiSanitizer:
    def product(self, raw_product):
        """Sanitizes a single product."""
        if not isinstance(raw_product, dict):
            return None

        if not raw_product.get('id'):
            return None

        if not raw_product['ean13']:
            ean13 = None
        else:
            ean13 = str(raw_product['ean13'])

        if raw_product['delivery_in_stock'] is True:
            in_stock = 'Y'
        else:
            in_stock = 'N'

        sanitized_product = {
            'product_id': int(raw_product['id']),
            'name': raw_product.get('name', {}).get('language', ''),
            'image': raw_product['id_default_image'],
            'price': float(raw_product['price']),
            'slug': str(raw_product['link_rewrite'].get('language', '')) or '',
            'wholesale_price': float(raw_product['wholesale_price']),
            'manufacturer': str(raw_product['manufacturer_name']),
            'ena13': ean13,
            'in_stock': str(in_stock),
            'additional_shipping_cost': float(raw_product['additional_shipping_cost']),
            'description': str(raw_product.get('description', {}).get('language', '')),
            'quantity': int(raw_product['quantity']),
            'mpn': str(raw_product['mpn']),
            'category': CategoryModel(category_id=int(raw_product['id_category_default']), name='', slug=''),
        }

        return ProductModel(**sanitized_product)

    def products(self, raw_products):
        result = [self.product(raw_product) for raw_product in raw_products]
        return result

    def category(self, raw_category):
        sanitized_category = {
            'category_id': int(raw_category['id']),
            'name': raw_category.get('name', {}).get('language', ''),
            'slug': raw_category.get('link_rewrite', {}).get('language', ''),
        }

        return CategoryModel(**sanitized_category)

    def categories(self, raw_categories):
        result = [self.category(raw_product) for raw_product in raw_categories]
        return result
