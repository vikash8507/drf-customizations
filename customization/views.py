from faker import Faker
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from .parsers import CSVTextParser
from .renderers import CSVTextRenderer
from .paginations import CustomPagination

def initial_data(total=5):
    data = []
    fake = Faker()
    for _ in range(total):
        data.append({"name": fake.name(), "address": fake.address()[:20] + '...'})
    return data

class CustomRendererAPIView(APIView):

    renderer_classes = [BrowsableAPIRenderer, JSONRenderer, ]
    parser_classes = [CSVTextParser, ]

    def post(self, request, format=None):
        return Response({"data": request.data})

    def get(self, request, format=None):
        response = initial_data(2)
        return Response(response)