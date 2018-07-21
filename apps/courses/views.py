# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        # 热门课程推荐
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程全局搜索功能
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # 参数name__icontains会被django转化为类似like的查询。其中参数icontains的首个i表示忽略大小写
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))


        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses
        })


class CourseDetailView(View):
    """课程详情页"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # ========================================================================
        # 通过课程筛选出学了该课程的所有人
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取学了该课程的人在UserCourse中的所有记录
        # User是UserCourse的外键,可以通过user_id传一个id进去，而不必传一个User实例
        # 另如果是列表参数，django模板给提供了user_id__in这个参数
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 取出学了该课程的用户，还学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        # ========================================================================

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses,
        })


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # ========================================================================
        # 通过课程筛选出学了该课程的所有人
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取学了该课程的人在UserCourse中的所有记录
        # User是UserCourse的外键,可以通过user_id传一个id进去，而不必传一个User实例
        # 另如果是列表参数，django模板给提供了user_id__in这个参数
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 取出学了该课程的用户，还学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        # ========================================================================

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            "course": course,
            "course_resources": all_resources,
            'all_comments': all_comments,
        })


class AddCommentView(View):
    """
    添加课程评论
    （目前通过ajax）
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type="application/json")

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status": "success", "msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type="application/json")

