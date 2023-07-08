from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (UserViewSet, StudentViewSet,
                       CuratorViewSet, DisciplineViewSet,
                       StudyGroupViewSet, FieldStudyViewSet,
                       GetExcelFiles)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('students', StudentViewSet, basename='students')
router_v1.register('curator', CuratorViewSet, basename='curators')
router_v1.register('disciplines', DisciplineViewSet, basename='disciplines')
router_v1.register('study_group', StudyGroupViewSet, basename='study_group')
router_v1.register('field_study', FieldStudyViewSet, basename='field_study')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('get_excel/', GetExcelFiles.as_view()),
]
