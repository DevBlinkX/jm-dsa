from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class AssetsInline(admin.StackedInline):
    model = KnowlageAssets
    extra = 0


@admin.register(OverviewBanner)
class OverviewBannerModelAdmin(admin.ModelAdmin):
    list_display = ['title']

# @admin.register(Category)
# class CategoryModelAdmin(ImportExportModelAdmin):
#     list_display = ['name','is_active']

# @admin.register(Tags)
# class TagsModelAdmin(ImportExportModelAdmin):
#     list_display = ['name']

# @admin.register(KnowlageCenter)
# class KnowlageCenterModelAdmin(ImportExportModelAdmin):
#     inlines = [AssetsInline]
#     list_display = ['title']
#     exclude = ('tags',)

# @admin.register(KnowlageAssets)
# class KnowlageAssetsModelAdmin(admin.ModelAdmin):
#     list_display = ['id']

@admin.register(Brokerage)
class BrokerageModelAdmin(ImportExportModelAdmin):
    list_display = ['id','dra','api_updated_date','created_at']

@admin.register(Payout)
class PayoutModelAdmin(ImportExportModelAdmin):
    list_display = ['id','dra']

@admin.register(Leads)
class LeadsModelAdmin(ImportExportModelAdmin):
    list_display = ['id', 'created_at','name','phone','email','user_tag','status',"mandate_status"]
    # list_filter = ('dra__user_type',)
    search_fields = ('dra__username','dra__user_type','dra__dra_tag')
    list_per_page  = 30

@admin.register(Incentive)
class IncentiveModelAdmin(ImportExportModelAdmin):
    list_display = ['id', 'dra']


@admin.register(Settlement)
class SettlementModelAdmin(ImportExportModelAdmin):
    list_display = ['id', 'dra', 'total']


# @admin.register(Keyword)
# class KeywordModelAdmin(ImportExportModelAdmin):
#     list_display = ['id', 'name', 'slug']

class FaqModelAdmin(ImportExportModelAdmin):
    list_display = ['id', 'question', 'answer']


# admin.site.register(Segment)
admin.site.register(FinancialYear)
admin.site.register(TDSCertificate)
admin.site.register(Faq,FaqModelAdmin)