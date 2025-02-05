from backpos.Services.login_services import login

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def login_controller(request):
    mensaje = login()
    return Response({"mensaje": mensaje})