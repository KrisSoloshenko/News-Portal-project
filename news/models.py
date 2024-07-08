from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    """Модель, содержащая объекты всех авторов.
    Содержит поле rating, связь name с моделью User, а также метод update_rating"""
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(p=Coalesce(Sum('rating'), 0))['p']
        comments_rating = self.name.comment_set.aggregate(c=Coalesce(Sum('rating'), 0))['c']
        comments_posts_rating = self.post_set.aggregate(cp=Coalesce(Sum('comment__rating'), 0))['cp']

        self.rating = posts_rating + comments_rating + comments_posts_rating * 3
        self.save()


class Category(models.Model):
    """Модель категории новостей/статей — темы, которые они отражают.
    Содержит одно поле category_name"""
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    """Модель содержит в себе статьи и новости, которые создают пользователи.
    Содержит связи: author, category
    Содержит поля: type, add_time, heading, text, rating.
    А также методы: like, dislike, preview"""
    article = "AR"
    news = "NW"

    TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=article)
    add_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255, )
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:125] + '...'

    def __str__(self):
        return f'{self.heading.title()}: {self.preview()}'


class PostCategory(models.Model):
    """Промежуточная модель для связи «многие ко многим.
    Содержит связи post, category"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Модель комментария, который можно оставить под каждой новостью/статьёй
    Содержит связи: post, user.
    Содержит поля: text, creation_time, rating.
    А также методы: like, dislike"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
