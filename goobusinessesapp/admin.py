from django.contrib import admin
from goobusinessesapp.models import RegistationFormDB, InternUserDetails, AllServices, ClickHistry, UserDetails, PerDayOrderPerUser, OrderList, FreeTrialUser, FreeTrialRequest, FreeTrialUnderReview, ContactMessage, ControlWeb, WhyUsDB, AboutDB, EmailSeenDB, ExtraImageDB, OpenViaEmail, InternalVisit, ClickHistryByUser, UnsubscribeList, SubscribeList, BatchesInstractions, AllInternBatchs, CallingConverssionTrack, TransectionHistory
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class AllServicesV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name','slID','selectImage','homepagecatagori','date')
admin.site.register(AllServices,AllServicesV)

class ClickHistryV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('name','slID','productLink','totalClick','timee','date')
admin.site.register(ClickHistry,ClickHistryV)

class ClickHistryByUserV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('userAuthDt','name','slID','productLink','totalClick','timee','date')
admin.site.register(ClickHistryByUser,ClickHistryByUserV)

class UserDetailsV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','totalSpent','totalPaymentReceived','lastOrderdate','joiningdate')
admin.site.register(UserDetails, UserDetailsV)

class InternUserDetailsV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','totalInternshipApply','totalInternshipCompleted','totalPaymentReceived','joiningdate')
admin.site.register(InternUserDetails, InternUserDetailsV)

class PerDayOrderPerUserV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','phone','orderNo','date')
admin.site.register(PerDayOrderPerUser, PerDayOrderPerUserV)

class FreeTrialRequestV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','date')
admin.site.register(FreeTrialRequest, FreeTrialRequestV)

class FreeTrialUnderReviewV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','date')
admin.site.register(FreeTrialUnderReview, FreeTrialUnderReviewV)

class ControlWebV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('VarName','charecterVar','integetVar','emailVar')
admin.site.register(ControlWeb, ControlWebV)

class ContactMessageV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','subject','message','dateee')
admin.site.register(ContactMessage,ContactMessageV)

class OrderListAdminV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('slID','fullname','email','servicesOption','otpStatus','expectedDeliveryDate','date','odrTime')
admin.site.register(OrderList,OrderListAdminV)

class RegistationFormDBAdminV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('slID','fullname','email','phone','otpStatus','date','odrTime','LinkedInProfile','ResumePDF')
admin.site.register(RegistationFormDB, RegistationFormDBAdminV)

class UserAdminNC(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('fullname','email','freeTrialStatus')
admin.site.register(FreeTrialUser, UserAdminNC)


class WhyUsDBV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('Title','Subtitle','ImagePic','description')
admin.site.register(WhyUsDB, WhyUsDBV)
class AboutDBV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('Title','Subtitle','ImagePic','description')
admin.site.register(AboutDB, AboutDBV)

class EmailSeenDBV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('email','numberOfSeen','Title','lastSeen','lastseenTime')
admin.site.register(EmailSeenDB, EmailSeenDBV)

class ExtraImageDBV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('Title','selectImage','upTime','date')
admin.site.register(ExtraImageDB, ExtraImageDBV)

class OpenViaEmailv(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('email','openType','openNo','opnmessage','lastTime','date')
admin.site.register(OpenViaEmail, OpenViaEmailv)

class InternalVisitV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('email','openType','openNo','opnmessage','lastTime','date')
admin.site.register(InternalVisit, InternalVisitV)

class UnsubscribeListV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('email','timee','date')
admin.site.register(UnsubscribeList, UnsubscribeListV)

class SubscribeListV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('email','count','timee','date')
admin.site.register(SubscribeList, SubscribeListV)

class BatchesInstractionsV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('batchName', 'lastUpdate', 'startDate')
admin.site.register(BatchesInstractions, BatchesInstractionsV)




class AllInternBatchsV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('slID', 'EmployeeID', 'batchName', 'fullname', 'email', 'countryCode', 'phone', 'whatsapp', 'ChooseJobOrInternship', 'ChooseFieldOfInterest', 'HighestQualification', 'CollegeName', 'MajorFieldOfStudy', 'YearOfGraduation', 'WorkExperienceIfAny', 'GitHubProfile', 'LinkedInProfile', 'address', 'country', 'pinCode', 'payment', 'paymentStatus', 'paymentAmount', 'projectGitHubLinkCount', 'liveLinkCount', 'totalMassage', 'confidenceMarks', 'codingMarks', 'outputMarks', 'onTimeSubmitMarks', 'remark', 'acceptTime', 'acceptdate')
admin.site.register(AllInternBatchs, AllInternBatchsV)

class CallingConverssionTrackV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('slID', 'EmployeeID', 'batchName', 'fullname', 'email', 'phone', 'payment', 'paymentStatus', 'paymentAmount', 'lastUpdateTime', 'lastUpdatedate', 'acceptTime', 'acceptdate')
admin.site.register(CallingConverssionTrack, CallingConverssionTrackV)

class TransectionHistoryV(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('slID', 'fullname', 'email', 'phone', 'payment', 'paymentStatus', 'paymentAmount', 'lastUpdateTime', 'lastUpdatedate', 'acceptTime', 'acceptdate','razorpay_payment_iddb','razorpay_order_iddb','razorpay_signaturedb')
admin.site.register(TransectionHistory, TransectionHistoryV)
