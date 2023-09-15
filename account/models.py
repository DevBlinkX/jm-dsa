from email.policy import default
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from model_utils import FieldTracker
from tinymce.models import HTMLField

GENDER_CHOICES = (('male','Male'), ('female', 'Female'))
REGISTRATION_MEDIUM_CHOICES = (
    ('web', 'Website'),
    ('app', 'App')
)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Platform(Base):
    name = models.CharField(max_length=150, null=False, default='Platform X')
    key = models.CharField(max_length=150, null=True, unique=True)
    icon = models.ImageField(upload_to="platform/", null=True, blank=True, default='platform/social-media.png')
    is_active = models.BooleanField(default=True)
    minimum_allowed_users = models.PositiveIntegerField(default=0)
    objects = models.Manager()
    active_platform = ActiveManager()

    class Meta:
        verbose_name = 'Platform'
        verbose_name_plural = "Platforms"

    def __str__(self):
        return f'{self.name}'


class Level(Base):
    name = models.CharField(max_length=250, null=True, blank=True)
    icon = models.ImageField(upload_to="leaderboard/level/", null=True, blank=True)
    bg_colour = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        verbose_name = 'Level'
        verbose_name_plural = verbose_name


class User(AbstractUser):
    USER_TYPE_CHOICE = (
        ('dsa', 'DSA'),
        ('rmj', 'RMJ')
        
    )
    ADMIN_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('unapproved', 'UnApproved'),
        ('approved', 'Approved'),
    )
    user_type = models.CharField(max_length=100, null=True, choices = USER_TYPE_CHOICE, default='rmj')
    reporting_manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,limit_choices_to={"user_type": "dsa"})
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=15, null=True, blank=True, unique=True)
    # platform = models.CharField(max_length=150, null=True, blank=True)
    platform = models.ForeignKey(Platform, null=True, blank=True, on_delete=models.SET_NULL)
    account_type = models.CharField(max_length=150, null=True, blank=True)
    account_id = models.CharField(max_length=150, null=True, blank=True)
    followers = models.CharField(max_length=150, null=True, blank=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=200, null=True, blank=True, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    aadhar_number = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile/", null=True, blank=True)
    short_bio = models.CharField(max_length=2000, null=True, blank=True)
    is_completed = models.BooleanField(default=False, editable=False)
    is_activated = models.BooleanField(default=False)
    is_dra = models.BooleanField(default=False)
    dra_tag = models.CharField(max_length=100, null=True, blank=True,verbose_name="user tag")
    dra_code_encrypted = models.CharField(max_length=250, null=True, blank=True)
    registration_medium = models.CharField(max_length=100, null=True, blank=True, choices=REGISTRATION_MEDIUM_CHOICES)
    activation_date = models.DateTimeField(null=True, blank=True, editable=False)
    extras_platform_detail = models.TextField(null=True, blank=True, editable=False)
    is_aggre_term_condition = models.BooleanField(default=False)
    term_condition_agree_time = models.DateTimeField(null=True, blank=True)
    incentive_perlead = models.PositiveIntegerField(null=True, blank=True,)
    previous_incentive_perlead = models.PositiveIntegerField(null=True, blank=True, editable=False)
    brokerage_percentage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2, validators=[
            MaxValueValidator(30.0),
            MinValueValidator(0.0)
        ])
    previous_brokerage_percentage = models.DecimalField(null=True, blank=True, max_digits=5,editable=False, decimal_places=2, validators=[
            MaxValueValidator(30.0),
            MinValueValidator(0.0)
        ])
    remark = HTMLField("Remark", blank=True,null=True,max_length=2500)
    admin_status = models.CharField(max_length=100, null=True, choices=ADMIN_STATUS_CHOICES, default='pending')
    total_brokerage = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4, default = 0.0,)
    total_kyc =  models.PositiveIntegerField(null=True, blank=True, default=0)
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.SET_NULL)
    #LSQ DRA Fields
    prospect_id = models.CharField(max_length=100, null=True, blank=True,)
    mx_client_code = models.CharField(max_length=100, null=True, blank=True,)
    mx_dra_code = models.CharField(max_length=100, null=True, blank=True,)
    mx_referred_dra_code = models.CharField(max_length=100, null=True, blank=True,)
    lsq_created_on = models.DateTimeField(null=True, blank=True, editable=True)
    my_first_trade_date = models.DateTimeField(null=True, blank=True, editable=True)

    tracker = FieldTracker(fields=['admin_status', 'brokerage_percentage', 'incentive_perlead'])

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.username}"

    @property
    def user_channel(self):
        return "facebook"
    
    @property
    def brokerage(self):
        try:
            value = round(self.total_brokerage,2)
        except:
            value = 0
        return value

    @property
    def kyc(self):
        try:
            value = round(self.total_kyc)
        except:
            value = 0
        return value

    @property
    def total_earning(self):
        try:
            incentives = self.incentives.aggregate(total=Sum('incentive_amount'))['total']
            if not incentives:
                incentives = 0
            value = round(self.total_brokerage+incentives)
        except:
            value = 0
        return value


    @property
    def date(self):
        new_fromat = self.date_joined.strftime("%d %B, %Y")
        return new_fromat

    @property
    def converted(self):
        return "10"

    @property
    def trade_avtive(self):
        return "33"

    @property
    def gross_brokerage(self):
        return "66"

    @property
    def incentive(self):
        return f'{self.incentive_perlead}'

    @property
    def net_brokerage(self):
        return "23000"

    @property
    def total(self):
        return "14000"

    @property
    def payment_mode(self):
        return "36000"

    @property
    def amount(self):
        return 45000

    @property
    def status(self):
        return True

    @property
    def mobile_no(self):
        return f"{self.mobile}"

    @property
    def trade_active(self):
        return True

    @property
    def stage(self):
        return "step 7"

    @property
    def agreement(self):
        return f"{self.is_aggre_term_condition}"

    @property
    def activated(self):
        return True

    @property
    def DRA_code(self):
        return f"{self.mx_dra_code}"

    @property
    def leads(self):
        return 45

    # @property
    # def successful_mandate(self):
    #     self.my_leads
    # @property
    # def disbursed_count(self):
    #     return self.my_leads_set.filter(mandate_status="Disbursed").count()
    
    # @property
    # def rejected_count(self):
    #     return self.my_leads_set.filter(mandate_status="Rejected").count()
    
    # @property
    # def in_Process_count(self):
    #     return self.my_leads_set.filter(mandate_status="In-Process").count()
                
class Address(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="addresses")
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=1000, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = verbose_name


class MobileVerificationCode(Base):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True)
    is_verified = models.BooleanField(default=False)
    code = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'code')
        verbose_name = 'Mobile Verification Code'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.code}"


# class UserPlatform(Base):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
#     platform_handle = models.CharField(max_length=150, null=True)
#     channel_id = models.CharField(max_length=150, null=True, blank=True)
#     thumbnail = models.ImageField(upload_to='platform/handle/', max_length=250, null=True, blank=True)
#     followers = models.CharField(max_length=100, null=True, blank=True)
#     extras = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user} {self.platform}"

#     class Meta:
#         unique_together = ('user', 'platform')


class CorporateDetail(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="corporate_detail")
    organisation_name = models.CharField(max_length=250, null=True, blank=True)
    nature_of_business = models.CharField(max_length=250, null=True, blank=True)
    website_link = models.CharField(max_length=250, null=True, blank=True)
    company_address = models.TextField(max_length=500, null=True, blank=True)
    company_pancard_number = models.CharField(max_length=100, null=True, blank=True)
    certificate_of_incorporation = models.FileField(upload_to="corporate/", null=True, blank=True)
    moa = models.FileField(upload_to="corporate/", null=True, blank=True)
    aoa = models.FileField(upload_to="corporate/", null=True, blank=True)
    gst_certificate = models.FileField(upload_to="corporate/", null=True, blank=True)
    cancelled_cheque = models.FileField(upload_to="corporate/", null=True, blank=True)

    class Meta:
        verbose_name = 'Corporate Detail'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return str(self.user)


class BankDetail(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_detail')
    pan_no = models.CharField(max_length=100, null=True)
    pan_card_file = models.FileField(upload_to="bank_detail", null=True, blank=True)
    bank_account_no = models.CharField(max_length=100)
    account_type = models.CharField(max_length=150, null=True)
    account_holder_name = models.CharField(max_length=200, null=True)
    ifsc_code = models.CharField(max_length=100, null=True)
    cancelled_cheque = models.FileField(upload_to="bank_detail", null=True, blank=True)
    aadhar_card_file = models.FileField(upload_to="bank_detail", null=True, blank=True)

    class Meta:
        verbose_name = 'Bank Detail'
        verbose_name_plural = verbose_name


class TimingSlot(Base):
    DAY_CHOICE = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('Saturday', 'Saturday')
    )
    day = models.CharField(max_length=100, null=True, choices=DAY_CHOICE)
    timing = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Timing Slot'
        verbose_name_plural = verbose_name


