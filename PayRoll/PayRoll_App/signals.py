# signals.py
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver
# from .services import process_payroll
from django.db import transaction
from num2words import num2words
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP, ROUND_CEILING, ROUND_UP
from .models import (
    PayrollMaster, EmployeeMaster, SlabMaster,
    PayrollDetail, PayrollPayheadDetail, AttendanceDetail, MonthMaster
)
def round_net_pay(value):
    return int(Decimal(value).quantize(0, rounding=ROUND_DOWN))

def round_half_up(value):
    return int(Decimal(value).quantize(0, rounding=ROUND_HALF_UP))

def round_up(value):
    return Decimal(value).to_integral_value(rounding=ROUND_CEILING)

@transaction.atomic
def process_payroll(payroll_master_id, sbrnchid):
    print("process_payroll called")
    
    # Fetch payroll master record
    payroll_master = PayrollMaster.objects.get(PRMID=payroll_master_id)

    # ✅ Get the latest or first active month record
    month_master = MonthMaster.objects.get(MONTHID=payroll_master.MONTHID)

    if not month_master:
        print("❌ No active month found in MonthMaster.")
        return  # Or raise an exception, depending on your use case
    
    # Filter only active employees in the same branch
    employees = EmployeeMaster.objects.filter(DISPSTATUS=0, SBRNCHID=sbrnchid)

    for emp in employees:
        emp_id = emp.CATEID
        branch_id = emp.SBRNCHID
        dsgn_id = emp.DSGNID
        grade_id = emp.GRADEID

        print(f"➡️ Employee ID: {emp.CATEID}")
        print(f"   🔹 BRNCHID: {branch_id}")
        print(f"   🔹 CATEID : {emp.DSGNID}")
        print(f"   🔹 DISPSTATUS=0")

        slab = SlabMaster.objects.filter(
            BRNCHID=branch_id,
            CATEID=emp.CATEID,
            DISPSTATUS=0
        ).order_by('-SLABMDATE').first()

        if not slab:
            print(f"❌ Skipping Employee {emp.CATEID}: No slab found for Branch={branch_id}, Category={emp.DSGNID}")
            continue
        
        # Attendance Calculation
        attendance_qs = AttendanceDetail.objects.filter(
            ECATEID=emp_id,
            ATTNDATE__month=payroll_master.PRMEDATE.month,
            ATTNDATE__year=payroll_master.PRMEDATE.year,
        )

        absent_days = attendance_qs.aggregate(total_absent=Sum('ATTNNOD'))['total_absent'] or Decimal('0.00')
        ot_hours = attendance_qs.aggregate(total_ot=Sum('OTAMT'))['total_ot'] or Decimal('0.00')
        increment = attendance_qs.aggregate(total_incr=Sum('INCAMT'))['total_incr'] or Decimal('0.00')
        bonus_days = attendance_qs.aggregate(total_bonus_days=Sum('ABAMT'))['total_bonus_days'] or Decimal('0.00')
        tea = attendance_qs.aggregate(total_tea=Sum('TEAAMT'))['total_tea'] or Decimal('0.00')
        food = attendance_qs.aggregate(total_food=Sum('FOODAMT'))['total_food'] or Decimal('0.00')
        odeduct = attendance_qs.aggregate(total_odeduct=Sum('ODAMT'))['total_odeduct'] or Decimal('0.00')

        total_days = Decimal(payroll_master.WRKDAYS)
        att_days = total_days - absent_days

        basic = slab.BAMT
        hra = slab.HRAAMT
        oallow = slab.OAMT
        waallow = slab.WAMT
        gross = basic + hra + oallow + waallow

        # Per day LOP
        per_day_basic = basic / total_days
        per_day_hra = hra / total_days
        per_day_oallow = oallow / total_days
        per_day_waallow = waallow / total_days

        lop_basic = per_day_basic * absent_days
        lop_hra = per_day_hra * absent_days
        lop_oallow = per_day_oallow * absent_days
        lop_waallow = per_day_waallow * absent_days

        if absent_days > 0:
            adj_basic = round_up(basic - lop_basic) 
            adj_hra = round_up(hra - lop_hra)
            adj_oallow = round_up(oallow - lop_oallow)
            adj_waallow = round_up(waallow - lop_waallow)
        else:
            adj_basic = basic
            adj_hra = hra
            adj_oallow = oallow
            adj_waallow = waallow

        gross = adj_basic + adj_hra + adj_oallow + adj_waallow

        if ot_hours > 0:
            per_day_salary = basic / Decimal(total_days)
            # Calculate per-hour rate and round to 2 decimal places (paise)
            per_hour_rate = (per_day_salary / Decimal('8')).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            ot_rate = per_hour_rate * Decimal('1')  # 1x rate, can be changed to 2 for double rate
            # Calculate OT amount and round up to nearest rupee
            ot_amount = (Decimal(ot_hours) * ot_rate).quantize(Decimal('1.'), rounding=ROUND_UP)

            print(f"   🟢 OT Hours: {ot_hours} × ₹{round_half_up(ot_rate)} = ₹{round_half_up(ot_amount)}")

            # net_pay += ot_amount

            # ✅ Prepare OT payhead entry (but don't append yet)
            ot_payhead_entry = {
                "PAYHID": 7,  # OT Payhead ID
                "PRHEXPRN": 0.00,
                "PRHAAMT": ot_hours,
                "PRHNAMT": round_up(ot_amount),
            }
        else:
            ot_amount = Decimal('0.00')
            ot_payhead_entry = None

        # Add Bonus Calculation (per-day basis)
        if bonus_days > 0:
            per_day_bonus = round_up(basic / Decimal(total_days))
            bonus_amount = per_day_bonus * Decimal(bonus_days)
            
            print(f"   Bonus Days: {bonus_days} × ₹{round_half_up(per_day_bonus)} = ₹{round_half_up(bonus_amount)}")
            
            # Prepare Bonus payhead entry
            bonus_payhead_entry = {
                "PAYHID": 10,  # Bonus Payhead ID (change to your actual payhead ID)
                "PRHEXPRN": 0.00,
                "PRHAAMT": bonus_days,
                "PRHNAMT": round_up(bonus_amount),
            }
        else:
            bonus_amount = Decimal('0.00')
            bonus_payhead_entry = None
        
        gross = gross + ot_amount + increment + bonus_amount + tea + food - odeduct

        pf_amt = Decimal('0.00')

        if slab.PFEXPRN > 0:
            # PF and ESI Calculations
            if (adj_basic + adj_oallow) >= 15000:
                pf_amt = Decimal('1800.00')
            else:
                pf_amt = (adj_basic + adj_oallow) * (slab.PFEXPRN / 100)

        esi_amt = min(adj_basic + adj_hra + adj_oallow + adj_waallow + increment + bonus_amount + tea + food + ot_amount, 25000) * (slab.ESIEXPRN / 100)

        # Optional deduction on allowances if absent
        lop_allowance_deductions = lop_oallow + lop_waallow if absent_days > 0 else Decimal('0.00')

        total_deductions = round_half_up(pf_amt) + round_up(esi_amt)
        net_pay = gross - total_deductions

        # Create PayrollDetail record
        prd = PayrollDetail.objects.create(
            PRMID=payroll_master,
            EMPLID=emp_id,
            SBRNCHID=branch_id,
            DSGNID=dsgn_id,
            GRADEID=grade_id,
            FDATE=payroll_master.PRMSDATE,
            TDATE=payroll_master.PRMEDATE,
            LOP=lop_basic + lop_hra + lop_oallow + lop_waallow,
            TNOD=payroll_master.WRKDAYS,
            PRD_BPAMT=adj_basic,
            PRD_ERAMT=gross,
            PRD_GPAMT=gross,
            PRD_DDAMT=total_deductions,
            PRD_NPAMT=net_pay,
            PRD_BP_ESI_AMT=0.00,
            PRD_OT_ESI_AMT=0.00,
            PRD_ER_AMT=pf_amt,
            PRDAMTWRDS=num2words(net_pay, to='currency', lang='en_IN'),
            PRD_MONTHID=month_master.MONTHID,
            PMDESC=month_master.MONTHCODE,
        )

        # ✅ Build payhead_entries (without OT yet)
        payhead_entries = [
            {"PAYHID": 2, "PRHEXPRN": 0.00, "PRHAAMT": basic, "PRHNAMT": adj_basic},                      # Basic
            {"PAYHID": 16, "PRHEXPRN": 0.00, "PRHAAMT": hra, "PRHNAMT": adj_hra},                         # HRA
            {"PAYHID": 13, "PRHEXPRN": 0.00, "PRHAAMT": oallow, "PRHNAMT": adj_oallow},                   # Other Allowance
            {"PAYHID": 30, "PRHEXPRN": 0.00, "PRHAAMT": waallow, "PRHNAMT": adj_waallow},                 # Washing Allowance
            {"PAYHID": 5, "PRHEXPRN": slab.PFEXPRN, "PRHAAMT": 0.00, "PRHNAMT": round_half_up(pf_amt)},   # PF
            {"PAYHID": 6, "PRHEXPRN": slab.ESIEXPRN, "PRHAAMT": 0.00, "PRHNAMT": round_up(esi_amt)},      # ESI

            {"PAYHID": 8, "PRHEXPRN": 0.00, "PRHAAMT": increment, "PRHNAMT": round_up(increment)},         # Increment
            {"PAYHID": 28, "PRHEXPRN": 0.00, "PRHAAMT": tea, "PRHNAMT": round_up(tea)},                     # Tea Allowance
            {"PAYHID": 31, "PRHEXPRN": 0.00, "PRHAAMT": food, "PRHNAMT": round_up(food)},                   # Food Allowance
            {"PAYHID": 20, "PRHEXPRN": 0.00, "PRHAAMT": odeduct, "PRHNAMT": round_up(odeduct)},             # Other Deduction
        ]

        # ✅ Add OT row to payhead_entries if applicable
        if ot_payhead_entry:
            payhead_entries.append(ot_payhead_entry)

        if bonus_payhead_entry:
            payhead_entries.append(bonus_payhead_entry)

        # ✅ Insert all payhead rows into PayrollPayheadDetail
        for entry in payhead_entries:
            PayrollPayheadDetail.objects.create(
                PRDID=prd,
                PAYHID=entry["PAYHID"],
                PRHEXPRN=entry["PRHEXPRN"],
                PRHAAMT=entry["PRHAAMT"],
                PRHNAMT=entry["PRHNAMT"],
            )

@receiver(post_save, sender=PayrollMaster)
def trigger_process_payroll(sender, instance, created, **kwargs):
    if created:
        # Now safe to access SBRNCHID
        process_payroll(instance.PRMID, instance.SBRNCHID)