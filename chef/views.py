from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.request import Request
from .models import Chef
from .serializers import ChefSerializer, LoginSerializer, SingUpSerializer


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


class ChefDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

    def put(self, request: Request, *args, **kwargs):
        return is_same_user_or_admin(request, *args, **kwargs) \
               or self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return is_same_user_or_admin(request, *args, **kwargs) \
               or self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):        
        return is_same_user_or_admin(request, *args, **kwargs) \
               or self.destroy(request, *args, **kwargs)


def is_same_user_or_admin(request, *args, **kwargs):
    '''
        Check if the user is authorized to operate the action
    '''
    pk = kwargs['pk']
    user = request.user
    if not user.is_superuser and user.id != pk:
        return Response(status=403)
