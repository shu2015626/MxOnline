# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from courses.models import Course

# Create your views here.


class OrgView(View):
    """课程机构列表功能"""
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 城市
        all_cities = CityDict.objects.all()

        # 机构排序，根据点击数
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 机构家数
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    """用户添加咨询"""
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)  # 这相当于userask = UserAsk(),然后在赋值，然后在save
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 知道了课程机构 course_org, 就可以通过这个 课程机构
        # 反向取出所有该课程机构下面的 课程 courses,(只能是get不能是filter等得到的集合)
        # 在 django 的 ORM 中 可以直接通过 course_set 来得到
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            "course_org": course_org,
            "current_page": current_page
        })


class OrgCourseView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 知道了课程机构 course_org, 就可以通过这个 课程机构
        # 反向取出所有该课程机构下面的 课程 courses,(只能是get不能是filter等得到的集合)
        # 在 django 的 ORM 中 可以直接通过 course_set 来得到
        all_courses = course_org.course_set.all()[:3]

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            "course_org": course_org,
            "current_page": current_page
        })