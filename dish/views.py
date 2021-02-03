from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Dish
from .serializers import DishSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class DishListView(ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return has_permission(request) or self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['chef'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DishDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs) \

    def put(self, request, *args, **kwargs):
        return self.is_owner_or_admin(request, *args, **kwargs) \
               or self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.is_owner_or_admin(request, *args, **kwargs) \
               or self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.is_owner_or_admin(request, *args, **kwargs) \
               or self.destroy(request, *args, **kwargs)

    def is_owner_or_admin(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user
        instance = self.get_object()
        if not instance:
            return Response(status=404)
        if not user.is_superuser and user.id != instance.chef.id:
            return Response(status=403)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['chef'] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


def has_permission(request):
    if not request.user.id:
        return Response(status=403)