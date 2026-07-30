from django.urls import path, re_path
from . import views

app_name = 'app02'
urlpatterns = [
    # 文章点赞点踩
    path('updown/', views.UpDownView.as_view(), name='UpDown'),

    # 文章评论
    path('comments/', views.CommentView.as_view(), name='Comment'),

    # 文章详情路由
    re_path(r'(?P<username>\w+)/(?P<id>\d+)/',
            views.ArticleDetailView.as_view(), name='ArticleDetail'),
    # 有过滤条件文章查询
    re_path(r'(?P<username>\w+)/(?P<method>tag|category|date)/(?P<params>.*)/',
            views.HomePersonPageView.as_view(), name='HomeKind'),
    # 无过滤文章条件查询
    path('<str:username>/', views.HomePersonPageView.as_view(), name='HomePerson'),

]
