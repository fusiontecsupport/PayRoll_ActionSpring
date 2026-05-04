from .models import AccountingYear, CompanyAccountingDetail
from datetime import date
from django.utils.timezone import now
def compyid_processor(request):
    return {
        'compyid': request.session.get('compyid', ''),
    }

def financial_year_context(request):
    try:
        # ✅ Look for session override first
        if request.session.get("financial_year_override"):
            current_fy = request.session["financial_year_override"]
        else:
            compy_id = request.session.get('accounting_year_id')
            detail = CompanyAccountingDetail.objects.get(COMPYID=compy_id)
            year_obj = AccountingYear.objects.get(YRID=detail.YRID)
            current_fy = year_obj.YRDESC
    except Exception:
        today = date.today()
        start_year = today.year if today.month >= 4 else today.year - 1
        end_year = start_year + 1
        current_fy = f"{start_year}-{end_year}"

    return {
        "current_financial_year": current_fy,
        "current_year": date.today().year,
    }
