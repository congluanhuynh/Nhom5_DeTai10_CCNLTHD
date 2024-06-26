
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Thesis, Major, User, Department, Comment, Score, Student, Council, CouncilMembership, InterviewSchedule
from .serializers import ThesisSerializer, MajorSerializer, UserSerializer, DepartmentSerializer, CommentSerializer, ScoreSerializer, StudentSerializer, CouncilSerializer, CouncilMembershipSerializer, InterviewScheduleSerializer
from . import paginator, perms


# Create your views here.
class DepartmentView(View):
    def get(self, request):
        deps = Department.objects.all()
        return render(request, 'departments/list.html',
                      {'departments': deps})
    def post(self, request):
        pass
def index(request):
    return HttpResponse("<h1>Hello lecturer</h1>")
def list(request):
    return HttpResponse("<h1>Major List</h1>")
def details(request, major_id):
    return HttpResponse(f"{major_id}")


class DepartmentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class MajorViewSet(viewsets.ViewSet,generics.ListAPIView, generics.CreateAPIView):
    queryset = Major.objects.filter(active=True).all()
    serializer_class = MajorSerializer
    pagination_class = paginator.PaginatorTheses

    def get_queryset(self):
        queries = self.queryset
        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(name__icontains=q)
        return queries

    @action(methods=['get'], detail=True)
    def theses(self, request, pk):
        theses = self.get_object().thesis_set.filter(active=True).all()
        q = request.query_params.get("q")
        if q:
            theses = theses.filter(name__icontains=q)
        return Response(ThesisSerializer(theses, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CouncilViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Council.objects.all()
    serializer_class = CouncilSerializer


class CouncilMembershipViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = CouncilMembership.objects.all()
    serializer_class = CouncilMembershipSerializer


class ThesisViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Thesis.objects.all()
    serializer_class = ThesisSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    @action(methods=['post'], url_path='scores', detail=True)
    def add_score(self, request, pk):
        s = Score.objects.create(user=request.user, thesis=self.get_object(), content=request.data.get('score_value'))
        return Response(ScoreSerializer(s).data, status=status.HTTP_201_CREATED)

    def calculate_average_score(thesis):
        scores = thesis.score_set.all()
        total_score = sum(score.score_value for score in scores)
        num_scores = scores.count()
        if num_scores > 0:
            average_score = total_score / num_scores
            return average_score
        else:
            return None

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user,lesson=self.get_object(), content = request.data.get('content'))
        return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)

class InterviewScheduleViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = InterviewSchedule.objects.all()
    serializer_class = InterviewScheduleSerializer

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]


    @action(methods=['get'], url_name='current', detail=False)
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)

    @action(methods=['put'], url_name='change_password', detail=False)
    def change_password(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')

            user = User.objects.filter(username=username).first()
            if user is None or not user.check_password(old_password):
                return JsonResponse({'message': 'Invalid username or password'}, status=400)

            user.set_password(new_password)
            user.save()

            return JsonResponse({'message': 'Password changed successfully'})
        else:
            return JsonResponse({'message': 'Method not allowed'}, status=405)

