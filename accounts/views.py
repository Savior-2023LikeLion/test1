from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, UserCreateForm
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings


import requests
import jwt
import time

from django.conf import settings
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
# from users.models import UserModel
# from users.views import LoginView, UserView




#* 회원가입
def signup_view(request):
    # GET 요청시 html 응답
    if request.method == 'GET':
        form = SignUpForm     #*  장고 제공 form SignUpForm
        # form = UserCreateForm     #*  기본 설정 내역
        # form = UserCreationForm       #*  장고 제공 form  (비밀번호 설정 조건 등 텍스트로 제공)
        
        context = {'form': form}
        return render(request, './signup.html', context)
    else:
        #* post 요청시 데이터 확인 후 회원 생성
        form = SignUpForm(request.POST)
        if form.is_valid():
            # 회원가입 처리
            instance = form.save()
            print(form.errors)
            return redirect('savior:map')
        
        else:
            # 리다이렉트
            print(form.errors)
            return redirect(':accounts')
    
#* 로그인 
def login_view(request):
    # GET, POST
    if request.method == 'GET':
        # 로그인 html 응답
        return render(request, './login.html', {'form': AuthenticationForm()})
    else:
        # 데이터 유효성 검사
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 비즈니스 로직 처리 - 로그인 처리
            login(request, form.user_cache)
            return redirect('savior:map')
        else:
            # 비즈니스 로직 처리 - 로그인 실패 (false)
            # form = AuthenticationForm(request.POST)
            return render(request, './login.html', {'form':form})

#* 로그아웃
def logout_view(request):
    # 데이터유효성 검사
    if request.user.is_authenticated:
    # 비즈니스 로직 처리 - 로그아웃
        logout(request)
    # 응답 (main 화면으로 이동)
    return redirect('savior:map')

#* 카카오
# 로그인 페이지 주소
# kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"

# #엑세스 토큰 발급받기 위한 주소
# kakao_token_uri = "https://kauth.kakao.com/oauth/token"

# # 프로필 정보 조회를 위한 주소
# kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

#사용자가 로그인 테스트 서버로 접속시 redirect URI를 반환한다.
# class KakaoLoginView(APIView):
    # permission_classes = [AllowAny]

    # def get(self, request):
    #     '''
    #     kakao code 요청

    #     ---
    #     '''
    #     client_id = settings.KAKAO_REST_API_KEY
    #     redirect_uri = settings.KAKAO_REDIRECT_URI
    #     uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
    #     res = redirect(uri)
    #     return res

# 사용자가 oauth 로그인시 code 검증 및 로그인 처리한다.
# class KakaoCallbackView(APIView):
    # permission_classes = [AllowAny]

    # @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    # def get(self, request):
    #     '''
    #     kakao access_token 및 user_info 요청
    #     ---
    #     '''
    #     data = request.query_params

    #     # access_token 발급 요청
    #     code = data.get('code')
    #     if not code:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    #     request_data = {
    #         'grant_type': 'authorization_code',
    #         'client_id': settings.KAKAO_REST_API_KEY,
    #         'redirect_uri': settings.KAKAO_REDIRECT_URI,
    #         'client_secret': settings.KAKAO_CLIENT_SECRET_KEY,
    #         'code': code,
    #     }
    #     token_headers = {
    #         'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    #     }
    #     token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

    #     token_json = token_res.json()
    #     access_token = token_json.get('access_token')

    #     if not access_token:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     access_token = f"Bearer {access_token}"  # 'Bearer ' 마지막 띄어쓰기 필수

    #     # kakao 회원정보 요청
    #     auth_headers = {
    #         "Authorization": access_token,
    #         "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    #     }
    #     user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
    #     user_info_json = user_info_res.json()

    #     social_type = 'kakao'
    #     social_id = f"{social_type}_{user_info_json.get('id')}"

    #     kakao_account = user_info_json.get('kakao_account')
    #     if not kakao_account:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     user_email = kakao_account.get('email')

    #     # 회원가입 및 로그인
    #     res = login_api(social_type=social_type, social_id=social_id, email=user_email)
    #     return res

#* 카카오 로그인 해결책 2
# def kakao_login(request):
#     client_id = settings.KAKAO_REST_API_KEY
#     REDIRECT_URI = "http://127.0.0.1:8000/accounts/login/kakao/callback"
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code"
#     )
# def kakao_callback(request):
#     try:
#     	#(1)
#         code = request.GET.get("code")
#         client_id = settings.KAKAO_REST_API_KEY
#         # client_id = os.environ.get("KAKAO_ID")
#         REDIRECT_URI = "http://127.0.0.1:8000/accounts/login/kakao/callback"
#         #(2)
#         token_request = requests.get(
#             f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={REDIRECT_URI}&code={code}"
#         )
#         #(3)
#         token_json = token_request.json()
#         error = token_json.get("error", None)
#         if error is not None:
#             raise KakaoException()
#         #(4)
#         access_token = token_json.get("access_token")
#         #(5)
#         profile_request = requests.get(
#             "https://kapi.kakao.com/v2/user/me",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )
#         profile_json = profile_request.json()
#         #(6)
#         email = profile_json.get("kakao_account", None).get("email")
#         if email is None:
#             raise KakaoException()
#         properties = profile_json.get("properties")
#         nickname = properties.get("nickname")
#         profile_image = properties.get("profile_image")
#         #(7)
#         try:
#             user = models.User.objects.get(email=email)
#             if user.login_method != models.User.LOGIN_KAKAO:
#                 raise KakaoException()
#         except models.User.DoesNotExist:
#             user = models.User.objects.create(
#                 email=email,
#                 username=email,
#                 first_name=nickname,
#                 login_method=models.User.LOGIN_KAKAO,
#                 email_verified=True,
#             )
#             user.set_unusable_password()
#             user.save()
#             #(8)
#             if profile_image is not None:
#                 photo_request = requests.get(profile_image)
#                 user.avatar.save(
#                     f"{nickname}-avatar", ContentFile(photo_request.content)
#                 )
#         login(request, user)
#         return redirect(reverse("savior:main"))
#     except KakaoException:
#         return redirect(reverse("accounts:login"))
