from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import SingUpSerializer, LoginSerializer, ChefSerializer
from .models import Chef
from django.db.utils import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request, *args, **kwargs):
    data = request.data
    serializer = SingUpSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(status=201)
        except IntegrityError as error:
            return Response(data={"error": f"{str(error).split('.')[-1]} must be unique"},  status=403)
    return Response(status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request, *args, **kwargs):
    data = request.data
    serializer = LoginSerializer(data=data)
    
    if serializer.is_valid():
        
        chef = authenticate(**serializer.data)
    
        if chef:
            refresh = RefreshToken.for_user(chef)
            return Response(data={
                "username": chef.username,
                "token": str(refresh.access_token)
            })
        return Response({"error": "Invalid credentials"}, status=401)

    return Response(status=400)


class ChefListView(ListAPIView):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer