from django.shortcuts import render, redirect, HttpResponse
from django.http import FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from goobusinessesapp.models import RegistationFormDB, InternUserDetails, AllServices, ClickHistry, UserDetails, PerDayOrderPerUser, OrderList, FreeTrialUser, FreeTrialRequest, FreeTrialUnderReview, ContactMessage, WhyUsDB, AboutDB, ControlWeb, EmailSeenDB, OpenViaEmail, InternalVisit, ClickHistryByUser, UnsubscribeList, SubscribeList, BatchesInstractions, AllInternBatchs, CallingConverssionTrack
from django.http import JsonResponse
import random
import re
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from datetime import timedelta
# import datetime as dtpari
import threading
import markdown
import json

OurMainURL = "https://goobusiness.autoimg.xyz/"

global lastUpdatetime
lastUpdatetime = datetime.now()


# for email functions
def sendEmail(emailReceiver,otp):
    if emailReceiver!="":
        senderEmail = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
        ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
        smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
        messagee = MIMEMultipart("alternative")
        messagee["Subject"] = f'OTP Varification {datetime.now()}'
        messagee["From"] = senderEmail
        messagee["To"] = emailReceiver
        htmlHead = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{margin: 0;padding: 0;font-family: Arial, Helvetica, sans-serif;
}
.header{background-color: #2874f0;width: 100%;min-height: 54px;}
h1{color: rgb(9, 164, 9);margin: 10px;text-align: center;}
.data{color: blueviolet;}
.msg{margin:60px 0px;color: #5f6368;text-align: center;}
.button {text-decoration: none;padding: 10px 20px;font-size: x-large;letter-spacing: 3px;color: #474a4f;}
.button:hover{color: black;}
</style>
</head>"""
        htmlBody = f"""<body>
<div class="header"></div>
<h1>Goo Business<br>OTP Verification</h1>
<div class="msg">This is your one time OTP<br><br><div class="button">{otp}</div></div>
<div class="msg">Please keep in mind do not refresh the page</div>
</body>
</html>"""
        html = htmlHead + htmlBody
        part2 = MIMEText(html, "html")
        messagee.attach(part2)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as server:
                server.login(senderEmail, ePassword)
                server.sendmail(senderEmail, emailReceiver, messagee.as_string())
                # emailStatus = 'Email also successfully received.....'
                # print('Success......')
        except:
            sendEmailFaild('Faild to send OTP')

def sendEmailAndPassword(emailReceiver,users_password):
    if emailReceiver!="":
        senderEmail = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
        ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
        smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
        messagee = MIMEMultipart("alternative")
        messagee["Subject"] = f'Successfully accepted your resume {datetime.now()}'
        messagee["From"] = senderEmail
        messagee["To"] = emailReceiver
        htmlHead = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{margin: 0;padding: 0;font-family: Arial, Helvetica, sans-serif;
}
.header{background-color: #2874f0;width: 100%;min-height: 54px;}
h1{color: rgb(9, 164, 9);margin: 10px;text-align: center;}
.data{color: blueviolet;}
.msg{margin:60px 0px;color: #5f6368;text-align: center;}
</style>
</head>"""
        htmlBody = f"""<body>
<div class="header"></div>
<h1>Goo Business<br>Successfully accepted your resume</h1>
<div class="msg">Your login credential:<br><br>Dashboard: <a href="{OurMainURL}dashboard">"{OurMainURL}dashboard"</a><br>Username: "{emailReceiver}"<br>Password: "{users_password}"</div>
<div class="msg">Please do not share your login credential with anyone.</div>
<img src="{OurMainURL}emailseen/{emailReceiver}/intern01batchusernamepassword" alt="Image not found" hidden>
</body>
</html>"""
        html = htmlHead + htmlBody
        part2 = MIMEText(html, "html")
        messagee.attach(part2)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as server:
                server.login(senderEmail, ePassword)
                server.sendmail(senderEmail, emailReceiver, messagee.as_string())
                # emailStatus = 'Email also successfully received.....'
                # print('Success......')
        except:
            sendEmailFaild('Faild to send LogIn credential')


def sendEmailFaild(messageText):
    emailReceiver="barmanpari163@gmail.com"
    emailSender = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
    ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
    smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
    subject = f"Website send Email Faild {datetime.now()}"
    body =messageText

    em = EmailMessage()
    em['From'] = emailSender
    em['To'] = emailReceiver
    em['subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as smtp:
        smtp.login(emailSender, ePassword)
        smtp.sendmail(emailSender, emailReceiver, em.as_string())

def sendEmailForTraking(emailReceiver,trakingLink,serviceLink):
    if emailReceiver!="":
        senderEmail = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
        ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
        smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
        messagee = MIMEMultipart("alternative")
        messagee["Subject"] = f'Order traking details {datetime.now()}'
        messagee["From"] = senderEmail
        messagee["To"] = emailReceiver

        htmlHead = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{margin: 0;padding: 0;font-family: Arial, Helvetica, sans-serif;
}
.header{background-color: #2874f0;width: 100%;min-height: 54px;}
h1{color: rgb(6, 173, 6);margin: 10px;text-align: center;}
.data{color: blueviolet;}
.msg{margin:60px 0px;color: #5f6368;text-align: center;}
.button {background-color: #2874f0;color: #ffffff;text-decoration: none;padding: 10px 20px;font-weight: bold;border-radius: 5px;}
.button:hover{background-color: #289dcf;}
</style>
</head>"""
        htmlBody = f"""<body>
<div class="header"></div>
<h1>Goo Business<br>Track your service</h1>
<div class="msg">Track your service by clicking the bellow button<br><br><a href="{trakingLink}" class="button" target="_blank" style="color: white;">Track Now</a></div>
<div class="msg">Open your choosen service by clicking the bellow button<br><br><a href="{serviceLink}" class="button" target="_blank" style="color: white;">Open Service</a></div>
</body>
</html>"""
        html = htmlHead + htmlBody
        part2 = MIMEText(html, "html")
        messagee.attach(part2)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as server:
                server.login(senderEmail, ePassword)
                server.sendmail(senderEmail, emailReceiver, messagee.as_string())
                # emailStatus = 'Email also successfully received.....'
                # print('Success......')
        except:
            sendEmailFaild('Faild to send Traking Seevice link')

def odrNDlastTime():
    randomMinTimeOB = ControlWeb.objects.get(VarName="RandomMinTime")
    randomMinTime = randomMinTimeOB.integetVar
    randomMaxTimeOB = ControlWeb.objects.get(VarName="RandomMaxTime")
    randomMaxTime = randomMaxTimeOB.integetVar
    randomTimeSecOB = ControlWeb.objects.get(VarName="RandomTimeSec")
    randomTimeSec = randomTimeSecOB.integetVar
    minimumOrderOB = ControlWeb.objects.get(VarName="MinimumOrder")
    totalOrderOB = ControlWeb.objects.get(VarName="TotalOrder")
    randomOrderOB = ControlWeb.objects.get(VarName="RandomOrder")
    randomOrderMinOB = ControlWeb.objects.get(VarName="RandomOrderMin")
    randomOrderMaxOB = ControlWeb.objects.get(VarName="RandomOrderMax")
    global lastUpdatetime
    ekhon = datetime.now()
    if (ekhon-lastUpdatetime).total_seconds()>randomTimeSec:
        randomTimeSec = random.randint(randomMinTime, randomMaxTime)
        randomTimeSecOB.integetVar = randomTimeSec
        randomTimeSecOB.save()
        lastUpdatetime = datetime.now()
        randomOrderOB.integetVar = random.randint(randomOrderMinOB.integetVar, randomOrderMaxOB.integetVar)
        randomOrderOB.save()
        totalOrderOB.integetVar = minimumOrderOB.integetVar+randomOrderOB.integetVar
        totalOrderOB.save()
        
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/home", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/home", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    randomMinTimeOB = ControlWeb.objects.get(VarName="RandomMinTime")
    randomMinTime = randomMinTimeOB.integetVar
    randomMaxTimeOB = ControlWeb.objects.get(VarName="RandomMaxTime")
    randomMaxTime = randomMaxTimeOB.integetVar
    randomTimeSecOB = ControlWeb.objects.get(VarName="RandomTimeSec")
    randomTimeSec = randomTimeSecOB.integetVar
    minimumOrderOB = ControlWeb.objects.get(VarName="MinimumOrder")
    totalOrderOB = ControlWeb.objects.get(VarName="TotalOrder")
    randomOrderOB = ControlWeb.objects.get(VarName="RandomOrder")
    randomOrderMinOB = ControlWeb.objects.get(VarName="RandomOrderMin")
    randomOrderMaxOB = ControlWeb.objects.get(VarName="RandomOrderMax")
    minmumShowTime = ControlWeb.objects.get(VarName="MinimumShowTime")
    global lastUpdatetime
    ekhon = datetime.now()
    if (ekhon-lastUpdatetime).total_seconds()>randomTimeSec:
        randomTimeSec = random.randint(randomMinTime, randomMaxTime)
        randomTimeSecOB.integetVar = randomTimeSec
        randomTimeSecOB.save()
        lastUpdatetime = datetime.now()
        randomOrderOB.integetVar = random.randint(randomOrderMinOB.integetVar, randomOrderMaxOB.integetVar)
        randomOrderOB.save()
        totalOrderOB.integetVar = minimumOrderOB.integetVar+randomOrderOB.integetVar
        totalOrderOB.save()
        numberoforder = totalOrderOB.integetVar
        lastdeliverytime = minmumShowTime.integetVar
    else:
        numberoforder = totalOrderOB.integetVar
        lastdeliverytime = minmumShowTime.integetVar + int((ekhon-lastUpdatetime).total_seconds()/60)

    leadGenerationProducts = AllServices.objects.filter(homepagecatagori__icontains="lead generation").all()
    LinkedInSpecialProducts = AllServices.objects.filter(homepagecatagori__icontains="LinkedIn Special").all()
    DataScrapingProducts = AllServices.objects.filter(homepagecatagori__icontains="Data Scraping").all()
    WebResearchProducts = AllServices.objects.filter(homepagecatagori__icontains="Web Research").all()
    DataEntrySpecialProducts = AllServices.objects.filter(homepagecatagori__icontains="Data Entry Special").all()
    FileConvertionProducts = AllServices.objects.filter(homepagecatagori__icontains="File Convertion").all()
    sendVar = {
            'numberoforder' : numberoforder,
            'lastdeliverytime' : lastdeliverytime,
            'leadGenerationProducts' : leadGenerationProducts,
            'LinkedInSpecialProducts' : LinkedInSpecialProducts,
            'WebResearchProducts' : WebResearchProducts,
            'DataScrapingProducts' : DataScrapingProducts,
            'DataEntrySpecialProducts' : DataEntrySpecialProducts,
            'FileConvertionProducts' : FileConvertionProducts
        }
    return render(request, 'index.html', sendVar)

def freetrail(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/freetrail", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/freetrail", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    return render(request, 'freetrialform.html')
def freetrialcheck(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/freetrialcheck", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/freetrialcheck", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        try:
            getfreetrialuser = FreeTrialUser.objects.get(email=email)
            getfreetrialuser.freeTrialStatus = "used"
            getfreetrialuser.save()
            try:
                cheackFretrialRequest = FreeTrialRequest.objects.get(email=email)
                return render(request, 'alreadyusefreetrial.html') 
            except:
                freeTrialRequestSave = FreeTrialRequest(fullname=fullname,email=email)
                freeTrialRequestSave.save()
                return render(request, 'orderanythingwewillautodd.html')
        except:
            return render(request, 'notfreetrialuserneedresister.html')
    
def searching(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/searching", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/searching", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    if request.method == "POST":
        searchingValue = request.POST.get('seachbar')
        searchingValue = searchingValue.lower()
        searchingValue = "".join(searchingValue.rstrip().lstrip())
        # print(f"This is search Value ====>>>>  {searchingValue}")
        # filteredProducts = AllProducts.objects.filter(tags_icontains=searchingValue).all()
        filteredProducts = AllServices.objects.filter(tags__icontains=searchingValue).all()
        flVar = {
            'totalResult' : len(filteredProducts),
            'filteredProducts' : filteredProducts
        }

    else:
        filteredProducts = AllServices.objects.all()
        flVar = {
            'totalResult' : len(filteredProducts),
            'filteredProducts' : filteredProducts
        }
    return render(request, 'searching.html', flVar)
def servicepage(request, slag, slID):
    searchingValue = slID
    filteredProducts = AllServices.objects.get(slID=searchingValue)
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/servicepage", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/servicepage", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
            
        try:
            clickProdectByUsr = ClickHistryByUser.objects.get(slID=slID, userAuthDt=request.user.get_username())
            clickProdectByUsr.totalClick = clickProdectByUsr.totalClick + 1
            clickProdectByUsr.save()
        except:
            addclickProdectByUsr = ClickHistryByUser(userAuthDt=request.user.get_username(), productLink=f"{OurMainURL}servicepage/{filteredProducts.slag}/{slID}", slID=slID, name=filteredProducts.name, totalClick=1)
            addclickProdectByUsr.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    # print(f'This is ======>>>>  {strr}')
    flVar = {
        'filteredProduct' : filteredProducts
    }
    try:
        clickProdect = ClickHistry.objects.get(slID=filteredProducts.slID)
        clickProdect.totalClick = clickProdect.totalClick + 1
        clickProdect.save()
    except:
        addclickProdect = ClickHistry(productLink=f"{OurMainURL}servicepage/{filteredProducts.slag}/{searchingValue}", slID=filteredProducts.slID, name=filteredProducts.name, totalClick=1)
        addclickProdect.save()
    return render(request, 'servicepage.html', flVar)
def ordercontinue(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/ordercontinue", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/ordercontinue", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('emaill')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        totalprice = request.POST.get('totalprice')
        countryoption = request.POST.get('countryoption')
        servicesOption = request.POST.get('servicesOption')
        enterbuget = request.POST.get('enterbuget')
        numberofleads = request.POST.get('numberofleads')
        requirmentdesc = request.POST.get('requirmentdesc')
        productID = request.POST.get('productID')
        if type(request.POST.get('file')) != str:
            file = request.FILES['file']
        else:
            file = None
        matchkora = re.search(r"\+.*", countryoption)
        onlyCountryCode = matchkora.group()
        onlyCountryCode = onlyCountryCode.replace(" ", "")
        onlyCountryCode = onlyCountryCode.replace("-", "")


        try:
            try:
                checkUser = UserDetails.objects.get(phone=phone)
                if checkUser.email == email:
                    # print('********************111111')
                    try:
                        PerDayOrderPerUserDB = PerDayOrderPerUser.objects.get(phone=phone)
                        if PerDayOrderPerUserDB.orderNo<5:
                            PerDayOrderPerUserDB.orderNo = PerDayOrderPerUserDB.orderNo+1
                            PerDayOrderPerUserDB.save()
                            otp = random.randint(1000, 9999)
                            try:
                                # sendEmail(email, str(otp))
                                thithi = threading.Thread(target=sendEmail, args=[email, str(otp)])
                                thithi.start()
                            except:
                                sendEmailFaild("OTP can't send please cheack the system")
                                # print('Faild...')
                            # print('********************22222222222')
                            OrderListDB = OrderList(selectFile=file, fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
                            OrderListDB.save()
                            passingSLID = OrderListDB.slID
                            
                            return render(request, 'otovarification.html', {'slid':passingSLID})
                        else:
                            return render(request, 'crossdailylimit.html')
                    except:
                        PerDayOrderPerUserDB = PerDayOrderPerUser(fullname=fullname, phone=phone, email=email, orderNo=1)
                        PerDayOrderPerUserDB.save()
                        otp = random.randint(1000, 9999)
                        try:
                            # sendEmail(email, str(otp))
                            thithi = threading.Thread(target=sendEmail, args=[email, str(otp)])
                            thithi.start()
                        except:
                            sendEmailFaild("OTP can't send please cheack the system")
                            # print('Faild...')
                        # print('********************33333333')
                        OrderListDB = OrderList(selectFile=file, fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
                        OrderListDB.save()
                        passingSLID = OrderListDB.slID
                        passingSLID = OrderListDB.slID
                        
                        return render(request, 'otovarification.html', {'slid':passingSLID})
                else:
                    # print('********************444444444')
                    return render(request, 'emailandphonenotmatch.html')
            except:
                checkUser = UserDetails.objects.get(email=email)
                # print('********************5555555555555555555')
                if checkUser.phone == phone:
                    # print('********************555555555555')
                    try:
                        PerDayOrderPerUserDB = PerDayOrderPerUser.objects.get(phone=phone)
                        if PerDayOrderPerUserDB.orderNo<5:
                            PerDayOrderPerUserDB.orderNo = PerDayOrderPerUserDB.orderNo+1
                            PerDayOrderPerUserDB.save()
                            otp = random.randint(1000, 9999)
                            try:
                                # sendEmail(email, str(otp))
                                thithi = threading.Thread(target=sendEmail, args=[email, str(otp)])
                                thithi.start()
                            except:
                                sendEmailFaild("OTP can't send please cheack the system")
                                # print('Faild...')
                            # print('********************6666666666666666')
                            OrderListDB = OrderList(selectFile=file, fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
                            OrderListDB.save()
                            passingSLID = OrderListDB.slID
                            passingSLID = OrderListDB.slID
                            
                            return render(request, 'otovarification.html', {'slid':passingSLID})
                        else:
                            # print('********************77777777777777')
                            return render(request, 'crossdailylimit.html')
                    except:
                        # print('********************88888888888888888')
                        PerDayOrderPerUserDB = PerDayOrderPerUser(fullname=fullname, phone=phone, email=email, orderNo=1)
                        PerDayOrderPerUserDB.save()
                        otp = random.randint(1000, 9999)
                        try:
                            # sendEmail(email, str(otp))
                            thithi = threading.Thread(target=sendEmail, args=[email, str(otp)])
                            thithi.start()
                        except:
                            sendEmailFaild("OTP can't send please cheack the system")
                            # print('Faild...')

                        OrderListDB = OrderList(selectFile=file, fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
                        OrderListDB.save()
                        passingSLID = OrderListDB.slID
                        passingSLID = OrderListDB.slID
                        
                        # print('********************999999999999999999')
                        return render(request, 'otovarification.html', {'slid':passingSLID})
                else:
                    # print('********************101010101010100101010')
                    return render(request, 'emailandphonenotmatch.html')
        except:
            # print('********************110110110110110110110110110110')
            UserDetailsDB = UserDetails(fullname=fullname, phone=phone, email=email, whatsapp=whatsapp, totalOrder=0, totalSpent=0)
            UserDetailsDB.save()
            PerDayOrderPerUserDB = PerDayOrderPerUser(fullname=fullname, phone=phone, email=email, orderNo=1)
            PerDayOrderPerUserDB.save()
            otp = random.randint(1000, 9999)
            try:
                # sendEmail(email, str(otp))
                thithi = threading.Thread(target=sendEmail, args=[email, str(otp)])
                thithi.start()
            except:
                sendEmailFaild("OTP can't send please cheack the system")
                # print('Faild...')
            # print('********************1212121212121212121212121212121')
            OrderListDB = OrderList(selectFile=file, fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
            # OrderListDB = OrderList(fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
            OrderListDB.save()
            passingSLID = OrderListDB.slID
            # print(passingSLID)
            # print('********************1313131313131313131313131313113')
            return render(request, 'otovarification.html', {'slid':passingSLID})
                 
def ordersuccessfull(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/ordersuccessfull", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/ordersuccessfull", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    if request.method == 'POST':
        otp = request.POST.get('otp')
        slid = request.POST.get('slid')
        # print(otp)
        # print(slid)
        OrderDetails = OrderList.objects.get(slID=int(slid))
        dbotp = OrderDetails.otp
        OrderDetails.trakingLink = f"{OurMainURL}ordertraking/{OrderDetails.email}/{OrderDetails.phone}/{OrderDetails.otp}/{OrderDetails.slID}"
        pID = OrderDetails.productID
        OrderDetails.productLink = f"{OurMainURL}servicepage/yourorder/{pID}"
        OrderDetails.save()
        OrderedServiseDetails = AllServices.objects.get(slID=pID)
        todayDate = datetime.today()
        if OrderDetails.servicesOption == 'silver':
            OrderDetails.expectedDeliveryDate = todayDate + timedelta(days=OrderedServiseDetails.silverDay)
            OrderDetails.save()
        elif OrderDetails.servicesOption == 'gold':
            OrderDetails.expectedDeliveryDate = todayDate + timedelta(days=OrderedServiseDetails.goldDay)
            OrderDetails.save()
        elif OrderDetails.servicesOption == 'diamond':
            OrderDetails.expectedDeliveryDate = todayDate + timedelta(days=OrderedServiseDetails.diamondDay)
            OrderDetails.save()
        else:
            OrderDetails.expectedDeliveryDate = todayDate
            OrderDetails.save()


        if OrderDetails.otpStatus == "oneChance" and dbotp==int(otp):
            OrderDetails.otpStatus = "OTP Verified"
            OrderDetails.save()
            
            try:
                thithi2 = threading.Thread(target=sendEmailForTraking, args=[OrderDetails.email, OrderDetails.trakingLink, OrderDetails.productLink])
                thithi2.start()
            except:
                sendEmailFaild("OTP can't send please cheack the system")
                # print('Faild...')
            UserUpdt = UserDetails.objects.get(email=OrderDetails.email)
            UserUpdt.totalOrder=UserUpdt.totalOrder+1
            UserUpdt.totalSpent=UserUpdt.totalSpent+OrderDetails.totalprice
            UserUpdt.save()
            return render(request, 'ordersuccessfull.html')
        else:
            OrderDetails.otpStatus = "Verification Faild"
            OrderDetails.save()
            return render(request, 'verificationfail.html')

        

def ordertraking(request, email, phone, otp, slID):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/ordertraking", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/ordertraking", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    trakingData = OrderList.objects.get(slID=slID, email=email, phone=phone, otp=otp)
    email = trakingData.email
    emln = len(email)
    slcemail = email[emln-int(emln/2):]
    hidenEmail=""
    for illllaa in range(0, emln-len(slcemail)):
        hidenEmail = hidenEmail+"*"
    hidenEmail = hidenEmail+slcemail
    try:
        serviceType = trakingData.servicesOption
        if (serviceType=="silver" or serviceType=="gold" or serviceType=="diamond" or "*" in serviceType) and "eliver" not in trakingData.orderStatus: 
            exptDLDt = trakingData.expectedDeliveryDate
            odrTm = trakingData.odrTime
            asakoraTime = datetime(exptDLDt.year, exptDLDt.month, exptDLDt.day, odrTm.hour, odrTm.minute, odrTm.second)
            elaTim = datetime.now()
            ekhonSomoy = datetime(elaTim.year, elaTim.month, elaTim.day, elaTim.hour, elaTim.minute, elaTim.second)
            bakiAcheTime = asakoraTime-ekhonSomoy
        else:
            bakiAcheTime=""
    except:
        # print('Fail..............................')
        pass
    try:
        if type(trakingData.jobDownload.url)==str:
            jobDownloadLink = trakingData.jobDownload.url
        else:
            jobDownloadLink=""
    except:
        jobDownloadLink=""
    # print(f'{jobDownloadLink}------------------------------------------------------')
    otd = {
        'name' : trakingData.fullname,
        'email' : hidenEmail,
        'phone' : f"XXXXXXX{trakingData.phone[7:]}",
        'package' : trakingData.servicesOption,
        'total' : trakingData.totalprice,
        'orderstatus' : trakingData.orderStatus,
        'ordercomplition' : trakingData.orderCoplition,
        'paymentstatus' : trakingData.peymentStatus,
        'paymentLink' : trakingData.paymentLink,
        'jobDownloadLink' : jobDownloadLink,
        'bakiAcheTime' : bakiAcheTime
    }
    return render(request, 'ordertraking.html', otd)
def successfulysendunderhumanreview(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/successfulysendunderhumanreview", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/successfulysendunderhumanreview", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        linkedinlink = request.POST.get('linkedinlink')
        savedt = FreeTrialUnderReview(fullname=fullname, email=email, linkedIn_Profile=linkedinlink)
        savedt.save()
        return render(request, 'successfulysendunderhumanreview.html')


def contact(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/contact", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/contact", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email3 = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        dateee = datetime.today()
        cmsgdb = ContactMessage(fullname=fullname, email=email3, phone=phone, subject=subject, message=message, dateee=dateee)
        cmsgdb.save()
        senderEmail = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
        ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
        smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
        receiverEmail = ControlWeb.objects.get(VarName="Receiver Email").emailVar
        # receiverEmail = "systemready2014@gmail.com"
        messagee = MIMEMultipart("alternative")
        messagee["Subject"] = f"GooBusinesses Contact Message form {fullname}"
        messagee["From"] = senderEmail
        messagee["To"] = receiverEmail

        htmlHead = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                *{
                    margin: 0;
                    padding: 0;
                }
                .header{
                    background-color: #417690;;
                    width: 100%;
                    height: 54px;
                }
                h1{
                    color: green;
                    margin: 10px;
                }
                .data{
                    color: blueviolet;
                }
                
                .subjectcl{
                    text-align:center;
                    margin: 5px 0px;
                    color:green;
                }
                .msg{
                    margin:3px 0px;
                }
            </style>
        </head>"""
        htmlBody = f"""
                    <body>
                <div class="header"></div>
                <h1>Hi Welcome to Goo Businesses</h1>
                    <h3><span>Date: </span><span class="data">{dateee}</span></h3>
                    <h3><span>Name: </span><span class="data">{fullname}</span></h3>
                    <h3><span>Phone: </span><span class="data">{phone}</span></h3>
                    <h3><span>Email: </span><span class="data">{email3}</span></h3>
                    <h2 class="data subjectcl">{subject}</h2>
                    <pre class="msg">{message}</pre>
            </body>
        </html>
                """
        html = htmlHead + htmlBody
        part2 = MIMEText(html, "html")
        messagee.attach(part2)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as server:
                server.login(senderEmail, ePassword)
                server.sendmail(senderEmail, receiverEmail, messagee.as_string())
                # emailStatus = 'Email also successfully received.....'
                # print('Success......')
        except:
            pass
            # print('Fail....')
            # emailStatus = ''
        return render(request, 'contact.html', {'backmsg': 'Message sent successfully'})
        
    return render(request, 'contact.html')



def whyus(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/whyus", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/whyus", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    whyusContents = WhyUsDB.objects.all()
    sendWhVar = {'whyusContents' : whyusContents}
    return render(request, 'whyus.html', sendWhVar)

def about(request):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/about", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/about", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    whyusContents = AboutDB.objects.all()
    sendWhVar = {'whyusContents' : whyusContents}
    return render(request, 'about.html', sendWhVar)


def emailseen(request, email, msgtitle):
    try:
        openEmail = EmailSeenDB.objects.get(email=email)
        openEmail.numberOfSeen = openEmail.numberOfSeen + 1
        openEmail.save()
    except:
        addopenEmail = EmailSeenDB(Title=msgtitle,email=email,numberOfSeen=1)
        addopenEmail.save()
    # img = open('static/img/ThankYou.JPG', 'rb')
    # response = FileResponse(img)
    # return response

def openvia(request, email, opentype, openmessage):
    user = authenticate(request, username=email, password="golgolgo1234golgolgol")
    if user is not None:
        login(request, user)
    try:
        openviaEmail = OpenViaEmail.objects.get(email=email, openType=opentype, opnmessage=openmessage)
        openviaEmail.openNo = openviaEmail.openNo + 1
        openviaEmail.save()
    except:
        openviaEmail = OpenViaEmail(email=email, openType=opentype, opnmessage=openmessage, openNo=1)
        openviaEmail.save()
    if opentype=="home":
        return redirect("/")
    else:
        return redirect(f'/{opentype}')
    
def unsubscribe(request, email):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/unsubscribe", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/unsubscribe", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    unsdata = UnsubscribeList(email=email)
    unsdata.save()
    try:
        unsdata = UnsubscribeList.objects.get(email=email)
        unsdata.count = unsdata.count + 1
        unsdata.save()
    except:
        unsdata = UnsubscribeList(email=email, count=1)
        unsdata.save()
    return render(request, 'unsubscribe.html', {'email':email})

def subscribe(request, email):
    if request.user.is_authenticated:
        try:
            internalVisitt = InternalVisit.objects.get(email=request.user.get_username(), openType="/subscribe", opnmessage="Internal Visit")
            internalVisitt.openNo = internalVisitt.openNo + 1
            internalVisitt.save()
        except:
            internalVisitt = InternalVisit(email=request.user.get_username(), openType="/subscribe", opnmessage="Internal Visit", openNo=1)
            internalVisitt.save()
    thuthuthu = threading.Thread(target=odrNDlastTime)
    thuthuthu.start()
    if request.method == 'POST':
        email3 = request.POST.get('email')
        try:
            unsdata = SubscribeList.objects.get(email=email3)
            unsdata.count = unsdata.count + 1
            unsdata.save()
        except:
            unsdata = SubscribeList(email=email3, count=1)
            unsdata.save()
        return render(request, 'subscribe.html')
    if "@" in email:
        try:
            user = authenticate(request, username=email, password="golgolgo1234golgolgol")
            if user is not None:
                login(request, user)
            try:
                unsdata = SubscribeList.objects.get(email=email)
                unsdata.count = unsdata.count + 1
                unsdata.save()
            except:
                unsdata = SubscribeList(email=email, count=1)
                unsdata.save()
        except:
            try:
                unsdata = SubscribeList.objects.get(email=email)
                unsdata.count = unsdata.count + 1
                unsdata.save()
            except:
                unsdata = SubscribeList(email=email, count=1)
                unsdata.save()
        return render(request, 'subscribe.html')
    else:
        if request.user.is_authenticated:
            try:
                unsdata = SubscribeList.objects.get(email=request.user.get_username())
                unsdata.count = unsdata.count + 1
                unsdata.save()
            except:
                unsdata = SubscribeList(email=request.user.get_username(), count=1)
                unsdata.save()
            return render(request, 'subscribe.html')
        else:
            return render(request, 'subscribeform.html')
        
def timeck(request):
    return HttpResponse(f"{datetime.now()}")

def registationform(request):
    return render(request, "registationform.html")

def registationcontinue(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        ChooseJobOrInternship = request.POST.get('jobType')
        ChooseFieldOfInterest = request.POST.get('fieldOfInterest')
        HighestQualification = request.POST.get('highestQualification')
        CollegeName = request.POST.get('collegeName')
        MajorFieldOfStudy = request.POST.get('major')
        YearOfGraduation = request.POST.get('graduationYear')
        WorkExperienceIfAny = request.POST.get('workExperience')
        GitHubProfile = request.POST.get('github')
        LinkedInProfile = request.POST.get('linkedin')

        if type(request.POST.get('resume')) != str:
            file = request.FILES['resume']
        else:
            file = None

        try:
            ccckkee = InternUserDetails.objects.get(email=email)
        except:
            InternUserDetailsDB = InternUserDetails(fullname=fullname, phone=phone, email=email)
            InternUserDetailsDB.save()
        otp = random.randint(1000, 9999)
        try:
            # sendEmail(email, str(otp))
            thithi = threading.Thread(target=sendEmail, args=[email, str(otp)])
            thithi.start()
        except:
            sendEmailFaild("OTP can't send please cheack the system")
            # print('Faild...')
        # print('********************1212121212121212121212121212121')
        OrderListDB = RegistationFormDB(ResumePDF=file, fullname=fullname, email=email, phone=phone, otp=otp, otpStatus="oneChance", peymentStatus="due", ChooseJobOrInternship=ChooseJobOrInternship, ChooseFieldOfInterest=ChooseFieldOfInterest, HighestQualification=HighestQualification, CollegeName=CollegeName, MajorFieldOfStudy=MajorFieldOfStudy, YearOfGraduation=YearOfGraduation, WorkExperienceIfAny=WorkExperienceIfAny, GitHubProfile=GitHubProfile, LinkedInProfile=LinkedInProfile)
        # OrderListDB = OrderList(fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
        OrderListDB.save()
        passingSLID = OrderListDB.slID
        # print(passingSLID)
        # print('********************1313131313131313131313131313113')
        return render(request, 'varification.html', {'slid':passingSLID})
            

               
def registationsuccessfull(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        slid = request.POST.get('slid')
        OrderDetails = RegistationFormDB.objects.get(slID=int(slid))
        dbotp = OrderDetails.otp

        if OrderDetails.otpStatus == "oneChance" and dbotp==int(otp):
            OrderDetails.otpStatus = "OTP Verified"
            OrderDetails.save()
            
            # try:
            #     thithi2 = threading.Thread(target=sendSuccessfullEmail, args=[OrderDetails.email, OrderDetails.trakingLink, OrderDetails.productLink])
            #     thithi2.start()
            # except:
            #     sendEmailFaild("OTP can't send please cheack the system")
                # print('Faild...')
            UserUpdt = InternUserDetails.objects.get(email=OrderDetails.email)
            UserUpdt.totalInternshipApply+=1
            UserUpdt.save()
            return render(request, 'registationsuccessfull.html')
        else:
            OrderDetails.otpStatus = "Verification Faild"
            OrderDetails.save()
            return render(request, 'verificationfail.html')


def Login(request):
    return render(request, "login.html")
def loginsuccess(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, "login.html", {"msg":"Invalid Credential!"})
    else:
        return redirect("/login")



def dashboard(request):
    if request.user.is_authenticated:
        # The user is logged in
        # Perform actions for authenticated users
        try:
            searchStudent = AllInternBatchs.objects.get(email=request.user.username)
            data = BatchesInstractions.objects.get(batchName=searchStudent.batchName)
            htmldata = markdown.markdown(data.Instractions)
            return render(request, "dashboard.html", {"htmldata":htmldata, "studentName":searchStudent.fullname})
        except:
            htmldata = '<h2 style="color:red;">Sorry you are no longer participant!</h2>'
            return render(request, "dashboard.html", {"htmldata":htmldata, "studentName":"Employee Dashboard"})
    else:
        # The user is not logged in
        # Perform actions for unauthenticated users
        return redirect("/login")
    

def newadminmanagingdashboard(request):
    if request.user.is_active and request.user.is_superuser:
        obj = RegistationFormDB.objects.filter(ChooseFieldOfInterest="Web", otpStatus="OTP Verified").all().order_by("slID")
        
        return render(request, "newadminmanagingdashboard.html", {'serverdata':obj[:5], "totalReamin":len(obj)})
    else:
        return HttpResponse("<h1>Sorry you have not permition to access</h1>")


@csrf_exempt
def userbatchandemailrequest(request):
    if request.method == 'POST' and request.user.is_staff:
        objdata = json.loads(request.body.decode('utf-8'))
        slid = objdata["slid"]
        email = objdata["email"]
        try:
            user = User.objects.create_user(email, email, "Intern123")
            user.save()

            searchData = RegistationFormDB.objects.get(slID=int(slid), email=email)
            searchData.otpStatus = "Complete"

            newData = AllInternBatchs(batchName="intrn_01", fullname=searchData.fullname, email=searchData.email, phone=searchData.phone, ChooseJobOrInternship=searchData.ChooseJobOrInternship, ChooseFieldOfInterest=searchData.ChooseFieldOfInterest, HighestQualification=searchData.HighestQualification, CollegeName=searchData.CollegeName, MajorFieldOfStudy=searchData.MajorFieldOfStudy, YearOfGraduation=searchData.YearOfGraduation, WorkExperienceIfAny=searchData.WorkExperienceIfAny, GitHubProfile=searchData.GitHubProfile, LinkedInProfile=searchData.LinkedInProfile)
            newData.save()
            searchData.save()

            newData.EmployeeID = f"intrn01_{newData.slID}"
            newData.save()

            # sendEmailAndPassword(email, "Intern123")
            try:
                openEmail = EmailSeenDB.objects.get(email=email, Title="intern01batchusernamepassword")
                openEmail.numberOfSeen = 0
                openEmail.Title = "intern01batchusernamepassword"
                openEmail.save()
            except:
                addopenEmail = EmailSeenDB(Title="intern01batchusernamepassword",email=email,numberOfSeen=0)
                addopenEmail.save()


            return JsonResponse({'massage':'success'})
        except:
            searchData = RegistationFormDB.objects.get(slID=int(slid), email=email)
            searchData.otpStatus = "Multi try"
            searchData.save()
            return JsonResponse({'massage':'Alrady exist!'})
    return JsonResponse({'massage':'faild'})

@csrf_exempt
def resentuserbatchandemailrequest(request):
    if request.method == 'POST' and request.user.is_staff:
        objdata = json.loads(request.body.decode('utf-8'))
        email = objdata["email"]
        # sendEmailAndPassword(email, "Intern123")
        print("Successfully Sent Email...")
        return JsonResponse({'massage':'success'})
    return JsonResponse({'massage':'faild'})






def notlogin(request, startnum):
    if request.user.is_active and request.user.is_staff:
        obj = User.objects.filter(last_login=None).all().order_by("date_joined")
        
        return render(request, "notlogin.html", {'serverdata':obj[startnum:startnum+5], "totalReamin":len(obj)})
    else:
        return HttpResponse("<h1>Sorry you have not permition to access</h1>")




@csrf_exempt
def contactdata(request):
    if request.method == 'POST' and request.user.is_staff:
        objdata = json.loads(request.body.decode('utf-8'))
        email = objdata["email"]
        try:
            searchData = AllInternBatchs.objects.get(email=email)
            try:
                trackData = CallingConverssionTrack.objects.get(slID=searchData.slID)
                trackData.save()
            except:
                trackData = CallingConverssionTrack(slID=searchData.slID, EmployeeID=searchData.EmployeeID, batchName=searchData.batchName, fullname=searchData.fullname, email=searchData.email, phone=searchData.phone, payment=searchData.payment, paymentStatus=searchData.paymentStatus, paymentAmount=searchData.paymentAmount)
                trackData.save()
            # print({'massage':'success', 'name':searchData.fullname, 'phone':searchData.phone, 'HighestQualification':searchData.HighestQualification, 'CollegeName':searchData.CollegeName, 'MajorFieldOfStudy':searchData.MajorFieldOfStudy, 'YearOfGraduation':searchData.YearOfGraduation, 'WorkExperienceIfAny':searchData.WorkExperienceIfAny})
            return JsonResponse({'massage':'success', 'name':searchData.fullname, 'phone':searchData.phone, 'choosefild':searchData.ChooseFieldOfInterest, 'HighestQualification':searchData.HighestQualification, 'CollegeName':searchData.CollegeName, 'MajorFieldOfStudy':searchData.MajorFieldOfStudy, 'YearOfGraduation':searchData.YearOfGraduation, 'WorkExperienceIfAny':searchData.WorkExperienceIfAny})
        except:
            return JsonResponse({'massage':'Invalid Request!'})
    return JsonResponse({'massage':'faild'})