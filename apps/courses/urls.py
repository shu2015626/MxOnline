# -*- coding: utf-8 -*-
'''
课程相关url的配置
'''
__author__ = "sunsn"
__date__ = '2018/7/15 12:56'


from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView

urlpatterns = [
    # 课程列表页
    url(r"^list/$", CourseListView.as_view(), name="course_list"),
    # 课程详情页
    url(r"^detail/(?P<course_id>\d+)/$", CourseDetailView.as_view(), name="course_detail"),
]