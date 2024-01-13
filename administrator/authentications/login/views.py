from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from commonConf.authentication import token_expire_handler
from commonConf.baseViewSet import aBaseViewset, nBaseViewset
from sitepanel.authentications.login.serializers import UserLoginSerializer
from sitepanel.models import UserProfile
import re
def home(request):
    data = "<h1>Welcome to ChicMic Canteen</h1>"
    return HttpResponse(data)

class AuthLoginViewset(nBaseViewset):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        
        try:
            email = request.data['email']
            if str(email).lstrip() == "":
                return Response({"message":"Please enter valid email address.",
                            "status": False,
                            "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)  
            else:
                regex = r'\b^(([^<>()\\.,;:\s@"]+(\.[^<>()\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$\b'
                if not (re.fullmatch(regex, email)):
                    return Response({"message":"Please enter valid email address.",
                            "status": False,
                            "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)  
            try:
                with transaction.atomic():
                   
                    if User.objects.filter(email=email).exists():
                        user = User.objects.get(email=email)
                    else:
                        return Response(
                            {"message": "Invalid credential",
                                "status": False,
                                "response": "fail" }, status=status.HTTP_400_BAD_REQUEST)
                            
                    password = request.data['password']
                    if user.check_password(password):
                        try:
                            if int(request.data['is_staff']) == 1 and user.is_staff == 1:
                                if Token.objects.filter(user_id=user.id).exists():
                                    Token.objects.get(user_id=user.id).delete()
                                  
                                token, created = Token.objects.get_or_create(user=user)
                                is_expired, token = token_expire_handler(token)
                                user.last_login = timezone.now()
                                user.save()
                                try:
                                    userProfile = UserProfile.objects.get(ref_user = user)
                                except:
                                    userProfile = UserProfile.objects.create(
                                          ref_user = user,
                                          verified = 1,
                                          user_type = "Admin"
                                    )
                                try:
                                    photo = userProfile.photo.url
                                except:
                                     photo = None
                                return Response({
                                    "message": "you have successfully logged in",
                                    "status": True,
                                    "response": "success",
                                    "token": token.key,
                                    "data": {
                                        'user_id': user.id,
                                        'email':user.email,
                                        "first_name": user.first_name,
                                        "last_name": user.last_name,
                                        "photo":photo
                                        }},status=status.HTTP_201_CREATED)
                            else:   
                                return Response(
                                {"message": "you are not authorized",
                                    "status": False,
                                    "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)

                        except:
                            return Response(
                                {"message": "you are not authorized",
                                    "status": False,
                                    "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(
                            {"message": "Invalid credential",
                                "status": False,
                                "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                    return Response({
                        "message": str(error),
                        "status": False,
                        "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
                    return Response({
                        "message": str(error),
                        "status": False,
                        "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)

# AuthLogoutViewset is aBaseViewset we are using this Admin Logout 
# we need only token using this class admin token will be deleted 

                    
class AuthLogoutViewset(aBaseViewset):
    queryset = User.objects.filter()
    serializer_class = UserLoginSerializer
    http_method_names = ['post']    
    
    def create(self, request, *args, **kwargs):
        try:
            Token.objects.get(user_id=request.user.id).delete()
            # Token.objects.create(user=request.user)
            # logout(request)
            return Response({
                "message":"Logged out successfully",
                "status":True,
                "response":"success"
            },status=status.HTTP_200_OK)
        except Exception as error:
                return Response({
                        "message": str(error),
                        "status": False,
                        "response": "fail"}, status=status.HTTP_400_BAD_REQUEST)



