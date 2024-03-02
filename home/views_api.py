from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .helpers import *
from django.contrib.auth import authenticate, login
from django.contrib import messages

class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data

            if data.get('username') is None:
                messages.error(request, 'Username not provided')
                raise Exception('Username not provided')

            if data.get('password') is None:
                messages.error(request, 'Password not provided')
                raise Exception('Password not provided')

            check_user = User.objects.filter(username=data.get('username')).first()

            if check_user is None:
                messages.error(request, 'Invalid username, user not found')
                raise Exception('Invalid username, user not found')

            if not Profile.objects.filter(user=check_user).first().is_verified:
                messages.error(request, 'Your profile is not verified')
                raise Exception('Profile not verified')

            user_obj = authenticate(username=data.get('username'), password=data.get('password'))
            if user_obj:
                login(request, user_obj)
                messages.success(request, 'Welcome')
                return Response({'status': 200, 'message': 'Welcome'})
            else:
                messages.error(request, 'Invalid password')
                raise Exception('Invalid password')

        except Exception as e:
            print(e)
            return Response({'status': 500, 'message': 'Something went wrong'})

LoginView = LoginView.as_view()



class RegisterView(APIView):

    def post(self, request):
        response = {'status': 500, 'message': 'Something went wrong'}
        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'key username not found'
                raise Exception('key username not found')

            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key password not found')
            check_user = User.objects.filter(
                username=data.get('username')).first()
            if check_user:
                response['message'] = 'username  already taken'
                raise Exception('username  already taken')

            user_obj = User.objects.create(email=data.get('username'),
                                           username=data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            token = generate_random_string(20)
            # set verified user
            Profile.objects.create(user=user_obj, token=token,
                                   is_verified=True)
            # send_mail_to_user(token , data.get('username'))
            response['message'] = 'User created '
            response['status'] = 200
        except Exception as e:
            print(e)

        return Response(response)


RegisterView = RegisterView.as_view()
