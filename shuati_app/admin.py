# Register your models here.
from django.apps import apps
from django.contrib import admin
from django.db.models import ManyToOneRel, ForeignKey, OneToOneField
from shuati.settings import CUSTOM_APPS


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        self.list_select_related = [
            x.name for x in model._meta.fields
            if isinstance(
                x, (
                    ManyToOneRel,
                    ForeignKey,
                    OneToOneField,
                )
            )
        ]

        # self.search_fields=[model.p]
        super(ListAdminMixin, self).__init__(model, admin_site)


for each in CUSTOM_APPS:
    app_models = apps.get_app_config(each).get_models()
    for model in app_models:
        admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
        try:
            admin.site.register(model, admin_class)
            # print(model," 在管理员后台注册成功")
        except admin.sites.AlreadyRegistered:
            print(model, " 注册失败")


