# -*- coding:utf-8 -*-
'''
注册users的model到xadmin的后台
'''
__author__ = "sunsn"

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    """
    EmailVerifyRecord的管理类
    """
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-envelope'


class BannerAdmin(object):
    """
    Banner的管理类
    """
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)


# 有些版本的xadmin后台自动注册的是django自带的用户表
# 如果是这样的话，通过下面的代码可以卸载掉自动注册的默认User类
# 并将我们自己定义的UserProfile注册进后台
# 我这里已经自动实现了，就不需要了
# from xadmin.plugins.auth import UserAdmin
# from .models import UserProfile
# from django.contrib.auth.models import User

# 后台展示的页面布局，都可以通过get_form_layout函数进行自定义，
# 自定义布局需要用到xadmin.layout中的函数
# from xadmin.layout import Fieldset, Main, Side, Row

# class UserProfileAdmin(UserAdmin):
#     # pass
#     def get_form_layout(self):
#         if self.org_obj:
#             self.form_layout = (
#                 Main(
#                     Fieldset('',
#                              'username', 'password',
#                              css_class='unsort no_title'
#                              ),
#                     Fieldset(_('Personal info'),
#                              Row('first_name', 'last_name'),
#                              'email'
#                              ),
#                     Fieldset(_('Permissions'),
#                              'groups', 'user_permissions'
#                              ),
#                     Fieldset(_('Important dates'),
#                              'last_login', 'date_joined'
#                              ),
#                 ),
#                 Side(
#                     Fieldset(_('Status'),
#                              'is_active', 'is_staff', 'is_superuser',
#                              ),
#                 )
#             )
#         return super(UserAdmin, self).get_form_layout()
# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProfileAdmin)