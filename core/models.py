from django.utils.translation import gettext_lazy as _
from django.db import models
from account.models import Base, User
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import FileExtensionValidator


QUARTER_CHOICES = (
    ('1', 'First Quarter'),
    ('2', 'Second Quarter'),
    ('3', 'Third Quarter'),
    ('4', 'Fourth Quarter')
)


class OverviewBanner(Base):
    title = models.CharField(max_length=250, null=True, blank=True)
    short_description = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to="dashboard/banner/", null=True, blank=True, help_text=f"Image dimension should be (1920 x 200)")

    class Meta:
        verbose_name = 'Overview Banner'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.title


class Category(Base):
    name = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tags(Base):
    name = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return self.name


class Keyword(Base):
    name = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = "Keywords"
    
    def __str__(self):
        return self.name


class KnowlageCenter(Base):
    title = models.CharField(max_length=250, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_trending = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
    slug = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='knowlage-center-image/', null=True, blank=True, help_text="Image should be in 1920*1080px dimension",validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    content = HTMLField(blank=True,null=True,max_length=4096)

    class Meta:
        verbose_name = 'Knowledge Center'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title

    def clean(self):
        if not self.image:
            pass
        else:
            w, h = get_image_dimensions(self.image)
            if w != 1920:
                raise ValidationError("The image is %i pixel wide. It's supposed to be 1920px" % w)
            if h != 1080:
                raise ValidationError("The image is %i pixel high. It's supposed to be 1080px" % h)

    @property
    def image_url(self):
        try:
            link = self.image.url
        except:
            link = None
        return link

    @property
    def new_date_format(self):
        new_format = self.created_at.strftime("%d %B, %Y")
        return new_format
    

class KnowlageAssets(Base):
    file = models.FileField(upload_to='knowlage-assets/', null=True, blank=True)
    knowlage = models.ForeignKey(KnowlageCenter, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Brand Assets'
        verbose_name_plural = verbose_name

    @property
    def file_url(self):
        try:
            link = self.file.url
        except:
            link = None
        return link


# LeaderBoard Model
MANDATE_STATUS = (('Not Initiated','Not Initiated'),('In-Process','In-Process'),('Rejected','Rejected'),('Disbursed','Disbursed'))
class Leads(Base):
    dra = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name="my_leads",)
    first_name = models.CharField(max_length=100, null=True, blank=True,)
    last_name = models.CharField(max_length=100, null=True, blank=True,)
    email = models.CharField(max_length=100, null=True, blank=True,)
    phone = models.CharField(max_length=100, null=True, blank=True,)
    prospect_id = models.CharField(max_length=100, null=True, blank=True,)
    mx_client_code = models.CharField(max_length=100, null=True, blank=True,)
    mx_dra_code = models.CharField(max_length=100, null=True, blank=True,)
    mx_referred_dra_code = models.CharField(max_length=100, null=True, blank=True,)
    source = models.CharField(max_length=100, null=True, blank=True,)
    source_medium = models.CharField(max_length=100, null=True, blank=True,)
    source_campaign = models.CharField(max_length=100, null=True, blank=True,)
    mx_diy_stage = models.CharField(max_length=100, null=True, blank=True,)
    lsq_created_on = models.DateTimeField(null=True, blank=True, editable=True)
    my_first_trade_date = models.DateTimeField(null=True, blank=True, editable=True)
    mandate_status=models.CharField(choices=MANDATE_STATUS,max_length=100, null=True, blank=True,default='Not Initiated')
    status=models.BooleanField(default=False, null=True, blank=True,)
    app_downloaded = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Leads'
        verbose_name_plural = verbose_name

    @property
    def name(self):
        try:
            name = f'{self.first_name +" "+self.last_name}'
        except:
            name = self.first_name
        return name
    
    @property
    def mobile_no(self):
        return f'{self.phone}'
    
    @property
    def date_created(self):
        format_date = self.created_at.strftime("%d %B, %Y")
        return format_date
    
    @property
    def step(self):
        return self.mx_diy_stage

    @property
    def mobile(self):
        return self.phone
        
    @property
    def user_channel(self):
        return self.source_medium
        
    @property
    def is_activated(self):
        return True

    @property
    def dra_code(self):
        return self.mx_referred_dra_code

    @property
    def net_brokerage(self):
        return 0

    @property
    def leads(self):
        return 0

    @property
    def dra_name(self):
        return self.dra.name

    @property
    def user_tag(self):
        if self.dra:
            if self.dra.dra_tag==None:
                return None
            else:
                return self.dra.dra_tag
        
        # return "de"

class Incentive(Base):
    dra = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incentives")
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE,)
    incentive_amount = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('dra', 'lead')
        verbose_name = 'Incentive'
        verbose_name_plural = verbose_name


class Brokerage(Base):
    dra = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    api_updated_date = models.DateTimeField(null=True, blank=True, editable=True)
    dra_code = models.CharField(max_length=100, null=True, blank=True)
    total_cummulative_brokerage = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4)
    total_cumulative_net_brokerage = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4)
    unique_cummulative_count = models.PositiveIntegerField(null=True, blank=True)
    sharing = models.DecimalField(null=True, blank=True, max_digits= 10,  decimal_places=6)
    branch = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Brokerage'
        verbose_name_plural = verbose_name
 
PAYMENT_MODE=(('IMPS','IMPS'),('NEFT','NEFT'))
PAYMENT_STATUS=(('Payment Done','Payment Done'),('On Hold','On Hold'))
class Payout(Base):
    dra = models.ForeignKey(User, on_delete=models.CASCADE,)
    rm_name=models.CharField(max_length=100, null=True, blank=True,)
    customer_name=models.CharField(max_length=100, null=True, blank=True,)
    voucher_date = models.DateTimeField(null=True, blank=True, editable=True)
    vtype = models.CharField(max_length=100, null=True, blank=True,)
    clear_status = models.CharField(max_length=100, null=True, blank=True,)
    voucher_number = models.CharField(max_length=100, null=True, blank=True,)
    ac_code = models.CharField(max_length=100, null=True, blank=True,)
    particulars = models.CharField(max_length=100, null=True, blank=True,)
    cheque_no = models.CharField(max_length=100, null=True, blank=True,)
    payment_mode = models.CharField(choices=PAYMENT_MODE,max_length=100, null=True, blank=True,)
    payment_status = models.CharField(choices=PAYMENT_STATUS,max_length=100, null=True, blank=True,)
    debit = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4,)
    credit = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4,)
    balance = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4,)

    class Meta:
        verbose_name = 'Payout'
        verbose_name_plural = verbose_name

    @property
    def date(self):
        d_ate = self.voucher_date
        new_date_format = d_ate.strftime("%d %B,%Y")
        return new_date_format

    # @property
    # def payment_mode(self):
    #     if self.payment_mode is None:
    #         pass
    #     return self.payment_mode
    
    @property
    def amount(self):
        if self.credit:
            value = f'{round(self.credit)}'+'(C)'
        else:
            value = f'{round(self.debit)}'+'(D)'
        return value
    
    @property
    def status(self):
        return f'{self.clear_status}'

    @property
    def DRA_code(self):
        return f"{self.ac_code}"

    @property
    def trade_active(self):
        return True

    @property
    def converted(self):
        try:
            value = round(self.debit)
        except:
            value = 0
        return value

    @property
    def gross_brokerage(self):
        try:
            value = round(self.debit)
        except:
            value = 0
        return value

    @property
    def incentive(self):
        try:
            value = round(self.debit)
        except:
            value = 0
        return value

    @property
    def net_brokerage(self):
        try:
            value = round(self.debit)
        except:
            value = 0
        return value

    @property
    def total(self):
        try:
            value = round(self.balance)
        except:
            value = 0
        return str(value)
    
    @property
    def created_month(self):
        return self.created_at.strftime("%B")
    
    @property
    def created_year(self):
        return self.created_at.strftime("%Y")


class Settlement(Base):
    # MONTH	CONVERTED	TRADE ACTIVE	GROSS BROKERAGE	INCENTIVE	NET BROKERAGE
    dra = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=100, null=True)
    converted = models.PositiveIntegerField(null=True, blank=True)
    trad_active = models.PositiveIntegerField(default=0)
    gross_brokerage = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4)
    incentive = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4)
    net_brokerage = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4)
    total = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=4)

    class Meta:
        verbose_name = 'Settlement'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.id}"

    @property
    def date(self):
        format_date = self.created_at.strftime("%d %B, %Y")
        return format_date

    @property
    def dra_code(self):
        return self.dra.dra_tag


class Segment(Base):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, null=True, unique=True, blank=True)

    class Meta:
        verbose_name = 'Segment'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.name}"


class FinancialYear(Base):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = 'Financial Year'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.name}"


class TDSCertificate(Base):
    dra = models.ForeignKey(User, on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, null=True, blank=True, on_delete=models.SET_NULL)
    quarter = models.CharField(max_length=100, null=True, choices=QUARTER_CHOICES)
    tds = models.DecimalField(null=True, blank=True, max_digits= 14,  decimal_places=2)
    tds_certificate = models.FileField(upload_to='tds-certificate/', null=True, blank=True)

    class Meta:
        verbose_name = 'TDS Certificate'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.dra} {self.financial_year} {self.quarter}"

class Faq(Base):
    question = models.CharField(max_length=1000, null=True,blank=True)
    answer = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.question}"