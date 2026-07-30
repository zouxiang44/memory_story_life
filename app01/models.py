from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Father(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True


class Person(AbstractUser, Father):
    avatar = models.ImageField(verbose_name="用户头像", upload_to="avatars/", default='avatars/default_avatar.jpg')
    phone = models.CharField(verbose_name="用户电话", max_length=11, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    blog = models.OneToOneField(to='Blog', related_name='person', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username


class Blog(Father):
    site_title = models.CharField(verbose_name="站点标题", max_length=20, default='默认站点名称')
    site_theme = models.FileField(verbose_name="站点样式", upload_to="blog_styles/", blank=True, null=True)

    class Meta:
        verbose_name = '站点'
        verbose_name_plural = '站点'

    def __str__(self):
        return self.site_title


class Articles(Father):
    title = models.CharField(verbose_name="文章标题", max_length=20, blank=True, null=True)
    desc = models.TextField(verbose_name="文章简介", max_length=300, blank=True, null=True)
    content = models.TextField(verbose_name="文章内容", blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    # 点赞点踩评论数目字段
    nums_up = models.IntegerField(verbose_name="点赞数", default=0)
    nums_down = models.IntegerField(verbose_name="点踩数", default=0)
    nums_comment = models.IntegerField(verbose_name="评论数", default=0)

    # 关系字段
    blog = models.ForeignKey(
        to='Blog', related_name='articles', on_delete=models.CASCADE, blank=True, null=True)
    categories = models.ForeignKey(
        to='Categories', related_name='articles', on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(to='Tags', related_name='articles', blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title


class Tags(Father):
    name = models.CharField(verbose_name="标签", max_length=10, blank=True, null=True)
    blog = models.ForeignKey(to='Blog', related_name='tags', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Categories(Father):
    name = models.CharField(verbose_name="分类", max_length=10, blank=True, null=True)
    blog = models.ForeignKey(to='Blog', related_name='categories', on_delete=models.CASCADE,
                             blank=True, null=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class UpOrDowns(models.Model):
    is_up = models.BooleanField(verbose_name="是否点赞")
    user = models.ForeignKey(to='Person', related_name='upordowns', on_delete=models.CASCADE)
    article = models.ForeignKey(to='Articles', related_name='upordowns', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '点赞点踩'
        verbose_name_plural = '点赞点踩'

    def __str__(self):
        return self.is_up


class Comments(models.Model):
    content = models.TextField(verbose_name="评论", max_length=100, blank=True, null=True)
    user = models.ForeignKey(to='Person', related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(to='Articles', related_name='comments', on_delete=models.CASCADE)
    # 自关联，当有人回复某条评论时他的评论会有这条字段用于说明回复的谁的评论
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return self.content
