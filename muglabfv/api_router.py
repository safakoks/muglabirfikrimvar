from fikir.api.viewsets import DepartmantViewSet, HomeIdeasViewSet

from rest_framework import routers

router = routers.DefaultRouter()

router.register('departments', DepartmantViewSet, base_name='department')
router.register('last_three_ideas', HomeIdeasViewSet, base_name='last_three_idea')
