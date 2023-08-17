from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name='savior'

urlpatterns = [
    path('', views.main , name='main'),
    path('pricelist/', views.pricelist , name='pricelist'),
    path('exchange/', views.exchange , name='exchange'),
    path('recommend/', views.recommend , name='recommend'),
    path('map/', views.map , name='map'),
    path('intro/', views.intro , name='intro'),

    #일본
    path('japan/', views.japan , name='japan'),
    path('japan_exchange/', views.japan_exchange , name='japan_exchange'),
    path('japan_pricelist/', views.japan_pricelist , name='japan_pricelist'),
    path('japan_clothes/', views.japan_clothes , name='japan_clothes'),
    path('japan_clothes_detail/<int:id>', views.japan_clothes_detail , name='japan_clothes_detail'),
    path('japan_foods/', views.japan_foods , name='japan_foods'),
    path('japan_foods_detail/<int:id>', views.japan_foods_detail , name='japan_foods_detail'),
    path('japan_others/', views.japan_others , name='japan_others'),
    path('japan_others_detail/<int:id>', views.japan_others_detail , name='japan_others_detail'),
    
    #미국
    path('USA/', views.usa , name='USA'),
    path('USA_exchange/', views.usa_exchange , name='USA_exchange'),
    path('USA_pricelist/', views.usa_pricelist , name='USA_pricelist'),
    path('USA_clothes/', views.usa_clothes , name='USA_clothes'),
    path('USA_clothes_detail/<int:id>', views.usa_clothes_detail , name='USA_clothes_detail'),
    path('USA_foods/', views.usa_foods , name='USA_foods'),
    path('USA_foods_detail/<int:id>', views.usa_foods_detail , name='USA_foods_detail'),
    path('USA_others/', views.usa_others , name='USA_others'),
    path('USA_others_detail/<int:id>', views.usa_others_detail , name='USA_others_detail'),

    #베트남
    path('vietnam/', views.vietnam , name='vietnam'),
    path('vietnam_exchange/', views.vietnam_exchange , name='vietnam_exchange'),
    path('vietnam_pricelist/', views.vietnam_pricelist , name='vietnam_pricelist'),
    path('vietnam_clothes/', views.vietnam_clothes , name='vietnam_clothes'),
    path('vietnam_clothes_detail/<int:id>', views.vietnam_clothes_detail , name='vietnam_clothes_detail'),
    path('vietnam_foods/', views.vietnam_foods , name='vietnam_foods'),
    path('vietnam_foods_detail/<int:id>', views.vietnam_foods_detail , name='vietnam_foods_detail'),
    path('vietnam_others/', views.vietnam_others , name='vietnam_others'),
    path('vietnam_others_detail/<int:id>', views.vietnam_others_detail , name='vietnam_others_detail'),
    
    #* 로그인 및 회원가입
    path('accounts/', include('accounts.urls', namespace='accounts' )),

    #* 마이페이지 
    path('mypage/', views.mypage, name='mypage'),
    
    #* 카카오 로그인
    path('users/', include('users.urls', namespace='users')),

    #커뮤니티
    path('community/', views.community, name='community'),
    path('community_post/', views.community_post, name='community_post'),
    path('community_tag/<str:tag_name>', views.community_tag, name='community_tag'),
    path('community_tag/일본', views.community_tag_japan, name='community_tag_japan'),
    path('community_tag/미국', views.community_tag_USA, name='community_tag_USA'),
    path('community_tag/베트남', views.community_tag_vietnam, name='community_tag_vietnam'),
    path('<int:id>/likes/', views.likes, name='likes'),
    path('community_detail/<int:id>', views.community_detail, name='community_detail'),
    path('community_delete/<int:id>', views.community_delete, name='community_delete'),

    #* 식당 추천 
    path('recommend_USA/', views.recommend_restaurant, name='recommend_USA'),
    path('recommend_japan/', views.Japan_restaurant, name='recommend_japan'),
    path('recommend_vietnam/', views.Vietnam_restaurant, name='recommend_vietnam'),


]

urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
