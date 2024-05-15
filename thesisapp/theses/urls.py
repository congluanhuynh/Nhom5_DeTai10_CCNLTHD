from django.urls import path, re_path, include
from .import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('theses', views.ThesisViewSet)
router.register('majors', views.MajorViewSet)
router.register('departments', views.DepartmentViewSet)
router.register('users', views.UserViewSet, basename="user")
router.register('councils', views.CouncilViewSet)
router.register('council_memberships', views.CouncilMembershipViewSet)
router.register('interview_schedule', views.InterviewScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('majors/', views.list, name='list'),
    path('majors/<int:major_id>', views.details, name='detail'),
    path('departments/', views.DepartmentView.as_view()),
]