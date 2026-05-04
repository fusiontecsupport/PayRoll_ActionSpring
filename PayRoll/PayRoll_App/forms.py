from django import forms
from .models import DesignationMaster
from .models import DepartmentMaster
from .models import CompanyMaster
from .models import StateMaster
from .models import GradeMaster
from .models import PayHeadTypeMaster
from .models import AccountGroupMaster
from .models import AdvanceTypeMaster
from .models import BloodGroupMaster
from .models import RelationshipMaster
from .models import AccountHeadMaster
from .models import LocationMaster
from .models import PayHeadMaster
from .models import LeaveHeadMaster
from .models import LeaveHeadDetail
from .models import SubBranchMaster
from .models import EmployeeMaster
from .models import SlabMaster
from .models import AttendanceDetail
from .models import PayrollMaster
from .models import MonthMaster
from .models import AccountingYear
from django.utils import timezone
# from .models import AspNetUsers
import datetime
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class DesignationMasterForm(forms.ModelForm):
    labels = {
        'DSGNDESC': 'Description',
        'DSGNCODE': 'Code',
        'DISPSTATUS': 'Status',
    }

    DISPSTATUS_CHOICES_DES = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_DES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Status'
    )

    class Meta:
        model = DesignationMaster
        fields = ['DSGNDESC', 'DSGNCODE', 'DISPSTATUS']

    def __init__(self, *args, **kwargs):
        super(DesignationMasterForm, self).__init__(*args, **kwargs)

        self.fields['DSGNDESC'].label = self.labels['DSGNDESC']
        self.fields['DSGNDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['DSGNCODE'].label = self.labels['DSGNCODE']
        self.fields['DSGNCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

        self.fields['DISPSTATUS'].label = self.labels['DISPSTATUS']


class DepartmentMasterForm(forms.ModelForm):
    DISPSTATUS_CHOICES_DEPT = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_DEPT,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = DepartmentMaster
        fields = ['DEPTDESC', 'DEPTCODE', 'DISPSTATUS']

        labels = {
            'DEPTDESC': 'Description',
            'DEPTCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentMasterForm, self).__init__(*args, **kwargs)

        self.fields['DEPTDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['DEPTCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })


class CompanyMasterForm(forms.ModelForm):
    DISPSTATUS_CHOICES = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = CompanyMaster
        exclude = ['CUSRID', 'LMUSRID', 'PRCSDATE']  # Exclude fields as needed

        labels = {
            'COMPNAME': 'Company Name',
            'COMPDNAME': 'Company Display Name',
            'COMPADDR1': 'Address Line 1',
            'COMPADDR2': 'Address Line 2',
            'COMPLOCTDESC': 'Location',
            'COMPPINCODE': 'Pincode',
            'COMPPHN1': 'Phone No.1',
            'COMPPHN2': 'Phone No.2',
            'COMPPHN3': 'Landline No.1',
            'COMPPHN4': 'Landline No.2',
            'COMPMAIL': 'Email',
            'COMPCPRSN': 'Contact Person',
            'COMPGSTNO': 'GSTIN',
            'COMPWEBSITE': 'Website (URL)',
            'COMPPANNO': 'PAN No.',
            'STATEID': 'State',
            'COMPCODE': 'Code',
            'DISPSTATUS': 'Status'
        }

    def __init__(self, *args, **kwargs):
        super(CompanyMasterForm, self).__init__(*args, **kwargs)

        text_fields = [
            'COMPNAME', 'COMPDNAME', 'COMPADDR1', 'COMPADDR2',
            'COMPLOCTDESC', 'COMPPINCODE', 'COMPPHN1', 'COMPPHN2',
            'COMPPHN3', 'COMPPHN4', 'COMPMAIL', 'COMPCPRSN',
            'COMPGSTNO', 'COMPWEBSITE', 'COMPPANNO', 'COMPCODE'
        ]

        for field in text_fields:
            self.fields[field].widget = forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': f'Enter {self.fields[field].label}'
            })

        # Specific types
        self.fields['COMPMAIL'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        })

        self.fields['COMPWEBSITE'].widget = forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Website URL'
        })

        # Dropdown for State
        states = StateMaster.objects.filter(DISPSTATUS=0).order_by('STATEDESC')
        state_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        state_choices += [(state.STATEID, state.STATEDESC) for state in states]
        
        self.fields['STATEID'] = forms.ChoiceField(
            choices=state_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='State'
        )

class StateMasterForm(forms.ModelForm):
    DISPSTATUS_CHOICES_STATE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_STATE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = StateMaster
        fields = ['STATEDESC', 'STATECODE', 'STATETYPE', 'DISPSTATUS']

        labels = {
            'STATEDESC': 'State Name',
            'STATECODE': 'Code',
            'STATETYPE': 'State Type',
        }

    def __init__(self, *args, **kwargs):
        super(StateMasterForm, self).__init__(*args, **kwargs)

        self.fields['STATEDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['STATECODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

        self.fields['STATETYPE'].required = True  # Make the field required
        self.fields['STATETYPE'].choices = [('', '-- Please select --')] + list(self.fields['STATETYPE'].choices)[1:]
        self.fields['STATETYPE'].widget.attrs.update({'class': 'form-control'})


class GradeMasterForm(forms.ModelForm):
    DISPSTATUS_CHOICES_GRADE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_GRADE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = GradeMaster
        fields = ['GRADEDESC', 'GRADECODE', 'DISPSTATUS']

        labels = {
            'GRADEDESC': 'Description',
            'GRADECODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(GradeMasterForm, self).__init__(*args, **kwargs)

        self.fields['GRADEDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['GRADECODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

class PayHeadTypeMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_PHEADTYPE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_PHEADTYPE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = PayHeadTypeMaster
        fields = ['PAYHTDESC', 'PAYHTCODE', 'DISPSTATUS']

        labels = {
            'PAYHTDESC': 'Description',
            'PAYHTCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(PayHeadTypeMasterForm, self).__init__(*args, **kwargs)

        self.fields['PAYHTDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['PAYHTCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

class AccountGroupMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_ACCGRUP = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_ACCGRUP,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = AccountGroupMaster
        fields = ['ACHEADGDESC', 'ACHEADGCODE', 'DISPSTATUS']

        labels = {
            'ACHEADGDESC': 'Description',
            'ACHEADGCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(AccountGroupMasterForm, self).__init__(*args, **kwargs)

        self.fields['ACHEADGDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['ACHEADGCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

class AdvanceTypeMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_ADVTYPE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_ADVTYPE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = AdvanceTypeMaster
        fields = ['ADVTDESC', 'ADVTCODE', 'DISPSTATUS']

        labels = {
            'ADVTDESC': 'Description',
            'ADVTCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(AdvanceTypeMasterForm, self).__init__(*args, **kwargs)

        self.fields['ADVTDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['ADVTCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

class BloodGroupMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_BLDGRUP = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_BLDGRUP,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = BloodGroupMaster
        fields = ['BLDGDESC', 'BLDGCODE', 'DISPSTATUS']

        labels = {
            'BLDGDESC': 'Description',
            'BLDGCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(BloodGroupMasterForm, self).__init__(*args, **kwargs)

        self.fields['BLDGDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['BLDGCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

class RelationshipMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_RELSHIP = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_RELSHIP,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = RelationshipMaster
        fields = ['RELMDESC', 'RELMCODE', 'DISPSTATUS']

        labels = {
            'RELMDESC': 'Description',
            'RELMCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(RelationshipMasterForm, self).__init__(*args, **kwargs)

        self.fields['RELMDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['RELMCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

class AccountHeadMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_ACCHEAD = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_ACCHEAD,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = AccountHeadMaster
        fields = ['ACHEADGID', 'ACHEADDESC', 'ACHEADCODE', 'DISPSTATUS']

        labels = {
            'ACHEADGID': 'Account Group Type',
            'ACHEADDESC': 'Description',
            'ACHEADCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(AccountHeadMasterForm, self).__init__(*args, **kwargs)

        self.fields['ACHEADDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['ACHEADCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

        # Fetch enabled account groups
        account_groups = AccountGroupMaster.objects.filter(DISPSTATUS=0).order_by('ACHEADGDESC')

        # Add "Please select" as the first disabled option
        choices = [('', '--- Please select ---')] + [(ag.pk, ag.ACHEADGDESC) for ag in account_groups]

        self.fields['ACHEADGID'] = forms.ModelChoiceField(
            queryset=account_groups,
            empty_label='--- Please select ---',
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Account Group Type'
        )

class LocationMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_LOCATION = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_LOCATION,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    STATEID = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="State"
    )

    class Meta:
        model = LocationMaster
        fields = ['LOCTDESC', 'LOCTCODE', 'STATEID', 'DISPSTATUS']

        labels = {
            'LOCTDESC': 'Description',
            'LOCTCODE': 'Code',
            'STATEID': "State",
        }

    def __init__(self, *args, **kwargs):
        super(LocationMasterForm, self).__init__(*args, **kwargs)

        self.fields['LOCTDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['LOCTCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

        # Load state choices from StateMaster where DISPSTATUS=0
        state_choices = [('', '--- Please Select ---')]
        state_choices += [
            (state.pk, state.STATEDESC)
            for state in StateMaster.objects.filter(DISPSTATUS=0).order_by('STATEDESC')
        ]
        self.fields['STATEID'].choices = state_choices

class PayHeadMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_PAYHEAD = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_PAYHEAD,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = PayHeadMaster
        fields = ['PAYHTID', 'PAYHDESC', 'PAYHCODE', 'DISPORDER', 'DISPSTATUS']

        labels = {
            'PAYHTID': 'Payhead Type',
            'PAYHDESC': 'Description',
            'PAYHCODE': 'Code',
            'DISPORDER': 'Order',
        }

    def __init__(self, *args, **kwargs):
        super(PayHeadMasterForm, self).__init__(*args, **kwargs)

        self.fields['PAYHDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['PAYHCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })

        self.fields['DISPORDER'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Order'
        })

        # Fetch enabled account groups
        payhead = PayHeadTypeMaster.objects.filter(DISPSTATUS=0).order_by('PAYHTDESC')

        # Add "Please select" as the first disabled option
        choices = [('', '--- Please select ---')] + [(ag.pk, ag.PAYHTDESC) for ag in payhead]

        self.fields['PAYHTID'] = forms.ModelChoiceField(
            queryset=payhead,
            empty_label='--- Please select ---',
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Payhead Type'
        )

class LeaveHeadMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_LEHEAD = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    LHMCTYPE_CHOICES = [
        ('', '--- Please Select ---'),
        (0, 'No'),
        (1, 'Yes'),
    ]

    GNDRID_CHOICES = [
        ('', '--- Please Select ---'),
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Both'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_LEHEAD,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    LHMCTYPE = forms.ChoiceField(
        choices=LHMCTYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="EN-Cash"
    )

    GNDRID = forms.ChoiceField(
        choices=GNDRID_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Gender"
    )

    class Meta:
        model = LeaveHeadMaster
        fields = ['LHMDESC', 'LHMCODE', 'LHMCTYPE', 'GNDRID', 'DISPSTATUS']

        labels = {
            'LHMDESC': 'Description',
            'LHMCODE': 'Code',
        }

    def __init__(self, *args, **kwargs):
        super(LeaveHeadMasterForm, self).__init__(*args, **kwargs)

        self.fields['LHMDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Description'
        })

        self.fields['LHMCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Code'
        })


class LeaveHeadDetailForm(forms.ModelForm):
    class Meta:
        model = LeaveHeadDetail
        fields = ['LHDID', 'DSGNID', 'LHDNOD', 'LHDMNOD', 'LHDLNOD']
        labels = {
            'DSGNID': 'Designation',
            'LHDNOD': 'NOD/YEAR',
            'LHDMNOD': 'MAX/YEAR',
            'LHDLNOD': 'LIMIT/YEAR',
        }

        widgets = {
            'LHDID': forms.HiddenInput(),
            'LHDNOD': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Number of Days',
                'required': 'required'
            }),
            'LHDMNOD': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Monthly Number of Days',
                'required': 'required'
            }),
            'LHDLNOD': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Leave Number of Days',
                'required': 'required'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(LeaveHeadDetailForm, self).__init__(*args, **kwargs)

        designations = DesignationMaster.objects.filter(DISPSTATUS=0).order_by('DSGNDESC')
        designation_choices = [('', '--- Please Select ---')] + [(d.DSGNID, d.DSGNDESC) for d in designations]

        self.fields['DSGNID'] = forms.ChoiceField(
            choices=designation_choices,
            widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            label='Designation' 
        )

class SubBranchMasterForm(forms.ModelForm):

    DISPSTATUS_CHOICES_SUBBRNC = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_SUBBRNC,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )

    class Meta:
        model = SubBranchMaster
        fields = ['SBRNCHNAME', 'SBRNCHADDR1', 'SBRNCHADDR2', 'SBRNCHLOCTDESC', 'SBRNCHPINCODE',
                  'SBRNCHGSTNO', 'SBRNCHWEBSITE', 'SBRNCHPANNO', 'STATEID', 'COMPID', 'SBRNCHCODE', 'DISPSTATUS']

        labels = {
            'SBRNCHNAME': 'Sub-Branch Name',
            'SBRNCHADDR1': 'Address line 1',
            'SBRNCHADDR2': 'Address Line 2',
            'SBRNCHLOCTDESC': 'Location',
            'SBRNCHPINCODE': 'Pincode',
            'SBRNCHGSTNO': 'GSTTIN No.',
            'SBRNCHWEBSITE': 'Website(URL)',
            'SBRNCHPANNO': 'PAN No.',
            'STATEID': 'State',
            'COMPID': 'Company',
            'SBRNCHCODE': 'Code',
            'DISPSTATUS': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super(SubBranchMasterForm, self).__init__(*args, **kwargs)

        self.fields['SBRNCHNAME'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Subbranch Name'
        })

        self.fields['SBRNCHADDR1'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 1',
            'rows': 4
        })

        self.fields['SBRNCHADDR2'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 2',
            'rows': 4
        })

        self.fields['SBRNCHLOCTDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Location'
        })

        self.fields['SBRNCHPINCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Pincode'
        })

        self.fields['SBRNCHGSTNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter GST No.'
        })

        self.fields['SBRNCHWEBSITE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the URL'
        })

        self.fields['SBRNCHPANNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter PAN No.'
        })

        self.fields['SBRNCHCODE'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Code'
        })

        # Fetch enabled Companies
        subbranch = CompanyMaster.objects.filter(DISPSTATUS=0).order_by('COMPNAME')

        # Add "Please select" as the first disabled option
        subbranch_choices = [('', '--- Please select ---')] + [(ag.pk, ag.COMPNAME) for ag in subbranch]

        self.fields['COMPID'] = forms.ChoiceField(
            choices=subbranch_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Company'
        )

        # Dropdown for State
        states = StateMaster.objects.filter(DISPSTATUS=0).order_by('STATEDESC')
        state_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        state_choices += [(state.STATEID, state.STATEDESC) for state in states]
        
        self.fields['STATEID'] = forms.ChoiceField(
            choices=state_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='State'
        )

class EmployeeMasterForm(forms.ModelForm):

    CATESEX_CHOICES=[
        ('', '--- Please Select ---'),
        (0, 'Male'),
        (1, 'Female'),
    ]

    CATEMSTATUS_CHOICES=[
        ('', '--- Please Select ---'),
        (0, 'Married'),
        (1, 'Unmarried'),
        (2, 'Widow'),
    ]

    CATEQTYPE_CHOICES = [
        ('', '--- Please Select ---'),
        (0, 'lliterate'),
        (1, 'Non-Matric'),
        (2, 'Matric'),
        (3, 'Senior Secondary'),
        (4, 'Graduate'),
        (5, 'Post Graduate'),
        (6, 'Doctorate'),
    ]

    CATEGTYPE_CHOICES = [
        ('', '--- Please Select ---'),
        (0, 'Not Eligible'),
        (1, 'Eligible'),
        (2, 'New Entrance'),
        (3, 'Left'),
    ]

    CATEMTYPE_CHOICES = [
        ('', '--- Please Select ---'),
        (0, 'Not Applicable'),
        (1, 'Applicable'),
        (2, 'New Entrance'),
    ]

    CATEATYPE_CHOICES = [
        ('', '--- Please Select ---'),
        (0, 'Not Applicable'),
        (1, 'Applicable'),
        (2, 'New Entrance'),
    ]

    CATEUTYPE_CHOICES = [
        ('', '--- Please Select ---'),
        (0, 'Yes'),
        (1, 'No'),
    ]

    DISPSTATUS_CHOICES_EMPLOYEE = [
        ('', '--- Please Select ---'),
        (0, 'On Roll'),
        (1, 'Resigned'),
        (2, 'Retired'),
        (3, 'Expired'),
    ]

    DISPSTATUS = forms.ChoiceField(
        choices=DISPSTATUS_CHOICES_EMPLOYEE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Display"
    )

    CATESEX = forms.ChoiceField(
        choices=CATESEX_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Gender"
    )

    CATEMSTATUS = forms.ChoiceField(
        choices=CATEMSTATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Marital Status"
    )

    CATEQTYPE = forms.ChoiceField(
        choices=CATEQTYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Qualification Type"
    )

    CATEGTYPE = forms.ChoiceField(
        choices=CATEGTYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Graduity"
    )

    CATEMTYPE = forms.ChoiceField(
        choices=CATEMTYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Medi Claim"
    )

    CATEATYPE = forms.ChoiceField(
        choices=CATEATYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Accident Type"
    )

    CATEUTYPE = forms.ChoiceField(
        choices=CATEUTYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Union Staff"
    )

    class Meta:
        model = EmployeeMaster
        fields = ['CATENAME', 'CATEADDR1', 'CATEADDR2', 'CATEADDR3', 'CATEADDR4',
                  'CATEADDR5', 'CATEMAIL', 'CATEPHN1', 'CATEPHN2', 'CATEPHN3', 'CATEPHN4', 'DISPSTATUS',
                  'CATESEX', 'CATEMSTATUS', 'CATEDOB', 'CATEAPPDT', 'CATECNDT', 'CATEQDESC', 'CATEGNAME',
                  'CATEACCNO', 'CATEEMPPF', 'CATEESINO', 'CATEPANNO', 'CATECNAME', 'REASON', 'CATENO',
                  'CATECODE', 'CATEREASON', 'CATERDATE', 'CATEGTYPE', 'CATEMTYPE', 'CATEATYPE', 'CATEUTYPE',
                  'CATEIDESC', 'CATELICNO', 'CATEAADHARNO', 'CATEUANNO', 'PFDATE', 'CATEQTYPE', 
                  'DEPTID', 'DSGNID', 'GRADEID', 'SBRNCHID', 'BLDGID', 'GRELMID',]
        
        labels = {
            'CATENAME': 'Employee Name',
            'CATEADDR1': 'Address line 1',
            'CATEADDR2': 'Address Line 2',
            'CATEADDR3': 'Address Line 3',
            'CATEADDR4': 'Address Line 4',
            'CATEADDR5': 'Address Line 5',
            'CATEMAIL': 'Email Address',
            'CATEPHN1': 'Phone Number 1',
            'CATEPHN2': 'Phone Number 2',
            'CATEPHN3': 'Phone Number 3',
            'CATEPHN4': 'Phone Number 4',
            'CATEDOB': 'Date of Birth',
            'CATEAPPDT': 'Appointment Date',
            'CATECNDT': 'Confirmation Date',
            'CATEQDESC': 'Qualification',
            'CATEGNAME': 'Guardian Name',
            'CATEACCNO': 'Bank Account Number',
            'CATEEMPPF': 'PF No.',
            'CATEESINO': 'ESI No.',
            'CATEPANNO': 'PAN No.',
            'CATECNAME': 'Contact Person Name',
            'REASON': 'Reason',

            'CATEREASON': 'Reason for Relieving',
            'CATERDATE': 'Resignation Date',
            'CATEIDESC': 'Identification Marks',
            'CATELICNO': 'LIC No.',
            'CATEAADHARNO': 'Aadhar No',
            'CATEUANNO': 'UAN No.',
            'PFDATE': 'PF Date',
            'CATENO': 'Increment',
            'CATECODE': 'Employee Code',

            'CATEQTYPE': 'Qualification Type',
            'DISPSTATUS': 'Display',
            'CATESEX': 'Gender',
            'CATEMSTATUS': 'Marital Status',
            'CATEGTYPE': 'Graduity',
            'CATEMTYPE': 'Medical Claim',
            'CATEATYPE': 'Accident Type',
            'CATEUTYPE': 'Union Staff',

            'DEPTID': 'Department',
            'DSGNID': 'Designation',
            'GRADEID': 'Grade',
            'SBRNCHID': 'Sub Branch',
            'BLDGID': 'Blood Group',
            'GRELMID': 'Relationship',
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeMasterForm, self).__init__(*args, **kwargs)

        self.fields['CATENAME'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Employee Name'
        })

        self.fields['CATEADDR1'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 1',
            'rows': 4
        })

        self.fields['CATEADDR2'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 2',
            'rows': 4
        })

        self.fields['CATEADDR3'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 3',
            'rows': 4
        })

        self.fields['CATEADDR4'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 4',
            'rows': 4
        })

        self.fields['CATEADDR5'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 5',
            'rows': 4
        })

        self.fields['CATEMAIL'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        })

        self.fields['CATEPHN1'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Mobile Number 1'
        })

        self.fields['CATEPHN2'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Mobile Number 2'
        })

        self.fields['CATEPHN3'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Mobile Number 3'
        })

        self.fields['CATEPHN4'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Mobile Number 4'
        })

        self.fields['CATEDOB'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })

        self.fields['CATEAPPDT'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })

        self.fields['CATECNDT'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })

        self.fields['CATEQDESC'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Qualification'
        })

        self.fields['CATEGNAME'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Guardian Name'
        })

        self.fields['CATEACCNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Bank Account No.'
        })

        self.fields['CATEEMPPF'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter PF No.'
        })

        self.fields['CATEESINO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter ESI No.'
        })

        self.fields['CATEPANNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter PAN No.'
        })

        self.fields['CATECNAME'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Contact Person Name'
        })

        self.fields['REASON'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Reason',
            'rows': 3
        })

        self.fields['CATEREASON'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Reason of Relieving',
            'rows': 3
        })

        self.fields['CATEIDESC'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Identification Marks',
            'rows': 3
        })

        self.fields['CATERDATE'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })

        self.fields['CATELICNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter LIC No.'
        })

        self.fields['CATEAADHARNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter AADHAR No.'
        })

        self.fields['CATEUANNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter UAN No.'
        })

        self.fields['PFDATE'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })

        self.fields['CATENO'].widget = forms.HiddenInput()

        self.fields['CATEUANNO'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter UAN No.'
        })

        # Dropdown for Department
        departments = DepartmentMaster.objects.filter(DISPSTATUS=0).order_by('DEPTDESC')
        department_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        department_choices += [(department.DEPTID, department.DEPTDESC) for department in departments]
        
        self.fields['DEPTID'] = forms.ChoiceField(
            choices=department_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Department'
        )

        # Dropdown for Designation
        designations = DesignationMaster.objects.filter(DISPSTATUS=0).order_by('DSGNDESC')
        designation_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        designation_choices += [(designation.DSGNID, designation.DSGNDESC) for designation in designations]
        
        self.fields['DSGNID'] = forms.ChoiceField(
            choices=designation_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Designation'
        )

        # Dropdown for Grade
        grades = GradeMaster.objects.filter(DISPSTATUS=0).order_by('GRADEDESC')
        grade_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        grade_choices += [(grade.GRADEID, grade.GRADEDESC) for grade in grades]
        
        self.fields['GRADEID'] = forms.ChoiceField(
            choices=grade_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Grade'
        )

        # Dropdown for Sub Branch
        subbranches = SubBranchMaster.objects.filter(DISPSTATUS=0).order_by('SBRNCHNAME')
        subbranch_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        subbranch_choices += [(subbranch.SBRNCHID, subbranch.SBRNCHNAME) for subbranch in subbranches]
        
        self.fields['SBRNCHID'] = forms.ChoiceField(
            choices=subbranch_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Sub Branch'
        )

        # Dropdown for Blood Group
        bloodgroups = BloodGroupMaster.objects.filter(DISPSTATUS=0).order_by('BLDGDESC')
        bloodgroup_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        bloodgroup_choices += [(bloodgroup.BLDGID, bloodgroup.BLDGDESC) for bloodgroup in bloodgroups]
        
        self.fields['BLDGID'] = forms.ChoiceField(
            choices=bloodgroup_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Blood Group'
        )

        # Dropdown for Relationship
        relationships = RelationshipMaster.objects.filter(DISPSTATUS=0).order_by('RELMDESC')
        relationship_choices = [(None, '--- Please Select ---')]  # Add default "Please select" option
        relationship_choices += [(relationship.RELMID, relationship.RELMDESC) for relationship in relationships]
        
        self.fields['GRELMID'] = forms.ChoiceField(
            choices=relationship_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Relationship'
        )
        
        if self.instance and self.instance.pk:
            self.fields['CATECODE'].widget.attrs.update({
                'readonly': True,
                'class': 'form-control text-muted bg-light',
            })

class SlabMasterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SlabMasterForm, self).__init__(*args, **kwargs)

        # Slab Date field
        self.fields['SLABMDATE'].widget = forms.DateTimeInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Select Date'
        })

        # Decimal fields
        decimal_fields = ['BAMT', 'HRAAMT', 'OAMT', 'PFEXPRN', 'ESIEXPRN', 'WAMT']
        for field_name in decimal_fields:
            self.fields[field_name].widget = forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'form-control',
                'placeholder': f'Enter {self.fields[field_name].label}'
            })

        # Dynamic Sub Branch dropdown
        subbranches = SubBranchMaster.objects.filter(DISPSTATUS=0).order_by('SBRNCHNAME')
        subbranch_choices = [('', '--- Please Select ---')] + [
            (sb.SBRNCHID, sb.SBRNCHNAME) for sb in subbranches
        ]
        self.fields['BRNCHID'] = forms.ChoiceField(
            choices=subbranch_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Sub Branch'
        )

        # Dynamically load employees based on branch
        if 'BRNCHID' in self.data:
            try:
                branch_id = int(self.data.get('BRNCHID'))
                employees = EmployeeMaster.objects.filter(DISPSTATUS=0, SBRNCHID=branch_id).order_by('CATENAME')
            except (ValueError, TypeError):
                employees = EmployeeMaster.objects.none()
        elif self.instance.pk:
            employees = EmployeeMaster.objects.filter(BRNCHID=self.instance.BRNCHID)
        else:
            employees = EmployeeMaster.objects.none()

        employee_choices = [('', '--- Please Select ---')] + [
            (emp.CATEID, emp.CATENAME) for emp in employees
        ]

        self.fields['CATEID'] = forms.ChoiceField(
            choices=employee_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Employee'
        )

    class Meta:
        model = SlabMaster
        fields = [
            'SLABMDATE', 'CATEID', 'BRNCHID', 'BAMT', 'HRAAMT',
            'OAMT', 'PFEXPRN', 'ESIEXPRN', 'WAMT'
        ]
        labels = {
            'SLABMDATE': 'Slab Date',
            'CATEID': 'Employee',
            'BRNCHID': 'Branch',
            'BAMT': 'Basic',
            'HRAAMT': 'HRA',
            'OAMT': 'O.Allow',
            'PFEXPRN': 'PF%',
            'ESIEXPRN': 'ESI%',
            'WAMT': 'W.Allow',
        }

class AttendanceDetailForm(forms.ModelForm):

    class Meta:
        model = AttendanceDetail
        fields = ['ATTNDATE', 'OTAMT', 'INCAMT', 'ATTNNOD', 'ABAMT', 'TEAAMT',
                  'FOODAMT', 'ODAMT']

        labels = {
            'ATTNDATE': 'Date',
            'OTAMT': 'OT(hrs)',
            'INCAMT': 'Inc.',
            'ATTNNOD': 'Absent',
            'ABAMT': 'Bonus(%)',
            'TEAAMT': 'Tea',
            'FOODAMT': 'Food',
            'ODAMT': 'O.Ded',
        }

    def __init__(self, *args, **kwargs):
        super(AttendanceDetailForm, self).__init__(*args, **kwargs)
        
        print(f"DEBUG: Form __init__ called with args: {args}")
        print(f"DEBUG: Form __init__ called with kwargs: {kwargs}")
        print(f"DEBUG: Form initial data: {self.initial}")

        self.fields['ATTNDATE'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
        
        # ✅ Set today as the default if it's a new form (not editing)
        if not self.initial.get('ATTNDATE') and not self.instance.pk:
            print("DEBUG: Setting default date to today")
            self.fields['ATTNDATE'].initial = timezone.now().date()
        elif self.initial and 'ATTNDATE' in self.initial:
            print(f"DEBUG: Processing initial date: {self.initial['ATTNDATE']}")
            # Handle initial values for auto-fill - ensure date is properly formatted
            try:
                # If it's a string, convert it to a date object
                if isinstance(self.initial['ATTNDATE'], str):
                    from datetime import datetime
                    date_obj = datetime.strptime(self.initial['ATTNDATE'], '%Y-%m-%d').date()
                    print(f"DEBUG: Converted string date to: {date_obj}")
                    self.fields['ATTNDATE'].initial = date_obj
                else:
                    print(f"DEBUG: Using existing date object: {self.initial['ATTNDATE']}")
                    self.fields['ATTNDATE'].initial = self.initial['ATTNDATE']
            except (ValueError, TypeError) as e:
                print(f"DEBUG: Error converting date: {e}")
                # If conversion fails, fall back to today's date
                self.fields['ATTNDATE'].initial = timezone.now().date()
        
        # Ensure the widget value is set correctly for HTML5 date input
        if self.fields['ATTNDATE'].initial:
            widget_value = self.fields['ATTNDATE'].initial.strftime('%Y-%m-%d')
            print(f"DEBUG: Setting widget value to: {widget_value}")
            self.fields['ATTNDATE'].widget.attrs['value'] = widget_value

        self.fields['OTAMT'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'O.Amt',
            'step': '0.01',
        })

        self.fields['INCAMT'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Inc.',
            'step': '0.01',
        })

        self.fields['ATTNNOD'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Absent Days',
            'step': '0.01',
        })

        self.fields['ABAMT'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bonus',
        })

        self.fields['TEAAMT'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tea Amt.',
            'step': '0.01',
        })

        self.fields['FOODAMT'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Food Amt.',
            'step': '0.01',
        })

        self.fields['ODAMT'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'O.Ded',
            'step': '0.01',
        })

        # Fetch enabled Subbranches
        subbranch = SubBranchMaster.objects.filter(DISPSTATUS=0).order_by('SBRNCHNAME')
        subbranch_choices = [('', '--- Please Select ---')] + [(ag.pk, ag.SBRNCHNAME) for ag in subbranch]
        self.fields['SBRNCHID'] = forms.TypedChoiceField(
            choices=subbranch_choices,
            coerce=int,
            empty_value='',
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Branch'
        )

        # Dynamically load Employees based on selected Sub Branch
        if 'SBRNCHID' in self.data:
            try:
                branch_id = int(self.data.get('SBRNCHID'))
                employees = EmployeeMaster.objects.filter(DISPSTATUS=0, SBRNCHID=branch_id).order_by('CATENAME')
            except (ValueError, TypeError):
                employees = EmployeeMaster.objects.none()
        elif self.instance.pk:
            employees = EmployeeMaster.objects.filter(DISPSTATUS=0, SBRNCHID=self.instance.SBRNCHID)
        elif self.initial and 'SBRNCHID' in self.initial:
            # Handle initial values (for auto-fill functionality)
            try:
                branch_id = int(self.initial.get('SBRNCHID'))
                employees = EmployeeMaster.objects.filter(DISPSTATUS=0, SBRNCHID=branch_id).order_by('CATENAME')
            except (ValueError, TypeError):
                employees = EmployeeMaster.objects.none()
        else:
            employees = EmployeeMaster.objects.none()

        employee_choices = [('', '--- Please Select ---')] + [
            (employee.CATEID, employee.CATENAME) for employee in employees
        ]

        self.fields['ECATEID'] = forms.TypedChoiceField(
            choices=employee_choices,
            coerce=int,
            empty_value='',
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Employee'
        )

        # Pre-select values if editing or if we have initial values
        if self.instance and self.instance.pk:
            self.fields['ECATEID'].initial = self.instance.ECATEID
            self.fields['SBRNCHID'].initial = self.instance.SBRNCHID
        elif self.initial:
            # Handle initial values for auto-fill
            if 'SBRNCHID' in self.initial:
                self.fields['SBRNCHID'].initial = self.initial['SBRNCHID']
            if 'ATTNDATE' in self.initial:
                self.fields['ATTNDATE'].initial = self.initial['ATTNDATE']


# Utility function to get current financial year
def get_current_accounting_year_start():
    today = datetime.date.today()
    return today.year - 1 if today.month < 4 else today.year

class PayrollMasterForm(forms.ModelForm):
    class Meta:
        model = PayrollMaster
        fields = ['COMPYID', 'PRMDATE', 'MONTHID', 'PRMSDATE', 'PRMEDATE', 'WRKDAYS', 'SBRNCHID']

        labels = {
            'COMPYID': 'Accounting Year',
            'PRMDATE': 'Date',
            'MONTHID': 'Month',
            'PRMSDATE': 'From',
            'PRMEDATE': 'Till',
            'WRKDAYS': 'Working Days',
        }

    def __init__(self, *args, accounting_year_id=None, company_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        # PRMDATE, PRMSDATE, PRMEDATE date fields
        date_widget_attrs = {'class': 'form-control', 'type': 'date'}
        self.fields['PRMDATE'].widget = forms.DateInput(attrs=date_widget_attrs)
        self.fields['PRMSDATE'].widget = forms.DateInput(attrs=date_widget_attrs)
        self.fields['PRMEDATE'].widget = forms.DateInput(attrs=date_widget_attrs)

        self.fields['WRKDAYS'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Days',
        })
        
        all_months = MonthMaster.objects.filter(DISPSTATUS=0).order_by('DISPORDER')
        available_months = all_months

        # self.fields['MONTHID'] = forms.TypedChoiceField(
        #     choices=[('', '--- Please select ---')] + [(m.pk, m.MONTHNAME) for m in available_months],
        #     coerce=int,
        #     empty_value='',
        #     widget=forms.Select(attrs={'class': 'form-control'}),
        #     label='Month'
        # )
        self.fields['MONTHID'] = forms.ChoiceField(
            choices=[('', '--- Please select ---')] + [(m.pk, m.MONTHNAME) for m in available_months],
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Month',
            required=True,
            initial=''
        )


        if accounting_year_id:
            year_obj = AccountingYear.objects.filter(YRID=accounting_year_id).first()
            if year_obj:
                year_label = year_obj.YRDESC
                self.fields['COMPYID'] = forms.TypedChoiceField(
                    choices=[(year_obj.YRID, year_label)],
                    coerce=int,
                    label="Accounting Year",
                    widget=forms.Select(attrs={'class': 'form-control'}),
                    initial=year_obj.YRID
                )

        # 🔥 Subbranch choices filtered by company_id
        if company_id:
            try:
                company_id = int(company_id)
                subbranches = SubBranchMaster.objects.filter(COMPID=company_id, DISPSTATUS=0).order_by('SBRNCHNAME')
            except ValueError:
                subbranches = SubBranchMaster.objects.none()
        else:
            subbranches = SubBranchMaster.objects.none()

        self.fields['SBRNCHID'] = forms.ChoiceField(
            choices=[('', '--- Please Select ---')] + [(sb.SBRNCHID, sb.SBRNCHNAME) for sb in subbranches],
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'subbranch'}),
            label='Branch',
            required=True,
        )
    
# class AspNetUsersForm(forms.ModelForm):
#     class Meta:
#         model = AspNetUsers
#         fields = ['username', 'password', 'FirstName', 'LastName', 'Email']
#         labels = {
#             'username': 'Username',
#             'password': 'Password',
#             'FirstName': 'First Name',
#             'LastName': 'Last Name',
#             'Email': 'Email',
#             # 'ubrnch_name': 'Branch',
#             # 'dept_name': 'Department',
#         }

#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Username',
#                 'required': 'required'
#             }),
#             'password': forms.PasswordInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Password',
#                 'required': 'required'
#             }),
#                 'FirstName': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter First Name',
#                 'required': 'required'
#             }),
#                 'LastName': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Last Name',
#                 'required': 'required'
#             }),
#                 'Email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Email-id',
#                 'required': 'required'
#             }),
#         }

    # def __init__(self, *args, **kwargs):
    #     super(AspNetUsersForm, self).__init__(*args, **kwargs)

    #     # Sub Branch Choices
    #     sub_branches = SubBranchMaster.objects.filter(DISPSTATUS=0).order_by('SBRNCHID')
    #     sub_branch_choices = [('', '--- Please Select ---')] + [(sb.SBRNCHNAME, sb.SBRNCHNAME) for sb in sub_branches]

    #     self.fields['ubrnch_name'] = forms.ChoiceField(
    #         choices=sub_branch_choices,
    #         widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
    #         label='Sub Branch'
    #     )

    #     # Department Choices
    #     departments = DepartmentMaster.objects.filter(DISPSTATUS=0).order_by('DEPTID')
    #     dept_choices = [('', '--- Please Select ---')] + [(d.DEPTDESC, d.DEPTDESC) for d in departments]

    #     self.fields['dept_name'] = forms.ChoiceField(
    #         choices=dept_choices,
    #         widget=forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
    #         label='Department'
    #     )

    #     # Set initial values when editing (important!)
    #     if self.instance and self.instance.pk:
    #         self.fields['ubrnch_name'].initial = self.instance.ubrnch_name
    #         self.fields['dept_name'].initial = self.instance.dept_name

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'mobile', 'username', 'password1', 'password2',
        ]
        
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'mobile': 'Phone Number',
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter First Name',
            'required':True
        })

        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Last Name'
        })

        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email Address',
            'required':True
        })

        self.fields['mobile'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Phone Number'
        })

        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })

        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })

        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'username', 'is_superuser', 'is_staff']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'mobile': 'Phone Number',
            'username': 'Username',
            'is_superuser': 'Is Superuser',
            'is_staff': 'Is Staff',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter First Name',
            'required':True
        })

        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Last Name'
        })

        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email Address',
            'required':True
        })

        self.fields['mobile'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Phone Number'
        })

        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })

        self.fields['is_superuser'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })

        self.fields['is_staff'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })

User = get_user_model()

class AdminPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm New Password')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password1")
        pw2 = cleaned_data.get("new_password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user