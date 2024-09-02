from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from goobusinessesapp.models import RegistationFormDB, InternUserDetails, AllServices, ClickHistry, UserDetails, PerDayOrderPerUser, OrderList, FreeTrialUser, FreeTrialRequest, FreeTrialUnderReview, ContactMessage, WhyUsDB, AboutDB, ControlWeb, EmailSeenDB, OpenViaEmail, InternalVisit, ClickHistryByUser, UnsubscribeList, SubscribeList, BatchesInstractions, AllInternBatchs, CallingConverssionTrack, TransectionHistory, ProductUser, AllStudentDetails, ReferrelData, StudentBatchesInstractions
from goobusinessesapp import emailhandel 
from goobusinessesapp import extraFunc
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
import os
import razorpay # pip install razorpay
from spire.pdf.common import *
from spire.pdf import *
from PyPDF2 import PdfWriter, PdfReader
import time

OurMainURL = "https://goobusines.com/"

global lastUpdatetime
lastUpdatetime = datetime.now()
key_id = "rzp_test_RVMxgfe1OWFMM7"
key_secret = "LC2iktMC9Q52rLgWdkVuFsCO"

############# 28th jan 2024 ################
deletExtraImagesRUNNINGstatus = True

def deletExtraImages():
    global deletExtraImagesRUNNINGstatus
    time.sleep(15)
    if deletExtraImagesRUNNINGstatus:
        deletExtraImagesRUNNINGstatus = False
        mainDir = "./media/publicofferlater"
        allfiles = os.listdir(mainDir)
        for file in allfiles:
            created = os.path.getctime(f"{mainDir}/{file}")
            if((datetime.fromtimestamp(created)+timedelta(minutes=1)) < datetime.now()):
                os.remove(f"{mainDir}/{file}")

        deletExtraImagesRUNNINGstatus = True
        




def pdfGenaretor(candName, candbatch, emplyid, exceptDate, documentType, upper_rightP, lower_leftP):
    # Create an object of the PdfDocument class
    
    doc = PdfDocument()
    # Load a PDF file
    doc.LoadFromFile(f"./media/offerlater/{candbatch}{documentType}.pdf")
    # Iterate through the pages in the document
    
    for i in range(doc.Pages.Count):
        # Get the current page
        page = doc.Pages[i]    
        # Create an object of the PdfTextReplace class and pass the page to the constructor of the class as a parameter
        replacer = PdfTextReplacer(page)
        # Replace All instances of a specific text with new text
        replacer.ReplaceAllText("Name25163,", f"{candName}")
        # Replace All instances of a specific text with new text and set text color
        #replacer.ReplaceAllText("Adobe Acrobat", "PDF Editor", Color.get_Yellow())
    for i in range(doc.Pages.Count):
        # Get the current page
        page = doc.Pages[i]    
        replacer = PdfTextReplacer(page)
        # Replace All instances of a specific text with new text
        replacer.ReplaceAllText("empid5163", f"{emplyid}")
    for i in range(doc.Pages.Count):
        # Get the current page
        page = doc.Pages[i]    
        replacer = PdfTextReplacer(page)
        # Replace All instances of a specific text with new text
        replacer.ReplaceAllText("exceptDate5163", f"{exceptDate}")

    # Save the resulting file
    # fileUnicName = f"pdf{datetime.now()}.pdf"
    fileUnicName = f"./media/publicofferlater/pdfofferlatter{emplyid}.pdf"
    doc.SaveToFile(fileUnicName)
    doc.Close()
    reader = PdfReader(fileUnicName)
    page = reader.pages[0]
    writer = PdfWriter()
    for page in reader.pages:
        # page.cropbox.upper_right = (900, 0)
        # page.cropbox.lower_left = (0, 815)
        page.cropbox.upper_right = upper_rightP
        page.cropbox.lower_left = lower_leftP
    
    writer.add_page(page) 

    with open(fileUnicName,'wb') as fp:
        writer.write(fp) 
    
    return fileUnicName


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
<div class="msg">Your login credential:<br><br>Dashboard: <a href="{OurMainURL}login">"{OurMainURL}login"</a><br>Username: "{emailReceiver}"<br>Password: "{users_password}"</div>
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

def sendEmailforstaff(emailReceiver, subject, msg, fullname):
    if emailReceiver!="":
        senderEmail = ControlWeb.objects.get(VarName="Fail cheack email").emailVar
        ePassword = ControlWeb.objects.get(VarName="Fail cheack email").charecterVar
        smtpServerName = ControlWeb.objects.get(VarName="smtpServerName").charecterVar
        messagee = MIMEMultipart("alternative")
        messagee["Subject"] = f'{subject} {datetime.now()}'
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
.msg{margin:60px 0px;color: #5f6368;text-align: left;}
</style>
</head>"""
        htmlBody = f"""<body>
<div class="header"></div>
<h1>Email from Goo Business</h1>
<div class="msg">{msg}</div>
<img src="{OurMainURL}emailseen/{emailReceiver}/EmailSendByStaff" alt="Image not found" hidden>
</body>
</html>"""
        html = htmlHead + htmlBody
        part2 = MIMEText(html, "html")
        messagee.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtpServerName, 465, context=context) as server:
            server.login(senderEmail, ePassword)
            server.sendmail(senderEmail, emailReceiver, messagee.as_string())
            # emailStatus = 'Email also successfully received.....'
            # print('Success......')
        


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
        if(User.objects.filter(username=email)):
            return render(request, "registationform.html", {'errmsg':'Sorry, this user already exists.'})
        
        ChooseJobOrInternship = request.POST.get('jobType')
        ChooseFieldOfInterest = request.POST.get('fieldOfInterest')
        HighestQualification = request.POST.get('highestQualification')
        CollegeName = request.POST.get('collegeName')
        MajorFieldOfStudy = request.POST.get('major')
        YearOfGraduation = request.POST.get('graduationYear')
        WorkExperienceIfAny = request.POST.get('workExperience')
        GitHubProfile = request.POST.get('github')
        LinkedInProfile = request.POST.get('linkedin')
        address = request.POST.get('address')
        country = request.POST.get('country')
        countryCode = request.POST.get('countryCode')
        pinCode = request.POST.get('pinCode')

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
        # OrderListDB = RegistationFormDB(ResumePDF=file, fullname=fullname, email=email, phone=phone, otp=otp, otpStatus="oneChance", peymentStatus="due", ChooseJobOrInternship=ChooseJobOrInternship, ChooseFieldOfInterest=ChooseFieldOfInterest, HighestQualification=HighestQualification, CollegeName=CollegeName, MajorFieldOfStudy=MajorFieldOfStudy, YearOfGraduation=YearOfGraduation, WorkExperienceIfAny=WorkExperienceIfAny, GitHubProfile=GitHubProfile, LinkedInProfile=LinkedInProfile)
        OrderListDB = AllInternBatchs(ResumePDF=file, batchName=f"{ChooseJobOrInternship}{ChooseFieldOfInterest}", fullname=fullname, email=email, phone=phone, ChooseJobOrInternship=ChooseJobOrInternship, ChooseFieldOfInterest=ChooseFieldOfInterest, HighestQualification=HighestQualification, CollegeName=CollegeName, MajorFieldOfStudy=MajorFieldOfStudy, YearOfGraduation=YearOfGraduation, WorkExperienceIfAny=WorkExperienceIfAny, GitHubProfile=GitHubProfile, LinkedInProfile=LinkedInProfile, address=address,country=country,countryCode=countryCode,pinCode=pinCode, otp=otp, otpStatus="oneChance")
        # OrderListDB = OrderList(fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
        OrderListDB.save()
        passingSLID = OrderListDB.slID
        OrderListDB.EmployeeID = f"{OrderListDB.batchName}_{OrderListDB.slID}"
        if OrderListDB.ChooseJobOrInternship=="j":
            OrderListDB.paymentAmount = 9
        elif OrderListDB.ChooseJobOrInternship=="i":
            OrderListDB.paymentAmount = 49
        else:
            OrderListDB.paymentAmount = 99
        OrderListDB.paymentStatus = "Due"
        OrderListDB.save()
        user = User.objects.create_user(OrderListDB.email, OrderListDB.email, OrderListDB.EmployeeID)
        user.save()
        # print(passingSLID)
        # print('********************1313131313131313131313131313113')
        return render(request, 'varification.html', {'slid':passingSLID})
            

               
def registationsuccessfull(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        slid = request.POST.get('slid')
        OrderDetails = AllInternBatchs.objects.get(slID=int(slid))
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
            # return render(request, 'registationsuccessfull.html')
            sendEmailAndPassword(OrderDetails.email, OrderDetails.EmployeeID)
            if(OrderDetails.ChooseJobOrInternship=="i" or OrderDetails.ChooseJobOrInternship=="j"):
                return redirect("/dashboard")

            return render(request, "applicationpaymentrequest.html", {"paymentmsg":"To ensure serious candidates and prevent unnecessary applications, we charge a nominal fee (for Job Rs.9 INR and Internship Rs.49 INR) for the interview and skills testing process to cover the costs of our thorough code review, final project, and interview round, ensuring a quality experience for all participants.", "redirectEndpoint":f"applicationpaymentrequest?slId={slid}", 'price':OrderDetails.paymentAmount})
            # return render(request, 'applicationpaymentrequest.html')
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
    try:
        if request.user.is_staff and request.GET['batch_name']:
            data = BatchesInstractions.objects.get(batchName=request.GET['batch_name'])
            htmldata = markdown.markdown(data.Instractions)
            return render(request, "dashboard.html", {"htmldata":htmldata, "studentName":"Staff Login", "email":"staff email", "batchname":"Staff Batch", "empid":"EmpID"})
    except:
        pass
    if request.user.is_authenticated:
        # The user is logged in
        # Perform actions for authenticated users
        try:
            searchStudent = AllInternBatchs.objects.get(email=request.user.username)
            data = BatchesInstractions.objects.get(batchName=searchStudent.batchName)
            # if(searchStudent.payment!=True and searchStudent.ChooseJobOrInternship=="j"):
            #     return render(request, "pymentforemp.html", {"paymentmsg":"To ensure serious candidates and prevent unnecessary applications, we charge a nominal fee (for Job Rs.9 INR and Internship Rs.49 INR) for the interview and skills testing process to cover the costs of our thorough code review, final project, and interview round, ensuring a quality experience for all participants.", "redirectEndpoint":"dashboard", 'price':searchStudent.paymentAmount})
            htmldata = markdown.markdown(data.Instractions)
            return render(request, "dashboard.html", {"htmldata":htmldata, "studentName":searchStudent.fullname, "email":searchStudent.email, "batchname":searchStudent.batchName, "empid":searchStudent.EmployeeID})
        except:
            htmldata = '<h2 style="color:red;">Sorry your batch has not been created yet Please wait.</h2>'
            return render(request, "dashboard.html", {"htmldata":htmldata, "studentName":searchStudent.fullname, "email":searchStudent.email, "batchname":searchStudent.batchName, "empid":searchStudent.EmployeeID})
    else:
        # The user is not logged in
        # Perform actions for unauthenticated users
        return redirect("/login")
    

def newadminmanagingdashboard(request):
    if request.user.is_active and request.user.is_staff:
        obj = AllInternBatchs.objects.filter().all().order_by("-slID")
        
        return render(request, "newadminmanagingdashboard.html", {'serverdata':obj[:60], "totalReamin":len(obj)})
    else:
        return HttpResponse("<h1>Sorry you have not permition to access</h1>")


@csrf_exempt
def interveiwemailsend(request):
    if request.method == 'POST' and request.user.is_staff:
        objdata = json.loads(request.body.decode('utf-8'))
        slid = objdata["slid"]
        email = objdata["email"]
        ivdate = objdata["ivdate"]
        ivtime = objdata["ivtime"]
        meetinglink = objdata["meetinglink"] 
        
        try:

            searchData = AllInternBatchs.objects.get(slID=int(slid), email=email)
            searchData.isInterviewSend = True
            
            emailhandel.sendInterveiwTime(email, ivdate, ivtime, meetinglink, searchData.fullname)
            searchData.save()

            return JsonResponse({'massage':'success'})
        except:
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



############## 28th jan 2024 ################ 
@csrf_exempt
def offerletter(request, email, batchname, empid):
    try:
        searchStudent = AllInternBatchs.objects.get(email=email, batchName=batchname, EmployeeID=empid)
        if(searchStudent.payment!=True):
            HttpResponse("<h1>Sorry, not found.</h1>")
        try:
            OfferLaterTotalDownload = ControlWeb.objects.get(VarName="OfferLaterTotalDownload")
            OfferLaterTotalDownload.integetVar += 1
            OfferLaterTotalDownload.save()
        except:
            OfferLaterTotalDownload = ControlWeb(VarName="OfferLaterTotalDownload", integetVar=1)
            OfferLaterTotalDownload.save()
        
        candName = searchStudent.fullname
        candbatch = searchStudent.batchName
        emplyid = searchStudent.EmployeeID
        exceptDate = searchStudent.acceptdate

        try:
            fileUnicName = pdfGenaretor(candName, candbatch, emplyid, exceptDate, "", (900, 0), (0, 815))
        except:
            return HttpResponse("<h1>Sorry, your document has not been created yet.</h1>")

        thithi2 = threading.Thread(target=deletExtraImages)
        thithi2.start()

        pdf = open(fileUnicName, 'rb')
        response = FileResponse(pdf)
        
        return response
    except:
        return HttpResponse("<h1>Sorry Request Not Found</h1>")
@csrf_exempt
def cirtificate(request, email, batchname, empid):
    try:
        searchStudent = AllInternBatchs.objects.get(email=email, batchName=batchname, EmployeeID=empid)
        if(searchStudent.payment!=True):
            HttpResponse("<h1>Sorry, not found.</h1>")
        try:
            OfferLaterTotalDownload = ControlWeb.objects.get(VarName="OfferLaterTotalDownload")
            OfferLaterTotalDownload.integetVar += 1
            OfferLaterTotalDownload.save()
        except:
            OfferLaterTotalDownload = ControlWeb(VarName="OfferLaterTotalDownload", integetVar=1)
            OfferLaterTotalDownload.save()
        
        candName = searchStudent.fullname
        candbatch = searchStudent.batchName
        emplyid = searchStudent.EmployeeID
        exceptDate = searchStudent.acceptdate

        try:
            fileUnicName = pdfGenaretor(candName, candbatch, emplyid, exceptDate, "cir", (900, 0), (0, 581))
        except:
            return HttpResponse("<h1>Sorry, your document has not been created yet.</h1>")

        thithi2 = threading.Thread(target=deletExtraImages)
        thithi2.start()

        pdf = open(fileUnicName, 'rb')
        response = FileResponse(pdf)
        return response
    except:
        return HttpResponse("<h1>Sorry Request Not Found</h1>")

############## 5th Feb 2024 ################
def termsandconditions(request):
    return render(request, 'termsandconditions.html')
def CancellationRefundPolicy(request):
    return render(request, 'CancellationRefundPolicy.html')
def courses(request):
    return render(request, 'courses.html')
def privacypolicy(request):
    return render(request, 'privacypolicy.html')
def LearnMoreaboutrqt(request):
    return render(request, 'LearnMoreaboutrqt.html')

############## 8th Feb 2024 ################
def paymentVaryfyForInt(request):
    pmtid = request.GET['pmtid']
    odrid = request.GET['odrid']
    sigid = request.GET['sigid']
    amount = request.GET['amount']
    client = razorpay.Client(auth=(ControlWeb.objects.get(VarName="key_id").charecterVar, ControlWeb.objects.get(VarName="key_secret").charecterVar))
    dictData = {'razorpay_payment_id': pmtid, 'razorpay_order_id': odrid, 'razorpay_signature': sigid}
    try:
        client.utility.verify_payment_signature(dictData)
        searchStudent = AllInternBatchs.objects.get(email=request.user.username)
        searchStudent.payment = True
        searchStudent.paymentStatus = "Success"
        searchStudent.paymentAmount = int(amount)
        searchStudent.save()
        trnsHistry = TransectionHistory(slID=searchStudent.slID,fullname=searchStudent.fullname, email=searchStudent.email, phone=searchStudent.phone, payment=searchStudent.payment, paymentStatus="Success", paymentAmount=int(amount), razorpay_payment_iddb=pmtid, razorpay_order_iddb=odrid, razorpay_signaturedb=sigid)
        trnsHistry.save()
        try:
            totalPaymentReceive = ControlWeb.objects.get(VarName="totalPaymentReceive")
            totalPaymentReceive.integetVar += int(amount)
            totalPaymentReceive.save()
        except:
            totalPaymentReceive = ControlWeb(VarName="totalPaymentReceive", integetVar=int(amount))
            totalPaymentReceive.save()
        return redirect("/dashboard")
    except:
        return HttpResponse("<h1>Sorry, your payment has been failed...(illegal activity detected!)</h1>")
    
def paymentRejectForEmp(request):
    searchStudent = AllInternBatchs.objects.get(email=request.user.username)
    searchStudent.payment = False
    searchStudent.save()
    return redirect("/dashboard")

def intrnpaymentrequest(request):
    searchStudent = AllInternBatchs.objects.get(email=request.user.username)
    client = razorpay.Client(auth=(ControlWeb.objects.get(VarName="key_id").charecterVar, ControlWeb.objects.get(VarName="key_secret").charecterVar))
    if searchStudent.paymentAmount!=0:
        price = searchStudent.paymentAmount
    else:
        price = 49

    data = { "amount": price*100, "currency": "INR", "receipt": f"{searchStudent.EmployeeID}", "notes":{
    "customername":f"{searchStudent.fullname}",
    'customeremail':f"{searchStudent.email}",
    'customerphone':f"{searchStudent.phone}",
    "payfor":"For code review interview request"
    } }

    order = client.order.create(data=data)
    # print(order)
    return render(request, 'intrnpaymentrequest.html', {'odr':order, 'pid':ControlWeb.objects.get(VarName="key_id").charecterVar, 'price':price})

def applicationpaymentrequest(request):
    slId = request.GET['slId']
    searchStudent = AllInternBatchs.objects.get(slID=slId)
    user = authenticate(request, username=searchStudent.email, password=searchStudent.EmployeeID)
    if user is not None:
        login(request, user)

    client = razorpay.Client(auth=(ControlWeb.objects.get(VarName="key_id").charecterVar, ControlWeb.objects.get(VarName="key_secret").charecterVar))
    price = searchStudent.paymentAmount
    data = { "amount": price*100, "currency": "INR", "receipt": f"{searchStudent.EmployeeID}", "notes":{
    "customername":f"{searchStudent.fullname}",
    'customeremail':f"{searchStudent.email}",
    'customerphone':f"{searchStudent.phone}",
    "payfor":"Application fee"
    } }

    order = client.order.create(data=data)
    # print(order)
    return render(request, 'intrnpaymentrequest.html', {'odr':order, 'pid':ControlWeb.objects.get(VarName="key_id").charecterVar, 'price':price})

############## Just for test ################
def everythingtest(request):
    searchReferrBy = ReferrelData.objects.get(RefrelID="ST3")
    
    refrelListJsonData = searchReferrBy.refrelList

    print(searchReferrBy.refrelList)
    print("********************")
    print(searchReferrBy.refrelList['listdata'])
    print("################")
    searchReferrBy.refrelList['listdata'].append({'name': 'DaktarPata', 'service_name': 'TestBhagina_Course', 'date': f'{datetime.now().date()}', 'profit': 100})
    print("################")

    # print(searchReferrBy.refrelList['listdata'])
    # print("################")
    # searchReferrBy.refrelList['listdata'].append({'name': '3nd', 'service_name': '3ndTestBatch_Course', 'date': '2024-03-27', 'profit': 100})
    print(searchReferrBy.refrelList)

    searchReferrBy.save()

    
    return JsonResponse(searchReferrBy.refrelList)

############## 06/03/2024 ################
def emailsendfromstaff(request):
    if request.user.is_staff:
        if request.method == 'POST':
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            fullname = request.POST.get('fullname')
            # sendEmailforstaff(email, subject, message, fullname)
            return render(request, 'emailsend.html', {'successmsg':"Send Successfully"})

        return render(request, 'emailsend.html')
    return HttpResponse("<h1>Sorry, You don't have permition</h1>")

@csrf_exempt
def emailMarketingAthenticate(request):
    if request.method == 'POST':
        objdata = json.loads(request.body.decode('utf-8'))
        slid = objdata["slid"]
        email = objdata["email"]
        user_id = objdata["user_id"]
        ip_address = objdata["ip_address"]
        host_name = objdata["host_name"]
        email_send = objdata["email_send"]
        password = objdata["password"]

        try:
            productUserData = ProductUser.objects.get(slid=slid, email=email, UserID=user_id, SenderEmailPassword=password)
            if email_send:
                productUserData.TotalSendEmail += 1
                productUserData.save()
        except:
            return JsonResponse({'massage':'error'})

        return JsonResponse({'massage':'success', 'sender_email':productUserData.email, "port":productUserData.port, "ssl":productUserData.SSLType,"password":productUserData.SenderEmailPassword})
    return JsonResponse({'massage':'error'})

###############  LMS #################
def studentregistation(request):
    try:
        if request.GET['refcode']:
            return render(request, 'studentregistation.html', {'refcode':request.GET['refcode']})
    except:
        pass
    if request.method == 'POST':
        allCoursePrice = 499
        fullname = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if(User.objects.filter(username=email)):
            return render(request, 'studentregistation.html', {'errmsg':'Sorry, this user already exists.'})
        
        ChooseFieldOfInterest = request.POST.get('fieldOfInterest')
        HighestQualification = request.POST.get('highestQualification')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        referral = request.POST.get('referral')
        
        otp = random.randint(1000, 9999)
        try:
            # sendEmail(email, str(otp))
            thithi = threading.Thread(target=sendEmail, args=[email, str(otp)])
            thithi.start()
        except:
            sendEmailFaild("OTP can't send please cheack the system")
            
        OrderListDB = AllStudentDetails(batchName=f"{ChooseFieldOfInterest}", fullname=fullname, email=email, phone=phone, gender=gender, ChooseFieldOfInterest=ChooseFieldOfInterest, HighestQualification=HighestQualification, otp=otp, otpStatus="oneChance", referdBy=referral, age=age)
        # OrderListDB = OrderList(fullname=fullname, email=email, phone=phone, whatsapp=whatsapp, totalprice=totalprice, countryoption=countryoption, servicesOption=servicesOption, enterbuget=enterbuget, numberofleads=numberofleads, requirmentdesc=requirmentdesc, productID=productID, onlyCountryCode=onlyCountryCode, otp=otp, otpStatus="oneChance", orderStatus="received", orderCoplition=0, peymentStatus="due")
        OrderListDB.save()
        passingSLID = OrderListDB.slID
        OrderListDB.StudentID = f"{OrderListDB.batchName}_{OrderListDB.slID}"

        try:
            fatchingRefrelData = ReferrelData.objects.get(RefrelID=referral)
            if fatchingRefrelData.discountAmount!=0:
                OrderListDB.paymentAmount = abs(allCoursePrice - fatchingRefrelData.discountAmount)    
            else:
                OrderListDB.paymentAmount = abs(allCoursePrice - ((allCoursePrice*fatchingRefrelData.commitionInPercentage)/100)) # Discount formula
            
        except:
            OrderListDB.paymentAmount = allCoursePrice
            
        
        OrderListDB.paymentStatus = "Due"
        OrderListDB.save()
        user = User.objects.create_user(OrderListDB.email, OrderListDB.email, OrderListDB.StudentID)
        user.save()
        # print(passingSLID)
        # print('********************1313131313131313131313131313113')
        return render(request, 'studentvarification.html', {'slid':passingSLID, 'referrelcode':referral})
    
    return render(request, 'studentregistation.html')


def studentregistationsuccessfull(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        slid = request.POST.get('slid')
        referrelcode = request.POST.get('referrelcode')
        OrderDetails = AllStudentDetails.objects.get(slID=int(slid))
        dbotp = OrderDetails.otp

        if OrderDetails.otpStatus == "oneChance" and dbotp==int(otp):
            OrderDetails.otpStatus = "OTP Verified"
            OrderDetails.save()
            
            emailhandel.sendEmailAndPassword(OrderDetails.email, OrderDetails.StudentID)
            

            return render(request, "studentpaymentrequest.html", {"paymentmsg":"", "redirectEndpoint":f"studentpaymentrequest?slId={slid}", 'price':OrderDetails.paymentAmount})

        else:
            OrderDetails.otpStatus = "Verification Faild"
            OrderDetails.save()
            return render(request, 'verificationfail.html')


def studentpaymentrequest(request):
    slId = request.GET['slId']
    searchStudent = AllStudentDetails.objects.get(slID=slId)
    user = authenticate(request, username=searchStudent.email, password=searchStudent.StudentID)
    if user is not None:
        login(request, user)

    client = razorpay.Client(auth=(ControlWeb.objects.get(VarName="key_id").charecterVar, ControlWeb.objects.get(VarName="key_secret").charecterVar))
    price = searchStudent.paymentAmount
    data = { "amount": price*100, "currency": "INR", "receipt": f"{searchStudent.StudentID}", "notes":{
    "customername":f"{searchStudent.fullname}",
    'customeremail':f"{searchStudent.email}",
    'customerphone':f"{searchStudent.phone}",
    "payfor":"Course registration fee"
    } }

    order = client.order.create(data=data)
    # print(order)
    return render(request, 'studentpaymentrequestcontinue.html', {'odr':order, 'pid':ControlWeb.objects.get(VarName="key_id").charecterVar, 'price':price})


def studentpaymentverification(request):
    pmtid = request.GET['pmtid']
    odrid = request.GET['odrid']
    sigid = request.GET['sigid']
    amount = request.GET['amount']
    client = razorpay.Client(auth=(ControlWeb.objects.get(VarName="key_id").charecterVar, ControlWeb.objects.get(VarName="key_secret").charecterVar))
    dictData = {'razorpay_payment_id': pmtid, 'razorpay_order_id': odrid, 'razorpay_signature': sigid}
    try:
        client.utility.verify_payment_signature(dictData)
        searchStudent = AllStudentDetails.objects.get(email=request.user.username)
        searchStudent.payment = True
        searchStudent.paymentStatus = "Success"
        searchStudent.paymentAmount = int(amount)
        searchStudent.save()
        trnsHistry = TransectionHistory(slID=searchStudent.slID,fullname=searchStudent.fullname, email=searchStudent.email, phone=searchStudent.phone, payment=searchStudent.payment, paymentStatus="Success", paymentAmount=int(amount), razorpay_payment_iddb=pmtid, razorpay_order_iddb=odrid, razorpay_signaturedb=sigid)
        trnsHistry.save()

        referrelAccount = ReferrelData(fullname=searchStudent.fullname,email=searchStudent.email,phone=searchStudent.phone,whatsapp=searchStudent.whatsapp,discountAmount=50,discountPercentage=0,commitionAmount=100,commitionInPercentage=0)
        referrelAccount.save()
        referrelAccount.RefrelID = f"ST{extraFunc.numToHexSlice(referrelAccount.slID)}"
        referrelAccount.save()

        try:
            rfID = searchStudent.referdBy
            if rfID!="":
                searchReferrBy = ReferrelData.objects.get(RefrelID=rfID)
                searchReferrBy.totalNumberOfRefer+=1
                searchReferrBy.totalEarning += searchReferrBy.commitionAmount
                searchReferrBy.totalBalance += searchReferrBy.commitionAmount
                searchReferrBy.save()
                searchReferrBy.refrelList['listdata'].append({'name':f'{searchStudent.fullname}', 'service_name':f"{searchStudent.batchName}_Course", 'date':f'{datetime.now().date()}', 'profit':f'{searchReferrBy.commitionAmount}'}) 
                searchReferrBy.save()
        except:
            pass
        
        try:
            totalPaymentReceive = ControlWeb.objects.get(VarName="totalPaymentReceive")
            totalPaymentReceive.integetVar += int(amount)
            totalPaymentReceive.save()
        except:
            totalPaymentReceive = ControlWeb(VarName="totalPaymentReceive", integetVar=int(amount))
            totalPaymentReceive.save()
        return redirect("/studentdashboard")
    except:
        return HttpResponse("<h1>Sorry, your payment has been failed...(illegal activity detected!)</h1>")
    


def studentdashboard(request):
    try:
        if request.user.is_staff and request.GET['batch_name']:
            data = BatchesInstractions.objects.get(batchName=request.GET['batch_name'])
            htmldata = markdown.markdown(data.Instractions)
            return render(request, "studentdashboard.html", {"htmldata":htmldata, "studentName":"Staff Login", "email":"staff email", "batchname":"Staff Batch", "empid":"EmpID"})
    except:
        pass
    if request.user.is_authenticated:
        # The user is logged in
        # Perform actions for authenticated users
        try:
            searchStudent = AllStudentDetails.objects.get(email=request.user.username)
            if(searchStudent.payment!=True):
                # return render(request, "pymentforemp.html", {"paymentmsg":"To ensure serious candidates and prevent unnecessary applications, we charge a nominal fee (for Job Rs.9 INR and Internship Rs.49 INR) for the interview and skills testing process to cover the costs of our thorough code review, final project, and interview round, ensuring a quality experience for all participants.", "redirectEndpoint":"dashboard", 'price':searchStudent.paymentAmount})
                print("***************************************///////")
                return render(request, "studentpaymentrequest.html", {"paymentmsg":"", "redirectEndpoint":f"studentpaymentrequest?slId={searchStudent.slID}", 'price':searchStudent.paymentAmount})
            data = StudentBatchesInstractions.objects.get(batchName=searchStudent.batchName)
            htmldata = markdown.markdown(data.Instractions)
            return render(request, "studentdashboard.html", {"htmldata":htmldata, "studentName":searchStudent.fullname, "email":searchStudent.email, "batchname":searchStudent.batchName, "empid":searchStudent.StudentID})
        except:
            htmldata = '<h2 style="color:red;">Sorry your batch has not been created yet Please wait.</h2>'
            return render(request, "studentdashboard.html", {"htmldata":htmldata, "studentName":searchStudent.fullname, "email":searchStudent.email, "batchname":searchStudent.batchName, "empid":searchStudent.StudentID})
    else:
        # The user is not logged in
        # Perform actions for unauthenticated users
        return redirect("/studentLogin")
   
def studentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/studentdashboard")
        else:
            return render(request, "studentlogin.html", {"msg":"Invalid Credential!"})
    else:
        return render(request, "studentlogin.html")

@csrf_exempt
def referraldashboard(request):
    if request.user.is_authenticated:
        referrelData = ReferrelData.objects.get(email=request.user.username)

        if request.method == 'POST':
            return JsonResponse({'massage':'success', 'referrelListData':referrelData.refrelList["listdata"]})
            
        return render(request, "referraldashboard.html", {'referrelData':referrelData})

    return render(request, "referral.html", {'loginshow':"true", 'signupshow':"false"})



def referral(request):
    # if(request.META.get('HTTP_REFERER')):
    return render(request, "referral.html", {'loginshow':"false", 'signupshow':"false"})

def referralsignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if(User.objects.filter(username=username)):
            return render(request, "referral.html", {'loginshow':"false", 'signupshow':"true", 'errmsg':"Sorry, this user already exists."})
        
        otp = random.randint(1000, 9999)
        try:
            # sendEmail(email, str(otp))
            thithi = threading.Thread(target=sendEmail, args=[username, str(otp)])
            thithi.start()
        except:
            sendEmailFaild("OTP can't send please cheack the system")
        
        user = User.objects.create_user(username, username, password)
        user.save()

        referrelAccount = ReferrelData(email=username,discountAmount=50,discountPercentage=0,commitionAmount=100,commitionInPercentage=0, otp=otp, otpStatus="oneChance")
        referrelAccount.save()
        referrelAccount.RefrelID = f"YT{extraFunc.numToHexSlice(referrelAccount.slID)}"
        referrelAccount.save()
        return render(request, 'referralotpverify.html', {'slid':referrelAccount.slID})

def referralotpverify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        slid = request.POST.get('slid')

        OrderDetails = ReferrelData.objects.get(slID=int(slid))
        dbotp = OrderDetails.otp

        if OrderDetails.otpStatus == "oneChance" and dbotp==int(otp):
            OrderDetails.otpStatus = "OTP Verified"
            OrderDetails.save()
            return render(request, "referral.html", {'loginshow':"true", 'signupshow':"false"})

        else:
            OrderDetails.otpStatus = "Verification Faild"
            OrderDetails.save()
            return render(request, 'verificationfail.html')
     
def referrallogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/referraldashboard")
        else:
            # return redirect("/referral")
            return render(request, "referral.html", {'loginshow':"true", 'signupshow':"false", 'errmsg':"Invalid Credential!"})
     
def studentcrmform(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect("/referraldashboard")
        # else:
        #     # return redirect("/referral")
        #     return render(request, "referral.html", {'loginshow':"true", 'signupshow':"false", 'errmsg':"Invalid Credential!"})
        pass

    return render(request, "studentcrmform.html")
    
     
def studentcallrequestdashboard(request):
    return render(request, "studentcallrequestdashboard.html")
