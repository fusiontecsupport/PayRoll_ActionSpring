# utils.py or top of views.py
from django.contrib import messages
from django.shortcuts import redirect
from datetime import datetime, timezone as dt_timezone
from django.utils.timezone import timezone
from django.db import transaction
from .models import AccountingYear, CompanyAccountingDetail
import traceback


def process_login_date_and_get_compyid(login_date_str):
    try:
        print("🔍 Processing login date:", login_date_str)

        # Parse login date string to date
        login_date = datetime.strptime(login_date_str, '%Y-%m-%d').date()
        month = login_date.month
        year = login_date.year

        # Determine financial year
        if month >= 4:
            pf_year = year
            pt_year = year + 1
        else:
            pf_year = year - 1
            pt_year = year

        yr_desc = f"{pf_year} - {pt_year}"

        # Build FDATE and TDATE
        fdate = datetime(pf_year, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
        tdate = datetime(pt_year, 3, 31, 0, 0, 0, tzinfo=timezone.utc)
        prcsdate = fdate
        # Format PRCSDATE similar to your table (e.g., FDATE + 4 days)

        print(f"🗓 Financial Year: {yr_desc}, Start: {fdate}, End: {tdate}, PRCSDATE: {prcsdate}")

        # Fetch or create AccountingYear
        accounting_year = AccountingYear.objects.filter(YRDESC=yr_desc).first()
        if not accounting_year:
            print("⚠️ AccountingYear not found. Creating new.")
            accounting_year = AccountingYear.objects.create(
                FDATE=fdate,
                TDATE=tdate,
                YRDESC=yr_desc,
                CUSRID=1,
                PRCSDATE=prcsdate
            )
            print(f"✅ Created AccountingYear ID={accounting_year.YRID}")
        else:
            print(f"✅ Found AccountingYear ID={accounting_year.YRID}")

        # Fetch or create CompanyAccountingDetail
        comp_detail = CompanyAccountingDetail.objects.filter(YRID=accounting_year.YRID, COMPID=1).first()
        if not comp_detail:
            print("⚠️ CompanyAccountingDetail not found. Creating new.")
            comp_detail = CompanyAccountingDetail.objects.create(
                COMPID=1,
                YRID=accounting_year.YRID,
                CUSRID=1,
                DISPSTATUS=0,
                PRCSDATE=fdate
            )
            print(f"✅ Created CompanyAccountingDetail COMPYID={comp_detail.COMPYID}")
        else:
            print(f"✅ Found CompanyAccountingDetail COMPYID={comp_detail.COMPYID}")

        return {
            'compyid': comp_detail.COMPYID,
            'login_date': login_date_str,
            'financial_year': yr_desc,
            'accounting_year_id': accounting_year.YRID,
        }

    except Exception as e:
        print("❌ An error occurred:", e)
        traceback.print_exc()
        raise


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Already protected by @login_required
        if not request.user.is_superuser:
            messages.error(request, "Login as admin to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper