
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from pircle.settings import EMAIL_HOST_USER
from .models import user
from django.urls import reverse
# Create your views here.
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def mail(otp,email):
    subject = "E-MAIL VERIFICATION FROM PIRCLE"
    message = "Thanks for Registering with PIRCLE \n Login with Verification code to Verify your Account! \n \n Verification Code : "+otp
    to_list = [email]
    from_email = EMAIL_HOST_USER
    send_mail(subject,message,from_email,to_list,fail_silently=False)

def verify(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST["email"]
        try:   
            rec = user.objects.get(email=email) 
        except Exception:
            return HttpResponseRedirect("/accounts/sign-up/")
        if rec.active == "active":
            return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Account is already Active, try Sign-in! <a href='/accounts/sign-in/'>Click here to Sign in to your Account!</a></p></div>")
        otp = request.POST["otp"]
        try:
         if request.POST["resend"] == "":
            otp = str(random_with_N_digits(8))
            rec.otp = otp
            rec.save()
            mail(otp,email)
            return HttpResponseRedirect("/accounts/verification/")   
        except:
         if rec.otp == otp:   
            rec.active ="active"
            rec.otp = None
            rec.save()
            return HttpResponseRedirect("/accounts/sign-in/") 
         else:
            return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Verification Code is Not Correct! Try Again</p></div>")
    return render(request,"verification.html",{})     

def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password != password2 or password == False or password2 == False:
            return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Passwords Doesn\'t Match, Try Again</p></div>")    
        try:
            user.objects.get(email = email)
        except Exception:
            obj = user()
            obj.email = email
            obj.password = password   
            otp = str(random_with_N_digits(8))
            obj.otp = otp
            obj.save()
            mail(otp,email)
            return HttpResponseRedirect('/accounts/verification/')  
        else:    
            if user.active == "active":
                return HttpResponseRedirect('/accounts/sign-in/')
            else:
                return HttpResponseRedirect('/accounts/verification/')  
    return render(request,"signup.html",{})    


def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]       
        try:   
         rec = user.objects.get(email=email,password=password) 
        except Exception as e:
         return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Email or Password you have entered is wrong!<br>"+str(e)+".</p></div>") 
        return redirect("/profiles/")     
    return render(request,"signin.html",{})    


def reset(request):
    if request.method == "POST":
        try:
         email = request.POST.get("email")
        except Exception:
            return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Please Enter Valid Email ID</p></div>")
        password = request.POST.get("password", False)
        password2 = request.POST.get("password2", False)
        otp = request.POST.get("otp", False)
        resend = request.POST.get("resend",False)
        try:
           rec = user.objects.get(email=email)
        except Exception as e:
          return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Account Doesnot Exist!<br><a href='/accounts/sign-up/'>Click here to Sign Up to your Account!</a></p></div>")   
        else:   
          if password == False and password2 == False and otp == False:
            otp = str(random_with_N_digits(8))
            rec.otp=otp
            rec.save()
            mail(otp,email)
            return render(request,"signin.html",{'r':'true','s':'true','p':'true','t':'true', 'u':'false'})   
          if resend != False:
            otp = str(random_with_N_digits(8))
            rec.otp = otp
            rec.save()
            mail(otp,email)
            return HttpResponseRedirect("/accounts/reset-password/")
          if password == False or password != password2:
            return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Invalid password!</p></div>")
          if rec.otp != otp:
            return HttpResponse("<div class='w3-panel w3-text-red w3-white w3-border'><h3>Error!</h3><p>Invalid Verification Code!</p></div>")                                            
        rec.password = password
        rec.otp = None
        rec.save()
        return HttpResponse("<div class='w3-panel w3-text-green w3-white w3-border'><h3>Success!</h3><p>Your Password is Updated!<a href='/accounts/sign-in/'>Click here to Sign in to your Account!</a></p></div>")                       
    return render(request,"resetpswd.html",{})   
            