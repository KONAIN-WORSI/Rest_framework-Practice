from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .helpers import save_pdf
from django.conf import settings
import pandas as pd
import uuid
from django.conf import settings


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
