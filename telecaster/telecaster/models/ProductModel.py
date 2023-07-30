from .CategoryModel import CategoryModel


class ProductModel:
    def __init__(
        self,
        product_id: str,
        name: str,
        image: str,
        price: float,
        wholesale_price: float,
        manufacturer: str,
        ena13: str,
        in_stock: int,
        additional_shipping_cost: float,
        description: str,
        quantity: int,
        slug: str,
        mpn: str,
        category: CategoryModel,
    ):
        self.product_id = product_id
        self.name = name
        self.image = image
        self.category = category
        self.price = price
        self.wholesale_price = wholesale_price
        self.manufacturer = manufacturer
        self.ean13 = ena13
        self.in_stock = in_stock
        self.additional_shipping_cost = additional_shipping_cost
        self.description = description
        self.quantity = quantity
        self.slug = slug
        self.mpn = mpn
