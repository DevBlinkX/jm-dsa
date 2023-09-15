from django.forms import ValidationError
from .models import Leads
from import_export import resources 
from import_export.results import RowResult
from import_export.fields import Field
from import_export.widgets import BooleanWidget,ForeignKeyWidget
from account.models import Base, User



# class UserForeignKeyWidget(ForeignKeyWidget):
#     model = User
#     field = 'username'

#     def get_queryset(self, value, row, *args, **kwargs):
#         print(value)
#         email = self.model.objects.filter(username=value)
#         if email.exists():
#             return self.model.objects.filter(username=value)
#         else:
#             pass
#             # return self.model.objects.filter(name=value)



class LeadResource(resources.ModelResource):
    # agent=Field(column_name='agent',attribute='dra',widget=UserForeignKeyWidget(User,'username'))
    # try:
    #     dra = Field(
    #         column_name='dra',
    #         attribute='dra',
    #         widget=ForeignKeyWidget(User, 'username')
    #     )
    # except User.DoesNotExist:
    #     dra=Field(
    #         column_name='dra',
    #         attribute='dra',
    #         widget=ForeignKeyWidget(User, 'email')
    #     )
    class Meta:
        model = Leads
        fields = ('first_name','last_name','email', 'phone')
        import_id_fields = ()

    def before_import_row(self, row, row_number=None, **kwargs):
        error=[]
        # if row['status'] == 'Approved':
        #     row['status'] = int(1)
        # elif row['status'] == 1:
        #     error.append(f'status {row["status"]} is not valid at row {row_number} use Approved or Rejected')
        #     # raise ValidationError()
        
        # if row['status'] == 'Rejected':
        #     row['status'] = int(0)
        # elif row['status'] == 0:
        #     error.append(f'status {row["status"]} is not valid at row {row_number} use Approved or Rejected')        
        if row['first_name'] == '':
            error.append(f'first_name is required at row {row_number}')

        if row['last_name'] == '':
            error.append(f'last_name is required at row {row_number}')

        if error:
            raise ValidationError(error)
        return super().before_import_row(row, row_number, **kwargs)

    def __init__(self, user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.imported_rows = []

    def before_save_instance(self, instance, using_transactions, dry_run):
        if not instance.pk and hasattr(self, 'user'):
            instance.dra = self.user
    
    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        result={}
        if row_result.import_type == RowResult.IMPORT_TYPE_NEW:
            for key,value in row.items():
                result[key]=value
        self.imported_rows.append(result)

    def import_data(self, dataset, dry_run=False, raise_errors=False, use_transactions=None, collect_failed_rows=False, rollback_on_validation_errors=False, **kwargs):
        # print(dataset.height)
        result= super().import_data(dataset, dry_run, raise_errors, use_transactions, collect_failed_rows, rollback_on_validation_errors, **kwargs)
        if dataset.height == 0:
            result.base_errors.append("No data found")
            return result
            # raise Exception("No data found")
        if raise_errors and result.has_errors() and result.base_errors():
            raise Exception(result.base_errors)
        if collect_failed_rows:
            return result
        return result
        



class LeadRMResource(resources.ModelResource):
    class Meta:
        model = Leads
        fields = ('first_name','last_name','email', 'phone',)
        import_id_fields = ()

    def before_import_row(self, row, row_number=None, **kwargs):
        error=[]
        # if row['status'] == 'Approved':
        #     row['status'] = int(1)
        # elif row['status'] == 1:
        #     error.append(f'status {row["status"]} is not valid at row {row_number} use Approved or Rejected')
        #     # raise ValidationError()
        
        # if row['status'] == 'Rejected':
        #     row['status'] = int(0)
        # elif row['status'] == 0:
        #     error.append(f'status {row["status"]} is not valid at row {row_number} use Approved or Rejected')        
        if row['first_name'] == '':
            error.append(f'first_name is required at row {row_number}')

        if row['last_name'] == '':
            error.append(f'last_name is required at row {row_number}')

        if error:
            raise ValidationError(error)
        return super().before_import_row(row, row_number, **kwargs)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imported_rows = []
    
    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        result={}
        if row_result.import_type == RowResult.IMPORT_TYPE_NEW:
            for key,value in row.items():
                result[key]=value
        self.imported_rows.append(result)

    def import_data(self, dataset, dry_run=False, raise_errors=False, use_transactions=None, collect_failed_rows=False, rollback_on_validation_errors=False, **kwargs):
        result= super().import_data(dataset, dry_run, raise_errors, use_transactions, collect_failed_rows, rollback_on_validation_errors, **kwargs)
        if dataset.height == 0:
            result.base_errors.append("No data found")
            return result
            # raise Exception("No data found")
        if raise_errors and result.has_errors() and result.base_errors():
            raise Exception(result.base_errors)
        if collect_failed_rows:
            return result
        return result
        



