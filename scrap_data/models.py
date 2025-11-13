from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import User


class Banner(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = 'Banner'


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='cat/icon', blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Category'


class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Tags'


class Data(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tags, blank=True)
    description = models.TextField()
    image = models.FileField(upload_to='images/')
    webpage = models.CharField(max_length=100, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        return self.title

    @property
    def is_new(self) -> bool:
        return self.created_at and self.created_at >= timezone.now() - timedelta(days=7)

    @property
    def tags(self):
        return self.tag

    class Meta:
        verbose_name = verbose_name_plural = 'Data'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favourite')
    data = models.ManyToManyField(Data)

    class Meta:
        verbose_name = verbose_name_plural = 'Favourite'


class ToolSubmit(models.Model):
    full_name = models.CharField(max_length=100)
    tool_name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    interested = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.tool_name


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to='news-images/', null=True, blank=True)
    webpage = models.CharField(max_length=500, null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        return self.title

    @property
    def is_new(self) -> bool:
        return self.created_at and self.created_at >= timezone.now() - timedelta(days=7)


class Research(models.Model):
    title = models.CharField(max_length=500)
    subject = models.TextField()
    webpage = models.CharField(max_length=500, null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        return self.title

    @property
    def is_new(self) -> bool:
        return self.created_at and self.created_at >= timezone.now() - timedelta(days=7)
