# -*- coding: utf-8 -*-
'''
注册organizations的model到xadmin的后台
'''
__author__ = "sunsn"
__date__ = '2018/7/1 22:44'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    """
    CityDict的管理类
    """
    list_display = ["name", "desc", "add_time"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]


class CourseOrgAdmin(object):
    """
    CourseOrg的管理类
    """
    list_display = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city", "add_time"]
    search_fields = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city"]
    list_filter = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city", "add_time"]
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    """
    Teacher的管理类
    """
    list_display = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums", "fav_nums", "add_time"]
    search_fields = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums", "fav_nums"]
    list_filter = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums", "fav_nums", "add_time"]


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
