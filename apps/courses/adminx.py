# -*- coding: utf-8 -*-
'''
注册courses的model到xadmin的后台
'''
__author__ = "sunsn"
__date__ = '2018/7/1 22:18'

import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organizations.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class VideoInline(object):
    model = Video
    extra = 0


class CourseAdmin(object):
    """
    Course的管理类
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'get_zj_nums', 'go_to', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums']
    # 需要注意的是readonly_fields和exclude是冲突的，如果一个字段出现在了readonly_fields属性中，那么即使设置了exclude也是无效的
    readonly_fields = ['click_nums']  # 后台不能修改click_nums的值
    exclude = ['fav_nums']  # 后台不显示fav_nums的值

    # 定义可以在列表页直接修改的字段
    list_editable = ['degree', 'desc']

    # 在添加课程的时候，添加章节信息，但是只能做一层，为章节添加视频就怒能继续做了
    # 但可以添加多个inline
    inlines = [LessonInline, CourseResourceInline]

    # 定时刷新列表页,[3, 5]表示是3s还是5s刷新一次，可以在页面选择
    refresh_times = [3, 5]

    # 设置富文本
    # detail是model中定义为UEditorField的字段，ueditor是我们自定义的插件中做判断用的需要一致
    style_fields = {"detail": "ueditor"}

    # 在toolbar里显示导入excel
    import_excel = True

    def queryset(self):
        """过滤后台显示的数据列表"""
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        """
        在保存课程的时候
        自动去更新对应课程机构下的课程数
        """
        obj = self.new_obj  # 获取Course对象
        obj.save()  # 先把课程保存

        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        # 这里的excel是前端（后台页面）里，定义的变量传回来的
        if 'excel' in request.FILES:
            # 写我们的处理逻辑
            # 可以将excel中的每一行变成一条记录，存到数据库里
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    """
    Course的管理类--->专门管理BannerCourse
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums']
    # 需要注意的是readonly_fields和exclude是冲突的，如果一个字段出现在了readonly_fields属性中，那么即使设置了exclude也是无效的
    readonly_fields = ['click_nums']  # 后台不能修改click_nums的值
    exclude = ['fav_nums']  # 后台不显示fav_nums的值

    # 在添加课程的时候，添加章节信息，但是只能做一层，为章节添加视频就怒能继续做了
    # 但可以添加多个inline
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    """
    Lesson的管理类
    由于在lesson表里，course是外键，所以list_filter等都不管用，
    要用两个下划线，指定搜索和过滤的是course的哪个字段
    """
    list_display = ['course', 'name', 'add_time']  # 这里不能使用__name
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    inlines = [VideoInline]


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)



