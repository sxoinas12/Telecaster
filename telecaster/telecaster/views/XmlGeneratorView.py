from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from django.http import JsonResponse
from ..Clients.PrestaShopClient import PrestaShopClient
from ..serializers import XmlGeneratorSerializer
from ..sanitizers.prestashop_backoffice_api_sanitizer import PrestashopBackOfficeApiSanitizer


class XmlGeneratorView(views.APIView):
    renderer_classes = [
        XMLRenderer,
    ]

    @classmethod
    def get(cls, request: Request, *args, **kwargs) -> JsonResponse:
        return JsonResponse({}, safe=False)

    @classmethod
    def post(cls, request: Request, *args, **kwargs) -> JsonResponse:
        url = request.data.get('url')
        token = request.data.get('token')

        prestashop_client = PrestaShopClient(base_url=url, token=token)

        # retrieve categories first since they are needed for products
        categories = prestashop_client.get_categories()
        products = prestashop_client.get_products({'limit': 5})
        sanitizer = PrestashopBackOfficeApiSanitizer()

        sanitized_categories = sanitizer.categories(categories)

        categories_dict = {category.category_id: vars(category) for category in sanitized_categories}
        sanitized_products = sanitizer.products(products)

        # serialize response
        serializer = XmlGeneratorSerializer()
        response_xml = serializer.for_xml(
            products=sanitized_products, categories=categories_dict, site_url=url
        )

        return Response(response_xml, content_type='text/xml')
