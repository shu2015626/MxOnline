# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/7/29 22:34'


import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


# excel导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_instance=context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)

