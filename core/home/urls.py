from django.urls import path
from . import views

urlpatterns = [
    # path('student/', views.StudentAPI.as_view()),
    path('register/', views.UserRegister.as_view()),
    path('generic-student/', views.GenericStudent.as_view()),
    path('generic-student/<id>', views.GenericStudent1.as_view()),
    path('pdf', views.GeneratePdf.as_view()),
    path('excel/', views.ImportExportExcel.as_view()),

    # path('', views.home, name='home'),
    # path('student', views.post_student, name='post_student'),
    # path('update_student/<id>', views.update_student, name='update_student'),
    # path('delete_student/<id>', views.delete_student, name='delete_student'),
    path('get_book', views.get_book, name='get_book')
]