from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CompanyMaster
from .forms import CompanyMasterForm
from .models import DepartmentMaster
from .forms import DepartmentMasterForm
from .models import DesignationMaster
from .forms import DesignationMasterForm
from .models import StateMaster
from .forms import StateMasterForm
from .models import GradeMaster
from .forms import GradeMasterForm
from .models import PayHeadTypeMaster
from .forms import PayHeadTypeMasterForm
from .models import AccountGroupMaster
from .forms import AccountGroupMasterForm
from .models import AdvanceTypeMaster
from .forms import AdvanceTypeMasterForm
from .models import BloodGroupMaster
from .forms import BloodGroupMasterForm
from .models import RelationshipMaster
from .forms import RelationshipMasterForm
from .models import AccountHeadMaster
from .forms import AccountHeadMasterForm
from .models import LocationMaster
from .forms import LocationMasterForm
from django.db.models.functions import TruncDate 
from .models import PayHeadMaster
from .forms import PayHeadMasterForm
from .models import LeaveHeadMaster
from .forms import LeaveHeadMasterForm
from django.forms import inlineformset_factory
from django.db import transaction   #Both deletion happens samely as a unit
from .models import LeaveHeadDetail
from .forms import LeaveHeadDetailForm
from .models import SubBranchMaster
from .forms import SubBranchMasterForm
from .models import EmployeeMaster
from .forms import EmployeeMasterForm
from .models import SlabMaster
from .forms import SlabMasterForm
from .db_utils import call_ratecard_proc  # Import the utility function
from .models import AttendanceDetail
from .forms import AttendanceDetailForm
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.utils.dateparse import parse_date       
from .db_utils import call_attendance_proc  # Import the utility function  
from django.core.paginator import Paginator                     
from .models import PayrollMaster
from .forms import PayrollMasterForm
from .models import PayrollDetail
from .models import PayrollPayheadDetail
from decimal import Decimal
from num2words import num2words  # Install via pip if needed
from django.db import transaction
from .signals import process_payroll
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from django.db.models import Max, Q
# from .models import AspNetUsers
# from .forms import AspNetUsersForm
from django.core.paginator import Paginator
from urllib.parse import urlencode
from .models import AccountingYear
from .models import CompanyAccountingDetail
from django.contrib import messages

from django.utils.timezone import make_aware, get_current_timezone
from django.utils import timezone
from pytz import timezone as pytz_timezone
from datetime import datetime, time, timezone as dt_timezone

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, get_user_model
from .models import CustomUser
from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from django.contrib.auth import logout
import traceback

from .utils import process_login_date_and_get_compyid, admin_required
from .forms import AdminPasswordChangeForm
from django.utils.dateformat import format as date_format

from django.utils.timezone import localtime


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TempReportID

# Create your views here.

# Index Page for StateMaster
def company_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page', 1)

    # Filtered QuerySet
    company_qs = CompanyMaster.objects.filter(COMPNAME__icontains=search_query)

    # Pagination
    paginator = Paginator(company_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Prepare query string (excluding 'page')
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "Companies/company_index.html", {
        "company_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add Company
def add_company(request):
    if request.method == "POST":
        form = CompanyMasterForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.CUSRID = request.user.username
            company.LMUSRID = request.user.username
            company.save()
            return redirect('company_index')
    else:
        form = CompanyMasterForm()

    return render(request, "Companies/add_company.html", {"form": form})

# Edit Company
def edit_company(request, id):
    company = get_object_or_404(CompanyMaster, pk=id)

    if request.method == "POST":
        form = CompanyMasterForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.LMUSRID = request.user.username
            company.save()
            return redirect('company_index')
    else:
        form = CompanyMasterForm(instance=company)

    return render(request, "Companies/edit_company.html", {"form": form})

# Delete Company
def delete_company(request, id):
    company = get_object_or_404(CompanyMaster, pk=id)

    # Check if the state is referenced in Sub Branch Master
    is_used = SubBranchMaster.objects.filter(COMPID=company.COMPID).exists()

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Company. It is referenced in one or more forms.")
            return redirect('company_index')
        else:
            company.delete()
            return redirect('company_index')
    return render(request, 'Companies/delete_company.html', {'company': company, 'is_used': is_used})

#----------------------------------------------------------------------------------------------------------------

# Index Page for DepartmentMaster

def department_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))  # Default to 10
    page_number = request.GET.get('page')

    # Filter departments
    department_qs = DepartmentMaster.objects.filter(DEPTDESC__icontains=search_query)

    # Paginate results
    paginator = Paginator(department_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string (excluding 'page') for pagination links
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "Departments/department_index.html", {
        "department_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add Department
def add_department(request):
    if request.method == "POST":
        form = DepartmentMasterForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.CUSRID = request.user.username
            department.LMUSRID = request.user.username
            department.save()
            return redirect('department_index')
    else:
        form = DepartmentMasterForm()

    return render(request, "Departments/add_department.html", {"form": form})

# Edit Department
def edit_department(request, id):
    department = get_object_or_404(DepartmentMaster, pk=id)

    if request.method == "POST":
        form = DepartmentMasterForm(request.POST, instance=department)
        if form.is_valid():
            department = form.save(commit=False)
            department.LMUSRID = request.user.username
            department.save()
            return redirect('department_index')
    else:
        form = DepartmentMasterForm(instance=department)

    return render(request, "Departments/edit_department.html", {"form": form})

# Delete Department
def delete_department(request, id):
    department = get_object_or_404(DepartmentMaster, pk=id)

    # Check if the department is referenced in Employee Master
    is_used = EmployeeMaster.objects.filter(DEPTID=department.DEPTID).exists()

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Department. It is referenced in one or more forms.")
            return redirect('department_index')
        else:
            department.delete()
            return redirect('department_index')
    return render(request, 'Departments/delete_department.html', {'department': department, 'is_used': is_used})

#-----------------------------------------------------------------------------------------------------------------

# Index Page for DesignationMaster

def designation_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))  # Default 10 if not set
    page_number = request.GET.get('page', 1)

    # Filter designations based on search query
    designation_qs = DesignationMaster.objects.filter(DSGNDESC__icontains=search_query)

    # Paginate the queryset
    paginator = Paginator(designation_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string for pagination links (excluding 'page')
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "Designations/designation_index.html", {
        "designations": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add Designation
def add_designation(request):
    if request.method == "POST":
        form = DesignationMasterForm(request.POST)
        if form.is_valid():
            designation = form.save(commit=False)
            designation.CUSRID = request.user.username
            designation.LMUSRID = request.user.username
            designation.save()
            return redirect('designation_index')
    else:
        form = DesignationMasterForm()

    return render(request, "Designations/add_designation.html", {"form": form})

# Edit Designation
def edit_designation(request, id):
    designation = get_object_or_404(DesignationMaster, pk=id)

    if request.method == "POST":
        form = DesignationMasterForm(request.POST, instance=designation)
        if form.is_valid():
            designation = form.save(commit=False)
            designation.LMUSRID = request.user.username
            designation.save()
            return redirect('designation_index')
    else:
        form = DesignationMasterForm(instance=designation)

    return render(request, "Designations/edit_designation.html", {"form": form})

# Delete Designation
def delete_designation(request, id):
    designation = get_object_or_404(DesignationMaster, pk=id)

    # Check if the state is referenced in CompanyMaster or LocationMaster
    is_used_in_lheaddetail = LeaveHeadDetail.objects.filter(DSGNID=designation.DSGNID).exists()
    is_used_in_employee = EmployeeMaster.objects.filter(DSGNID=designation.DSGNID).exists()

    is_used = is_used_in_lheaddetail or is_used_in_employee

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Designation. It is referenced in one or more forms.")
            return redirect('designation_index')
        else:
            designation.delete()
            return redirect('designation_index')
    return render(request, 'Designations/delete_designation.html', {'designation': designation, 'is_used': is_used})

#-----------------------------------------------------------------------------------------------------------------

# Index Page for StateMaster
def state_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page', 1)

    # Filter states
    state_qs = StateMaster.objects.filter(STATEDESC__icontains=search_query)

    # Paginate
    paginator = Paginator(state_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Generate query string (excluding 'page')
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "States/state_index.html", {
        "states": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add State Form
def add_state(request):
    if request.method == "POST":
        form = StateMasterForm(request.POST)
        if form.is_valid():
            state = form.save(commit=False)
            state.CUSRID = request.user.username
            state.LMUSRID = request.user.username
            state.save()
            return redirect('state_index')
    else:
        form = StateMasterForm()

    return render(request, "States/add_state.html", {"form": form})

# Edit State Form
def edit_state(request, id):
    state = get_object_or_404(StateMaster, pk=id)

    if request.method == "POST":
        form = StateMasterForm(request.POST, instance=state)
        if form.is_valid():
            state = form.save(commit=False)
            state.LMUSRID = request.user.username
            state.save()
            return redirect('state_index')
    else:
        form = StateMasterForm(instance=state)

    return render(request, "States/edit_state.html", {"form": form})

# Delete State
def delete_state(request, id):
    state = get_object_or_404(StateMaster, pk=id)

    # Check if the state is referenced in CompanyMaster or LocationMaster
    is_used_in_company = CompanyMaster.objects.filter(STATEID=state.STATEID).exists()
    is_used_in_location = LocationMaster.objects.filter(STATEID=state.STATEID).exists()
    is_used_in_subbranch = SubBranchMaster.objects.filter(STATEID=state.STATEID).exists()

    is_used = is_used_in_company or is_used_in_location or is_used_in_subbranch

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete State. It is referenced in one or more companies, locations and branches.")
            return redirect('state_index')
        else:
            state.delete()
            return redirect('state_index')

    return render(request, 'States/delete_state.html', {'state': state, 'is_used': is_used})

#------------------------------------------------------------------------------------------------------------------------

# Index Page for GradeMaster
def grade_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page', 1)

    # Filter queryset
    grade_qs = GradeMaster.objects.filter(GRADEDESC__icontains=search_query)

    # Set up pagination
    paginator = Paginator(grade_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string excluding 'page'
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "Grades/grade_index.html", {
        "grade_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add Grade
def add_grade(request):
    if request.method == "POST":
        form = GradeMasterForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.CUSRID = request.user.username
            grade.LMUSRID = request.user.username
            grade.save()
            return redirect('grade_index')
    else:
        form = GradeMasterForm()

    return render(request, "Grades/add_grade.html", {"form": form})

# Edit Grade
def edit_grade(request, id):
    grade = get_object_or_404(GradeMaster, pk=id)

    if request.method == "POST":
        form = GradeMasterForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.LMUSRID = request.user.username
            grade.save()
            return redirect('grade_index')
    else:
        form = GradeMasterForm(instance=grade)

    return render(request, "Grades/edit_grade.html", {"form": form})

# Delete Grade
def delete_grade(request, id):
    grade = get_object_or_404(GradeMaster, pk=id)

    # Check if the Grade is referenced in Employee Master
    is_used = EmployeeMaster.objects.filter(GRADEID=grade.GRADEID).exists()

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Grade. It is referenced in one or more forms.")
            return redirect('grade_index')
        else:
            grade.delete()
            return redirect('grade_index')
    return render(request, 'Grades/delete_grade.html', {'grade': grade, 'is_used': is_used})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for PayHeadTypeMaster
def payheadtype_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')

    # Filter queryset
    payheadtype_qs = PayHeadTypeMaster.objects.filter(PAYHTDESC__icontains=search_query)

    # Paginate
    paginator = Paginator(payheadtype_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string without 'page'
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "PayHeadTypes/payheadtype_index.html", {
        "payheadtype_index": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "query_string": query_string,
    })

# Add PayHeadType
def add_payheadtype(request):
    if request.method == "POST":
        form = PayHeadTypeMasterForm(request.POST)
        if form.is_valid():
            payheadtype = form.save(commit=False)
            payheadtype.CUSRID = request.user.username
            payheadtype.LMUSRID = request.user.username
            payheadtype.save()
            return redirect('payheadtype_index')
    else:
        form = PayHeadTypeMasterForm()

    return render(request, "PayHeadTypes/add_payheadtype.html", {"form": form})

# Edit PayHeadType
def edit_payheadtype(request, id):
    payheadtype = get_object_or_404(PayHeadTypeMaster, pk=id)

    if request.method == "POST":
        form = PayHeadTypeMasterForm(request.POST, instance=payheadtype)
        if form.is_valid():
            payheadtype = form.save(commit=False)
            payheadtype.LMUSRID = request.user.username
            payheadtype.save()
            return redirect('payheadtype_index')
    else:
        form = PayHeadTypeMasterForm(instance=payheadtype)

    return render(request, "PayHeadTypes/edit_payheadtype.html", {"form": form})

# Delete PayHeadType
def delete_payheadtype(request, id):
    payheadtype = get_object_or_404(PayHeadTypeMaster, pk=id)

    # Check if the state is referenced in Payhead
    is_used = PayHeadMaster.objects.filter(PAYHTID=payheadtype.PAYHTID).exists()

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Payhead Type. It is referenced in one or more forms.")
            return redirect('payheadtype_index')
        else:
            payheadtype.delete()
            return redirect('payheadtype_index')
        
    return render(request, 'PayHeadTypes/delete_payheadtype.html', {'payheadtype': payheadtype, 'is_used': is_used})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for AccountGroupMaster
def accountgroup_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')

    accountgroup_queryset = AccountGroupMaster.objects.filter(ACHEADGDESC__icontains=search_query)
    paginator = Paginator(accountgroup_queryset, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string excluding 'page' so it can be reused in pagination links
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "AccountGroups/accountgroup_index.html", {
        "accountgroup_index": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "query_string": query_string,
    })

# Add Account group
def add_accountgroup(request):
    if request.method == "POST":
        form = AccountGroupMasterForm(request.POST)
        if form.is_valid():
            accountgroup = form.save(commit=False)
            accountgroup.CUSRID = request.user.username
            accountgroup.LMUSRID = request.user.username
            accountgroup.save()
            return redirect('accountgroup_index')
    else:
        form = AccountGroupMasterForm()

    return render(request, "AccountGroups/add_accountgroup.html", {"form": form})

# Edit Account group
def edit_accountgroup(request, id):
    accountgroup = get_object_or_404(AccountGroupMaster, pk=id)

    if request.method == "POST":
        form = AccountGroupMasterForm(request.POST, instance=accountgroup)
        if form.is_valid():
            accountgroup = form.save(commit=False)
            accountgroup.LMUSRID = request.user.username
            accountgroup.save()
            return redirect('accountgroup_index')
    else:
        form = AccountGroupMasterForm(instance=accountgroup)

    return render(request, "AccountGroups/edit_accountgroup.html", {"form": form})

# Delete Account group
def delete_accountgroup(request, id):
    accountgroup = get_object_or_404(AccountGroupMaster, pk=id)

    # Check if the state is referenced in AccountHead
    is_used = AccountHeadMaster.objects.filter(ACHEADGID=accountgroup.ACHEADGID).exists()
    
    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Account Group. It is referenced in one or more Forms.")
            return redirect('accountgroup_index')
        else:
            accountgroup.delete()
            return redirect('accountgroup_index')
    return render(request, 'AccountGroups/delete_accountgroup.html', {'accountgroup': accountgroup, 'is_used': is_used})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for AdvanceTypesMaster
def advancetype_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page', 1)

    advancetype_qs = AdvanceTypeMaster.objects.filter(ADVTDESC__icontains=search_query)

    paginator = Paginator(advancetype_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string excluding 'page'
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "AdvanceTypes/advancetype_index.html", {
        "advancetype_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add Advance Type
def add_advancetype(request):
    if request.method == "POST":
        form = AdvanceTypeMasterForm(request.POST)
        if form.is_valid():
            advancetype = form.save(commit=False)
            advancetype.CUSRID = request.user.username
            advancetype.LMUSRID = request.user.username
            advancetype.save()
            return redirect('advancetype_index')
    else:
        form = AdvanceTypeMasterForm()

    return render(request, "AdvanceTypes/add_advancetype.html", {"form": form})

# Edit Advance Type
def edit_advancetype(request, id):
    advancetype = get_object_or_404(AdvanceTypeMaster, pk=id)

    if request.method == "POST":
        form = AdvanceTypeMasterForm(request.POST, instance=advancetype)
        if form.is_valid():
            advancetype = form.save(commit=False)
            advancetype.LMUSRID = request.user.username
            advancetype.save()
            return redirect('advancetype_index')
    else:
        form = AdvanceTypeMasterForm(instance=advancetype)

    return render(request, "AdvanceTypes/edit_advancetype.html", {"form": form})

# Delete Advance Type
def delete_advancetype(request, id):
    advancetype = get_object_or_404(AdvanceTypeMaster, pk=id)
    if request.method == 'POST':
        advancetype.delete()
        return redirect('advancetype_index')
    return render(request, 'AdvanceTypes/delete_advancetype.html', {'object': advancetype})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for BloodGroupMaster
def bloodgroup_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))  # Default: 10 items per page
    page_number = request.GET.get('page', 1)

    # Filter results
    bloodgroup_qs = BloodGroupMaster.objects.filter(BLDGDESC__icontains=search_query)

    # Paginate
    paginator = Paginator(bloodgroup_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Maintain query string for pagination links
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "BloodGroups/bloodgroup_index.html", {
        "bloodgroup_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add BloodGroup
def add_bloodgroup(request):
    if request.method == "POST":
        form = BloodGroupMasterForm(request.POST)
        if form.is_valid():
            bloodgroup = form.save(commit=False)
            bloodgroup.CUSRID = request.user.username
            bloodgroup.LMUSRID = request.user.username
            bloodgroup.save()
            return redirect('bloodgroup_index')
    else:
        form = BloodGroupMasterForm()

    return render(request, "BloodGroups/add_bloodgroup.html", {"form": form})

# Edit BloodGroup
def edit_bloodgroup(request, id):
    bloodgroup = get_object_or_404(BloodGroupMaster, pk=id)

    if request.method == "POST":
        form = BloodGroupMasterForm(request.POST, instance=bloodgroup)
        if form.is_valid():
            bloodgroup = form.save(commit=False)
            bloodgroup.LMUSRID = request.user.username
            bloodgroup.save()
            return redirect('bloodgroup_index')
    else:
        form = BloodGroupMasterForm(instance=bloodgroup)

    return render(request, "BloodGroups/edit_bloodgroup.html", {"form": form})

# Delete BloodGroup
def delete_bloodgroup(request, id):
    bloodgroup = get_object_or_404(BloodGroupMaster, pk=id)

    # Check if the bloodgroup is referenced in employee Master
    is_used = BloodGroupMaster.objects.filter(BLDGID=bloodgroup.BLDGID).exists()

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Blood group. It is referenced in one or more forms.")
            return redirect('bloodgroup_index')
        else:
            bloodgroup.delete()
            return redirect('bloodgroup_index')
    return render(request, 'BloodGroups/delete_bloodgroup.html', {'bloodgroup': bloodgroup, 'is_used': is_used})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for RelationshipMaster
def relationship_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))  # Default: 10 per page
    page_number = request.GET.get('page', 1)

    # Filter based on search query
    relationships = RelationshipMaster.objects.filter(RELMDESC__icontains=search_query)

    # Paginate the filtered results
    paginator = Paginator(relationships, per_page)
    page_obj = paginator.get_page(page_number)

    # Build querystring for pagination links (excluding 'page')
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "Relationships/relationship_index.html", {
        "relationship_index": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "query_string": query_string,
    })

# Add Relationship
def add_relationship(request):
    if request.method == "POST":
        form = RelationshipMasterForm(request.POST)
        if form.is_valid():
            relationship = form.save(commit=False)
            relationship.CUSRID = request.user.username
            relationship.LMUSRID = request.user.username
            relationship.save()
            return redirect('relationship_index')
    else:
        form = RelationshipMasterForm()

    return render(request, "Relationships/add_relationship.html", {"form": form})

# Edit Relationship
def edit_relationship(request, id):
    relationship = get_object_or_404(RelationshipMaster, pk=id)

    if request.method == "POST":
        form = RelationshipMasterForm(request.POST, instance=relationship)
        if form.is_valid():
            relationship = form.save(commit=False)
            relationship.LMUSRID = request.user.username
            relationship.save()
            return redirect('relationship_index')
    else:
        form = RelationshipMasterForm(instance=relationship)

    return render(request, "Relationships/edit_relationship.html", {"form": form})

# Delete Relationship
def delete_relationship(request, id):
    relationship = get_object_or_404(RelationshipMaster, pk=id)

    # Check if the state is referenced in Sub Branch Master
    is_used = EmployeeMaster.objects.filter(GRELMID=relationship.RELMID).exists()

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Relationship. It is referenced in one or more forms.")
            return redirect('relationship_index')
        else:
            relationship.delete()
            return redirect('relationship_index')
    return render(request, 'Relationships/delete_relationship.html', {'relationship': relationship, 'is_used': is_used})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for AccountHeadMaster
def accounthead_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')

    accounthead = AccountHeadMaster.objects.filter(ACHEADDESC__icontains=search_query)

    paginator = Paginator(accounthead, per_page)
    page_obj = paginator.get_page(page_number)

    # Keep other query params (like `search`) in pagination links
    query_dict = request.GET.copy()
    if 'page' in query_dict:
        del query_dict['page']
    query_string = '&' + urlencode(query_dict)

    context = {
        "accounthead_index": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "query_string": query_string,
    }

    return render(request, "AccountHeads/accounthead_index.html", context)

# Add AccountHead
def add_accounthead(request):
    if request.method == "POST":
        form = AccountHeadMasterForm(request.POST)
        if form.is_valid():
            accounthead = form.save(commit=False)
            accounthead.CUSRID = request.user.username
            accounthead.LMUSRID = request.user.username
            accounthead.save()
            return redirect('accounthead_index')
    else:
        form = AccountHeadMasterForm()

    return render(request, "AccountHeads/add_accounthead.html", {"form": form})

# Edit AccountHead
def edit_accounthead(request, id):
    accounthead = get_object_or_404(AccountHeadMaster, pk=id)

    if request.method == "POST":
        form = AccountHeadMasterForm(request.POST, instance=accounthead)
        if form.is_valid():
            accounthead = form.save(commit=False)
            accounthead.LMUSRID = request.user.username
            accounthead.save()
            return redirect('accounthead_index')
    else:
        form = AccountHeadMasterForm(instance=accounthead)

    return render(request, "AccountHeads/edit_accounthead.html", {"form": form})

# Delete AccountHead
def delete_accounthead(request, id):
    accounthead = get_object_or_404(AccountHeadMaster, pk=id)
    if request.method == 'POST':
        accounthead.delete()
        return redirect('accounthead_index')
    return render(request, 'AccountHeads/delete_accounthead.html', {'object': accounthead})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for LocationMaster
def location_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))  # default to 10
    page_number = request.GET.get('page', 1)

    # Filter results
    location_qs = LocationMaster.objects.filter(LOCTDESC__icontains=search_query)

    # Pagination
    paginator = Paginator(location_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Get query string excluding page
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    # Build state mapping
    states = {state.pk: state.STATEDESC for state in StateMaster.objects.all()}

    return render(request, "Locations/location_index.html", {
        "location_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "states": states,
        "search_query": search_query,
    })

# Add Location
def add_location(request):
    if request.method == "POST":
        form = LocationMasterForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.CUSRID = request.user.username
            location.LMUSRID = request.user.username
            location.save()
            return redirect('location_index')
    else:
        form = LocationMasterForm()

    return render(request, "Locations/add_location.html", {"form": form})

# Edit Location
def edit_location(request, id):
    location = get_object_or_404(LocationMaster, pk=id)

    if request.method == "POST":
        form = LocationMasterForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.LMUSRID = request.user.username
            location.save()
            return redirect('location_index')
    else:
        form = LocationMasterForm(instance=location)

    return render(request, "Locations/edit_location.html", {"form": form})

# Delete Location
def delete_location(request, id):
    location = get_object_or_404(LocationMaster, pk=id)
    if request.method == 'POST':
        location.delete()
        return redirect('location_index')
    return render(request, 'Locations/delete_location.html', {'object': location})

#-------------------------------------------------------------------------------------------------------------------------

# Index Page for PayHeadMaster
def payhead_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')

    # Filter the queryset
    payhead_qs = PayHeadMaster.objects.filter(PAYHDESC__icontains=search_query)

    # Paginate the queryset
    paginator = Paginator(payhead_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build querystring for pagination links (excluding 'page')
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "PayHeads/payhead_index.html", {
        "payhead_index": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "query_string": query_string,
    })

# Add PayHead
def add_payhead(request):
    if request.method == "POST":
        form = PayHeadMasterForm(request.POST)
        if form.is_valid():
            payhead = form.save(commit=False)
            payhead.CUSRID = request.user.username
            payhead.LMUSRID = request.user.username
            payhead.save()
            return redirect('payhead_index')
    else:
        form = PayHeadMasterForm()

    return render(request, "PayHeads/add_payhead.html", {"form": form})

# Edit PayHead
def edit_payhead(request, id):
    payhead = get_object_or_404(PayHeadMaster, pk=id)

    if request.method == "POST":
        form = PayHeadMasterForm(request.POST, instance=payhead)
        if form.is_valid():
            payhead = form.save(commit=False)
            payhead.LMUSRID = request.user.username
            payhead.save()
            return redirect('payhead_index')
    else:
        form = PayHeadMasterForm(instance=payhead)

    return render(request, "PayHeads/edit_payhead.html", {"form": form})

# Delete PayHead
def delete_payhead(request, id):
    payhead = get_object_or_404(PayHeadMaster, pk=id)
    if request.method == 'POST':
        payhead.delete()
        return redirect('payhead_index')
    return render(request, 'PayHeads/delete_payhead.html', {'object': payhead})

#------------------------------------------------------------------------------------------------------------------------

def leavehead_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')

    # Filter based on search
    leavehead_qs = LeaveHeadMaster.objects.filter(LHMDESC__icontains=search_query)

    # Paginate
    paginator = Paginator(leavehead_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string for pagination (exclude 'page')
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, 'LeaveHeads/leavehead_index.html', {
        "leavehead_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

LeaveHeadDetailFormSet = inlineformset_factory(
    LeaveHeadMaster,
    LeaveHeadDetail,
    form=LeaveHeadDetailForm,
    extra=1,
    can_delete=True
)

def add_leavehead(request):
    if request.method == 'POST':
        master_form = LeaveHeadMasterForm(request.POST)
        detail_formset = LeaveHeadDetailFormSet(request.POST, queryset=LeaveHeadDetail.objects.none())

        if master_form.is_valid() and detail_formset.is_valid():
            master = master_form.save()
            master.CUSRID = request.user.username
            master.LMUSRID = request.user.username
            master.save()

            for detail_form in detail_formset:
                detail = detail_form.save(commit=False)
                detail.LHMID = master
                detail.save()
            return redirect('leavehead_index')
    else:
        master_form = LeaveHeadMasterForm()
        detail_formset = LeaveHeadDetailFormSet(queryset=LeaveHeadDetail.objects.none())

    return render(request, 'LeaveHeads/add_leavehead.html', {
        'master_form': master_form,
        'detail_formset': detail_formset,
    })

def edit_leavehead(request, id):
    leavehead = get_object_or_404(LeaveHeadMaster, pk=id)
    
    if request.method == 'POST':
        master_form = LeaveHeadMasterForm(request.POST, instance=leavehead)
        detail_formset = LeaveHeadDetailFormSet(
            request.POST,
            instance=leavehead,
            queryset=LeaveHeadDetail.objects.filter(LHMID=leavehead)
        )
        
        if master_form.is_valid() and detail_formset.is_valid():
            master = master_form.save(commit=False)
            master.LMUSRID = request.user.username
            master.save()
            # Save formset instances while handling deletions
            instances = detail_formset.save(commit=False)
            for instance in instances:
                instance.LHMID = master  # Ensure foreign key is set
                instance.save()
            
            # Handle deleted instances
            for instance in detail_formset.deleted_objects:
                instance.delete()
                
            return redirect('leavehead_index')
    else:
        master_form = LeaveHeadMasterForm(instance=leavehead)
        detail_formset = LeaveHeadDetailFormSet(
            instance=leavehead,
            queryset=LeaveHeadDetail.objects.filter(LHMID=leavehead))
    
    return render(request, 'LeaveHeads/edit_leavehead.html', {
        'master_form': master_form,
        'detail_formset': detail_formset,
        'edit_mode': True,  # Useful for template conditional rendering
    })

def delete_leavehead(request, id):
    leavehead = get_object_or_404(LeaveHeadMaster, pk=id)

    if request.method == 'POST':
        with transaction.atomic():
            LeaveHeadDetail.objects.filter(LHMID=leavehead).delete()
            leavehead.delete()
        return redirect('leavehead_index')

    return render(request, 'LeaveHeads/delete_leavehead.html', {'object': leavehead})

#--------------------------------------------------------------------------------------------------------------------------

# Index Page for Sub Branch
def subbranch_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))  # Default to 10 items per page
    page_number = request.GET.get('page')

    # Filter subbranches
    subbranch_qs = SubBranchMaster.objects.filter(SBRNCHNAME__icontains=search_query)

    # Pagination setup
    paginator = Paginator(subbranch_qs, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string for pagination (excluding 'page')
    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "SubBranches/subbranch_index.html", {
        "subbranch_index": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })

# Add Subbranch
def add_subbranch(request):
    if request.method == "POST":
        form = SubBranchMasterForm(request.POST)
        if form.is_valid():
            subbranch = form.save(commit=False)
            subbranch.CUSRID = request.user.username
            subbranch.LMUSRID = request.user.username
            subbranch.save()
            return redirect('subbranch_index')
        else:
            print("form:", form.errors)
    else:
        form = SubBranchMasterForm()

    return render(request, "SubBranches/add_subbranch.html", {"form": form})

# Edit Subbranch
def edit_subbranch(request, id):
    subbranch = get_object_or_404(SubBranchMaster, pk=id)

    if request.method == "POST":
        form = SubBranchMasterForm(request.POST, instance=subbranch)
        if form.is_valid():
            subbranch = form.save(commit=False)
            subbranch.LMUSRID = request.user.username
            subbranch.save()
            return redirect('subbranch_index')
    else:
        form = SubBranchMasterForm(instance=subbranch)

    return render(request, "SubBranches/edit_subbranch.html", {"form": form})

# Delete Subbranch
def delete_subbranch(request, id):
    subbranch = get_object_or_404(SubBranchMaster, pk=id)

    # Check if the subbranch is referenced in employee master
    is_used = EmployeeMaster.objects.filter(SBRNCHID=subbranch.SBRNCHID).exists()

    if request.method == 'POST':
        if is_used:
            messages.error(request, "Cannot delete Subbranch. It is referenced in one or more forms.")
            return redirect('subbranch_index')
        else:
            subbranch.delete()
            return redirect('subbranch_index')
    return render(request, 'SubBranches/delete_subbranch.html', {'subbranch': subbranch, 'is_used': is_used})

#--------------------------------------------------------------------------------------------------------------------------

# Index Page for Employee Master
def employee_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = request.GET.get('per_page', 10)
    page_number = request.GET.get('page')

    # Cast per_page to integer safely
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    employee_list = EmployeeMaster.objects.filter(CATENAME__icontains=search_query)

    paginator = Paginator(employee_list, per_page)
    page_obj = paginator.get_page(page_number)

    # Build query string for preserving other params (e.g., search)
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = '&' + urlencode(query_params) if query_params else ''

    context = {
        "employee_index": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "per_page": per_page,
        "query_string": query_string
    }

    return render(request, "Employees/employee_index.html", context)

# Add Employee
def add_employee(request):
    if request.method == "POST":
        form = EmployeeMasterForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.CUSRID = request.user.username
            employee.LMUSRID = request.user.username
            employee.save()
            return redirect('employee_index')
        else:
            print("form:", form.errors)
    else:
        form = EmployeeMasterForm()

    return render(request, "Employees/add_employee.html", {"form": form})

# Edit Employee
def edit_employee(request, id):
    employee = get_object_or_404(EmployeeMaster, pk=id)

    if request.method == "POST":
        form = EmployeeMasterForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.LMUSRID = request.user.username
            employee.save()
            return redirect('employee_index')
        else:
            print("form:", form.errors)
    else:
        form = EmployeeMasterForm(instance=employee)

    return render(request, "Employees/edit_employee.html", {"form": form})

# Delete Employee
def delete_employee(request, id):
    employee = get_object_or_404(EmployeeMaster, pk=id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_index')
    return render(request, 'Employees/delete_employee.html', {'object': employee})

#---------------------------------------------------------------------------------------------------------------------

#Slab Index

def slab_index(request):
    branch_id = request.GET.get('branch_id')
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page = request.GET.get('page', 1)

    # Fetch branches for dropdown
    branches = SubBranchMaster.objects.filter(DISPSTATUS=0).order_by('SBRNCHNAME')

    # Load slab data
    if branch_id:
        data = call_ratecard_proc(branch_id)
        slab_data = data
    else:
        slab_data = SlabMaster.objects.filter(SLABMDATE__icontains=search_query)

    # Paginate slab_data
    paginator = Paginator(slab_data, per_page)
    page_obj = paginator.get_page(page)

    # Maps for display
    category_map = {
        emp.CATEID: emp.CATENAME
        for emp in EmployeeMaster.objects.all()
    }
    branch_map = {
        sb.SBRNCHID: sb.SBRNCHNAME
        for sb in SubBranchMaster.objects.all()
    }

    # Build query string for pagination links
    query_dict = {
        "branch_id": branch_id,
        "search": search_query,
        "per_page": per_page,
    }
    query_string = urlencode({k: v for k, v in query_dict.items() if v})
    query_string = f"&{query_string}" if query_string else ""

    return render(request, "Slabs/slab_index.html", {
        "slab_index": page_obj,
        "search_query": search_query,
        "category_map": category_map,
        "branch_map": branch_map,
        "branches": branches,
        "selected_branch_id": int(branch_id) if branch_id and branch_id.isdigit() else None,
        "per_page": per_page,
        "query_string": query_string,
    })

# Add slab
def add_slab(request):
    compyid = request.session.get('compyid')  # Get from session

    if not compyid:
        # Handle missing compyid, maybe redirect to login or error page
        return redirect('login')

    if request.method == 'POST':
        form = SlabMasterForm(request.POST)
        if form.is_valid():
            slab = form.save(commit=False)
            slab.COMPYID = compyid
            slab.CUSRID = request.user.username
            slab.LMUSRID = request.user.username
            slab.save()
            return redirect('slab_index')
    else:
        form = SlabMasterForm()
    
    return render(request, 'Slabs/add_slab.html', {'form': form, 'compyid': compyid})


# Delete Slab
def delete_slab(request, id):
    slab = get_object_or_404(SlabMaster, pk=id)
    if request.method == 'POST':
        slab.delete()
        return redirect('slab_index')
    return render(request, 'Slabs/delete_slab.html', {'object': slab})

# Based on the Subbranch the Employee list show
def load_employees(request):
    branch_id = request.GET.get('branch_id')
    employees = EmployeeMaster.objects.filter(DISPSTATUS=0, SBRNCHID=branch_id).order_by('CATENAME')
    return JsonResponse(list(employees.values('CATEID', 'CATENAME')), safe=False)

#---------------------------------------------------------------------------------------------------------------------

# Index Page for Attendance Master
def attendance_index(request):
    branch_id = request.GET.get('branch_id')
    search_query = request.GET.get('search', '').strip()
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')
    page_number = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))  # Default to 10 items per page

    today = date.today()
    from_date = parse_date(from_date_str) if from_date_str else today
    to_date = parse_date(to_date_str) if to_date_str else today

    if branch_id:
        attendance = call_attendance_proc(branch_id)
        # If call_attendance_proc returns a queryset-like object
        if hasattr(attendance, 'filter'):
            attendance = attendance.order_by('-ATTNDATE')
    else:
        attendance = AttendanceDetail.objects.filter(
            ATTNDATE__date__range=(from_date, to_date)
        ).order_by('-ATTNDATE')
        if search_query:
            attendance = attendance.filter(ECATEID__icontains=search_query)

    # Pagination
    paginator = Paginator(attendance, per_page)
    page_obj = paginator.get_page(page_number)

    # Lookup dictionaries
    employee_dict = {e.CATEID: e.CATENAME for e in EmployeeMaster.objects.all()}
    branch_dict = {b.SBRNCHID: b.SBRNCHNAME for b in SubBranchMaster.objects.all()}
    branches = SubBranchMaster.objects.filter(DISPSTATUS=0).order_by("SBRNCHNAME")

    return render(request, "Attendances/attendance_index.html", {
        "page_obj": page_obj,  # Changed from attendance_index to page_obj
        "search_query": search_query,
        "from_date": from_date,
        "to_date": to_date,
        "employee_dict": employee_dict,
        "branch_dict": branch_dict,
        "branches": branches,
        "selected_branch_id": int(branch_id) if branch_id else None,
        "per_page": per_page,
    })


# Add Attendance
def add_attendance(request):
    form = AttendanceDetailForm(request.POST or None)
    attendance_list = AttendanceDetail.objects.order_by('-ATTNDATE')[:50]
    compyid = request.session.get('compyid')
    error_message = None

    if request.method == 'POST' and form.is_valid():
        attn_date = form.cleaned_data['ATTNDATE']
        branch = form.cleaned_data['SBRNCHID']
        month = attn_date.month
        year = attn_date.year

        # ✅ Check if payroll is generated (DISPSTATUS = 1 means locked)
        payroll_locked = PayrollMaster.objects.filter(
            SBRNCHID=branch,
            PRMASDATE__lte=attn_date,
            PRMAEDATE__gte=attn_date,
            DISPSTATUS=1
        ).exists()

        if payroll_locked:
            error_message = f"Cannot add attendance for {attn_date.strftime('%B %Y')}. Payroll has already been generated."
        else:
            # ✅ Proceed to save attendance
            attendance = form.save(commit=False)
            attendance.ECATEID = form.cleaned_data['ECATEID']
            attendance.SBRNCHID = branch
            if compyid:
                attendance.COMPYID = compyid
            attendance.CUSRID = request.user.username  # ✅ Set created user
            attendance.LMUSRID = request.user.username  # ✅ Set last modified user
            attendance.save()

            messages.success(request, "Attendance added successfully.")
            # Check which button was clicked
            if 'save_and_continue' in request.POST:
                # Store date and branch in session for auto-fill
                request.session['attendance_date'] = attn_date.strftime('%Y-%m-%d')  # Store as YYYY-MM-DD string
                request.session['attendance_branch'] = branch
                # Redirect back to the add page with auto-filled form
                return redirect('add_attendance')
            else:
                # Regular save - clear session and go to list view
                if 'attendance_date' in request.session:
                    del request.session['attendance_date']
                if 'attendance_branch' in request.session:
                    del request.session['attendance_branch']
                return redirect('attendance_index')

    # For employee display in table
    employee_dict = {e.CATEID: e.CATENAME for e in EmployeeMaster.objects.all()}

    # Check if we have stored values in session for auto-fill
    if 'attendance_date' in request.session and 'attendance_branch' in request.session:
        try:
            stored_date = request.session['attendance_date']
            stored_branch = request.session['attendance_branch']
            print(f"DEBUG: Found session values - Date: {stored_date}, Branch: {stored_branch}")
            # Create a new form instance with the stored values
            initial_data = {
                'ATTNDATE': stored_date,
                'SBRNCHID': stored_branch
            }
            print(f"DEBUG: Creating form with initial data: {initial_data}")
            form = AttendanceDetailForm(initial=initial_data)
            print(f"DEBUG: Form created with initial values - Date: {form.initial.get('ATTNDATE')}, Branch: {form.initial.get('SBRNCHID')}")
        except (ValueError, TypeError) as e:
            print(f"DEBUG: Error creating form: {e}")
            # If there's an error with stored values, clear them
            if 'attendance_date' in request.session:
                del request.session['attendance_date']
            if 'attendance_branch' in request.session:
                del request.session['attendance_branch']

    return render(request, 'Attendances/add_attendance.html', {
        'form': form,
        'attendance_list': attendance_list,
        'employee_dict': employee_dict,
        'error_message': error_message,
        'debug': True,  # Set to False in production
    })

#Edit Attendance
def edit_attendance(request, id):
    attendance = get_object_or_404(AttendanceDetail, pk=id)
    attendance_list = AttendanceDetail.objects.order_by('-ATTNDATE')[:50]

    # Get designation name for pre-fill
    designation = ""
    try:
        employee = EmployeeMaster.objects.get(CATEID=attendance.ECATEID)
        designation_obj = DesignationMaster.objects.get(DSGNID=employee.DSGNID)
        designation = designation_obj.DSGNDESC
    except (EmployeeMaster.DoesNotExist, DesignationMaster.DoesNotExist):
        pass

    error_message_edit = None

    if request.method == "POST":
        form = AttendanceDetailForm(request.POST, instance=attendance)
        if form.is_valid():
            attn_date = form.cleaned_data['ATTNDATE']
            branch = form.cleaned_data['SBRNCHID']

            # ✅ Check if payroll is locked
            payroll_locked = PayrollMaster.objects.filter(
                SBRNCHID=branch,
                PRMSDATE__lte=attn_date,
                PRMEDATE__gte=attn_date,
                DISPSTATUS=1
            ).exists()

            if payroll_locked:
                error_message_edit = f"Cannot edit attendance for {attn_date.strftime('%B %Y')}. Payroll has already been generated."
            else:
                attendance = form.save(commit=False)
                attendance.LMUSRID = request.user.username
                attendance.ECATEID = form.cleaned_data['ECATEID']
                attendance.SBRNCHID = form.cleaned_data['SBRNCHID']
                attendance.save()
                return redirect('attendance_index')
        else:
            print("form errors:", form.errors)
    else:
        form = AttendanceDetailForm(instance=attendance)

    employee_dict = {e.CATEID: e.CATENAME for e in EmployeeMaster.objects.all()}

    return render(request, "Attendances/edit_attendance.html", {
        "form": form,
        "designation": designation,  # Pass to template
        'attendance_list': attendance_list,
        'employee_dict': employee_dict,
        "error_message_edit": error_message_edit,
    })

# Delete Attendance
def delete_attendance(request, id):
    attendance = get_object_or_404(AttendanceDetail, pk=id)
    error_message_delete = None

    if request.method == 'POST':
        attn_date = attendance.ATTNDATE
        branch = attendance.SBRNCHID

        # ✅ Check if payroll has been generated
        payroll_locked = PayrollMaster.objects.filter(
            SBRNCHID=branch,
            PRMSDATE__lte=attn_date,
            PRMEDATE__gte=attn_date,
            DISPSTATUS=1
        ).exists()

        if payroll_locked:
            error_message_delete = f"Cannot delete attendance for {attn_date.strftime('%B %Y')}. Payroll has already been generated."
        else:
            attendance.delete()
            return redirect('attendance_index')

    return render(request, 'Attendances/delete_attendance.html', {
        'object': attendance,
        'error_message_delete': error_message_delete,
    })

# def load_employees_attendance(request):
#     branch_id = request.GET.get('branch_id')
#     employees = EmployeeMaster.objects.filter(DISPSTATUS=0, SBRNCHID=branch_id).order_by('CATENAME')
#     return JsonResponse(list(employees.values('CATEID', 'CATENAME')), safe=False)

#-------------------------------------------------------------------------------------------------------------

#Get Desination based on the employee in Attendance 
def get_designation(request, emp_id):
    try:
        employee = EmployeeMaster.objects.get(pk=emp_id)
        designation = DesignationMaster.objects.get(DSGNID=employee.DSGNID)
        return JsonResponse({'designation': designation.DSGNDESC})
    
    except EmployeeMaster.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)
    
    except DesignationMaster.DoesNotExist:
        return JsonResponse({'error': 'Designation not found'}, status=404)
    
#----------------------------------------------------------------------------------------------------------------

# Index Page for Payroll Master
# def payroll_index(request):
#     search_query = request.GET.get('search', '').strip()
#     payroll = PayrollMaster.objects.filter(COMPYID__icontains=search_query)

#     return render(request, "Payrolls/payroll_index.html", {"payroll_index": payroll, "search_query": search_query})

def calendar_month_to_fiscal_disp_order(month_num):
    if month_num >= 4:
        return month_num - 3
    else:
        return month_num + 9

def get_generated_months(request):
    branch_id = request.GET.get('branch_id')
    accounting_year_id = request.GET.get('accounting_year_id')

    try:
        branch_id = int(branch_id)
        accounting_year_id = int(accounting_year_id)
    except (ValueError, TypeError):
        return JsonResponse({'used_months': []})

    used_months = PayrollMaster.objects.filter(
        SBRNCHID=branch_id,
        COMPYID=accounting_year_id  # ✅ Only filter months for this accounting year
    ).values_list('MONTHID', flat=True).distinct()

    return JsonResponse({'used_months': list(used_months)})



def add_payroll(request):
    company_id = request.POST.get('company') if request.method == "POST" else request.GET.get('company')

    compyid = request.session.get('compyid')
    accounting_year_id = request.session.get('accounting_year_id')
    financial_year = request.session.get('financial_year')

    # Fetch used month IDs and keys
    used_month_ids = PayrollMaster.objects.filter(COMPYID=accounting_year_id).values_list('MONTHID', flat=True)
    used_month_keys = [
        f"{row['COMPYID']}-{row['MONTHID']}"
        for row in PayrollMaster.objects.values('COMPYID', 'MONTHID')
    ]

    if request.method == "POST":
        form = PayrollMasterForm(request.POST, accounting_year_id=accounting_year_id, company_id=company_id)
        if form.is_valid():
            payroll_master = form.save(commit=False)

            if compyid:
                try:
                    payroll_master.COMPYID = int(compyid)
                except ValueError:
                    payroll_master.COMPYID = None

            payroll_master.DISPSTATUS = 1
            payroll_master.CUSRID = request.user.username
            payroll_master.LMUSRID = request.user.username
            payroll_master.save()

            messages.success(request, "Payroll successfully generated.")
            return redirect('payroll_index')
        else:
            messages.error(request, "There were errors in the form.")
    else:
        # ⬇️ Pre-fill COMPYID based on session value (e.g., 2026-2027 accounting year)
        form = PayrollMasterForm(
            initial={'COMPYID': accounting_year_id},
            accounting_year_id=accounting_year_id,
            company_id=company_id
        )

    companies = CompanyMaster.objects.filter(DISPSTATUS=0).order_by('COMPNAME')

    context = {
        "form": form,
        "companies": companies,
        "used_month_ids": list(used_month_ids),
        "used_month_keys": used_month_keys,
        "selected_company": int(compyid) if compyid else '',
        "accounting_year_id": accounting_year_id,
        "financial_year": financial_year,
    }

    return render(request, "Payrolls/add_payroll.html", context)


# Delete Payroll

def delete_payroll(request, prmid):
    with transaction.atomic():
        payroll_master = get_object_or_404(PayrollMaster, PRMID=prmid)
        payroll_details = PayrollDetail.objects.filter(PRMID=payroll_master)

        for detail in payroll_details:
            PayrollPayheadDetail.objects.filter(PRDID=detail).delete()

        payroll_details.delete()
        payroll_master.delete()
        messages.success(request, "Payroll deleted. You can now regenerate it.")

    return redirect('payroll_index')

#---------------------------------------------------------------------------------------------------------------------

#Index for getting sub-branches based on the company in payroll
def get_subbranches(request):
    company_id = request.GET.get('company_id')

    # Ensure company_id is not None and cast to int
    if company_id is not None:
        try:
            company_id = int(company_id)
            subbranches = SubBranchMaster.objects.filter(COMPID=company_id, DISPSTATUS=0).order_by('SBRNCHNAME')
            data = [{'id': sb.SBRNCHID, 'name': sb.SBRNCHNAME} for sb in subbranches]
        except ValueError:
            data = []
    else:
        data = []

    return JsonResponse({'subbranches': data})

#-----------------------------------------------------------------------------------------------------------------------

def payroll_index(request):
    branches = SubBranchMaster.objects.all()

    selected_branch_id = request.GET.get('branch_id')
    selected_year = request.GET.get('accounting_year')
    selected_date = request.GET.get('payroll_date')
    per_page = int(request.GET.get('per_page', 10))
    page = request.GET.get('page', 1)

    # Initialize variables with default values
    accounting_year_choices = []
    payroll_dates_display = []
    filtered_date = None  # Initialize filtered_date
    latest_master = None
    payroll_qs = PayrollDetail.objects.none()
    employee_map = {}
    show_data = False

    # Build accounting year dropdown options
    used_compy_ids = PayrollMaster.objects.values_list('COMPYID', flat=True).distinct()
    company_details = CompanyAccountingDetail.objects.filter(COMPYID__in=used_compy_ids)
    accounting_years = AccountingYear.objects.in_bulk([cd.YRID for cd in company_details])
    accounting_year_choices = [
        (cd.COMPYID, accounting_years.get(cd.YRID).YRDESC if accounting_years.get(cd.YRID) else f"YRID {cd.YRID}")
        for cd in company_details
    ]

    # Filter PayrollMaster by branch and company/year
    payroll_master_qs = PayrollMaster.objects.all()
    if selected_branch_id:
        payroll_master_qs = payroll_master_qs.filter(SBRNCHID=selected_branch_id)
    if selected_year:
        payroll_master_qs = payroll_master_qs.filter(COMPYID=selected_year)

    # Build payroll date dropdown
    payroll_dates = payroll_master_qs.order_by('-PRMDATE').values_list('PRMDATE', flat=True).distinct()
    payroll_dates_display = [(d, date_format(localtime(d), 'd-m-Y')) for d in payroll_dates if d]

    # Filter by date (or default to latest)
    if selected_date:
        try:
            filtered_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            payroll_master_qs = payroll_master_qs.filter(PRMDATE__date=filtered_date)
        except ValueError:
            filtered_date = payroll_master_qs.aggregate(Max('PRMDATE'))['PRMDATE__max']
            if filtered_date:
                payroll_master_qs = payroll_master_qs.filter(PRMDATE=filtered_date)
    else:
        filtered_date = payroll_master_qs.aggregate(Max('PRMDATE'))['PRMDATE__max']
        if filtered_date:
            payroll_master_qs = payroll_master_qs.filter(PRMDATE=filtered_date)

    latest_master = payroll_master_qs.first()

    # Get payroll details and employee map
    if latest_master:
        show_data = True
        payroll_qs = PayrollDetail.objects.filter(PRMID=latest_master).order_by('EMPLID')
        employee_ids = payroll_qs.values_list('EMPLID', flat=True).distinct()
        employees = EmployeeMaster.objects.filter(CATEID__in=employee_ids)
        employee_map = {emp.CATEID: emp for emp in employees}

    # Pagination and per-page options
    per_page_options = [10, 20, 50, 100]
    paginator = Paginator(payroll_qs, per_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Preserve filters in pagination links
    params = {
        "branch_id": selected_branch_id,
        "accounting_year": selected_year,
        "payroll_date": selected_date,
        "per_page": per_page,
    }
    qs = urlencode({k: v for k, v in params.items() if v})
    query_string = f"&{qs}" if qs else ""

    context = {
        'branches': branches,
        'accounting_year_choices': accounting_year_choices,
        'payroll_dates_display': payroll_dates_display,
        'selected_branch_id': int(selected_branch_id) if selected_branch_id else None,
        'selected_year': int(selected_year) if selected_year else None,
        'selected_date': selected_date,
        'filtered_date': filtered_date,  # Now always defined
        'per_page': per_page,
        'per_page_options': per_page_options,
        'slab_index': page_obj,
        'employee_map': employee_map,
        'latest_master': latest_master,
        'query_string': query_string,
        'show_data': show_data,
        'current_branch': SubBranchMaster.objects.filter(SBRNCHID=latest_master.SBRNCHID).first() if latest_master else None,
    }

    return render(request, 'Payrolls/payroll_index.html', context)
    
def payroll_print_index(request):
    # Clear previous selection
    TempReportID.objects.filter(KUSRID=request.user.username, OPTNSTR="PaySlip").delete()

    branches = SubBranchMaster.objects.all()
    selected_branch_id = request.GET.get('branch_id')
    selected_date_str = request.GET.get('payroll_date')
    per_page = int(request.GET.get('per_page', 10))
    page = request.GET.get('page', 1)

    accounting_year_choices = []
    payroll_dates_display = []
    selected_year = None
    filtered_date = None
    latest_master = None
    prmid = None
    payroll_qs = PayrollDetail.objects.none()
    employee_map = {}
    show_data = False

    if selected_branch_id:
        payroll_master_qs = PayrollMaster.objects.filter(SBRNCHID=selected_branch_id)
        used_compy_ids = payroll_master_qs.values_list('COMPYID', flat=True).distinct()
        company_details = CompanyAccountingDetail.objects.filter(COMPYID__in=used_compy_ids)
        accounting_years = AccountingYear.objects.in_bulk([cd.YRID for cd in company_details])
        accounting_year_choices = [
            (cd.COMPYID, accounting_years.get(cd.YRID).YRDESC if accounting_years.get(cd.YRID) else f"YRID {cd.YRID}")
            for cd in company_details
        ]

        payroll_dates = payroll_master_qs.order_by('-PRMDATE').values_list('PRMDATE', flat=True).distinct()
        payroll_dates_display = [(d, date_format(localtime(d), 'd-m-Y')) for d in payroll_dates if d]

        if selected_date_str:
            try:
                filtered_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
                payroll_master_qs = payroll_master_qs.annotate(
                    prm_date_only=TruncDate('PRMDATE')
                ).filter(prm_date_only=filtered_date.date())
            except ValueError:
                filtered_date = payroll_master_qs.aggregate(Max('PRMDATE'))['PRMDATE__max']
                if filtered_date:
                    payroll_master_qs = payroll_master_qs.filter(PRMDATE=filtered_date)
        else:
            filtered_date = payroll_master_qs.aggregate(Max('PRMDATE'))['PRMDATE__max']
            if filtered_date:
                payroll_master_qs = payroll_master_qs.filter(PRMDATE=filtered_date)

        latest_master = payroll_master_qs.first()

        if latest_master:
            prmid = latest_master.PRMID
            selected_year = latest_master.COMPYID
            show_data = True
            payroll_qs = PayrollDetail.objects.filter(PRMID=latest_master).order_by('EMPLID')
            employee_ids = payroll_qs.values_list('EMPLID', flat=True).distinct()
            employees = EmployeeMaster.objects.filter(CATEID__in=employee_ids)
            employee_map = {emp.CATEID: emp for emp in employees}

    paginator = Paginator(payroll_qs, per_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    query_dict = {
        "branch_id": selected_branch_id,
        "payroll_date": filtered_date.strftime('%Y-%m-%d') if filtered_date else None,
        "per_page": per_page,
    }
    query_string = urlencode({k: v for k, v in query_dict.items() if v})
    query_string = f"&{query_string}" if query_string else ""

    context = {
        'branches': branches,
        'selected_branch_id': int(selected_branch_id) if selected_branch_id else None,
        'accounting_year_choices': accounting_year_choices,
        'selected_year': int(selected_year) if selected_year else None,
        'payroll_dates_display': payroll_dates_display,
        'selected_date': filtered_date,
        'slab_index': page_obj,
        'employee_map': employee_map,
        'latest_master': latest_master,
        'per_page': per_page,
        'query_string': query_string,
        'show_data': show_data,
        'prmid': prmid,
        'kusrid': request.user.username,
    }

    return render(request, 'Reports/payroll_print_index.html', context)

def payrolltax_details(request, prdid):
    payroll_detail = get_object_or_404(PayrollDetail, pk=prdid)
    payhead_details = PayrollPayheadDetail.objects.filter(PRDID=prdid)

    employee_name = ""
    designation_name = ""
    
    if payroll_detail.EMPLID:
        employee = EmployeeMaster.objects.filter(CATEID=payroll_detail.EMPLID).first()
        if employee:
            employee_name = employee.CATENAME
            # Fetch designation name
            designation = DesignationMaster.objects.filter(DSGNID=employee.DSGNID).first()
            designation_name = designation.DSGNDESC if designation else ""

    # Payhead ID to Description mapping
    payhead_map = {
        ph.PAYHID: ph.PAYHDESC for ph in PayHeadMaster.objects.filter(PAYHID__in=payhead_details.values_list('PAYHID', flat=True))
    }

    context = {
        'payroll_detail': payroll_detail,
        'employee_name': employee_name,
        'designation_name': designation_name,
        'payhead_details': payhead_details,
        'payhead_map': payhead_map,
    }
    return render(request, 'Payrolls/payrolltax_details.html', context)


def get_available_months(request):
    company_id = request.GET.get('company_id')

    used_months = PayrollMaster.objects.filter(COMPYID=company_id).values_list('MONTHID', flat=True)

    # All months (1 to 12)
    all_months = [
        {"id": 1, "name": "April"},
        {"id": 2, "name": "May"},
        {"id": 3, "name": "June"},
        {"id": 4, "name": "July"},
        {"id": 5, "name": "August"},
        {"id": 6, "name": "September"},
        {"id": 7, "name": "October"},
        {"id": 8, "name": "November"},
        {"id": 9, "name": "December"},
        {"id": 10, "name": "January"},
        {"id": 11, "name": "February"},
        {"id": 12, "name": "March"},
    ]

    # Filter out used months
    available_months = [month for month in all_months if month["id"] not in used_months]

    return JsonResponse({"months": available_months})

#-----------------------------------------------------------------------------------------------------

User = get_user_model()

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_date_str = request.POST.get('LDATE')

        if not username or not password or not login_date_str:
            messages.error(request, "All fields are required.")
            return render(request, 'Registration/login.html')

        user = User.objects.filter(username=username).first()
        if user and not user.is_active:
            messages.error(request, "Your account is inactive. Please contact admin.")
            return render(request, 'Registration/login.html')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, 'Registration/login.html')

        login(request, user)

        try:
            result = process_login_date_and_get_compyid(login_date_str)

            # Store compyid in session as string for safety
            request.session['compyid'] = str(result['compyid'])
            request.session['financial_year'] = result['financial_year']  # ✅ Add this
            request.session['financial_year_override'] = result['financial_year']
            request.session['accounting_year_id'] = result['accounting_year_id']
            print(f"🧩 Stored compyid in session: {request.session['compyid']}")

            context = {
                'user_fullname': user.username,
                'login_date': result['login_date'],
                'financial_year': result['financial_year'],
                'accounting_year_id': result['accounting_year_id'],
                'compyid': result['compyid'],
            }

            # Render dashboard template directly after login
            return render(request, 'Registration/dashboard.html', context)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'Registration/login.html')

    return render(request, 'Registration/login.html')

def dashboard(request):
    compyid = request.session.get('compyid')
    print("🧩 compyid in session on dashboard:", compyid)
    return render(request, 'Registration/dashboard.html')

#------------------------------------------------------------------------------------------------------------------
   
from django.contrib.auth import logout
def custom_admin_logout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('login')

#------------------------------------------------------------------------------------------------------------------------------

def user_index(request):
    search_query = request.GET.get('search', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')

    if request.user.is_superuser:
        user_qs = CustomUser.objects.all()
    else:
        user_qs = CustomUser.objects.filter(id=request.user.id)  # Only self

    if search_query:
        user_qs = user_qs.filter(username__icontains=search_query)

    user_qs = user_qs.order_by('id')

    paginator = Paginator(user_qs.distinct(), per_page)
    page_obj = paginator.get_page(page_number)

    query_dict = request.GET.copy()
    query_dict.pop('page', None)
    query_string = '&' + urlencode(query_dict)

    return render(request, "Users/user_index.html", {
        "user_list": page_obj.object_list,
        "page_obj": page_obj,
        "per_page": per_page,
        "query_string": query_string,
        "search_query": search_query,
    })


# Check if user is superuser or staff
def is_admin(user):
    return user.is_superuser


# ✅ ADD User
@login_required
@admin_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_index')
        else:
            print("Form is invalid:", form.errors)  # Debug print
            # Optional: add a message to show in the template
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'Users/add_user.html', {'form': form})

# ✏️ EDIT User
@login_required
@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    form = CustomUserChangeForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user_index')

    return render(request, 'Users/edit_user.html', {'form': form})

# ❌ DELETE User
@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_index')
    return render(request, 'Users/delete_user.html', {'object': user})

#Set the Users to Active and Inactive
@login_required
@admin_required
def toggle_user_active(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot change your own active status.")
    else:
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f"{user.username} is now {'active' if user.is_active else 'inactive'}.")

    return redirect('user_index') 

#Change Password for the user
User = get_user_model()
def change_user_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Password for {user.username} changed successfully.")
            return redirect('user_index')  # adjust this name to match your user list view
    else:
        form = AdminPasswordChangeForm(user)

    return render(request, 'Users/change_password.html', {'form': form, 'user': user})

#----------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@require_POST
@login_required
def toggle_selected_employee(request):
    user_id = request.user.username
    employee_id = request.POST.get("EMPLID")
    checked = request.POST.get("checked") == "true"

    if not employee_id:
        return JsonResponse({"status": "error", "message": "Missing employee ID"}, status=400)
    
    try:
        if checked:
            # 🛑 Safe insert
            if not TempReportID.objects.filter(
                KUSRID=user_id,
                OPTNSTR="PaySlip",
                RPTID=employee_id
            ).exists():
                TempReportID.objects.create(
                    KUSRID=user_id,
                    OPTNSTR="PaySlip",
                    RPTID=employee_id
                )
        else:
            TempReportID.objects.filter(
                KUSRID=user_id,
                OPTNSTR="PaySlip",
                RPTID=employee_id
            ).delete()

        return JsonResponse({"status": "success"})

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from openpyxl import Workbook
from openpyxl.styles import Font

def payroll_report(request):
    # Get selected branch if any
    selected_branch = request.GET.get('branch_id')
    selected_prm_id = request.GET.get('prm_id')

    with connection.cursor() as cursor:
        # Get all branches
        cursor.execute("SELECT DISTINCT SBRNCHID, SBRNCHNAME FROM VW_EMPLOYEE_PAYROLL_DETAIL_RPT ORDER BY SBRNCHNAME")
        branches = cursor.fetchall()

        # Get periods only if branch is selected
        periods = []
        if selected_branch:
            cursor.execute("""
                SELECT DISTINCT PRMID, CONVERT(VARCHAR, PRMDATE, 103) 
                FROM VW_EMPLOYEE_PAYROLL_DETAIL_RPT 
                WHERE SBRNCHID = %s 
                ORDER BY PRMID DESC
            """, [selected_branch])
            periods = cursor.fetchall()

    return render(request, 'Reports/payroll_report.html', {
        'branches': branches,
        'periods': periods,
        'selected_branch': selected_branch,
        'selected_prm_id': selected_prm_id
    })

def generate_payroll_excel(request):
    branch_id = request.GET.get('branch_id')
    prm_id = request.GET.get('prm_id')
    
    # Use the stored procedure instead of direct query
    with connection.cursor() as cursor:
        # Execute the stored procedure with parameters
        cursor.execute("EXEC [dbo].[SP_EMPLOYEE_PAYROLL_DETAIL_RPT] @PID=%s, @BID=%s", [prm_id, branch_id])
        
        # Fetch the results
        rows = cursor.fetchall()
        
        # Get column names from the cursor description
        columns = [col[0] for col in cursor.description]
    
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Payroll Report"
    
    # Write headers
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_num, value=column_title)
        cell.font = Font(bold=True)
    
    # Write data
    for row_num, row in enumerate(rows, 2):
        for col_num, cell_value in enumerate(row, 1):
            ws.cell(row=row_num, column=col_num, value=cell_value)
    
    # Auto-size columns
    for column in ws.columns:
        max_length = max(len(str(cell.value)) for cell in column)
        ws.column_dimensions[column[0].column_letter].width = max_length + 2
    
    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"payroll_{branch_id or 'all'}_period_{prm_id}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    wb.save(response)
    return response