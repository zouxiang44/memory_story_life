from django.urls import path, re_path
from . import views

app_name = 'app01'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='Register'),
    path('login/', views.LoginView.as_view(), name='Login'),
    path('setusername/', views.SetUsernameView.as_view(), name='SetUsername'),
    path('setavatar/', views.SetAvatarView.as_view(), name='SetAvatar'),
    path('setpassword/', views.SetPasswordView.as_view(), name='SetPassword'),
    path('admin/', views.AdminView.as_view(), name='Admin'),
    path('logout/', views.LogoutView.as_view(), name='Logout'),
    path('userNotExist/', views.UserNotExistView.as_view(), name='UserNotExist'),

    path('admin_author/', views.AdminAuthorView.as_view(), name='AdminAuthor'),  # admin六个部分的路由
    path('admin_blog/', views.AdminBlogView.as_view(), name='AdminBlog'),
    path('admin_tag/', views.AdminTagView.as_view(), name='AdminTag'),
    path('admin_category/', views.AdminCategoryView.as_view(), name='AdminCategory'),
    path('admin_article/', views.AdminArticleView.as_view(), name='AdminArticle'),
    path('admin_comment/', views.AdminCommentView.as_view(), name='AdminComment'),

    path('admin_tag_add/', views.AdminTagAddView.as_view(), name='AdminTagAdd'),  # 标签
    path('admin_tag_edit/', views.AdminTagEditView.as_view(), name='AdminTagEdit'),
    path('admin_tag_delete/', views.AdminTagDeleteView.as_view(), name='AdminTagDelete'),

    path('admin_category_add/', views.AdminCategoryAddView.as_view(), name='AdminCategoryAdd'),  # 分类
    path('admin_category_edit/', views.AdminCategoryEditView.as_view(), name='AdminCategoryEdit'),
    path('admin_category_delete/', views.AdminCategoryDeleteView.as_view(), name='AdminCategoryDelete'),

    path('admin_article_add/', views.AdminArticleAddView.as_view(), name='AdminArticleAdd'),     # 文章
    path('admin_article_edit/', views.AdminArticleEditView.as_view(), name='AdminArticleEdit'),
    path('admin_article_delete/', views.AdminArticleDeleteView.as_view(), name='AdminArticleDelete'),

    path('admin_comment_delete/', views.AdminCommentDeleteView.as_view(), name='AdminCommentDelete'),  # 评论

]
