from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class DesignationMaster(models.Model):

    DISPSTATUS_CHOICES_DES = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DSGNID = models.AutoField(primary_key=True)
    DSGNDESC = models.CharField(max_length=100)
    DSGNCODE = models.CharField(max_length=15)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_DES, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DESIGNATIONMASTER'
        managed = False  # Set to True only if Django should create/update this table
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'

    def __str__(self):
        return self.DSGNDESC
    
class DepartmentMaster(models.Model):

    DISPSTATUS_CHOICES_DEPT = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    DEPTID = models.AutoField(primary_key=True)  # IDENTITY column
    DEPTDESC = models.CharField(max_length=100)
    DEPTCODE = models.CharField(max_length=15)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_DEPT, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DEPARTMENTMASTER'
        managed = False  # Prevents Django from modifying this existing table
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.DEPTDESC} ({self.DEPTCODE})"
    
class CompanyMaster(models.Model):

    DISPSTATUS_CHOICES_COMPMAS = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    COMPID = models.AutoField(primary_key=True)
    COMPNAME = models.CharField(max_length=100)
    COMPDNAME = models.CharField(max_length=100)
    COMPADDR1 = models.CharField(max_length=100)
    COMPADDR2 = models.CharField(max_length=100, null=True, blank=True)
    COMPLOCTDESC = models.CharField(max_length=100)
    COMPPINCODE = models.CharField(max_length=100)
    COMPPHN1 = models.CharField(max_length=50, null=True, blank=True)
    COMPPHN2 = models.CharField(max_length=50, null=True, blank=True)
    COMPPHN3 = models.CharField(max_length=50, null=True, blank=True)
    COMPPHN4 = models.CharField(max_length=50, null=True, blank=True)
    COMPMAIL = models.CharField(max_length=50, null=True, blank=True)
    COMPCPRSN = models.CharField(max_length=50, null=True, blank=True)     #Contact Person
    COMPGSTNO = models.CharField(max_length=50, null=True, blank=True)
    COMPWEBSITE = models.CharField(max_length=50, null=True, blank=True)
    COMPPANNO = models.CharField(max_length=50, null=True, blank=True)
    STATEID = models.IntegerField()
    COMPCODE = models.CharField(max_length=50)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_COMPMAS, db_column='DISPSTATUS')
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'COMPANYMASTER'
        managed = False
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.COMPNAME


class StateMaster(models.Model):
    # Define choices for STATETYPE
    STATETYPE_CHOICES = [
        (0, 'Local'),
        (1, 'Interstate'),
    ]

    DISPSTATUS_CHOICES_STATE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    STATEID = models.AutoField(primary_key=True)  # Auto-incrementing integer field for STATEID
    STATEDESC = models.CharField(max_length=100)  
    STATECODE = models.CharField(max_length=15)  
    STATETYPE = models.SmallIntegerField(choices=STATETYPE_CHOICES, db_column='STATETYPE')  # SmallInteger for state type (0=local, 1=interstate)
    CUSRID = models.CharField(max_length=100)  
    LMUSRID = models.CharField(max_length=100)  
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_STATE, db_column='DISPSTATUS')  
    PRCSDATE = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'STATEMASTER' 
        managed = False 
        verbose_name = 'State'
        verbose_name_plural = 'States' 

    def __str__(self):
        return self.STATEDESC
    
class GradeMaster(models.Model):

    DISPSTATUS_CHOICES_GRADE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    GRADEID = models.AutoField(primary_key=True)
    GRADEDESC = models.CharField(max_length=50)
    GRADECODE = models.CharField(max_length=50)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_GRADE, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'GRADEMASTER'  
        managed = False
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return self.GRADEDESC
    
class PayHeadTypeMaster(models.Model):

    DISPSTATUS_CHOICES_PHEADTYPE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    PAYHTID = models.AutoField(primary_key=True)  
    PAYHTDESC = models.CharField(max_length=100) 
    PAYHTCODE = models.CharField(max_length=15) 
    CUSRID = models.CharField(max_length=100)    
    LMUSRID = models.CharField(max_length=100)   
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_PHEADTYPE, db_column='DISPSTATUS')  
    PRCSDATE = models.DateTimeField(auto_now_add=True)        

    class Meta:
        db_table = 'PAYHEADTYPEMASTER'
        managed = False
        verbose_name = 'Pay Head Type'
        verbose_name_plural = 'Pay Head Types'

    def __str__(self):
        return self.PAYHTDESC
    
class AccountGroupMaster(models.Model):

    DISPSTATUS_CHOICES_ACCGRUP = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    ACHEADGID = models.AutoField(primary_key=True)
    ACHEADGDESC = models.CharField(max_length=100)
    ACHEADGCODE = models.CharField(max_length=15)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_ACCGRUP, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ACCOUNTGROUPMASTER'
        managed = False
        verbose_name = 'Account Group'
        verbose_name_plural = 'Account Groups'

    def __str__(self):
        return self.ACHEADGDESC
    
class AdvanceTypeMaster(models.Model):

    DISPSTATUS_CHOICES_ADVTYPE = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    ADVTID = models.AutoField(primary_key=True)
    ADVTDESC = models.CharField(max_length=100)
    ADVTCODE = models.CharField(max_length=50)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_ADVTYPE, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ADVANCETYPEMASTER'
        managed = False
        verbose_name = 'Advance Type'
        verbose_name_plural = 'Advance Types'

    def __str__(self):
        return self.ADVTDESC
    

class BloodGroupMaster(models.Model):

    DISPSTATUS_CHOICES_BLDGRUP = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    BLDGID = models.AutoField(primary_key=True)
    BLDGDESC = models.CharField(max_length=100)
    BLDGCODE = models.CharField(max_length=50)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_BLDGRUP, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BLOODGROUPMASTER'
        managed = False
        verbose_name = 'Blood Group'
        verbose_name_plural = 'Blood Groups'

    def __str__(self):
        return self.BLDGDESC
    
class RelationshipMaster(models.Model):

    DISPSTATUS_CHOICES_RELSHIP = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    RELMID = models.AutoField(primary_key=True)
    RELMDESC = models.CharField(max_length=100)
    RELMCODE = models.CharField(max_length=50)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_RELSHIP, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'RELATIONSHIPMASTER'
        managed = False
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'

    def __str__(self):
        return self.RELMDESC
    
class AccountHeadMaster(models.Model):

    DISPSTATUS_CHOICES_ACCHEAD = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    ACHEADID = models.AutoField(primary_key=True) 
    ACHEADGID = models.ForeignKey(AccountGroupMaster, on_delete=models.PROTECT, db_column='ACHEADGID')   
    ACHEADDESC = models.CharField(max_length=100)  
    ACHEADCODE = models.CharField(max_length=15)  
    CUSRID = models.CharField(max_length=100)  
    LMUSRID = models.CharField(max_length=100)  
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_ACCHEAD, db_column='DISPSTATUS') 
    PRCSDATE = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'ACCOUNTHEADMASTER'
        managed = False
        verbose_name = 'Account Head Master'
        verbose_name_plural = 'Account Head Masters'

    def __str__(self):
        return self.ACHEADDESC
    
class LocationMaster(models.Model):

    DISPSTATUS_CHOICES_LOCATION = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    LOCTID = models.AutoField(primary_key=True)   
    LOCTDESC = models.CharField(max_length=100)
    LOCTCODE = models.CharField(max_length=15)
    STATEID = models.IntegerField()
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_LOCATION, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'LOCATIONMASTER'
        managed = False
        verbose_name = 'Location Master'
        verbose_name_plural = 'Location Masters'

    def __str__(self):
        return self.LOCTDESC
    
class PayHeadMaster(models.Model):

    DISPSTATUS_CHOICES_PAYHEAD = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    PAYHID = models.AutoField(primary_key=True)
    PAYHTID = models.ForeignKey(PayHeadTypeMaster, on_delete=models.PROTECT, db_column='PAYHTID')
    PAYHDESC = models.CharField(max_length=100)
    PAYHCODE = models.CharField(max_length=50)
    DISPORDER = models.SmallIntegerField()
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_PAYHEAD, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PAYHEADMASTER'
        managed = False
        verbose_name = 'Pay Head Master'
        verbose_name_plural = 'Pay Head Masters'

    def __str__(self):
        return self.PAYHDESC
    
class LeaveHeadMaster(models.Model):

    DISPSTATUS_CHOICES_LEHEAD = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    LHMCTYPE_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]

    GNDRID_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Both'),
    ]

    LHMID = models.AutoField(primary_key=True)  
    LHMDESC = models.CharField(max_length=100)
    LHMCODE = models.CharField(max_length=50)
    LHMCTYPE = models.SmallIntegerField(choices=LHMCTYPE_CHOICES, db_column='LHMCTYPE')
    GNDRID = models.IntegerField(choices=GNDRID_CHOICES, db_column='GNDRID')
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_LEHEAD, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'LEAVEHEADMASTER'
        managed = False
        verbose_name = 'Leave Head Master'
        verbose_name_plural = 'Leave Head Masters'

    def __str__(self):
        return self.LHMDESC
    
class LeaveHeadDetail(models.Model):
    LHDID = models.AutoField(primary_key=True)
    LHMID = models.ForeignKey('LeaveHeadMaster', on_delete=models.CASCADE, db_column='LHMID')               
    DSGNID = models.IntegerField()
    LHDNOD = models.SmallIntegerField()
    LHDMNOD = models.SmallIntegerField()
    LHDLNOD = models.SmallIntegerField()

    class Meta:
        db_table = 'LEAVEHEADDETAIL'
        managed = False
        verbose_name = 'Leave Head Detail'
        verbose_name_plural = 'Leave Head Details'

    def __str__(self):
        return self.DSGNID
    
class SubBranchMaster(models.Model):

    DISPSTATUS_CHOICES_SUBBRNC = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    SBRNCHID = models.AutoField(primary_key=True)
    COMPID = models.IntegerField()
    SBRNCHNAME = models.CharField(max_length=50)
    SBRNCHADDR1 = models.CharField(max_length=100)
    SBRNCHADDR2 = models.CharField(max_length=100, blank=True, null=True)
    SBRNCHLOCTDESC = models.CharField(max_length=100)
    SBRNCHPINCODE = models.CharField(max_length=100)
    SBRNCHGSTNO = models.CharField(max_length=50, blank=True, null=True)
    SBRNCHWEBSITE = models.CharField(max_length=50, blank=True, null=True)
    SBRNCHPANNO = models.CharField(max_length=50, blank=True, null=True)
    STATEID = models.IntegerField()
    DISPORDER = models.SmallIntegerField(default=0)
    SBRNCHCODE = models.CharField(max_length=50)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_SUBBRNC, db_column='DISPSTATUS')
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SUBBRANCHMASTER'
        managed = False
        verbose_name = 'Sub Branch'
        verbose_name_plural = 'Sub Branches'

    def __str__(self):
        return self.SBRNCHNAME
    
class EmployeeMaster(models.Model):
    CATESEX_CHOICES=[
        (0, 'Male'),
        (1, 'Female'),
    ]

    CATEMSTATUS_CHOICES=[
        (0, 'Married'),
        (1, 'Unmarried'),
        (2, 'Widow'),
    ]

    CATEQTYPE_CHOICES = [
        (0, 'lliterate'),
        (1, 'Non-Matric'),
        (2, 'Matric'),
        (3, 'Senior Secondary'),
        (4, 'Graduate'),
        (5, 'Post Graduate'),
        (6, 'Doctorate'),
    ]

    CATEGTYPE_CHOICES = [
        (0, 'Not Eligible'),
        (1, 'Eligible'),
        (2, 'New Entrance'),
        (3, 'Left'),
    ]

    CATEMTYPE_CHOICES = [
        (0, 'Not Applicable'),
        (1, 'Applicable'),
        (2, 'New Entrance'),
    ]

    CATEATYPE_CHOICES = [
        (0, 'Not Applicable'),
        (1, 'Applicable'),
        (2, 'New Entrance'),
    ]

    CATEUTYPE_CHOICES = [
        (0, 'Yes'),
        (1, 'No'),
    ]

    DISPSTATUS_CHOICES_EMPLOYEE = [
        (0, 'On Roll'),
        (1, 'Resigned'),
        (1, 'Retired'),
        (1, 'Expired'),
    ]
        
    CATEID = models.AutoField(primary_key=True)
    CATENAME = models.CharField(max_length=100)
    SBRNCHID = models.IntegerField()                                                #Sub-branch ID
    CATEADDR1 = models.CharField(max_length=100, null=True, blank=True)
    CATEADDR2 = models.CharField(max_length=100, null=True, blank=True)
    CATEADDR3 = models.CharField(max_length=100, null=True, blank=True)
    CATEADDR4 = models.CharField(max_length=100, null=True, blank=True)
    CATEADDR5 = models.CharField(max_length=100, null=True, blank=True)
    CATEMAIL = models.CharField(max_length=50, null=True, blank=True)
    CATEPHN1 = models.CharField(max_length=50, null=True, blank=True)
    CATEPHN2 = models.CharField(max_length=50, null=True, blank=True)
    CATEPHN3 = models.CharField(max_length=50, null=True, blank=True)
    CATEPHN4 = models.CharField(max_length=50, null=True, blank=True)
    CATESEX = models.SmallIntegerField(choices=CATESEX_CHOICES, db_column='CATESEX')
    CATEMSTATUS = models.SmallIntegerField(choices=CATEMSTATUS_CHOICES, db_column='CATEMSTATUS')
    CATEDOB = models.DateTimeField(null=True, blank=True)
    CATEAPPDT = models.DateTimeField(null=True, blank=True)
    CATECNDT = models.DateTimeField(null=True, blank=True)
    BLDGID = models.IntegerField()                                                   #Blood Group ID
    GRELMID = models.IntegerField()                                                  #Relationship ID
    CATEQDESC = models.CharField(max_length=50, null=True, blank=True)
    CATEGNAME = models.CharField(max_length=50, null=True, blank=True)
    DEPTID = models.IntegerField()                                                   #Department ID
    DSGNID = models.IntegerField()                                                   #Designation ID
    GRADEID = models.IntegerField()                                                  #Grade ID
    CATEACCNO = models.CharField(max_length=50, null=True, blank=True)
    CATEEMPPF = models.CharField(max_length=50, null=True, blank=True)
    CATEESINO = models.CharField(max_length=50, null=True, blank=True)
    CATEPANNO = models.CharField(max_length=50, null=True, blank=True)
    CATECNAME = models.CharField(max_length=50, null=True, blank=True)
    REASON = models.CharField(max_length=250, null=True, blank=True)
    CATENO = models.IntegerField(null=True, blank=True)
    CATECODE = models.CharField(max_length=50, null=True, blank=True)
    CATEREASON = models.CharField(max_length=250, null=True, blank=True)
    CATERDATE = models.DateTimeField(null=True, blank=True)
    CATEGTYPE = models.SmallIntegerField(null=True, blank=True, choices=CATEGTYPE_CHOICES, db_column='CATEGTYPE')
    CATEMTYPE = models.SmallIntegerField(null=True, blank=True, choices=CATEMTYPE_CHOICES, db_column='CATEMTYPE')
    CATEATYPE = models.SmallIntegerField(null=True, blank=True, choices=CATEATYPE_CHOICES, db_column='CATEATYPE')
    CATEUTYPE = models.SmallIntegerField(null=True, blank=True, choices=CATEUTYPE_CHOICES, db_column='CATEUTYPE')
    CATEIDESC = models.CharField(max_length=250, null=True, blank=True)
    CATELICNO = models.CharField(max_length=100, null=True, blank=True)
    CATEAADHARNO = models.CharField(max_length=25, null=True, blank=True)
    CATEUANNO = models.CharField(max_length=25, null=True, blank=True)
    PFDATE = models.DateTimeField(null=True, blank=True)
    CATEBTYPE = models.SmallIntegerField(default=2)
    CATEQTYPE = models.SmallIntegerField(choices=CATEQTYPE_CHOICES, db_column='CATEQTYPE')
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_EMPLOYEE, db_column='DISPSTATUS')
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.CATECODE:
            last = EmployeeMaster.objects.order_by('-CATEID').first()
            if last and last.CATECODE.isdigit():
                next_code = int(last.CATECODE) + 1
            else:
                next_code = 1
            self.CATECODE = str(next_code).zfill(4)  # Formats like 0001, 0002
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'EMPLOYEEMASTER'
        managed = False
        verbose_name = 'Employee Master'
        verbose_name_plural = 'Employee Masters'

    def __str__(self):
        return self.CATENAME

class SlabMaster(models.Model):

    DISPSTATUS_CHOICES_SLAB = [
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    SLABMID = models.AutoField(primary_key=True)
    COMPYID = models.IntegerField()
    SLABMDATE = models.DateTimeField()
    SLABTID = models.IntegerField(default=2)
    TARIFFMID = models.IntegerField(default=2)
    CATEID = models.IntegerField()
    BRNCHID = models.IntegerField()
    BAMT = models.DecimalField(max_digits=18, decimal_places=2)
    HRAAMT = models.DecimalField(max_digits=18, decimal_places=2)
    OAMT = models.DecimalField(max_digits=18, decimal_places=2)
    PFEXPRN = models.DecimalField(max_digits=18, decimal_places=2)
    ESIEXPRN = models.DecimalField(max_digits=18, decimal_places=2)
    WAMT = models.DecimalField(max_digits=18, decimal_places=2)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.IntegerField(choices=DISPSTATUS_CHOICES_SLAB, db_column='DISPSTATUS', default=0)
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SLABMASTER'
        managed = False
        verbose_name = 'Slab Master'
        verbose_name_plural = 'Slab Masters'

    def __str__(self):
        return self.SLABMDATE

class AttendanceDetail(models.Model):
    
    DISPSTATUS_CHOICES_ATTENDANCE=[
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]

    ATTNDID = models.AutoField(primary_key=True)
    COMPYID = models.IntegerField()
    REGSTRID = models.IntegerField(default=2)
    MONTHID = models.IntegerField()
    ATTNDATE = models.DateTimeField()
    ATTNTFHOUR = models.DateTimeField(null=True, blank=True)
    ATTNTTHOUR = models.DateTimeField(null=True, blank=True)
    ECATEID = models.IntegerField()
    SBRNCHID = models.IntegerField()
    LHMID = models.IntegerField(default=2)
    ATTNFDATE = models.DateTimeField()
    ATTNTDATE = models.DateTimeField()
    ATTNNOD = models.DecimalField(max_digits=18, decimal_places=2)
    ATTNNOB = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ADVAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PFAMT = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    ATTNWNOD = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PATTNDID = models.IntegerField(null=True, blank=True, default=0)
    OTAMT = models.DecimalField(max_digits=18, decimal_places=2)
    INCAMT = models.DecimalField(max_digits=18, decimal_places=2)
    ABAMT = models.DecimalField(max_digits=18, decimal_places=2)
    TEAAMT = models.DecimalField(max_digits=18, decimal_places=2)
    FOODAMT = models.DecimalField(max_digits=18, decimal_places=2)
    OAAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ODAMT = models.DecimalField(max_digits=18, decimal_places=2)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.IntegerField(choices=DISPSTATUS_CHOICES_ATTENDANCE, db_column='DISPSTATUS', default=0)
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ATTENDANCEDETAIL'
        managed = False
        verbose_name = 'Attendance Detail'
        verbose_name_plural = 'Attendance Details'

    def __str__(self):
        return str(self.ECATEID)

    def save(self, *args, **kwargs):
        # Set MONTHID from ATTNDATE
        if self.ATTNDATE:
            self.MONTHID = self.ATTNDATE.month
            self.ATTNFDATE = self.ATTNDATE
            self.ATTNTDATE = self.ATTNDATE

        # Save the object first, so the ATTNDID is populated (if AutoField)
        super().save(*args, **kwargs)


class PayrollMaster(models.Model):

    DISPSTATUS_CHOICES_ATTENDANCE=[
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    PRMID = models.AutoField(primary_key=True)
    COMPYID = models.IntegerField()
    REGSTRID = models.IntegerField(default=1)
    SBRNCHID = models.IntegerField(null=False)
    PRMDATE = models.DateTimeField()
    PRMTYPE = models.SmallIntegerField(default=3)
    MONTHID = models.IntegerField()
    PRMSDATE = models.DateTimeField()
    PRMEDATE = models.DateTimeField()
    WRKDAYS = models.SmallIntegerField()
    PRM_BPAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRM_ERAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRM_GPAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRM_DDAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRM_NPAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRMASDATE = models.DateTimeField()
    PRMAEDATE = models.DateTimeField()
    PTRANID = models.IntegerField(default=0)
    CUSRID = models.CharField(max_length=100)
    LMUSRID = models.CharField(max_length=100)
    DISPSTATUS = models.IntegerField(choices=DISPSTATUS_CHOICES_ATTENDANCE, db_column='DISPSTATUS' ,default=0)
    PRCSDATE = models.DateTimeField(auto_now_add=True)
    PRMBDESC = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'PAYROLLMASTER'
        managed = False
        verbose_name = 'Payroll Master'
        verbose_name_plural = 'Payroll Master'

    def __str__(self):
        return str(self.PRMID)
    
    def save(self, *args, **kwargs):
        if not self.PRMASDATE and self.PRMSDATE:
            self.PRMASDATE = self.PRMSDATE

        if not self.PRMAEDATE and self.PRMEDATE:
            self.PRMAEDATE = self.PRMEDATE

        super().save(*args, **kwargs)


class MonthMaster(models.Model):

    DISPSTATUS_CHOICES_MONTH=[
        (0, 'Enabled'),
        (1, 'Disabled'),
    ]
        
    MONTHID = models.IntegerField(primary_key=True)                        #pk
    MONTHNAME = models.CharField(max_length=50)                            #Month Name                
    MONTHCODE = models.CharField(max_length=5, null=True, blank=True)      #Month Code eg - Jan, Feb etc..,
    DISPORDER = models.SmallIntegerField(null=True, blank=True)            #Disporder
    DISPSTATUS = models.SmallIntegerField(choices=DISPSTATUS_CHOICES_MONTH, db_column='DISPSTATUS', default=0)  #disp_status

    class Meta:
        db_table = 'MONTHMASTER'
        managed = False
        verbose_name = 'Month Master'
        verbose_name_plural = 'Month Masters'

    def __str__(self):
        return self.month_name
    
class AccountingYear(models.Model):
    YRID = models.AutoField(primary_key=True)                               # IDENTITY(1,1)
    FDATE = models.DateTimeField()                                          # smalldatetime maps to DateTimeField
    TDATE = models.DateTimeField()
    YRDESC = models.CharField(max_length=15)
    CUSRID = models.CharField(max_length=100, default=1)
    PRCSDATE = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ACCOUNTINGYEAR'
        managed = False
        verbose_name = 'AccountingYear'
        verbose_name_plural = 'AccountingYears'

    def __str__(self):
        return self.YRDESC
    
class CompanyAccountingDetail(models.Model):
    COMPYID = models.AutoField(primary_key=True)  
    COMPID = models.IntegerField(default=1)              
    YRID = models.IntegerField()                 
    CUSRID = models.CharField(max_length=100, default=1)    
    DISPSTATUS = models.SmallIntegerField(default=0)     
    PRCSDATE = models.DateTimeField(auto_now_add=True)            

    class Meta:
        db_table = 'COMPANYACCOUNTINGDETAIL'    
        managed = False  # Set to True if you want Django to manage the table
        verbose_name = "Company Accounting Detail"
        verbose_name_plural = "Company Accounting Details"

    def __str__(self):
        return f"CompanyAccountingDetail({self.COMPYID})"
    
class PayrollDetail(models.Model):
    PRDID = models.AutoField(primary_key=True)
    PRMID = models.ForeignKey(PayrollMaster, on_delete=models.PROTECT, db_column='PRMID')       #Per Month salary for each employee based on the company and branch
    EMPLID = models.IntegerField()                                                              #Employee id
    SBRNCHID = models.IntegerField()                                                            #Branch id for the employee
    DSGNID = models.IntegerField()                                                              #Employee Designation id
    GRADEID = models.IntegerField()                                                             #Grade id
    FDATE = models.DateTimeField()                                                              #Month Startdate from the Payrollmaster table
    TDATE = models.DateTimeField()                                                              #Month Enddate from the Payrollmaster table
    LOP = models.DecimalField(max_digits=18, decimal_places=2)                                  #Howmany Days Leave in Attendance
    ENOD = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    OTNOD = models.DecimalField(max_digits=18, decimal_places=2, default=0)            
    TNOD = models.DecimalField(max_digits=18, decimal_places=2)                                 #Total Number of days per month
    PRD_BPAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)                 #Basic Amount in slab
    PRD_ERAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)                 #Basic + HRA Amount in slab
    PRD_GPAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)                 #Gross Amount (Basic + HRA) in slab
    PRD_DDAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)                 #Deduction Amount (ESI + PF) - 
    PRD_NPAMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)                 #NP Amount is - Actual Salary
    PRD_BP_ESI_AMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRD_OT_ESI_AMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRD_ER_AMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    PRDAMTWRDS = models.CharField(max_length=250, null=True, blank=True, default=0)             #please covert in words from PRD_NPAMT
    PMONTHID = models.IntegerField(default=0)
    PMDESC = models.CharField(max_length=10, default=0)
    PRD_MONTHID = models.IntegerField(default=0)
    DISPORDER = models.SmallIntegerField(default=0)
    PSTATUS = models.SmallIntegerField(default=0)
    PRD_OP_AMT = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    PRD_CL_AMT = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    PRD_DP_AMT = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    PRD_OT_AMT = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = 'PAYROLLDETAIL'
        managed = False  # Set to True if you want Django to manage the table
        verbose_name = 'Payroll Detail'
        verbose_name_plural = 'Payroll Details'

    def __str__(self):
        return f"PayrollDetail {self.PRDID}"
    
class PayrollPayheadDetail(models.Model):
    PRHID = models.AutoField(primary_key=True)                                              #Pk
    PRDID = models.ForeignKey(PayrollDetail, on_delete=models.PROTECT, db_column='PRDID')   #fk for Payroll detail
    PAYHID = models.IntegerField()                                                          #payhead master (enabled)
    PRHEXPRN = models.DecimalField(max_digits=18, decimal_places=2)                         #PRHEXPRN in slab PF,ESI only
    PRHAAMT = models.DecimalField(max_digits=18, decimal_places=2)                          #PRHAAMT Basic, HRA, O-Allow, W-Allow
    PRHNAMT = models.DecimalField(max_digits=18, decimal_places=2)                          #PRHNAMT Basic, HRA, O-Allow, W-Allow
    PRHSTATUS = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'PAYROLLPAYHEADDETAIL'
        managed = False  # Set to True if you want Django to manage the table
        verbose_name = 'Payroll Payhead Detail'
        verbose_name_plural = 'Payroll Payhead Details'

    def __str__(self):
        return f"PayrollDetail {self.PRHID}"


class CustomUser(AbstractUser):
    mobile = models.TextField(db_column='mobile', null=True, blank=True)  # better to allow blank=True for forms

    class Meta:
        db_table = 'PayRoll_App_customuser' 
        managed = False
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.username  # simplified, username always exists on AbstractUser


class TempReportID(models.Model):
    KUSRID = models.CharField(max_length=50)
    OPTNSTR = models.CharField(max_length=50)
    RPTID = models.IntegerField()

    class Meta:
        db_table = 'TMPRPT_IDS'
        unique_together = ('KUSRID', 'OPTNSTR', 'RPTID')  # Important!
        verbose_name = 'TempReportID'
        verbose_name_plural = 'TempReportIDS'
        managed = False  # If it's a legacy table, don't let Django try to create it