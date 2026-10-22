from django.urls import path
from . import views
from home.views import JobListView, job_detail, RegisterView, my_profile, LogOutView

urlpatterns = [
    path('student/', views.StudentAPI.as_view()),
    path('register/', views.UserRegister.as_view()),
    path('generic-student/', views.GenericStudent.as_view()),
    path('generic-student/<id>', views.GenericStudent1.as_view()),
    path('pdf', views.GeneratePdf.as_view()),
    path('excel/', views.ImportExportExcel.as_view()),

    # path('', views.home, name='home'),
    # path('student', views.post_student, name='post_student'),
    # path('update_student/<id>', views.update_student, name='update_student'),
    # path('delete_student/<id>', views.delete_student, name='delete_student'),
    path('get_book', views.get_book, name='get_book'),
    path('api/job/', JobListView.as_view(), name = 'job_list'),
    path('api/job/<int:pk>/', views.job_detail, name = 'job_detail'),

    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/me/", my_profile, name="my-profile"),
    path("api/auth/logout/", LogOutView.as_view(), name="logout")
]