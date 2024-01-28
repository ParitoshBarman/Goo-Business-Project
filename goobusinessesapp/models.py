from django.db import models
from datetime import datetime

# Create your models here.
class AllServices(models.Model):
    slID = models.AutoField(primary_key=True)
    selectImage = models.ImageField( upload_to="AllServicesDBimgFolder")
    name = models.CharField(max_length=122)
    homepagecatagori = models.CharField(blank=True, null=True, max_length=50)
    Offer = models.IntegerField()
    silverPrice = models.IntegerField()
    silverLeads = models.CharField(max_length=40)
    silverDay = models.IntegerField()
    goldPrice = models.IntegerField()
    goldLeads = models.CharField(max_length=40)
    goldDay = models.IntegerField()
    diamondPrice = models.IntegerField()
    diamondLeads = models.CharField(max_length=40)
    diamondDay = models.IntegerField()
    desc = models.TextField()
    slag = models.SlugField(default="best")
    tags = models.CharField(max_length=200, blank=True, null=True,)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

class ClickHistry(models.Model):
    productLink = models.URLField()
    slID = models.IntegerField()
    name = models.CharField(max_length=122)
    totalClick = models.IntegerField()
    timee = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.name

class UserDetails(models.Model):
    slID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=122)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    whatsapp = models.CharField(null=True,blank=True,max_length=20)
    totalOrder = models.IntegerField(default=0)
    totalSpent = models.IntegerField(default=0)
    totalPaymentReceived = models.IntegerField(null=True,blank=True,default=0)
    lastOrderdate = models.DateField(auto_now=True)
    joiningdate = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.fullname
    
class PerDayOrderPerUser(models.Model):
    fullname = models.CharField(max_length=122)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    orderNo = models.IntegerField()
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.fullname

class OrderList(models.Model):
    slID = models.AutoField(primary_key=True)
    expectedDeliveryDate = models.DateField(blank=True, null=True)
    selectFile = models.FileField(null=True, blank=True, upload_to="FileDBFolder")
    fullname = models.CharField(max_length=122)
    trakingLink = models.URLField(blank=True, default="")
    paymentLink = models.URLField(blank=True, default="")
    productLink = models.URLField(blank=True,default="")
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(null=True,blank=True,max_length=20)
    totalprice = models.IntegerField(null=True, blank=True)
    countryoption = models.CharField(max_length=100)
    servicesOption = models.CharField(max_length=50)
    enterbuget = models.IntegerField(null=True, blank=True)
    numberofleads = models.IntegerField(null=True, blank=True)
    requirmentdesc = models.TextField(null=True, blank=True)
    productID = models.IntegerField()
    onlyCountryCode = models.CharField(max_length=20)
    otp = models.IntegerField()
    otpStatus = models.CharField(max_length=50)
    orderStatus = models.CharField(max_length=70)
    orderCoplition = models.IntegerField()
    peymentStatus = models.CharField(max_length=50)
    jobDownload = models.FileField(null=True, blank=True, upload_to="CompleteJobDBFolder")
    odrTime = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
   
    


class FreeTrialUser(models.Model):
    slID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    freeTrialStatus = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    

class FreeTrialRequest(models.Model):
    slID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.email
    
class FreeTrialUnderReview(models.Model):
    slID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    linkedIn_Profile = models.URLField()
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.email
    
class ControlWeb(models.Model):
    VarName = models.CharField(max_length=122)
    charecterVar = models.CharField(max_length=122, null=True, blank=True)
    integetVar = models.IntegerField(null=True, blank=True)
    emailVar = models.EmailField(max_length=254, null=True, blank=True)
    textVar = models.TextField(null=True, blank=True)
    datetimeVar = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.VarName
    

class ContactMessage(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    dateee = models.DateField()
    def __str__(self):
        return self.fullname


class WhyUsDB(models.Model):
    Title = models.CharField(null=True,blank=True,max_length=50)
    Subtitle = models.CharField(null=True,blank=True,max_length=254)
    ImagePic = models.ImageField(null=True,blank=True, upload_to="WhyDBFolder")
    imageWidth = models.CharField(null=True,blank=True,max_length=10,default="")
    imageHeight = models.CharField(null=True,blank=True,max_length=10,default="")
    description = models.TextField(null=True,blank=True)
    

class AboutDB(models.Model):
    Title = models.CharField(null=True,blank=True,max_length=50)
    Subtitle = models.CharField(null=True,blank=True,max_length=254)
    ImagePic = models.ImageField(null=True,blank=True, upload_to="AboutDBFolder")
    imageWidth = models.CharField(null=True,blank=True,max_length=10,default="")
    imageHeight = models.CharField(null=True,blank=True,max_length=10,default="")
    description = models.TextField(null=True,blank=True)



class EmailSeenDB(models.Model):
    Title = models.CharField(null=True,blank=True,max_length=50)
    email = models.EmailField(null=True, blank=True, max_length=254)
    numberOfSeen = models.IntegerField()
    lastseenTime = models.TimeField(auto_now=True)
    lastSeen = models.DateField(auto_now=True)


    
class ExtraImageDB(models.Model):
    Title = models.CharField(null=True,blank=True,max_length=50)
    selectImage = models.ImageField(upload_to="ExtraImageDBFolder")
    upTime = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

class OpenViaEmail(models.Model):
    email = models.EmailField(max_length=254)
    openType = models.CharField(max_length=100)
    openNo = models.IntegerField()
    opnmessage = models.CharField(max_length=120)
    lastTime = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)

class InternalVisit(models.Model):
    email = models.EmailField(max_length=254)
    openType = models.CharField(max_length=100)
    openNo = models.IntegerField()
    opnmessage = models.CharField(max_length=120)
    lastTime = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)

class ClickHistryByUser(models.Model):
    userAuthDt = models.CharField(max_length=254)
    productLink = models.URLField()
    slID = models.IntegerField()
    name = models.CharField(max_length=122)
    totalClick = models.IntegerField()
    timee = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.name
    
class UnsubscribeList(models.Model):
    email = models.EmailField(max_length=254)
    count = models.IntegerField(default=1)
    timee = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)

class SubscribeList(models.Model):
    email = models.EmailField(max_length=254)
    count = models.IntegerField(default=1)
    timee = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)


class RegistationFormDB(models.Model):
    slID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    ChooseJobOrInternship = models.CharField(max_length=50)
    ChooseFieldOfInterest = models.CharField(max_length=50)
    HighestQualification = models.CharField(max_length=50)
    CollegeName = models.CharField(max_length=100)
    MajorFieldOfStudy = models.CharField(max_length=50)
    YearOfGraduation = models.IntegerField(null=True, blank=True)
    WorkExperienceIfAny = models.TextField(null=True, blank=True)
    GitHubProfile = models.URLField(blank=True, default="")
    LinkedInProfile = models.URLField(blank=True, default="")
    ResumePDF = models.FileField(null=True, blank=True, upload_to="Resumes")
    otp = models.IntegerField()
    otpStatus = models.CharField(max_length=50)
    peymentStatus = models.CharField(max_length=50)
    odrTime = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)



class InternUserDetails(models.Model):
    slID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=122)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    whatsapp = models.CharField(null=True,blank=True,max_length=20)
    totalInternshipApply = models.IntegerField(default=0)
    totalInternshipCompleted = models.IntegerField(default=0)
    totalPaymentReceived = models.IntegerField(null=True,blank=True,default=0)
    lastInterndate = models.DateField(auto_now=True)
    joiningdate = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.fullname

class BatchesInstractions(models.Model):
    batchName = models.CharField(max_length=50)
    Instractions = models.TextField(null=True, blank=True)
    lastUpdate = models.DateField(auto_now=True)
    startDate = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.batchName

class AllInternBatchs(models.Model):
    slID = models.AutoField(primary_key=True)
    EmployeeID = models.CharField(max_length=40)
    batchName = models.CharField(max_length=30)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20 , null=True, blank=True)
    ChooseJobOrInternship = models.CharField(max_length=50)
    ChooseFieldOfInterest = models.CharField(max_length=50)
    HighestQualification = models.CharField(max_length=50)
    CollegeName = models.CharField(max_length=100)
    MajorFieldOfStudy = models.CharField(max_length=50)
    YearOfGraduation = models.IntegerField(null=True, blank=True)
    WorkExperienceIfAny = models.TextField(null=True, blank=True)
    GitHubProfile = models.URLField(blank=True, default="")
    LinkedInProfile = models.URLField(blank=True, default="")
    address = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    countryCode = models.CharField(max_length=6)
    pinCode = models.CharField(max_length=6)
    payment = models.BooleanField(default=False)
    paymentStatus = models.CharField(max_length=30,null=True,blank=True)
    paymentAmount = models.IntegerField(null=True,blank=True,default=0)
    projectGitHubLinkCount = models.IntegerField(null=True,blank=True,default=0)
    liveLinkCount = models.IntegerField(null=True,blank=True,default=0)
    totalMassage = models.IntegerField(null=True,blank=True,default=0)
    confidenceMarks = models.IntegerField(null=True,blank=True,default=0)
    codingMarks = models.IntegerField(null=True,blank=True,default=0)
    outputMarks = models.IntegerField(null=True,blank=True,default=0)
    onTimeSubmitMarks = models.IntegerField(null=True,blank=True,default=0)
    remark = models.CharField(max_length=30)
    acceptTime = models.TimeField(auto_now_add=True)
    acceptdate = models.DateField(auto_now_add=True)

class CallingConverssionTrack(models.Model):
    slID = models.IntegerField(null=True,blank=True,default=0)
    EmployeeID = models.CharField(max_length=40)
    batchName = models.CharField(max_length=30)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    payment = models.BooleanField(default=False)
    paymentStatus = models.CharField(max_length=30,null=True,blank=True)
    paymentAmount = models.IntegerField(null=True,blank=True,default=0)
    lastUpdateTime = models.TimeField(auto_now=True)
    lastUpdatedate = models.DateField(auto_now=True)
    acceptTime = models.TimeField(auto_now_add=True)
    acceptdate = models.DateField(auto_now_add=True)
