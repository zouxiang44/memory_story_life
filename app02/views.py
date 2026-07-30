from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import DetailView
from django.http import JsonResponse

from app01.models import Person, Blog, Categories, Tags, Articles, UpOrDowns, Comments
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import TruncMonth
import json

# Create your views here.
class HomePageView(View):
    def get(self, request):
        article_list = Articles.objects.all()
        return render(request, 'home.html', locals())


class HomePersonPageView(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = Person.objects.filter(username=username).first()
        if not user:
            return render(request, 'PrivatePerson_Page/userNotExist.html')

        blog = user.blog
        article_list = Articles.objects.filter(is_deleted=False, blog=blog)  # 获取该用户所有文章

        method = kwargs.get('method')
        params = kwargs.get('params')

        tags_list = (Tags.objects.filter(blog=blog, is_deleted=False).
                     annotate(count_num=Count('articles__id')).
                     values_list('name', 'count_num'))

        category_list = (Categories.objects.filter(is_deleted=False, blog=blog).
                         annotate(count_num=Count('articles__id')).
                         values_list('name', 'count_num'))

        date_list = (article_list.
                     annotate(month=TruncMonth('create_date')).
                     values('month').annotate(count_num=Count('id')).
                     values_list('month', 'count_num'))

        # 这里详细介绍下,TruncMonth,他会直接把Month后的d,h,m,s重置为0,这样就方便对相同的年月时间,进行分组
        # 还有:TruncYear,TruncQuarter(季),TruncMonth,TruncWeek,TruncDay,TruncHour,TruncMinute

        if method and params:       # 判断是否是点击用户进来的，否则就是点击页面右边便签进来的
            if method == 'tag':
                article_list = article_list.filter(tags__name=params)
            elif method == 'category':
                article_list = article_list.filter(categories__name=params)
            else:
                year, month, day = params.split('-')
                article_list = article_list.filter(  # 如果不是点击用户进来的，就通过条件过滤文章
                    create_date__year=year,
                    create_date__month=month,
                )
        return render(request, 'home_person.html', locals())


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = Person.objects.filter(username=username).first()
        if not user:
            return render(request, 'PrivatePerson_Page/userNotExist.html')

        article_id = kwargs.get('id')
        article_obj = Articles.objects.get(id=article_id)
        comment_list = Comments.objects.filter(article=article_obj)
        return render(request, 'article_detail.html', locals())


class UpDownView(View):
    def post(self, request, *args, **kwargs):
        back_dict = {'code': 0, 'msg': ''}

        user_id = request.user.id
        article_id = request.GET.get('article_id')
        kind = request.GET.get('kind')

        is_up = True if kind == 'up' else False
        article = Articles.objects.filter(id=article_id)
        upordown = UpOrDowns.objects.filter(user_id=user_id, article_id=article_id, is_up=is_up)
        if kind == 'up':
            if not upordown.exists():
                back_dict['code'] = 1001
                back_dict['msg'] = 'up'
                add_up = UpOrDowns.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
                add_up.save()
                article.update(nums_up=F('nums_up') + 1)
            else:
                back_dict['code'] = 1002
                back_dict['msg'] = 'up'
                upordown.delete()
                article.update(nums_up=F('nums_up') - 1)
        else:
            if not upordown.exists():
                back_dict['code'] = 1001
                back_dict['msg'] = 'down'
                add_down = UpOrDowns.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
                add_down.save()
                article.update(nums_down=F('nums_down') + 1)
            else:
                back_dict['code'] = 1002
                back_dict['msg'] = 'down'
                upordown.delete()
                article.update(nums_down=F('nums_down') - 1)

        return JsonResponse(back_dict)


class CommentView(View):
    def post(self, request, *args, **kwargs):
        back_dict = {'code': 0, 'msg': True}
        request = json.loads(request.body.decode('utf-8'))

        sayer = request.get('sayer')
        parent = request.get('parent')
        article = request.get('article')
        content = request.get('content')

        sayer = Person.objects.filter(username=sayer).first()
        parent = Comments.objects.filter(id=parent).first()
        article = Articles.objects.filter(title=article).first()

        Comments.objects.create(user=sayer, article=article, content=content, parent=parent)
        article.nums_comment += 1           # 文章评论数加一
        article.save()

        return JsonResponse(back_dict)

