from django.db import connection

def call_ratecard_proc(branch_id):
    """
    Executes the stored procedure and returns results with a 'pk' field
    mapped from 'SLABMID' to support Django URL reversal in templates.
    """
    with connection.cursor() as cursor:
        cursor.execute("EXEC pr_NEW_RATECARDMASTER_FLX_ASSGN_01 %s", [branch_id])
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            row_dict['pk'] = row_dict.get('SLABMID')  # map the primary key
            results.append(row_dict)
    return results


def call_attendance_proc(branch_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC pr_search_ATTENDANCEDETAIL %s", [branch_id])
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results