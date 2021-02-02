from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Category
from .serializers import CategorySerializer

class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        return is_admin(request) or self.create(request, *args, **kwargs)


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return is_admin(request) or self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return is_admin(request) or self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return is_admin(request) or self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return is_admin(request) or self.destroy(request, *args, **kwargs)

def is_admin(request):
    user = request.user
    if not user.is_superuser:
        return Response(status=403)

