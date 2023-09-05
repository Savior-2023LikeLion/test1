from django.db import models
from users.models import *
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

#일본
class Japan_clothes(models.Model):  
    japan_clothes = models.CharField(max_length=10)

    def __str__(self):
        return self.japan_clothes

#* 시세 입력 페이지
class Japan_clothes_Comment(models.Model):  
    user = models.ForeignKey(
        "users.User",
        verbose_name="일본 의류 시세 댓글 작성자",
        on_delete=models.CASCADE,
    )
    japan_clothes_post = models.ForeignKey(Japan_clothes, verbose_name="일본 의류 시세 댓글", on_delete=models.CASCADE)
    content = models.TextField("내용")
    number = models.IntegerField("숫자") #! 금액 입력 창 
    created = models.DateTimeField(auto_now_add=True)

class Japan_foods(models.Model):
    japan_foods = models.CharField(max_length=10)

    def __str__(self):
        return self.japan_foods
    
class Japan_others(models.Model):
    japan_others = models.CharField(max_length=10)

    def __str__(self):
        return self.japan_others
    
class Japan_others_Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="일본 잡화 시세 댓글 작성자",
        on_delete=models.CASCADE,
    )
    japan_others_post = models.ForeignKey(Japan_others, verbose_name="일본 잡화 시세 댓글", on_delete=models.CASCADE)
    content = models.TextField("내용")
    number = models.IntegerField("숫자")
    created = models.DateTimeField(auto_now_add=True)

#미국
class USA_clothes(models.Model):
    usa_clothes = models.CharField(max_length=10)

    def __str__(self):
        return self.usa_clothes
    
class USA_clothes_Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="미국 의류 시세 댓글 작성자",
        on_delete=models.CASCADE,
    )
    usa_clothes_post = models.ForeignKey(USA_clothes, verbose_name="미국 의류 시세 댓글", on_delete=models.CASCADE)
    content = models.TextField("내용")
    number = models.IntegerField("숫자")
    created = models.DateTimeField(auto_now_add=True)

class USA_foods(models.Model):
    usa_foods = models.CharField(max_length=10)

    def __str__(self):
        return self.usa_foods
    
class USA_others(models.Model):
    usa_others = models.CharField(max_length=10)

    def __str__(self):
        return self.usa_others
    
    
    #* 미국 잡화 시세 입력 페이지
class USA_others_Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="미국 잡화 시세 댓글 작성자",
        on_delete=models.CASCADE,
    )
    usa_others_post = models.ForeignKey(USA_others, verbose_name="미국 잡화 시세 댓글", on_delete=models.CASCADE)
    content = models.TextField("내용")
    number = models.IntegerField("숫자")
    created = models.DateTimeField(auto_now_add=True)
    
#베트남
class Vietnam_clothes(models.Model):
    vietnam_clothes = models.CharField(max_length=10)

    def __str__(self):
        return self.vietnam_clothes
    
    #* 시세 입력 페이지
class Vietnam_clothes_Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="베트남 의류 시세 댓글 작성자",
        on_delete=models.CASCADE,
    )
    vietnam_clothes_post = models.ForeignKey(Vietnam_clothes, verbose_name="베트남 의류 시세 댓글", on_delete=models.CASCADE)
    content = models.TextField("내용")
    number = models.IntegerField("숫자")
    created = models.DateTimeField(auto_now_add=True)

class Vietnam_foods(models.Model):
    vietnam_foods = models.CharField(max_length=10)

    def __str__(self):
        return self.vietnam_foods
    
class Vietnam_others(models.Model):
    vietnam_others = models.CharField(max_length=10)

    def __str__(self):
        return self.vietnam_others
    
class Vietnam_others_Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="베트남 잡화 시세 댓글 작성자",
        on_delete=models.CASCADE,
    )
    vietnam_others_post = models.ForeignKey(Vietnam_others, verbose_name="베트남 잡화 시세 댓글", on_delete=models.CASCADE)
    content = models.TextField("내용")
    number = models.IntegerField("숫자")
    created = models.DateTimeField(auto_now_add=True)


#커뮤니티 기능
class Post(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
    )
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    title = models.CharField("제목", max_length=30, default='')
    content = models.TextField("내용")
    created = models.DateTimeField("생성일시", auto_now_add=True)
    thumbnail = models.ImageField("썸네일 이미지", upload_to="post", blank=True)
    tags = models.ManyToManyField('HashTag', verbose_name='해시태그 목록', blank=True)

class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name="포스트",
        on_delete=models.CASCADE,
    )
    photo = models.ImageField("사진", upload_to="post")

class Comment(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, verbose_name="포스트", on_delete=models.CASCADE)
    content = models.TextField("내용")
    created = models.DateTimeField("생성일시", auto_now_add=True)

class HashTag(models.Model):
    name = models.CharField("태그명", max_length=20)

    def __str__(self):
        return self.name
    

