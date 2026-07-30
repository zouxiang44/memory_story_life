from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Person, Blog, Tags, Comments, Articles, Categories
from app01.forms.register import RegisterForm
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
import json


# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        forms = RegisterForm()
        return render(request, 'PrivatePerson_Page/register.html', locals())

    def post(self, request):
        back_dict = {'code': 0, 'message': ''}
        result = RegisterForm(data=request.POST)

        if result.is_valid():
            result.cleaned_data.pop('password_again')  # 删掉重复密码，因为经过了forms组件
            file = request.FILES.get('avatar')  # 获取文件，因为没在request.POST里
            if file is not None:  # 判断文件是否存在，不然就用默认的
                result.cleaned_data['avatar'] = file  # 存在则添加文件

            blog = Blog.objects.create()  # 新建一个blog
            result.cleaned_data['blog'] = blog  # 把这个blog加给clean_data
            Person.objects.create_user(**result.cleaned_data)  # 数据库创建用户,要用create_user
            back_dict['message'] = '/app01/login/'
        else:
            back_dict['code'] = 2000
            back_dict['message'] = result.errors

        return JsonResponse(back_dict)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/login.html')

    def post(self, request, *args, **kwargs):
        back_dict = {'code': 0, 'message': ''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            url = request.GET.get('next')  # 判断用户是在哪里被要求登录的，有就加到message里
            if url:
                back_dict['message'] = url
            else:
                back_dict['message'] = '/'
        else:
            back_dict['code'] = 2000
            back_dict['message'] = '用户名或密码错误'
        return JsonResponse(back_dict)


class SetUsernameView(LoginRequiredMixin, View):  # 继承LoginRequiredMixin类用于验证是否登录
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/changeUsername.html')

    def post(self, request, *args, **kwargs):
        back_dict = {'code': 0, 'message': ''}

        user_name_data = json.loads(request.body.decode('utf-8'))  # axios普通的data放在body里
        old_username = user_name_data.get('old_username')
        new_username = user_name_data.get('new_username')
        user = Person.objects.filter(username=old_username)
        user.update(username=new_username)

        back_dict['message'] = '/'
        return JsonResponse(back_dict)


class SetAvatarView(LoginRequiredMixin, View):  # 继承LoginRequiredMixin类用于验证是否登录
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/changeAvatar.html')

    def post(self, request, *args, **kwargs):
        back_dict = {'code': 0, 'message': '/'}
        username = request.POST.get('username')
        avatar = request.FILES.get('avatar')

        user = Person.objects.filter(username=username).first()
        user.avatar = avatar  # 不可以使用update,因为不能update不能识别文件
        user.save()
        return JsonResponse(back_dict)


class SetPasswordView(LoginRequiredMixin, View):  # 继承LoginRequiredMixin类用于验证是否登录
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/changePassword.html')

    def post(self, request, *args, **kwargs):
        back_dict = {'code': 0, 'message': ''}
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password_again = request.POST.get('new_password_again')
        if request.user.check_password(old_password):
            if new_password == new_password_again:
                if 8 <= len(new_password) <= 10:
                    request.user.set_password(new_password)
                    request.user.save()
                    back_dict['message'] = '/'
                else:
                    back_dict['code'] = 2001
                    back_dict['message'] = '长度过长或过短'
            else:
                back_dict['code'] = 2002
                back_dict['message'] = '两次密码不一致'
        else:
            back_dict['code'] = 2003
            back_dict['message'] = '旧密码输入错误'
        return JsonResponse(back_dict)


class AdminView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/admin.html')


# class LogoutView(LoginRequiredMixin, View):  # 继承LoginRequiredMixin类用于验证是否登录
#     def get(self, request, *args, **kwargs):
#         print(f'用户{request.user}退出登录')
#         auth.logout(request)
#         return redirect('/')

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            print(f'用户{request.user}退出登录')
        response = redirect('/')
        request.session.flush()  # 清session
        response.delete_cookie('sessionid')  # 删cookie
        return response


class UserNotExistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/userNotExist.html')


# -----------------------------------上方为登录功能，下方为admin功能------------------------------------

class AdminAuthorView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/admin_author.html', locals())

    def post(self, request, *args, **kwargs):
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone')

        request.user.username = new_username
        request.user.email = new_email
        request.user.phone = new_phone
        request.user.save()

        return redirect('app01:AdminAuthor')


# ----------------------------------------------------------------------------------------------

class AdminBlogView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'PrivatePerson_Page/admin_blog.html')

    def post(self, request, *args, **kwargs):
        new_blog_name = request.POST.get('site_name')
        css_file = request.FILES.get('css_file')

        request.user.blog.site_title = new_blog_name
        request.user.blog.site_theme = css_file
        request.user.blog.save()

        return redirect('app01:AdminBlog')


# ---------------------------------------------------------------------------------------------

class AdminTagView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tag_queryset = request.user.blog.tags.all()
        return render(request, 'PrivatePerson_Page/admin_tag/admin_tag.html', locals())


class AdminTagAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'PrivatePerson_Page/admin_tag/admin_tag_add.html',
                      locals())

    def post(self, request, *args, **kwargs):
        blog = request.user.blog
        tag = request.POST.get('tag')
        Tags.objects.create(blog=blog, name=tag)
        return redirect('app01:AdminTag')


class AdminTagEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tag_id = request.GET.get('id')
        tag_obj = Tags.objects.get(id=tag_id)
        return render(request,
                      'PrivatePerson_Page/admin_tag/admin_tag_edit.html',
                      locals())

    def post(self, request, *args, **kwargs):
        old_tag = request.POST.get('old_tag')
        new_tag = request.POST.get('new_tag')
        tag_obj = Tags.objects.filter(name=old_tag).first()
        tag_obj.name = new_tag
        tag_obj.save()
        return redirect('app01:AdminTag')


class AdminTagDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tag_id = request.GET.get('id')
        tag_obj = Tags.objects.get(id=tag_id)
        tag_obj.delete()

        return redirect('app01:AdminTag')


# ---------------------------------------------------------------------------------------------

class AdminCategoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_queryset = request.user.blog.categories.all()
        return render(request, 'PrivatePerson_Page/admin_category/admin_category.html', locals())


class AdminCategoryAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      'PrivatePerson_Page/admin_category/admin_category_add.html',
                      locals())

    def post(self, request, *args, **kwargs):
        blog = request.user.blog
        category = request.POST.get('category')
        Categories.objects.create(blog=blog, name=category)
        return redirect('app01:AdminCategory')


class AdminCategoryEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('id')
        category_obj = Categories.objects.get(id=category_id)
        return render(request,
                      'PrivatePerson_Page/admin_category/admin_category_edit.html',
                      locals())

    def post(self, request, *args, **kwargs):
        old_category = request.POST.get('old_category')
        new_category = request.POST.get('new_category')

        category_obj = Categories.objects.filter(name=old_category).first()
        category_obj.name = new_category
        category_obj.save()
        return redirect('app01:AdminCategory')


class AdminCategoryDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('id')
        category_obj = Categories.objects.get(id=category_id)
        category_obj.delete()

        return redirect('app01:AdminCategory')


# ---------------------------------------------------------------------------------------------

class AdminArticleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article_queryset = request.user.blog.articles.all()
        return render(request, 'PrivatePerson_Page/admin_article/admin_article.html', locals())


class AdminArticleAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tag_queryset = request.user.blog.tags.all()
        category_queryset = request.user.blog.categories.all()
        return render(request, 'PrivatePerson_Page/admin_article/admin_article_add.html', locals())

    def post(self, request, *args, **kwargs):
        blog = request.user.blog
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        category = request.POST.get('category')
        if len(title) > 20:
            title = title[:20:]
        if len(content) > 200:
            desc = content[:200:]
        else:
            desc = content
        category_obj = Categories.objects.filter(id=category).first()

        article_obj = Articles.objects.create(
            title=title,
            desc=desc,
            content=content,
            blog=blog,
            categories=category_obj)
        if tags:  # 空值无法遍历
            tags = [int(Id) for Id in tags]
            article_obj.tags.set(tags)

        return redirect('app01:AdminArticle')


class AdminArticleEditView(View):
    def get(self, request, *args, **kwargs):
        article_id = request.GET.get('id')
        article_obj = Articles.objects.get(id=article_id)
        tag_queryset = request.user.blog.tags.all()
        category_queryset = request.user.blog.categories.all()

        return render(request, 'PrivatePerson_Page/admin_article/admin_article_edit.html', locals())

    def post(self, request, *args, **kwargs):
        blog = request.user.blog
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        category = request.POST.get('category')
        if len(title) > 20:
            title = title[:20:]
        if len(content) > 200:
            desc = content[:200:]
        else:
            desc = content

        category_obj = Categories.objects.filter(id=category).first()

        article_obj = Articles.objects.filter(id=request.POST.get('article_id'))
        article_obj.update(
            title=title,
            desc=desc,
            content=content,
            blog=blog,
            categories=category_obj)
        if tags:  # 空值无法遍历
            tags = [int(Id) for Id in tags]
            article_obj.first().tags.set(tags)

        return redirect('app01:AdminArticle')


class AdminArticleDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article_id = request.GET.get('id')
        article = Articles.objects.get(id=article_id)
        article.delete()
        return redirect('app01:AdminArticle')


# ---------------------------------------------------------------------------------------------

class AdminCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article_queryset = Articles.objects.filter(blog=request.user.blog)
        article_id_list = []
        for article in article_queryset:
            article_id_list.append(article.id)  # 先获取站点文章，再获取每篇文章的评论

        comment_queryset = Comments.objects.filter(article_id__in=article_id_list)
        return render(request, 'PrivatePerson_Page/admin_comment.html', locals())


class AdminCommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment_id = request.GET.get('id')
        comment_obj = Comments.objects.get(id=comment_id)

        article_obj = comment_obj.article
        article_obj.nums_comment -= 1
        article_obj.save()

        comment_obj.delete()
        return redirect('app01:AdminComment')
