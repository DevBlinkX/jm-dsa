from django.contrib import admin
from account.models import Level, Platform, User, MobileVerificationCode, TimingSlot
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from tinymce.widgets import TinyMCE
from django.urls import reverse
from import_export.admin import ImportExportMixin


class UserCustomAdmin(ImportExportMixin, UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'name',
            'user_type',
            'reporting_manager',
            'mobile',
            'email',
            # 'platform',
            # 'account_type',
            # 'account_id',
            # 'followers',
            # 'mobile_verified',
            # 'email_verified',
            # 'gender',
            # 'date_of_birth',
            # 'aadhar_number',
            # 'profile_image',
            # 'short_bio',
            'is_dra',
            'dra_tag',
            'dra_code_encrypted',
            'registration_medium',
            'is_completed',
            'is_activated',
            'activation_date',
            'incentive_perlead',
            'brokerage_percentage',
            'remark',
            'admin_status',
            'is_aggre_term_condition',
            # 'term_condition_agree_time',
            'total_brokerage',
            'level',
            'total_kyc',
        )}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'name', 'is_staff', 'is_completed', 'activation_date')
    readonly_fields = ('is_completed', 'activation_date','dra_tag') 
    search_fields = ('username', 'name', 'id', 'email')
    list_filter = ('user_type', 'admin_status')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'remark':
            return db_field.formfield(widget=TinyMCE())
        return super().formfield_for_dbfield(db_field, **kwargs)

class MobileVerificationCodeAdmin(admin.ModelAdmin):
    list_display=['mobile','email','code', 'created_at']

# Register your models here.
admin.site.register(User, UserCustomAdmin)
# admin.site.register(Platform)
# admin.site.register(Level)
admin.site.register(TimingSlot)
admin.site.register(MobileVerificationCode, MobileVerificationCodeAdmin)
