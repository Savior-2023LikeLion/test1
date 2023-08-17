from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from accounts.views import *
from accounts.urls import *
from users.models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from crawling import main_function  # crawling.py 파일의 main_search 함수 임포트

from django.views.decorators.http import require_POST
import pandas as pd
import requests
from bs4 import BeautifulSoup
import cloudscraper
import requests
import json
import csv

from crawling_Vietnam import main_function_vietnam  # crawling.py 파일의 main_search 함수 임포트
from crawling_Japan import main_function_japan
import math

#인트로 맵 페이지
def intro(request):
    return render(request, "intro.html")

#임시용 메인페이지
def main(request):
    return render(request, "main.html")

#메인 맵 페이지
def map(request):
    return render(request, "map.html")


#nav바 시세 선택 페이지
def pricelist(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        if country=='Japan':
            return redirect('savior:japan_pricelist')
        elif country=='USA':
            return redirect('savior:USA_pricelist')
        else:
            return redirect('savior:vietnam_pricelist')
    return render(request, 'pricelist.html')

def usa_pricelist(request):
    return render(request, 'USA_pricelist.html')

def japan_pricelist(request):
    return render(request, 'japan_pricelist.html')

def vietnam_pricelist(request):
    return render(request, 'vietnam_pricelist.html')

#nav바 환율 선택 페이지
# def exchange(request):
#     return render(request, 'exchange.html')


#일본 상세페이지
def japan(request):
    exchange_rate = get_exchange_rate1()
    clouds_info, icon_info, temperature = japan_weather()
    context = {
        'clouds_info': clouds_info,
        'icon_info': icon_info,
        'temperature': temperature,
        'exchange_rate': exchange_rate,
    }
    return render(request, "japan.html", context)

#! 일본 의류 시세 페이지
def japan_clothes(request):
    keyword = request.GET.get("keyword")
    clothes = Japan_clothes.objects.all()
    if keyword is not None:
        clothes = Japan_clothes.objects.filter(japan_clothes__contains=keyword)
    context ={
        "clothes": clothes,
    }
    return render(request, "japan_clothes.html", context)

#! 일본 의류 시세 상세 페이지 -> 댓글을 통해 시세(금액) 평균, 최대, 최소 
def japan_clothes_detail(request, id):
    japan_clothes_post = get_object_or_404(Japan_clothes, pk=id)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            comment_number = request.POST.get("number", 0)
            Japan_clothes_Comment.objects.create(
                user=request.user,
                japan_clothes_post=japan_clothes_post,
                content=comment_content,
                number=comment_number,
            )
        else:
            return redirect('savior:accounts:login')
    comments = Japan_clothes_Comment.objects.filter(japan_clothes_post=japan_clothes_post)
    
    # 숫자 데이터 리스트 생성
    number_list = [comment.number for comment in comments]
    
    # 계산
    # average_number = sum(number_list) / len(number_list) if number_list else 0
    average_number = math.ceil(sum(number_list) / len(number_list)) if number_list else 0 #* 소수점 아래 반올림
    max_number = max(number_list) if number_list else 0
    min_number = min(number_list) if number_list else 0
    
    return render(request, "japan_clothes_detail.html", {
        "japan_clothes_post": japan_clothes_post,
        "comments": comments,
        "average_number": average_number,
        "max_number": max_number,
        "min_number": min_number,
        "login_required_for_comment": True if not request.user.is_authenticated else False,
    })

#일본 음식 시세 페이지
def japan_foods(request):
    keyword = request.GET.get("keyword")
    foods = Japan_foods.objects.all()
    if keyword is not None:
        foods = Japan_foods.objects.filter(japan_foods__contains=keyword)
    context ={
        "foods": foods,
    }
    return render(request, "japan_foods.html", context)

#일본 음식 시세 상세 페이지
def japan_foods_detail(request, id):
    # japan_foods_post = get_object_or_404(Japan_foods, pk=id)
    # if request.method == "POST":
    #     comment_content = request.POST["comment"]
    #     comment_number = request.POST.get("number", 0)
    #     Japan_foods_Comment.objects.create(
    #         user=request.user,
    #         japan_foods_post=japan_foods_post,
    #         content=comment_content,
    #         number=comment_number,
    #     )
    return render(request, "japan_foods_detail.html")

#일본 잡화 시세 페이지
def japan_others(request):
    keyword = request.GET.get("keyword")
    others = Japan_others.objects.all()
    if keyword is not None:
        others = Japan_others.objects.filter(japan_others__contains=keyword)
    context ={
        "others": others,
    }
    return render(request, "japan_others.html", context)

#! 일본 잡화 시세 상세 페이지 -> 시세 입력, 평균, 최대, 최소 도출
def japan_others_detail(request, id):
    japan_others_post = get_object_or_404(Japan_others, pk=id)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            comment_number = request.POST.get("number", 0)
            Japan_others_Comment.objects.create(
                user=request.user,
                japan_others_post=japan_others_post,
                content=comment_content,
                number=comment_number,
            )
        else:
            return redirect('savior:accounts:login')
    # return render(request, "japan_clothes_detail.html", {"japan_clothes_post":japan_clothes_post})
    comments = Japan_others_Comment.objects.filter(japan_others_post=japan_others_post)
    
    # 숫자 데이터 리스트 생성
    number_list = [comment.number for comment in comments]
    
    # 계산
    # average_number = sum(number_list) / len(number_list) if number_list else 0
    average_number = math.ceil(sum(number_list) / len(number_list)) if number_list else 0 #* 소수점 아래 반올림
    max_number = max(number_list) if number_list else 0
    min_number = min(number_list) if number_list else 0
    
    return render(request, "japan_others_detail.html", {
        "japan_others_post": japan_others_post,
        "comments": comments,
        "average_number": average_number,
        "max_number": max_number,
        "min_number": min_number,
    })


#일본 날씨
def japan_weather():
    city = "Tokyo"
    apikey = "1a34ea4698296cf6cb4bb168b8356219"
    lang = "kr"
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
    result = requests.get(api)
    data = json.loads(result.text)

    clouds_info = data.get('weather', [{'main': 'N/A'}])[0]['main']  # 하늘 상태
    icon_info = data.get('weather', [{'icon': 'N/A'}])[0]['icon']  # 아이콘
    temperature = int(data.get('main', {'temp': 'N/A'})['temp'])  # 기온

    return clouds_info, icon_info, temperature

#일본 환율계산기
def exchange(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        if country=='japan':
            return redirect('savior:japan_exchange')
        elif country=='USA':
            return redirect('savior:USA_exchange')
        else:
            return redirect('savior:vietnam_exchange')
    return render(request, 'exchange.html')

def get_exchange_rate1():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html; charset=utf-8'
    }

    scraper = cloudscraper.create_scraper()
    url = "https://kr.investing.com/currencies/jpy-krw"
    html = scraper.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    containers = soup.find('span', {'data-test': 'instrument-price-last'})
    exchange_rate = containers.text if containers else None

    return exchange_rate

def japan_exchange(request):
    if request.method == 'POST':
        JPY = request.POST.get('JPY', 0)
        JPY = int(JPY)
        exchange_rate = get_exchange_rate1()

        if exchange_rate:
            exchange_rate = float(exchange_rate.replace(',', ''))
            KRW = JPY * exchange_rate
            return render(request, 'japan_exchange.html', {'JPY': JPY, 'KRW': KRW, 'exchange_rate': exchange_rate})
        else:
            return render(request, 'japan_exchange.html', {'JPY': JPY, 'exchange_rate': 'Error'})
    else:
        return render(request, 'japan_exchange.html')

#미국 상세페이지
def usa(request):
    exchange_rate = get_exchange_rate2()
    clouds_info, icon_info, temperature = usa_weather()
    context = {
        'clouds_info': clouds_info,
        'icon_info': icon_info,
        'temperature': temperature,
        'exchange_rate': exchange_rate,
    }
    return render(request, "USA.html", context)

#미국 의류 시세 페이지
def usa_clothes(request):
    keyword = request.GET.get("keyword")
    clothes = USA_clothes.objects.all()
    if keyword is not None:
        clothes = USA_clothes.objects.filter(usa_clothes__contains=keyword)
    context ={
        "clothes": clothes,
    }
    return render(request, "USA_clothes.html", context)

#! 미국 의류 시세 상세 페이지 -> 시세(금액) 평균, 최대, 최소 
def usa_clothes_detail(request, id):
    usa_clothes_post = get_object_or_404(USA_clothes, pk=id)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            comment_number = request.POST.get("number", 0)
            USA_clothes_Comment.objects.create(
                user=request.user,
                usa_clothes_post=usa_clothes_post,
                content=comment_content,
                number=comment_number,
            )
        else:
            return redirect('savior:accounts:login')
    comments = USA_clothes_Comment.objects.filter(usa_clothes_post=usa_clothes_post)
    
    # 숫자 데이터 리스트 생성
    number_list = [comment.number for comment in comments]
    
    # 계산
    # average_number = sum(number_list) / len(number_list) if number_list else 0
    average_number = math.ceil(sum(number_list) / len(number_list)) if number_list else 0 #* 소수점 아래 반올림
    max_number = max(number_list) if number_list else 0
    min_number = min(number_list) if number_list else 0
    
    return render(request, "USA_clothes_detail.html", {
        "usa_clothes_post": usa_clothes_post,
        "comments": comments,
        "average_number": average_number,
        "max_number": max_number,
        "min_number": min_number,
    })


#미국 음식 시세 페이지
def usa_foods(request):
    keyword = request.GET.get("keyword")
    foods = USA_foods.objects.all()
    if keyword is not None:
        foods = USA_foods.objects.filter(usa_foods__contains=keyword)
    context ={
        "foods": foods,
    }
    return render(request, "USA_foods.html", context)

#미국 음식 시세 상세 페이지 
def usa_foods_detail(request, id):
    return render(request, "USA_foods_detail.html")

#미국 잡화 시세 페이지
def usa_others(request):
    keyword = request.GET.get("keyword")
    others = USA_others.objects.all()
    if keyword is not None:
        others = USA_others.objects.filter(usa_others__contains=keyword)
    context ={
        "others": others,
    }
    return render(request, "USA_others.html", context)

#! 미국 잡화 시세 상세 페이지 -> 시세(금액) 평균, 최대, 최소 
def usa_others_detail(request, id):
    USA_others_post = get_object_or_404(USA_others, pk=id)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            comment_number = request.POST.get("number", 0)
            USA_others_Comment.objects.create(
                user=request.user,
                usa_others_post=USA_others_post,
                content=comment_content,
                number=comment_number,
            )
        else:
            return redirect('savior:accounts:login')
    comments = USA_others_Comment.objects.filter(usa_others_post=USA_others_post)
    
    # 숫자 데이터 리스트 생성
    number_list = [comment.number for comment in comments]
    
    # 계산
    # average_number = sum(number_list) / len(number_list) if number_list else 0
    average_number = math.ceil(sum(number_list) / len(number_list)) if number_list else 0 #* 소수점 아래 반올림
    max_number = max(number_list) if number_list else 0
    min_number = min(number_list) if number_list else 0
    
    return render(request, "USA_others_detail.html", {
        "USA_others_post": USA_others_post,
        "comments": comments,
        "average_number": average_number,
        "max_number": max_number,
        "min_number": min_number,
    })

#미국 날씨
def usa_weather():
    city = "Washington D.C."
    apikey = "1a34ea4698296cf6cb4bb168b8356219"
    lang = "kr"
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
    result = requests.get(api)
    data = json.loads(result.text)
    clouds_info = data.get('weather', [{'main': 'N/A'}])[0]['main']  # 하늘 상태
    icon_info = data.get('weather', [{'icon': 'N/A'}])[0]['icon']  # 아이콘
    temperature = int(data.get('main', {'temp': 'N/A'})['temp'])  # 기온

    return clouds_info, icon_info, temperature

#미국 환율계산기

def get_exchange_rate2():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html; charset=utf-8'
    }
    scraper = cloudscraper.create_scraper()
    url = "https://kr.investing.com/currencies/usd-krw"
    html = scraper.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    containers = soup.find('span', {'data-test': 'instrument-price-last'})
    exchange_rate = containers.text if containers else None

    return exchange_rate

def usa_exchange(request):
    if request.method == 'POST':
        USD = request.POST.get('USD', 0)
        USD = int(USD)
        exchange_rate = get_exchange_rate2()
        if exchange_rate:
            exchange_rate = float(exchange_rate.replace(',', ''))
            KRW = USD * exchange_rate
            return render(request, 'USA_exchange.html', {'USD': USD, 'KRW': KRW, 'exchange_rate': exchange_rate})
        else:
            return render(request, 'USA_exchange.html', {'USD': USD, 'exchange_rate': 'Error'})
    else:
        return render(request, 'USA_exchange.html')

#베트남 상세페이지
def vietnam(request):
    exchange_rate = 5.47
    clouds_info, icon_info, temperature = vietnam_weather()
    context = {
        'clouds_info': clouds_info,
        'icon_info': icon_info,
        'temperature': temperature,
        'exchange_rate': exchange_rate,
    }
    return render(request, "vietnam.html", context)

#베트남 의류 시세 페이지
def vietnam_clothes(request):
    keyword = request.GET.get("keyword")
    clothes = Vietnam_clothes.objects.all()
    if keyword is not None:
        clothes = Vietnam_clothes.objects.filter(vietnam_clothes__contains=keyword)
    context ={
        "clothes": clothes,
    }
    return render(request, "vietnam_clothes.html", context)

#! 베트남 의류 시세 상세 페이지 -> 시세(금액) 평균, 최대, 최소 
def vietnam_clothes_detail(request, id):
    vietnam_clothes_post = get_object_or_404(Vietnam_clothes, pk=id)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            comment_number = request.POST.get("number", 0)
            Vietnam_clothes_Comment.objects.create(
                user=request.user,
                vietnam_clothes_post=vietnam_clothes_post,
                content=comment_content,
                number=comment_number,
            )
        else:
            return redirect('savior:accounts:login')
    comments = Vietnam_clothes_Comment.objects.filter(vietnam_clothes_post=vietnam_clothes_post)
    
    # 숫자 데이터 리스트 생성
    number_list = [comment.number for comment in comments]
    
    # 계산
    # average_number = sum(number_list) / len(number_list) if number_list else 0
    average_number = math.ceil(sum(number_list) / len(number_list)) if number_list else 0 #* 소수점 아래 반올림
    max_number = max(number_list) if number_list else 0
    min_number = min(number_list) if number_list else 0
    
    return render(request, "vietnam_clothes_detail.html", {
        "vietnam_clothes_post": vietnam_clothes_post,
        "comments": comments,
        "average_number": average_number,
        "max_number": max_number,
        "min_number": min_number,
    })

#베트남 음식 시세 페이지
def vietnam_foods(request):
    keyword = request.GET.get("keyword")
    foods = Vietnam_foods.objects.all()
    if keyword is not None:
        foods = Vietnam_foods.objects.filter(vietnam_foods__contains=keyword)
    context ={
        "foods": foods,
    }
    return render(request, "vietnam_foods.html", context)

#베트남 음식 시세 상세 페이지
def vietnam_foods_detail(request, id):
    return render(request, "vietnam_foods_detail.html")

#베트남 잡화 시세 페이지
def vietnam_others(request):
    keyword = request.GET.get("keyword")
    others = Vietnam_others.objects.all()
    if keyword is not None:
        others = Vietnam_others.objects.filter(vietnam_others__contains=keyword)
    context ={
        "others": others,
    }
    return render(request, "vietnam_others.html", context)

#! 베트남 잡화 시세 상세 페이지 -> 시세(금액) 평균, 최대, 최소 
def vietnam_others_detail(request, id):
    vietnam_others_post = get_object_or_404(Vietnam_others, pk=id)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_content = request.POST["comment"]
            comment_number = request.POST.get("number", 0)
            Vietnam_others_Comment.objects.create(
                user=request.user,
                vietnam_others_post=vietnam_others_post,
                content=comment_content,
                number=comment_number,
            )
        else:
            return redirect('savior:accounts:login')
    comments = Vietnam_others_Comment.objects.filter(vietnam_others_post=vietnam_others_post)
    
    # 숫자 데이터 리스트 생성
    number_list = [comment.number for comment in comments]
    
    # 계산
    # average_number = sum(number_list) / len(number_list) if number_list else 0
    average_number = math.ceil(sum(number_list) / len(number_list)) if number_list else 0 #* 소수점 아래 반올림
    max_number = max(number_list) if number_list else 0
    min_number = min(number_list) if number_list else 0
    
    return render(request, "vietnam_others_detail.html", {
        "vietnam_others_post": vietnam_others_post,
        "comments": comments,
        "average_number": average_number,
        "max_number": max_number,
        "min_number": min_number,
    })


#베트남 날씨
def vietnam_weather():
    city = "Hanoi"
    apikey = "1a34ea4698296cf6cb4bb168b8356219"
    lang = "kr"
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
    result = requests.get(api)
    data = json.loads(result.text)
    clouds_info = data.get('weather', [{'main': 'N/A'}])[0]['main']  # 하늘 상태
    icon_info = data.get('weather', [{'icon': 'N/A'}])[0]['icon']  # 아이콘
    temperature = int(data.get('main', {'temp': 'N/A'})['temp'])  # 기온

    return clouds_info, icon_info, temperature

#베트남 환율계산기
def vietnam_exchange(request):
    if request.method == 'POST':
        VND = request.POST['VND']
        VND = int(VND)
        exchange_rate = 5.47 * 0.01
        KRW = VND * exchange_rate
        return render(request,'vietnam_exchange.html',{'VND':VND,'KRW':KRW})
    else:
        return render(request, 'vietnam_exchange.html')

#임시 마이페이지
def mypage(request):
    return render(request, "mypage.html")

#커뮤니티
def community(request):
    if not request.user.is_authenticated:
        return redirect("savior:accounts:login")
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "community.html", context)

def community_tag(request, tag_name):
    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    else:
        posts = Post.objects.filter(tags=tag)
    context = {
        "tag_name": tag_name,
        "posts": posts,
    }
    return render(request, "community_tag.html", context)

def community_tag_japan(request):
    return render(request, "community_tag.html")

def community_tag_USA(request):
    return render(request, "community_tag.html")

def community_tag_vietnam(request):
    return render(request, "community_tag.html")

def community_post(request):
    if request.method == 'POST':
        title = request.POST["title"]
        content = request.POST["content"]
        thumbnail = request.FILES.get("thumbnail")
        if thumbnail is None:
            post = Post.objects.create(
                title=title,
                content=content,
                user=request.user,
            )
        else:
            post = Post.objects.create(
                title=title,
                content=content,
                thumbnail=thumbnail,
                user=request.user,
            )
        tag_string = request.POST.get("tags")
        if tag_string:
            tag_names = [tag_name.strip() for tag_name in tag_string.split(",")]
            for tag_name in tag_names:
                tag, _ = HashTag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
        url = reverse("savior:community") + f"#post-{post.id}"
        return redirect('savior:community')
    return render(request, "community_post.html")

@login_required
def community_detail(request, id): 
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        comment_content = request.POST["comment"]
        Comment.objects.create(
            post=post,
            content=comment_content,
            user=request.user,
        )
    return render(request, "community_detail.html", {"post":post})

@login_required
def community_delete(request, id): 
    delete_post = get_object_or_404(Post, pk=id) 
    if request.user == delete_post.user:
        delete_post.delete()
    return redirect('savior:community')

@login_required
def likes(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=id)
        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)
        return redirect(reverse('savior:community_detail', args=[post.pk]))
    return redirect('accounts:login')

#* 미국 USA 식당 소개 페이지 
def recommend_restaurant(request):
    csv_data = []
    
    if request.method == 'POST':
        user_input_search = request.POST.get('user_input_search')

        # food_names, food_codes = main_function(5, [], [], [], [], None, search_name)  # 예시로 5개의 결과만 가져옴
        main_function(user_input_search)  # 예시로 5개의 결과만 가져옴
        print("main_function 함수 실행")
        
        csv_filename = f'{user_input_search}_search_result_USA.csv' # user_input_search 이름을 활용해서 파일 명 생성
        with open(csv_filename, 'r', encoding='utf-8-sig') as file:
            # 'r'-> 읽기(read) 모드로 열겠다
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                csv_data.append(row)

        return render(request, 'recommend_restaurant.html', {'csv_data': csv_data})
        # return render(request, 'recommend_restaurant.html', context)

    return render(request, 'recommend_restaurant.html')


 

#* 일본 Japan 식당 소개 페이지 
def Japan_restaurant(request):
    csv_data_j = []
    
    if request.method == 'POST':
        user_input_search_j = request.POST.get('user_input_search_j')

        # food_names, food_codes = main_function(5, [], [], [], [], None, search_name)  # 예시로 5개의 결과만 가져옴
        main_function_japan(user_input_search_j)  # 예시로 5개의 결과만 가져옴
        print("main_function 함수 실행")
        
        csv_filenam_j = f'{user_input_search_j}_search_result_Japan.csv' # user_input_search_j 이름을 활용해서 파일 명 생성
        with open(csv_filenam_j, 'r', encoding='utf-8-sig') as file:
            # 'r'-> 읽기(read) 모드로 열겠다
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                csv_data_j.append(row)

        return render(request, 'Japan_restaurant_list.html', {'csv_data': csv_data_j})
        # return render(request, 'recommend_restaurant.html', context)

    return render(request, 'Japan_restaurant_list.html')

#* 베트남 Vietnam 식당 소개 페이지 
def Vietnam_restaurant(request):
    csv_dat_v = []
    
    if request.method == 'POST':
        user_input_search_v = request.POST.get('user_input_search_v')

        # food_names, food_codes = main_function(5, [], [], [], [], None, search_name)  # 예시로 5개의 결과만 가져옴
        main_function_vietnam(user_input_search_v)  # 예시로 5개의 결과만 가져옴
        print("main_function 함수 실행")
        
        csv_filename_v = f'{user_input_search_v}_search_result_Vietnam.csv' # user_input_search_v 이름을 활용해서 파일 명 생성
        with open(csv_filename_v, 'r', encoding='utf-8-sig') as file:
            # 'r'-> 읽기(read) 모드로 열겠다
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                csv_dat_v.append(row)

        return render(request, 'Vietnam_restaurant_list.html', {'csv_data': csv_dat_v})
        # return render(request, 'recommend_restaurant.html', context)

    return render(request, 'Vietnam_restaurant_list.html')

def recommend(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        if country=='japan':
            return redirect('savior:recommend_japan')
        elif country=='USA':
            return redirect('savior:recommend_USA')
        else:
            return redirect('savior:recommend_vietnam')
    return render(request, 'recommend.html')