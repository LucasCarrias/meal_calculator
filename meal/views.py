from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Meal
from .serializers import MealSerializer, MealWriteSerializer, MealCalculateSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


class MealListView(ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return has_permission(request) or self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['chef'] = request.user.id
        serializer = MealWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MealDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
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
        serializer = MealWriteSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def meal_calculate(request, *args, **kwargs):
    meal = Meal.objects.filter(pk=kwargs.get('pk')).first()

    if not meal:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {
        "name": meal.name,
        "total_cost": meal.total_cost,
        "total_portions": meal.total_portions,
        "cooking_time": meal.cooking_time,
    }

    serializer = MealCalculateSerializer(data=data)
    serializer.is_valid()
    return Response(serializer.data)


def has_permission(request):
    if not request.user.id:
        return Response(status=403)


