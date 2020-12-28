from weathx.settings import MESSAGE_STORAGE
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from PIL import Image
from captcha.image import ImageCaptcha
import datetime
import random
from django.core import mail
from django.conf import settings 
from django.core.mail import send_mail 
from newaccount.models import Person, Contact
# Create your views here.







@csrf_exempt
@csrf_protect
def contact(request):
    if request.method == 'POST':
        name1 = request.POST['firstname']
        email1 = request.POST['email']
        contact1 = request.POST['contact']
        content1 = request.POST['content']
        now = datetime.datetime.now()
        all11 = {}
        if name1=='' or email1=='' or contact1=='' or content1=='':
            messages.error(request, "You can not leave fields blank")
        else:
            x = Contact(name=name1.lower(), email=email1.lower(),contact=contact1.lower(), content=content1.lower())
            x.save()
            print(name1, email1, contact1, content1)
            print(now.now())
            # send_mail(
            #     subject = 'Test Mail',
            #     message = 'Kindly Ignore',
            #     from_email = 'sanjaysheel1997@gmail.com',
            #     recipient_list = ['jain.suvidh@gmail.com'],
            #     fail_silently = True,
            # )
            # subject = 'Reply for contact CISBlogs'
            # message = f'Hi {name1}, thank you for connecting with us \n Name: {name1} \n Email: {email1} \n your message: {content1} \n\n\n\n Our team will contact you soon..!'
            # email_from = settings.EMAIL_HOST_USER 
            # recipient_list = [email1] 
            # send_mail( subject, message, email_from, recipient_list)
            messages.success(request, "your message has received. Thankyou for connecting with us..")


            
    elif request.session.has_key('person_id'):
        PersonID = request.session['person_id']
        all11 = Person.objects.filter(id=PersonID).first()
        all11 = {"all11":all11}
        return render(request, './contact/contact.html',all11)
    return render(request, 'contact/contact.html')





@csrf_protect
def signup(request):
    global temp
    if request.method != 'POST':
        randint = random.randint(1,100000000)
        imagepart = ImageCaptcha(width =250 , height = 100)
        temp = str(randint)
        imagepart = imagepart.generate_image(str(randint))
        imagepart.save("./MEDIA/another/image/trial1.png")
    if request.method == 'POST':
        fname1 = request.POST['firstname']
        lname1 = request.POST['lastname']
        contact1 = request.POST['contact']
        email1 = request.POST['email']
        state1 = request.POST['state']
        city1 = request.POST['city']
        password1 = request.POST['password']
        password12 = request.POST['confirm_pass']
        captcha1 = request.POST['captcha']
        now = datetime.datetime.now()
        if captcha1 == str(temp):
            if  (fname1 == '') or (lname1 == '') or (contact1 == '') or (email1 == '') or (state1 == '') or (city1 == ''):
                print(fname1)
                messages.error(request, "you can not leave the field empty....")
            elif Person.objects.filter(email=email1.lower()).exists():
                messages.error(request, "this email id already exists...")
                return render(request,'./newaccount/signup.html', {"fname":fname1, "lname":lname1, "contact":contact1, "email":email1, "state":state1, "city":city1})
        
            elif ((password1 !='') and (password12 !='')):
                if ((password1==password12)):
                    # https://docs.djangoproject.com/en/3.1/topics/signing/
                    #  This is like for cryptographic signing 
                    # signer = Signer()
                    # value = signer.sign(password1)
                    s = random.randrange(20,100000000)
                    if Person.objects.filter(userslug=s):
                        s = random.randrange(20,100000000)
                        x = Person(fname=fname1.lower(), lname=lname1.lower(), userslug=fname1+lname1+str(s), contact=contact1, email=email1.lower(), state=state1.lower(), city=city1.lower(), password=password1)
                        x.save()
                        messages.success(request, "wooo....! your Account has successfully created...! Thankyou for connecting with us...")
                        return render(request,"./newaccount/signin.html",{"email":email1})
                    else:
                        x = Person(fname=fname1.lower(), lname=lname1.lower(), userslug=fname1+lname1+str(s), contact=contact1, email=email1.lower(), state=state1.lower(), city=city1.lower(), password=password1)
                        x.save()
                        messages.success(request, "wooo....! your Account has successfully created...! Thankyou for connecting with us...")
                        return render(request,"./newaccount/signin.html") 
                else:
                    messages.error(request, "Your Password did not matched please make it correct...")
                    return render(request,'./newaccount/signup.html', {"fname":fname1, "lname":lname1, "contact":contact1, "email":email1, "state":state1, "city":city1})
        else:
            randint = random.randint(1,100000000)
            imagepart = ImageCaptcha(width =250 , height = 100)
            temp = str(randint)
            imagepart = imagepart.generate_image(str(randint))
            imagepart.save("./MEDIA/another/image/trial1.png")
            messages.error(request, "captcha did not matched please try again...")
            return render(request,'./newaccount/signup.html', {"fname":fname1, "lname":lname1, "contact":contact1, "email":email1, "state":state1, "city":city1,"password1":password1, "password12":password12})
    return render(request, './newaccount/signup.html')







@csrf_protect
@csrf_exempt
def signin(request):
    if request.method == 'POST':
        user = Person.objects.all()
        email1 = request.POST['email']
        password1 = request.POST['password']
        loggedin_user_email=email1
        votes_email = Person.objects.filter(email = email1.lower()).exists()
        votes_password = Person.objects.filter(password = password1).exists()
        a = Person.objects.filter(email=email1.lower(),password= password1).first()
        print(a)
        if votes_email and votes_password:
            print('yes')
            request.session['person_id'] = a.id
            request.session['person_fname'] = a.fname
            all1 = {"name":a.fname}
            print(all1)
            return redirect(f'/')
        else:
            if votes_email:
                if votes_password:
                   pass
                else:
                    messages.error(request, "Please fill correct email and password")
            all1 = {"votes_table":'0'}
            print(all1)
            return redirect(f"../../account/signin")
    return render(request, './newaccount/signin.html')






@csrf_protect
def logout(request):
    Session.objects.all().delete() 
    return redirect(f'../../account/signin/')


