from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

#from api.tasks import make_excel_task
from users.models import User
from api.permissions import CuratorPermission
from api.serializers import (UserSerializer, StudentSerializer,
                             CuratorSerializer, StudyGroupSerializer,
                             DisciplineSerializer, FieldStudySerializer)
from api.models import (Student, Curator, StudyGroup,
                        Discipline,
                        FieldStudy)


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def get_self_page(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (CuratorPermission,)
    pagination_class = None


class CuratorViewSet(viewsets.ModelViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = None


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None


class StudyGroupViewSet(viewsets.ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = (CuratorPermission,)
    pagination_class = None


class FieldStudyViewSet(viewsets.ModelViewSet):
    queryset = FieldStudy.objects.all()
    serializer_class = FieldStudySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None


""" class GetExcelFiles(APIView):
    def post(self, request):
        if request.user.is_staff == True:
            make_excel_task.apply_asunc()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST) """