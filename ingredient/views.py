from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Ingredient
from .serializers import IngredientSerializer
from rest_framework import status
from django.core.exceptions import FieldError


class IngredientListView(ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        filter = "name"
        if request.GET.get("filter"):
            try:
                queryset = queryset.order_by(request.GET.get("filter"))
                filter = request.GET.get("filter")
            except FieldError:
                pass

        if request.GET.get("ord") == "DESC":
            queryset = queryset.order_by(f"-{filter}")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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


class IngredientDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
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


class IngredientSearchView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        query = request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        else:
            queryset = queryset.none()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def has_permission(request):
    if not request.user.id:
        return Response(status=403)