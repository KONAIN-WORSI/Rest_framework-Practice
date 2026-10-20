from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, filters, permissions
from .helpers import save_pdf
from django.conf import settings
import pandas as pd
import uuid
from django.conf import settings
from .serializers import JobSerializer
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsRecruiterOrReadOnly
from rest_framework.permissions import AllowAny
from .auth_serializers import RegisterSerializer



# Create your views here.
class ImportExportExcel(APIView):
    def get(self, request):
        student_obj = Student.objects.all()
        serializers = StudentSerializer(student_obj, many=True)
        df = pd.DataFrame(serializers.data)
        df.to_csv(f'public/static/excel/{uuid.uuid4()}.csv', encoding='UTF-8', index=False)

        return Response({'status':200, 'message': 'file saved successfully'})


    def post(self, request):
        excel_file_upload = ExcelFileUpload.objects.create(excel_file_upload = request.FILES['files'])
        df = pd.read_csv(f'{settings.BASE_DIR}/public/static/{excel_file_upload.excel_file_upload}')

        for student in (df.values.tolist()):
            print(student)

        return Response({'status': 200, 'message': "file imported successfully"})



class GeneratePdf(APIView):
    def get(self, request):
        student_objs = Student.objects.all()

        file_name, status = save_pdf({
            "student_objs": student_objs
        })

        if not status:
            return Response({
                "status": 400,
                "message": "Something went wrong."
            })

        return Response({
            "status": 200,
            "path": f"{settings.MEDIA_URL}{file_name}"
        })



class GenericStudent(generics.ListAPIView, generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class GenericStudent1(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'



class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({'status':403, 'errors': serializer.errors})
        
        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({'status':200, 
                        'payload': serializer.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'message': 'You sent'})


class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_objs = Student.objects.all()
        serializers = StudentSerializer(student_objs, many=True)
        print(request.user)
        return Response({'status':200, 'payload': serializers.data})

    def post(self, request):
        data = request.data
        serializers = StudentSerializer(data=request.data)

        if not serializers.is_valid():
            return Response({'status':403, 'errors': serializers.errors})

        serializers.save()
        return Response({'status':200, 'payload': serializers.data, 'message': 'You sent'})

    def put(self, request):
        try: 
            student_objs = Student.objects.get(id = request.data['id'])
            serializers = StudentSerializer(student_objs, data=request.data, partial=False)

            if not serializers.is_valid():
                print(serializers.errors)
                return Response({'status':403, 'errors': serializers.errors})

            serializers.save()
            return Response({'status':200, 'payload': serializers.data, 'message': 'updated'})
        except Exception as e:
            return Response({'status': 403, 'error': 'invalid id', 'errors': serializers.error_messages})

    def patch(self, request):
        try: 
            student_objs = Student.objects.get(id = request.data['id'])
            serializers = StudentSerializer(student_objs, data=request.data, partial=True)

            if not serializers.is_valid():
                print(serializers.errors)
                return Response({'status':403, 'errors': serializers.errors})

            serializers.save()
            return Response({'status':200, 'payload': serializers.data, 'message': 'updated'})
        except Exception as e:
            return Response({'status': 403, 'error': 'invalid id', 'errors': serializers.error_messages})

    def delete(self, request):
        try:
            student_objs = Student.objects.get(id = request.data['id'])
            student_objs.delete()
            return Response({'status': 200, 'message': 'deleted'})
        except Exception as e:
            print(e)
            return Response({'status': 403, 'error': 'invalid id'})

JOBS = [
        {
            "id": 1,
            "title": "Junior Python Developer",
            "company": "Example Tech Nepal",
            "location": "Kathmandu",
            "skills": ["Python", "Django", "REST API"],
        },
        {
            "id": 2,
            "title": "Backend Developer Intern",
            "company": "Sample Software Pvt. Ltd.",
            "location": "Itahari",
            "skills": ["Python", "SQL", "Git"],
        },
        {
            "id": 3,
            "title": "Junior Data Analyst",
            "company": "Example Analytics",
            "location": "Biratnagar",
            "skills": ["Python", "SQL", "Pandas"],
        },
        {
            "id": 4,
            "title": "Junior Backend Developer",
            "company": "Example Development",
            "location": "Itahari",
            "skills": ["Python", "SQL", "Django"],
        }
    ]

class JobPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50



class JobListView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = JobPagination
    permission_classes = [IsRecruiterOrReadOnly]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["title", "company", "location", "description"]
    ordering_fields = ["created_at", "title", "company"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Job.objects.all()

        location = self.request.query_params.get("location")
        company = self.request.query_params.get("company")

        if location:
            queryset = queryset.filter(
                location__iexact=location.strip()
            )

        if company:
            queryset = queryset.filter(
                company__iexact=company.strip()
            )

        return queryset
    

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([IsRecruiterOrReadOnly])
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'GET':
        serializer = JobSerializer(job)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method in ['PATCH', 'PUT']:
        serializer = JobSerializer(job, data=request.data, partial=(request.method == 'PATCH'))

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    job.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

      
 
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"role": UserProfile.JOB_SEEKER},
    )

    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "role": profile.role,
    })
     












# @api_view(['GET'])
# def home(request):
#     student_objs = Student.objects.all()
#     serializers = StudentSerializer(student_objs, many=True)

#     return Response({'status':200, 'payload': serializers.data})

# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     serializers = StudentSerializer(data=request.data)

#     if not serializers.is_valid():
#         return Response({'status':403, 'errors': serializers.errors})

#     serializers.save()
#     return Response({'status':200, 'payload': serializers.data, 'message': 'You sent'})


# @api_view(['PUT'])
# def update_student(request, id):
#     try: 
#         student_objs = Student.objects.get(id = id)
#         serializers = StudentSerializer(student_objs, data=request.data, partial=True)

#         if not serializers.is_valid():
#             print(serializers.errors)
#             return Response({'status':403, 'errors': serializers.errors})

#         serializers.save()
#         return Response({'status':200, 'payload': serializers.data, 'message': 'updated'})
#     except Exception as e:
#         return Response({'status': 403, 'error': 'invalid id', 'errors': serializers.error_messages})


# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_objs = Student.objects.get(id = id)
#         student_objs.delete()
#         return Response({'status': 200, 'message': 'deleted'})
#     except Exception as e:
#         print(e)
#         return Response({'status': 403, 'error': 'invalid id'})

@api_view(['GET'])
def get_book(request):
    book_objs = Book.objects.all()
    serializers = BookSerializer(book_objs, many=True)

    return Response({'status': 200, 'payload': serializers.data})
