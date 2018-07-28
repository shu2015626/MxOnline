# -*- coding: utf-8 -*-
'''
注册courses的model到xadmin的后台
'''
__author__ = "sunsn"
__date__ = '2018/7/1 22:18'

import xadmin
from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    """
    Course的管理类
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums']
    # 需要注意的是readonly_fields和exclude是冲突的，如果一个字段出现在了readonly_fields属性中，那么即使设置了exclude也是无效的
    readonly_fields = ['click_nums']  # 后台不能修改click_nums的值
    exclude = ['fav_nums']  # 后台不显示fav_nums的值


class LessonAdmin(object):
    """
    Lesson的管理类
    由于在lesson表里，course是外键，所以list_filter等都不管用，
    要用两个下划线，指定搜索和过滤的是course的哪个字段
    """
    list_display = ['course', 'name', 'add_time']  # 这里不能使用__name
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    """
    Video的管理类
    """
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    """
    CourseResource的管理类
    """
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)



