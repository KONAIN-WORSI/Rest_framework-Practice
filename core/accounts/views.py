from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from accounts.serializers import *
from rest_framework.views import APIView
from .helpers import *


class RegisterView(APIView):

    def post(self, request):
        try:
            serializers = UserSerializer(data = request.data)

            if not serializers.is_valid():
                return Response({'status': 403, 'error': serializers.errors})

            serializers.save()
            return Response({'status': 200, 'message': 'an OTP was sent to your email'})
        except Exception as e:
            print(e)
            return Response({'status': 404, 'error': 'something went wrong'})


class verify_otp(APIView):
    def post(self, request):
        try:
            data = request.data
            user_obj = User.objects.get(phone = data.get('phone'))
            otp = data.get('otp')

            if user_obj.otp == otp:
                user_obj.is_phone_verified = True
                user_obj.save()

                return Response({'status':200, 'message': 'your otp is verified'})

            return Response({'status': 403, 'error': 'your otp is wrong'})
        except Exception as e:
            print(e)
        return Response({'status': 404, 'error': 'something went wrong'})

    def patch(self, request):
        try:
            data = request.data

            user_obj = User.objects.filter(phone = data.get('phone'))

            if not user_obj.exists():
                return Response({'status': 404, 'error': 'user not found'})

            status, time = send_otp_mobile(data.get('phone'), user_obj[0])

            if status:
                return Response({'status': 200, 'error': 'otp was sent!'})

            return Response({'status': 40, 'error': f'try after a minutes {time}'})

        except Exception as e:
            print(e)
        return Response({'status': 404, 'error': 'something went wrong'})