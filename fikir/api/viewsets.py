from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fikir.models import Department, Idea
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import DepartmentSerializer, IdeaSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class DepartmantViewSet(viewsets.ModelViewSet):
        serializer_class = DepartmentSerializer
        queryset = Department.objects.all()

        # authentication_classes = (TokenAuthentication,)
        # permission_classes = (IsAuthenticated,)

        @action(methods=['get'], detail=False)
        def all(self, request):
                all_departments = self.get_queryset()
                serializer = self.get_serializer_class()(all_departments)
                return Response(serializer.data)


class HomeIdeasViewSet(viewsets.ModelViewSet):
        serializer_class = IdeaSerializer
        queryset = Idea.objects.all().filter(IsApproved=True).filter(IsActive=True).order_by('-id')[:3]
        
        authentication_classes = []
        permission_classes = []
        
        @action(methods=['get'], detail=False)
        def all(self, request):
                three_ideas= self.get_queryset()
                serializer = self.get_serializer_class()(three_ideas)
                return Response(serializer.data)

