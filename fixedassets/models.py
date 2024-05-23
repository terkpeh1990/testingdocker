from django.db import models
from simple_history.models import HistoricalRecords
from .util import *
from company.models import Devision,Sub_Devision
from authentication.models import Grade


# Create your models here.
class Classification(models.Model):
    name = models.CharField(max_length=100)
    
    history = HistoricalRecords()
    class Meta:
        db_table = 'Classifications'
        verbose_name = 'Classification'
        verbose_name_plural = 'Classifications'

        permissions = [
            ("custom_create_classification", "Can Create Classification"),
        ]

    def __str__(self):
        return self.name
    

class AccountingRecognition(models.Model):
    name = models.CharField(max_length=100)
    classification = models.ForeignKey('Classification', related_name='recognitionclassification', on_delete=models.CASCADE,null=True,blank=True)
    history = HistoricalRecords()
    class Meta:
        db_table = 'AccountingRecognitions'
        verbose_name = 'AccountingRecognition'
        verbose_name_plural = 'AccountingRecognitions'

        permissions = [
            ("custom_create_accounting_recognition", "Can Create Accounting Recognition"),
        ]

    def __str__(self):
        return self.name

class GFSCategory(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255,null=True)
    history = HistoricalRecords()
    class Meta:
        db_table = 'GFSCategorys'
        verbose_name = 'GFSCategory'
        verbose_name_plural = 'GFSCategory'

        permissions = [
            ("custom_create_gfscategory", "Can Create GFSCategory"),
        ]

    def __str__(self):
        return f"{self.code}-{self.name}"


class IPSASCategory(models.Model):
    name = models.CharField(max_length=255)
    classification = models.ForeignKey('Classification', related_name='ipsasclassification', on_delete=models.CASCADE)
    gfscategory = models.ForeignKey('GFSCategory', related_name='ipsasgfscategory', on_delete=models.CASCADE,null=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'IPSASCategorys'
        verbose_name = 'IPSASCategory'
        verbose_name_plural = 'IPSASCategorys'
        permissions = [
            ("custom_create_IPSAS_category", "Can Create IPSAS Category"),
        ]
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    ipsascategory = models.ForeignKey('IPSASCategory', related_name='subcategoryipsas', on_delete=models.CASCADE,null=True)
    history = HistoricalRecords()
    class Meta:
        db_table = 'SubCategorys'
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategorys'

        permissions = [
            ("custom_create_subcategory", "Can Create Sub Category"),
        ]

    def __str__(self):
        return self.name

class Location(models.Model):
    code = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    history = HistoricalRecords()

    class Meta:
        db_table = 'Locations'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        permissions = [
            ("custom_create_location", "Can Create Location"),
        ]
    def __str__(self):
        return f"{self.code} {self.location}"


class SourceOfFunding(models.Model):
    code = models.CharField(max_length=255)
    funding = models.CharField(max_length=255)
    history = HistoricalRecords()

    class Meta:
        db_table = 'SourceOfFundings'
        verbose_name = 'SourceOfFunding'
        verbose_name_plural = 'SourceOfFundings'
        permissions = [
            ("custom_create_source_of_fundings", "Can Create SourceOfFunding"),
        ]
    
    def __str__(self):
        return f"{self.code } {self.funding}"

class MothodofAcquisition(models.Model):
    name = models.CharField(max_length=100)
    
    history = HistoricalRecords()
    class Meta:
        db_table = 'MothodofAcquisitions'
        verbose_name = 'MothodofAcquisition'
        verbose_name_plural = 'MothodofAcquisitions'

        permissions = [
            ("custom_create_mothodofacquisition", "Can Create Mothod of Acquisition"),
        ]

    def __str__(self):
        return self.name


class FixedAsset(models.Model):
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usage = (
        ('Public Domain', 'Public Domain'),
        ('Private Domain', 'Private Domain'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    status = (
        ('In Use', 'In Use'),
        ('Not in Use', 'Not in Use'),
        ('Retired', 'Retired'),
        ('Disposed', 'Disposed'),
        ('On-going', 'On-going'),
        ('Abandoned', 'Abandoned'),
        ('Suspended', 'Suspended'),
        
    )
    st = (
        
        ('Assigned', 'Assigned'),
        ('Avialable', 'Avialable'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    bcondition = (
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    accountingstatus = (
        ('In-progress','In-progress'),
        ('Completed','Completed'),
        ('Completed and Transferred','Completed and Transferred'),
       
    )
    asset_id = models.CharField(max_length=255,null=True)
    classification = models.ForeignKey('Classification', related_name='classification', on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=255,null=True)
    registrationnumber = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Vehicle With this Registration number already exist."})
    accountingrecognition = models.ForeignKey('AccountingRecognition', related_name='accountingrecognition', on_delete=models.CASCADE,null=True)
    depreciation = models.CharField(max_length=4,choices=condition,null=True)
    amotization = models.CharField(max_length=4, choices=condition, null=True)
    usage = models.CharField(max_length=17, choices=usage, null=True)
    ipsascategory  = models.ForeignKey('IPSASCategory', related_name='ipsascategory', on_delete=models.CASCADE,null=True)
    subcategory  = models.ForeignKey('SubCategory', related_name='subcategory', on_delete=models.CASCADE,null=True)
    gfscategory  = models.ForeignKey('GFSCategory', related_name='gfscategory', on_delete=models.CASCADE,null=True)
    size =  models.CharField(max_length=255,null=True)
    quantity =models.PositiveIntegerField(default=1,null=True)
    location  = models.ForeignKey('Location', related_name='assetlocation', on_delete=models.CASCADE,null=True)
    usagetype = models.CharField(max_length=10,choices=usagetype,null=True)
    ghanapostgpsaddress = models.CharField(max_length=255,null=True)
    dateplacedinservice = models.DateField(null=True)
    colour = models.CharField(max_length=255,null=True)
    chassisno = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Asset With this Chassis/Serial number already exist."})
    tagno = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Asset With this Chassis/Serial number already exist."})
    engineserialno = models.CharField(max_length=255,null=True,unique=True, error_messages={'unique':"Asset With this Tag number already exist."})
    manufacturer = models.ForeignKey('inventory.Brands', related_name='manufacturername', on_delete=models.CASCADE,null=True)
    model = models.CharField(max_length=255,null=True)
    modelyear = models.IntegerField(null=True)
    costcenter = models.ForeignKey('company.Devision', related_name='assetcostcenter', on_delete=models.CASCADE,null=True)
    subcostcenter = models.name = models.ForeignKey('company.Sub_Devision', related_name='assetsubcostcenter', on_delete=models.CASCADE,null=True)
    titled = models.CharField(max_length=4, choices=condition, null=True)
    staffid = models.CharField(max_length=255,null=True)
    fullname = models.CharField(max_length=255,null=True)
    position = models.name = models.ForeignKey('authentication.Grade', related_name='position', on_delete=models.CASCADE,null=True)
    methodofacquisition  = models.ForeignKey('MothodofAcquisition', related_name='assetmethodofacquisition', on_delete=models.CASCADE,null=True)
    currentstatus = models.CharField(max_length=30,choices=status,default='In Use',null=True)
    conditions = models.CharField(max_length=40,choices=bcondition,null=True)
    investmentproperty = models.CharField(max_length=4,choices=condition,null=True)
    fundsource = models.ForeignKey('SourceOfFunding', related_name='assetfundsource', on_delete=models.CASCADE,null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    usefullife = models.PositiveIntegerField(default=0,null=True) 
    desposal_date = models.DateField(null=True)
    methodofdesposal = models.CharField(max_length=50,choices=disposal,null=True)
    proceedsfromsales = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    commencement_date = models.DateField(null=True)
    expectedcompletion_date = models.DateField(null=True)
    accountingstatus = models.CharField(max_length=50,choices=accountingstatus,null=True)
    costbf = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    currentperiodcost = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    costcf = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    comments = models.CharField(max_length=255,null=True)
    accumulateddepreciation = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    currentdepreciation = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    totaldepreciation = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    netbookvalue = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    user = models.ForeignKey('authentication.User', related_name='currentuser', on_delete=models.CASCADE,null=True)
    product= models.ForeignKey('inventory.Products', related_name='fixedassetproduct', on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=30,choices=st,null=True)
    depreciatedlife  = models.PositiveIntegerField(default=0,null=True)
    usefullifebalance = models.PositiveIntegerField(default=0,null=True)
    sra=models.CharField(max_length=255,null=True)
    class Meta:
        db_table = 'FixedAssets'
        verbose_name = 'FixedAsset'
        verbose_name_plural = 'FixedAssets'

        permissions = [
            ("custom_create_fixedassets", "Can Create Fixed Assets"),
            ("custom_view_fixedassets", "Can View Fixed Assets"),
            ("custom_delete_fixedassets", "Can Delete Fixed Assets"),
            ("custom_run_depreciation_on_fixed", "Can Run Depreciaition on Fixed Assets"),
        ]

    def __str__(self):
        return self.description


    def save(self, *args, **kwargs):
        if not self.asset_id:
            incrementor = None
            if self.classification.name == 'Land':
                incrementor = asset_incrementor(100000)
            elif self.classification.name == 'Buldings And Other Structures':
                incrementor = asset_incrementor(200000)
            elif self.classification.name == 'Transport Equipments':
                incrementor = asset_incrementor(400000)
            elif self.classification.name == 'Outdoor Machinery And Equipments':
                incrementor = asset_incrementor(500000)
            elif self.classification.name == 'Indoor':
                incrementor = asset_incrementor(600000)
            else:
                incrementor = asset_incrementor(800000)

            if incrementor:
                self.asset_id = incrementor()
                while FixedAsset.objects.filter(asset_id=self.asset_id, classification=self.classification).exists():
                    self.asset_id = incrementor()
        self.gfscategory = self.ipsascategory.gfscategory
        self.usefullifebalance = self.usefullife - self.depreciatedlife
        self.netbookvalue = float(self.value) - float(self.accumulateddepreciation)
        super(FixedAsset, self).save(*args, **kwargs)
    

class FixedAssetsAssignment(models.Model):
       usagetype = (
            ('Pool', 'Pool'),
            ('Assigned', 'Assigned'),
        )

       status = (
            ('Returned', 'Returned'),
            ('Assigned', 'Assigned'),
        )

       usagetype = models.CharField(max_length=10,choices=usagetype,null=True)
       asset = models.ForeignKey('FixedAsset', related_name='fixedasset', on_delete=models.CASCADE)
       user = models.ForeignKey('authentication.User', related_name='assignedto', on_delete=models.CASCADE,null=True)
       costcenter = models.ForeignKey('company.Devision', related_name='assigntocostcenter', on_delete=models.CASCADE,null=True)
       subcostcenter = models.name = models.ForeignKey('company.Sub_Devision', related_name='assigntoubcostcenter', on_delete=models.CASCADE,null=True)
       assigndate = models.DateField(null=True)
       status = models.CharField(max_length=50,choices=status,default='Assigned',null=True)
       requisition  = models.ForeignKey('inventory.Requisition', related_name='assignrequisition', on_delete=models.CASCADE,null=True)
       allocation = models.ForeignKey('inventory.Allocation', related_name='assignallocation', on_delete=models.CASCADE,null=True)
       returndate = models.DateField(null=True)

       class Meta:

            db_table = 'FixedAssetsAssignments'
            verbose_name = 'FixedAssetsAssignment'
            verbose_name_plural = 'FixedAssetsAssignments'

       def __str__(self):
            return self.user

    
class Depreciation(models.Model):
    status = (
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
        )
    accountingyear = models.OneToOneField('accounting.Fiscal_year', related_name='accountingyear', on_delete=models.CASCADE,unique=True, error_messages={'unique':"Depreciation For This Accounting Year Has Already Been Calculated."})
    depreciationvalue = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    status = models.CharField(max_length=50,choices=status,default='In Progress',null=True)
    class Meta:
    
        db_table = 'Depreciations'
        verbose_name = 'Depreciation'
        verbose_name_plural = 'Depreciations'

        def __str__(self):
            return self.user

class DepreciationDetail(models.Model):
    
    depreciation = models.ForeignKey('Depreciation', related_name='depreciationdetail', on_delete=models.CASCADE,null=True)
    asset = models.ForeignKey('FixedAsset', related_name='depreciationasset', on_delete=models.CASCADE,null=True)
    depreciationvalue = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    

    def __str__(self):
        return str(self.depreciationvalue)

    class Meta:
        db_table = 'DepreciationDetails'
        managed = True
        verbose_name = 'DepreciationDetail'
        verbose_name_plural = 'DepreciationDetails'


class Reevaluation(models.Model):
   
    accountingyear = models.ForeignKey('accounting.Fiscal_year', related_name='evaluateaccountingyear', on_delete=models.CASCADE)
    asset = models.ForeignKey('FixedAsset', related_name='evaluationasset', on_delete=models.CASCADE,null=True)
    oldvalue = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    newvalue = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True)
    previoususefullife = models.PositiveIntegerField(default=0,null=True) 
    usefullife = models.PositiveIntegerField(default=0,null=True) 
    class Meta:
    
        db_table = 'Reevaluations'
        verbose_name = 'Reevaluation'
        verbose_name_plural = 'Reevaluations'

        def __str__(self):
            return self.asset.description


class Disposals(models.Model):

    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
       
    accountingyear = models.ForeignKey('accounting.Fiscal_year', related_name='disposalaccountingyear', on_delete=models.CASCADE)
    asset = models.ForeignKey('FixedAsset', related_name='disposalasset', on_delete=models.CASCADE,null=True)
    desposal_date = models.DateField(null=True)
    methodofdesposal = models.CharField(max_length=50,choices=disposal,null=True)
    proceedsfromsales = models.DecimalField(max_digits=18, decimal_places=2,default=0.00,null=True)
    class Meta:
    
        db_table = 'Disposals'
        verbose_name = 'Disposal'
        verbose_name_plural = 'Disposals'

        def __str__(self):
            return self.asset.description




