from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *
from datetime import datetime
import re
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
import stripe
import sys
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import FormView
import traceback
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
import logging
from django.core.mail import send_mail

RAZORPAY_API_KEY='rzp_test_J6uOGsJeFFNksN'
RAZORPAY_API_SECRET_KEY='RUk7RAg5hRy9tBfxXXdkdn1P'
#home
def index(request):
    if request.method=="POST":
        form = loginform(request.POST)
        if form.is_valid():
            e = form.cleaned_data["email"]
            p = form.cleaned_data["password"]
            data1=registrationmodel.objects.filter(email=e,password=p)
            data2=employemodel.objects.filter(email=e,password=p)
            data3=adminmodel.objects.filter(email=e,password=p)
            if data1:
                request.session["user"] = e
                return redirect("userhome",e)
            elif data2:
                request.session["user"] = e
                return redirect("employeehome", e)
            elif data3:
                request.session["user"] = e
                return redirect("adminhome", e)
            else:
                messages.error(request, 'Login failed.Pls Check Your Email And Password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    elif 'user' in request.session:
        current_user=request.session['user']
        data = registrationmodel.objects.filter(email=current_user)
        return render(request, 'userhome.html', {"data":data})
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def course(request):
    return render(request,"courses.html")
#userregi
def register(request):
    if request.method=="POST":
        form=regiform(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data['photo']
            bio = form.cleaned_data["bio"]
            password = form.cleaned_data["password"]
            cfpassword = form.cleaned_data["cfpassword"]
            pattern = re.compile(r'^(?:\+91|0)?[6-9]\d{9}$')
            if pattern.match(str(phone)):
                if cfpassword==password:
                    data=registrationmodel(name=name,username=username,email=email,phone=phone,photo=photo,bio=bio,password=password)
                    data.save()
                    return redirect("home")
                else:
                    messages.error(request, "Passwords doesn't match,Please check your both Password.")
            else:
                messages.error(request,'invalid phone number')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    return render(request,"register.html")
def test(request):
    return render(request, 'test.html')
def home(request):
    return render(request,"home.html")
#employe
def employregidter(request):
    if request.method == "POST":
        form = employregisterform(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            bio = form.cleaned_data["bio"]
            photo=form.cleaned_data['photo']
            city=form.cleaned_data['city']
            password = form.cleaned_data["password"]
            rate=form.cleaned_data['rate']
            cfpassword = request.POST["cfpassword"]
            pattern = re.compile(r'^(?:\+91|0)?[6-9]\d{9}$')
            if pattern.match(str(phone)):
                if cfpassword == password:
                    data = employemodel(name=name, photo=photo,rate=rate, email=email, phone=phone, bio=bio,city=city,password=password)
                    data.save()
                    return redirect("home")
                elif  cfpassword != password:
                    messages.error(request, 'Registration failed. Please check your Email and Password.')
                else:
                    messages.error(request, 'Registration failed. Please Fill all the filed.')
            else:
                messages.error(request,'invalid phone number')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    return render(request, "employeregister.html")
def userhome(request,usname):
    if request.session.get('user') != usname:
        messages.error(request, "You are not authorized to view That page.pls login")
        return redirect('home')
    details = slotmodel.objects.all()
    data = registrationmodel.objects.filter(email=usname)
    return render(request,"userhome.html",{"data":data,"details":details})
def search(request, usname):
    form = ShopSearchForm(request.GET or None)
    data = registrationmodel.objects.filter(email=usname)
    details = slotmodel.objects.all()
    if form.is_valid():
        services = form.cleaned_data.get('services')
        if services:
            details = slotmodel.objects.filter(stname=services)
        else:
            messages.error(request, "NO services available")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")
    return render(request, "userhome.html", {"data": data, "details": details, "form": form})
def logout(request):
    try:
        del request.session["user"]
    except:
        return redirect("home")
    return redirect('home')
def profile(request,usname):
    data1 = registrationmodel.objects.filter(email=usname)
    data2=employemodel.objects.filter(email=usname)
    if data1:
        return render(request, "profile.html", {"data": data1})
    else:
        return render(request, "profile.html", {"data": data2})
def editpro(request,usname):
    data1 = registrationmodel.objects.filter(email=usname)
    data2=employemodel.objects.filter(email=usname)
    if data1:
        if request.method == "POST":
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST["email"]
            phone = request.POST["phone"]
            bio = request.POST["bio"]
            photo = request.FILES.get('photo')
            if photo:
                pho=get_object_or_404(registrationmodel,email=usname)
                pho.photo=photo
                pho.save()
                data1.update(name=name, username=username, email=email, phone=phone, bio=bio)
            else:
                data1.update(name=name, username=username, email=email, phone=phone, bio=bio)
            return redirect("profile", usname)
        return render(request, "editpro.html", {"data": data1})
    else:
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST["email"]
            phone = request.POST["phone"]
            bio = request.POST["bio"]
            photo = request.FILES.get('photo')
            if photo:
                pho=get_object_or_404(employemodel,email=usname)
                pho.photo=photo
                pho.save()
                data2.update(name=name, email=email, phone=phone, bio=bio)
            else:
                data2.update(name=name, email=email, phone=phone, bio=bio)
            return redirect("profile", usname)
        return render(request, "editpro.html", {"data": data2})
def employeehome(request,usname):
    if request.session.get('user') != usname:
        messages.error(request, "You are not authorized to view That page.pls login")
        return redirect('home')
    data = employemodel.objects.filter(email=usname)
    employe=get_object_or_404(employemodel, email=usname)
    custom=Appointment.objects.filter(employee=employe)
    if custom:
        if request.method == "POST":
            custom.update(activation=True)
        return render(request, "employeehome.html", {"data": data, "details": custom})
    else:
        messages.error(request, "No Appointments")
    return render(request, "employeehome.html", {"data": data})
def adminhome(request,usname):
    if request.session.get('user') != usname:
        messages.error(request, "You are not authorized to view That page.pls login")
        return redirect('home')
    de=adminmodel.objects.filter(email=usname)
    data = employemodel.objects.filter(activation=False)
    if request.method=="POST":
        data.update(activation=True)
    return render(request,"adminhome.html",{"dat":data,"data":de})


from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def slotbooking(request, usname, stname, emplnme):
    details = slotmodel.objects.filter(stname=stname)
    data = registrationmodel.objects.filter(email=usname)
    employe = employemodel.objects.filter(email=emplnme)

    if request.method == "POST":
        employ = get_object_or_404(employemodel, email=emplnme)
        user = get_object_or_404(registrationmodel, email=usname)
        stdata_obj = get_object_or_404(slotmodel, stname=stname)
        location = request.POST.get("location")
        date_str = request.POST.get("date")

        if not location or not date_str:
            messages.error(request, "Please provide all details.")
        else:
            try:
                # Add debugging print statements to check the received date string
                print(f"Received date string: {date_str}")

                # Convert the date string to a datetime object
                selected_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
                current_date = datetime.now()

                # Check if the selected date is in the past
                if selected_date < current_date:
                    messages.error(request, "Selected date cannot be in the past.")
                else:
                    data = Appointment(employee=employ, user=user, services=stdata_obj, location=location,
                                       date=selected_date)
                    data.save()

                    return redirect("userhome",usname)
            except ValueError:
                messages.error(request, "Invalid date format.")

    return render(request, "slotbooking.html", {"data": data, "details": details, "emdet": employe})


def employeeapooint(request,usname,stname):
    dat=employemodel.objects.filter(bio=stname,activation=True)
    data = registrationmodel.objects.filter(email=usname)
    details = slotmodel.objects.filter(stname=stname)
    return render(request, "employeeappoint.html", {"dat": dat, "data": data, "details": details})
def employee_search(request,usname,stname):
    dat = employemodel.objects.filter(bio=stname,activation=True)
    data = registrationmodel.objects.filter(email=usname)
    details = slotmodel.objects.filter(stname=stname)
    form=employeesearchform(request.GET or None)
    if form.is_valid():
        location = form.cleaned_data.get('location')
        if location:
            dat = employemodel.objects.filter(city=location)
        else:
            messages.error(request, "No workers found at your location")
    return render(request, "employeeappoint.html", {"dat": dat, "data": data, "details": details})
def appointment(request,usname,stdata,employee):
    form = appoimentform(request.GET or None)
    if form.is_valid():
        employ = get_object_or_404(employemodel, email=employee)
        user = get_object_or_404(registrationmodel, email=usname)
        stdata_obj = get_object_or_404(slotmodel, stname=stdata)
        location = form.cleaned_data.get('location')
        date = form.cleaned_data.get('date')
        if location and date:
            data=Appointment(employee=employ,user=user,services=stdata_obj,location=location,date=date)
            data.save()
            return redirect("userhome", usname)
        else:
            messages.error(request, "Pls provide all details")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")
    return redirect("userhome", usname)
def changepass(request,usname):
    data1 = registrationmodel.objects.filter(email=usname)
    data2=employemodel.objects.filter(email=usname)
    if data1:
        if request.method == "POST":
            oldpass = request.POST['oldpass']
            newpass = request.POST['newpass']
            confpass = request.POST['confpass']
            for i in data1:
                if i.password == oldpass:
                    if newpass == confpass:
                        data1.update(password=newpass)
                        return redirect("profile", usname)
                    else:
                        messages.error(request, "New password and conformed password doesn't match ")
            else:
                messages.error(request, "Wrong old password")
        return render(request, "passwordchange.html", {"data": data1})
    else:
        if request.method == "POST":
            oldpass = request.POST['oldpass']
            newpass = request.POST['newpass']
            confpass = request.POST['confpass']
            for i in data2:
                if i.password == oldpass:
                    if newpass == confpass:
                        data2.update(password=newpass)
                        return redirect("profile", usname)
                    else:
                        messages.error(request, "New password and conformed password doesn't match ")
            else:
                messages.error(request, "Wrong old password")
        return render(request, "passwordchange.html", {"data": data2})
def createslot(request,usname):
    data = registrationmodel.objects.filter(email=usname)
    details=Appointment.objects.filter(customerdetails=usname)
    if details:
        errormessage="You cannot create a slot,You Already Have A Slot"
        deta = slotmodel.objects.all()
        return render(request,"userhome.html",{"data":data,"details":deta,"errormessage":errormessage})
    else:
        if request.method=="POST":
            stn=request.POST["stname"]
            std=request.POST['stdetails']
            stc=request.POST['city']
            sploc=request.POST['sploc']
            if stn and std and stc:
                for i in data:
                    if sploc:
                        stdata = raiseslotmodel(stname=stn, stdeteals=std,username=i.email,userphoto=i.photo,city=stc,splocation=sploc)
                        stdata.save()
                        return redirect("userhome", usname)
                    else:
                        stdata = raiseslotmodel(stname=stn, stdeteals=std,username=i.username,userphoto=i.photo,city=stc)
                        stdata.save()
                        return redirect("userhome", usname)
            else:
                messages.error(request, "Need to fill Name, Details and City")
        return render(request, "createslot.html", {"data": data})
def joinslot(request,usname):
    data = registrationmodel.objects.filter(email=usname)
    slotdet=raiseslotmodel.objects.all()
    return render(request,"joinslot.html",{"data":data,"details":slotdet})
def myslot(request,usname):
    data = registrationmodel.objects.filter(email=usname)
    user=get_object_or_404(registrationmodel, email=usname)
    appo=Appointment.objects.filter(user=user)
    if appo:
        return render(request, "myslot.html", {"data": data,"appo":appo})
    else:
        messages.error(request, "You have no appointment")
    return render(request, "myslot.html", {"data": data})
def stdelete(request,usname,stname,emponame):
    user = get_object_or_404(registrationmodel, email=usname)
    employee = get_object_or_404(employemodel, email=emponame)
    services = get_object_or_404(slotmodel, stname=stname)
    slotdet = Appointment.objects.filter(user=user,employee=employee,services=services)

    if slotdet:
        slotdet.delete()
        return redirect("userhome", usname)
def stemdelete(request,usname,stname,emponame):
    user = get_object_or_404(registrationmodel, email=usname)
    employee = get_object_or_404(employemodel, email=emponame)
    services = get_object_or_404(slotmodel, stname=stname)
    slotdet = Appointment.objects.filter(user=user,employee=employee,services=services)

    if slotdet:
        slotdet.delete()
        return redirect("employeehome", emponame)
def empodelte(request,usname,employe):
    employee=employemodel.objects.filter(email=employe)
    if employee:
        employee.delete()
        return redirect("adminhome", usname)
# class PasswordResetConfirmView(FormView):
#     template_name = 'password_reset_confirm.html'
#     success_url = reverse_lazy('login')
#     form_class = SetPasswordForm
#
#     def get_user(self, uidb64):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = registrationmodel.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, registrationmodel.DoesNotExist):
#             user = None
#         return user
#
#     def get(self, request, uidb64=None, token=None, *args, **kwargs):
#         user = self.get_user(uidb64)
#         if user is not None and default_token_generator.check_token(user, token):
#             return super().get(request, *args, **kwargs)
#         else:
#             messages.error(request, "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.")
#             return redirect('password_reset')
#
#     def form_valid(self, form):
#         user = self.get_user(self.kwargs['uidb64'])
#         form.save(user)
#         messages.success(self.request, "Your password has been set. You may go ahead and log in now.")
#         return super().form_valid(form)
#
def password_reset_request(request):
    if request.method == "POST":
        form = RequestResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            data = registrationmodel.objects.filter(email=email)
            if data.exists():
                user = data.first()
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                mail_subject = 'Reset your password'
                reset_link = f"{request.scheme}://{current_site.domain}/reset/{uid}/{token}/"
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                send_mail(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                messages.success(request, "If your email is valid, a password reset link has been sent to your email.")
            else:
                messages.error(request, "No user found with this email.")
        else:
            messages.error(request, "Invalid email form submission.")
    else:
        form = RequestResetForm()

    return render(request, "forgot_password.html", {'form': form})
def payment_page(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    amount = appointment.employee.rate * 100  # Convert to paise
    customer = appointment.user  # Assuming 'user' is the related customer field

    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    DATA = {
        "amount": amount,  # Amount in paise
        "currency": "INR",
        "receipt": str(id),  # Use appointment id as receipt
        "notes": {
            "key1": RAZORPAY_API_KEY,
            "key2": RAZORPAY_API_SECRET_KEY
        }
    }
    payment_order = client.order.create(data=DATA)
    payment_order_id = payment_order['id']

    customer_details = {
        "name": customer.name,
        "email": customer.email,
        "contact": customer.phone
    }

    return render(request, 'payment.html', {
        "amount": amount // 100,  # Convert back to rupees for display
        "api_key": RAZORPAY_API_KEY,
        "order_id": payment_order_id,
        "customer_details": customer_details,
        "id":id,
        "email":appointment.user.email,
    })





@csrf_exempt
def payment_callback(request,id):
    logger = logging.getLogger(__name__)
    if request.method == "POST":
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

        # Log incoming request data
        logger.debug("Incoming request data: %s", request.POST)

        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Log the received payment details
        logger.debug("Payment ID: %s, Order ID: %s, Signature: %s", payment_id, order_id, signature)

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify the payment signature
            client.utility.verify_payment_signature(params_dict)

            # Log verification success
            logger.debug("Payment signature verified successfully.")

            # Fetch the appointment object using receipt (which is the order_id)
            try:
                appointment = Appointment.objects.get(id=id)
            except Appointment.DoesNotExist:
                logger.error("Appointment with order ID %s does not exist.", order_id)
                return HttpResponse("Invalid order ID.", status=400)

            # Update the payment status
            appointment.payment = True
            appointment.save()

            logger.debug("Appointment %s payment status updated to True.", order_id)
            return redirect("success_page",id)

        except razorpay.errors.SignatureVerificationError as e:
            # Log the verification failure
            logger.error("Signature verification failed: %s", e)
            return redirect("cancel_page",id)
    return HttpResponse("Invalid request method.", status=400)
def success_page(request,id):
    det = get_object_or_404(Appointment, id=id)
    return render(request, 'payment_sucess.html',{"email":det.user.email})

def cancel_page(request,id):
    det = get_object_or_404(Appointment, id=id)
    return render(request, 'payment_cancel.html',{"email":det.user.email})




def refund_form(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    return render(request, 'refund_form.html', {'slot': appointment})


logger = logging.getLogger(__name__)
@csrf_exempt
def refund_request(request, id):
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

    if request.method == "POST":
        # Get appointment object
        try:
            appointment = Appointment.objects.get(id=id)
        except Appointment.DoesNotExist:
            return HttpResponse("Appointment not found.", status=404)

        # Validate bank details from form
        account_holder = request.POST.get('account_holder')
        bank_account_number = request.POST.get('bank_account_number')
        ifsc_code = request.POST.get('ifsc_code')
        payment_id = request.POST.get('payment_id')

        # Create refund (Razorpay API request)
        try:
            amount = appointment.employee.rate * 100  # Amount in paise
            response = client.payment.refund(payment_id, {
                'amount': amount,
                'currency': 'INR'
            })
            logger.info("Razorpay API response: %s", response)
            appointment.delete()
            return HttpResponse("Refund requested successfully and appointment deleted.")
        except Exception as e:
            error_message = f"Error processing refund: {str(e)}"
            logger.error(error_message)
            logger.error("Traceback: %s", traceback.format_exc())
            return HttpResponse(error_message, status=500)

    return HttpResponse("Invalid request method.", status=400)
# def test_mailgun():
#     send_mail(
#         'Test Email',
#         'This is a test email sent using Mailgun.',
#         settings.EMAIL_HOST_USER,
#         ['your_email@example.com'],  # Replace with your test email address
#     )
# class PasswordResetRequestView(FormView):
#     template_name = "password_reset.html"
#     success_url = reverse_lazy('password_reset_done')
#     form_class = PasswordResetForm
#     def form_valid(self, form):
#         form.save(
#             request=self.request,
#             use_https=self.request.is_secure(),
#             email_template_name='password_reset_email.html',
#         )
#         return super().form_valid(form)