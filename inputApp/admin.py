from django.contrib import admin
from .models import Input, FSAPL, FSAPLReport, FSABS, FSABSReport, WACC, WACCParticulars, YOYGrowth, DCF, Output
from import_export.admin import ImportExportModelAdmin
from .resources import WACCResource, FSAPLResource, FSABSResource

admin.site.register(Input)
admin.site.register(FSAPLReport)
admin.site.register(FSABSReport)
admin.site.register(WACCParticulars)
admin.site.register(YOYGrowth)
admin.site.register(DCF)
admin.site.register(Output)


@admin.register(FSAPL)
class FSAPLAdmin(ImportExportModelAdmin):
    pass
    # , admin.ModelAdmin
    # resource_class = FSAPLResource


@admin.register(FSABS)
class FSABSAdmin(ImportExportModelAdmin):
    pass
    # , admin.ModelAdmin
    # resource_class = FSABSResource


@admin.register(WACC)
class WACCAdmin(ImportExportModelAdmin):
    resource_class = WACCResource
    # , admin.ModelAdmin
    # resource_class = WACCResource
