import sys

import pytest
import os
from telecaster.telecaster.parsers.PrestaShopParser import PrestaShopParser


@pytest.fixture
def mock_categories_response():
    with open(os.path.join(sys.path[0], 'mock_categories_response.xml'), 'r') as f:
        return f.read()


@pytest.fixture()
def mock_products_response():
    with open(os.path.join(sys.path[0], 'mock_products_response.xml'), 'r') as f:
        return f.read()


def test_categories(mock_categories_response):
    categories = PrestaShopParser.parse_categories(mock_categories_response)
    first_category = categories.get('1')

    assert len(categories) == 3
    assert list(first_category.keys()) == ['id', 'name']


def test_parse_products(mock_products_response, mock_categories_response):
    categories = PrestaShopParser.parse_categories(mock_categories_response)
    products = PrestaShopParser.parse_products(mock_products_response, categories)
    first_product = products[0]

    assert len(products) == 4
    assert list(first_product.keys()) == [
        'id',
        'id_category_default',
        'id_default_image',
        'manufacturer_name',
        'quantity',
        'ean13',
        'delivery_in_stock',
        'price',
        'wholesale_price',
        'additional_shipping_cost',
        'name',
        'description',
        'category_name',  # not sure if this conversion is right
    ]
