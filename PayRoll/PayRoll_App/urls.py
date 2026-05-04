from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #Urls for Companies
    path('company/add/', views.add_company, name='add_company'),
    path('company', views.company_index, name='company_index'),
    path('company/edit/<int:id>/', views.edit_company, name='edit_company'),
    path('company/delete/<int:id>/', views.delete_company, name='delete_company'),

    #Urls for Designation
    path('designations/', views.designation_index, name='designation_index'),
    path('designation/add/', views.add_designation, name='add_designation'),
    path('designation/edit/<int:id>/', views.edit_designation, name='edit_designation'),
    path('designation/delete/<int:id>/', views.delete_designation, name='delete_designation'),

    #Urls for Department
    path('Departments/', views.department_index, name='department_index'),
    path('Department/add/', views.add_department, name='add_department'),
    path('Department/edit/<int:id>/', views.edit_department, name='edit_department'),
    path('Department/delete/<int:id>/', views.delete_department, name='delete_department'),

    #Urls for State
    path('states/', views.state_index, name='state_index'),
    path('states/add/', views.add_state, name='add_state'),
    path('states/edit/<int:id>/', views.edit_state, name='edit_state'),
    path('states/delete/<int:id>/', views.delete_state, name='delete_state'),

    #Urls for Grade
    path('grades/', views.grade_index, name='grade_index'),
    path('grades/add/', views.add_grade, name='add_grade'),
    path('grades/edit/<int:id>/', views.edit_grade, name='edit_grade'),
    path('grades/delete/<int:id>/', views.delete_grade, name='delete_grade'),

    #Urls for PayHeadType
    path('pay-head-type/', views.payheadtype_index, name='payheadtype_index'),
    path('pay-head-type/add/', views.add_payheadtype, name='add_payheadtype'),
    path('pay-head-type/edit/<int:id>/', views.edit_payheadtype, name='edit_payheadtype'),
    path('pay-head-type/delete/<int:id>/', views.delete_payheadtype, name='delete_payheadtype'),

    #Urls for PayHead
    path('pay-head/', views.payhead_index, name='payhead_index'),
    path('pay-head/add/', views.add_payhead, name='add_payhead'),
    path('pay-head/edit/<int:id>/', views.edit_payhead, name='edit_payhead'),
    path('pay-head/delete/<int:id>/', views.delete_payhead, name='delete_payhead'),

    #Urls for Account Group
    path('accountgroup/', views.accountgroup_index, name='accountgroup_index'),
    path('accountgroup/add/', views.add_accountgroup, name='add_accountgroup'),
    path('accountgroup/edit/<int:id>/', views.edit_accountgroup, name='edit_accountgroup'),
    path('accountgroup/delete/<int:id>/', views.delete_accountgroup, name='delete_accountgroup'),

    #Urls for Account Head
    path('accounthead/', views.accounthead_index, name='accounthead_index'),
    path('accounthead/add/', views.add_accounthead, name='add_accounthead'),
    path('accounthead/edit/<int:id>/', views.edit_accounthead, name='edit_accounthead'),
    path('accounthead/delete/<int:id>/', views.delete_accounthead, name='delete_accounthead'),

    #Urls for Advance Type
    path('advancetype/', views.advancetype_index, name='advancetype_index'),
    path('advancetype/add/', views.add_advancetype, name='add_advancetype'),
    path('advancetype/edit/<int:id>/', views.edit_advancetype, name='edit_advancetype'),
    path('advancetype/delete/<int:id>/', views.delete_advancetype, name='delete_advancetype'),

    #Urls for BloodGroup
    path('bloodgroup/', views.bloodgroup_index, name='bloodgroup_index'),
    path('bloodgroup/add/', views.add_bloodgroup, name='add_bloodgroup'),
    path('bloodgroup/edit/<int:id>/', views.edit_bloodgroup, name='edit_bloodgroup'),
    path('bloodgroup/delete/<int:id>/', views.delete_bloodgroup, name='delete_bloodgroup'),

    #Urls for Relationship
    path('relationship/', views.relationship_index, name='relationship_index'),
    path('relationship/add/', views.add_relationship, name='add_relationship'),
    path('relationship/edit/<int:id>/', views.edit_relationship, name='edit_relationship'),
    path('relationship/delete/<int:id>/', views.delete_relationship, name='delete_relationship'),

    #Urls for Location
    path('locations/', views.location_index, name='location_index'),
    path('locations/add/', views.add_location, name='add_location'),
    path('locations/edit/<int:id>/', views.edit_location, name='edit_location'),
    path('locations/delete/<int:id>/', views.delete_location, name='delete_location'),

    #Urls for LeaveHead
    path('leavehead/', views.leavehead_index, name='leavehead_index'),
    path('leavehead/add/', views.add_leavehead, name='add_leavehead'),
    path('leavehead/edit/<int:id>/', views.edit_leavehead, name='edit_leavehead'),
    path('leavehead/delete/<int:id>/', views.delete_leavehead, name='delete_leavehead'),

    #Urls for SubBranch
    path('subbranch/', views.subbranch_index, name='subbranch_index'),
    path('subbranch/add/', views.add_subbranch, name='add_subbranch'),
    path('subbranch/edit/<int:id>/', views.edit_subbranch, name='edit_subbranch'),
    path('subbranch/delete/<int:id>/', views.delete_subbranch, name='delete_subbranch'),

    #Urls for Employee
    path('employee/', views.employee_index, name='employee_index'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    #Urls for Slab
    path('slab/', views.slab_index, name='slab_index'),
    path('slab/add/', views.add_slab, name='add_slab'),
    path('slab/delete/<int:id>/', views.delete_slab, name='delete_slab'),

    #Urls for Attendance
    path('attendance/', views.attendance_index, name='attendance_index'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('attendance/edit/<int:id>/', views.edit_attendance, name='edit_attendance'),
    path('attendance/delete/<int:id>/', views.delete_attendance, name='delete_attendance'),

    #Urls for Get-Designation in Attendance(Add)
    path('ajax/load-employees/', views.load_employees, name='ajax_load_employees'),
    # path('ajax/load-employees-attendance/', views.load_employees_attendance, name='ajax_load_employees_attendance'),
    path('get-designation/<int:emp_id>/', views.get_designation, name='get_designation'),
    path('ajax/get-subbranches/', views.get_subbranches, name='get_subbranches'),
    path("ajax/get-available-months/", views.get_available_months, name="get_available_months"),

    #Urls for Payroll
    path('payrolls', views.payroll_index, name='payroll_index'),
    path('payroll/add/', views.add_payroll, name='add_payroll'),
    path('payroll/view/<int:prdid>/', views.payrolltax_details, name='tax_view'),
    path('payroll/delete/<int:prmid>/', views.delete_payroll, name='delete_payroll'),

    path('payroll/print/', views.payroll_print_index, name='payroll_print_index'),
    path("toggle_selected/", views.toggle_selected_employee, name="toggle_selected_employee"),

    path('login/', views.custom_login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('logout/', views.logout_view, name='logout'),

    #Urls for Users
    path('users/', views.user_index, name='user_index'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('toggle-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('users/<int:user_id>/change-password/', views.change_user_password, name='change_user_password'),


    # Password reset views
    # path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='ForgetPassword/password_reset_form.html'), name='password_reset'),
    # path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='ForgetPassword/password_reset_done.html'), name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='ForgetPassword/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='ForgetPassword/password_reset_complete.html'), name='password_reset_complete'),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('ajax/get-generated-months/', views.get_generated_months, name='get_generated_months'),


    path('payroll-report/', views.payroll_report, name='payroll_report'),
    path('payroll-excel/', views.generate_payroll_excel, name='generate_payroll_excel'),

]


# Serve static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
