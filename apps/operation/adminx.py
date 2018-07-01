# -*- coding: utf-8 -*-
'''
注册operations的model到xadmin的后台
'''
__author__ = "sunsn"
__date__ = '2018/7/1 22:54'

import xadmin

from .models import UserAsk, UserCourse, UserMessage, CourseComments, UserFavorite


class UserAskAdmin(object):
    """
    UserAsk的管理类
    """
    list_display = ["name", "mobile", "course_name", "add_time"]
    search_fields = ["name", "mobile", "course_name"]
    list_filter = ["name", "mobile", "course_name", "add_time"]


class UserCourseAdmin(object):
    """
    UserCourse的管理类
    """
    list_display = ["user", "course", "add_time"]
    search_fields = ["user__username", "course__name"]
    list_filter = ["user__username", "course__name", "add_time"]


class CourseCommentsAdmin(object):
    """
    CourseComments的管理类
    """
    list_display = ["user", "course", "comments", "add_time"]
    search_fields = ["user__username", "course__name", "comments"]
    list_filter = ["user__username", "course__name", "comments", "add_time"]


class UserMessageAdmin(object):
    """
    UserMessage的管理类
    """
    list_display = ["user", "message", "has_read", "add_time"]
    search_fields = ["user", "message", "has_read"]
    list_filter = ["user", "message", "has_read", "add_time"]


class UserFavoriteAdmin(object):
    """
    UserFavorite的管理类
    """
    list_display = ["user", "fav_id", "fav_type", "add_time"]
    search_fields = ["user__username", "fav_id", "fav_type"]
    list_filter = ["user__username", "fav_id", "fav_type", "add_time"]


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)