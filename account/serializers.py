from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from account.models import Level, User, Platform
from core.models import *


def validate_bank_detail(data):
    validated = True
    error_list = []
    required_fields = ["pan_no", "bank_account_no", "account_holder_name", "ifsc_code", "account_type"]
    for r in required_fields:
        if r not in data:
            validated = False
            error_list.append(f"{r} is required")
    return validated, error_list


def get_serialized_bank_detail(bd):
    try:
        return {
            "id": bd.id,
            "pan_no": bd.pan_no,
            "pan_card_file": bd.pan_card_file.url if bd.pan_card_file else None,
            "bank_account_no": bd.bank_account_no,
            "account_type": bd.account_type,
            "account_holder_name": bd.account_holder_name,
            "ifsc_code": bd.ifsc_code,
            "cancelled_cheque": bd.cancelled_cheque.url if bd.cancelled_cheque else None,
            "aadhar_card_file": bd.aadhar_card_file.url if bd.aadhar_card_file else None
        }
    except Exception as e:
        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'is_active', 'date_joined')


class PlatformsSerializer(serializers.ModelSerializer):
    """docstring for Profile Serializer."""
    class Meta:
        model = Platform
        fields = '__all__'

class DRAUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = ('name', 'email', 'mobile', 'user_channel', 'is_activated', 'dra_code', 'dra_name')

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('name', 'icon', 'bg_colour')

class BrokerUserListSerializer(serializers.ModelSerializer): 
    level = LevelSerializer(many=False)
    class Meta:
        model = User
        fields = ('name', 'brokerage', 'level')


class TotalEarningListSerializer(serializers.ModelSerializer): 
    level = LevelSerializer(many=False)
    class Meta:
        model = User
        fields = ('name', 'brokerage', 'kyc', 'total_earning', 'level')


class KYCUserListSerializer(serializers.ModelSerializer):
    level = LevelSerializer(many=False)
    class Meta:
        model = User
        fields = ('name', 'kyc', 'level')

class SettlementListSerializer(serializers.ModelSerializer):
    trad_active = serializers.SerializerMethodField('get_trad_active')
    gross_brokerage = serializers.SerializerMethodField('get_gross_brokerage')
    incentive = serializers.SerializerMethodField('get_incentive')
    net_brokerage = serializers.SerializerMethodField('get_net_brokerage')
    total = serializers.SerializerMethodField('get_total')

    def get_trad_active(self, obj):
        return round(obj.trad_active, 2)
    
    def get_gross_brokerage(self, obj):
        return round(obj.gross_brokerage, 2)
    
    def get_incentive(self, obj):
        return round(obj.incentive, 2)
    
    def get_net_brokerage(self, obj):
        return round(obj.net_brokerage, 2)
    
    def get_total(self, obj):
        return round(obj.total, 2)

    class Meta:
        model = Settlement
        fields = ('date', 'month', 'year', 'converted', 'trad_active','gross_brokerage','incentive','net_brokerage','total', 'dra_code')

class PayoutPageSerializer(serializers.ModelSerializer):
    dra_code = serializers.SerializerMethodField('get_dra_code')
    name = serializers.SerializerMethodField('get_name')
    email = serializers.SerializerMethodField('get_email')

    def get_dra_code(self, obj):
        if obj.dra:
            return obj.dra.dra_tag
        else:
            return None
    
    def get_name(self, obj):
        if obj.dra:
            return obj.dra.name
        else:
            return None
    
    def get_email(self, obj):
        if obj.dra:
            return obj.dra.email
        else:
            return None

    class Meta:
        model = Payout
        fields = ('date','dra_code','customer_name','rm_name','name','email','payment_mode','amount','status')

class RMPayoutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ('date', 'DRA_code', 'trade_active', 'converted', 'gross_brokerage', 'incentive', 'net_brokerage', 'total')

class MyRmSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    email = serializers.SerializerMethodField('get_email')
    mobile = serializers.SerializerMethodField('get_mobile')
    date_joined = serializers.SerializerMethodField('get_date_joined')
    successful_mandate = serializers.SerializerMethodField('get_successful_mandate')
    pending_mandate = serializers.SerializerMethodField('get_pending_mandate')
    rejected_mandate = serializers.SerializerMethodField('get_rejected_mandate')
    rm_code=serializers.SerializerMethodField('get_rm_code')
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile', 'date_joined','rm_code','successful_mandate','pending_mandate','rejected_mandate')

    
    def get_name(self, obj):
        return obj.name
    
    def get_email(self, obj):
        return obj.email
    
    def get_mobile(self, obj):
        return obj.mobile
    
    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%d %b %Y")

    def get_successful_mandate(self, obj):
        reporting_manager_id = obj.reporting_manager.id
        return Leads.objects.filter(dra__reporting_manager_id=reporting_manager_id, mandate_status="Disbursed").count()
    
    def get_pending_mandate(self, obj):
        reporting_manager_id = obj.reporting_manager.id
        return Leads.objects.filter(dra__reporting_manager_id=reporting_manager_id, mandate_status="In-Process").count()
    
    def get_rejected_mandate(self, obj):
        reporting_manager_id = obj.reporting_manager.id
        return Leads.objects.filter(dra__reporting_manager_id=reporting_manager_id, mandate_status="Rejected").count()
    
    def get_rm_code(self, obj):
        if obj.dra_tag:
            return obj.dra_tag
        else:
            return None

class PayoutInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('incentive', 'brokerage')
        
class LeadsSerializer(serializers.ModelSerializer):
    mandate_status=serializers.SerializerMethodField('get_mandate_status')
    dra_code = serializers.SerializerMethodField('get_dra_code')
    class Meta:
        model = Leads
        fields = ('name', 'email', 'mobile_no', 'date_created', 'step', 'dra_code', 'dra_name','mandate_status','status',)

    def get_mandate_status(self, obj):
        if obj.mandate_status == "Not Initiated":
            return 'Not Initiated'
        elif obj.mandate_status == "In-Process":
            return 'In-Process'
        elif obj.mandate_status == "Rejected":
            return 'Rejected'
        elif obj.mandate_status == "Disbursed":
            return 'Disbursed'
    def get_dra_code(self,obj):
        if obj.dra:
            return obj.dra.dra_tag
        else:
            return None

class RMSignUpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'mobile', 'date_joined', 'stage', 'agreement', 'admin_status', 'date')

class RMOpportunitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = ('name', 'mobile_no', 'dra_code', 'leads', 'is_activated', 'net_brokerage')


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('name', 'slug')