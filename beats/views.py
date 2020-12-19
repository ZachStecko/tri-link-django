from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomSignupForm,DocumentForm,ChangeEmail
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import BeatVideo, Customer, Document, Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
import stripe
import os
from django.http import HttpResponse, HttpResponseRedirect
from .utils import handle_uploaded_file, handle_uploaded_image, download, deleteTheFile
from .videoExports import export_video, Spectrum
from django.conf import settings
from pathlib import Path
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.db.models import F
import shutil
from django.utils import timezone
from datetime import datetime, timedelta
import string
import random
stripe.api_key = ""

def home(request):
    plans = BeatVideo.objects

    current_user = request.user
    send = current_user.id
    
    #random_value = Customer.objects.get(user = request.user).random_id
    audio = './Magic/Audio/user_'+str(send)
    img = './Magic/Image/user_'+str(send)
    file_path = './Magic/Video/user_'+str(send)+'.mp4'

    field_name = 'total'
    obj = Count.objects.first()
    field_value = getattr(obj, field_name)

    my_file = Path(file_path)
    #if my_file.is_file():
    #    os.remove(my_file)
    #try:
    #    shutil.rmtree(audio)
    #    shutil.rmtree(img)
    #    print(current_user)
    #except:
    #    print("We good")

    return render(request, 'beats/home.html', {'plans':plans,'user':current_user, 'total': field_value})

#Which payment plan the user chose
#If the user is authenticated and signed up,
#Send them to the request plan webpage the signed up and paid to see
#Except if the customer hasn't signed up send them to a page to join the site
def plan(request,pk):
    plan = get_object_or_404(BeatVideo, pk=pk)
    if plan.premium :
        if request.user.is_authenticated:
            try:
                if request.user.customer.membership:
                    return render(request, 'beats/video.html', {'plan':plan})
            except Customer.DoesNotExist:
                    return redirect('join')
        return redirect('join')
    else:
        return render(request, 'beats/video.html', {'plan':plan})

#Sends the user to a page showing the different plans to chose from.
def join(request):
    return render(request, 'beats/join.html')

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def software(request):
    if request.user.is_authenticated:
        try:
            if request.user.customer.membership:
                # Handle file upload
                current_user = request.user
                send = current_user.username
                random_value = Customer.objects.get(user = request.user).random_id
                file_path = './Magic/Video/'+random_value+'user_'+str(send)+'.mp4'
                my_file = Path(file_path)
                audio = 'Magic/Audio/user_'+str(send)
                img = 'Magic/Image/user_'+str(send)
                tmp = 'Magic/Temp/'+str(send)+'tmp'+'.mp4'
                try:
                    shutil.rmtree(audio)
                    shutil.rmtree(img)
                    os.remove(tmp)
                except:
                    print("We good1")
                if request.method == 'POST':
                    form = DocumentForm(request.POST, request.FILES)
                    if form.is_valid():
                        
                        vidCount = Customer.objects.get(user = request.user).video_count
                        lastDate = Customer.objects.get(user = request.user).created
                        now = timezone.now()
                        print('now')
                        if now-timedelta(hours=24) <= lastDate <= now:
                            #less than 24 hours
                            if vidCount == 10:
                                #less than 24 hours but daily limit reached
                                return redirect(home)
                        else:
                            #more than 24 hours
                            Customer.objects.filter(user=request.user).update(created=now)
                            Customer.objects.filter(user=request.user).update(video_count=0)
                            print('later')
                        
                        #1
                        random_id = id_generator()
                        random_value = Customer.objects.get(user = request.user).random_id
                        file_path = './Magic/Video/'+random_value+'user_'+str(send)+'.mp4'
                        my_file = Path(file_path)
                        if my_file.is_file():
                            os.remove(my_file)

                        fileExts = request.FILES['docfile']
                        audioType = os.path.splitext(fileExts.name)[1]

                        handle_uploaded_file(request.FILES['docfile'], send)
                        audioPathToExport = 'Magic/Audio/user_'+str(send)+'/user_'+str(send)+'%s'%(audioType)
                        audioPathToDelete = 'Magic/Audio/user_'+str(send)
                        
                        fileExt = request.FILES['imgfile']
                        ext = os.path.splitext(fileExt.name)[1]
                        handle_uploaded_image(request.FILES['imgfile'], send)
                        imgPathToExport = 'Magic/Image/user_'+str(send)+'/user_'+str(send)+'%s'%(ext)
                        imgPathToDelete = 'Magic/Image/user_'+str(send)

                        #2
                        userPath = 'Magic/Video/'+random_id+'user_'+str(send)+'.mp4'
                        
                        strokeCol = request.POST['strokeColour']
                        fillCol = request.POST['fillColour']

                        strokeColour = strokeCol.split(',')
                        fillColour = fillCol.split(',')

                        current_user = request.user
                        userID = current_user.username
                        try:
                            export_video(audioPathToExport,userPath,imgPathToExport, userID, strokeColour[0], strokeColour[1], strokeColour[2], fillColour[0], fillColour[1], fillColour[2])
                        except:
                            print('oh oks')
                            
                        try:
                            shutil.rmtree(audioPathToDelete)
                            shutil.rmtree(imgPathToDelete)
                        except:
                            print("We good2")

                        try:
                            Customer.objects.filter(user=request.user).update(video_count=F('video_count') + 1)
                            Customer.objects.filter(user=request.user).update(total_count=F('total_count') + 1)
                            Customer.objects.filter(user=request.user).update(random_id=random_id)
                            return redirect(thanks)
                        except Exception as e:
                            return None
                else:
                    form = DocumentForm()  # A empty, unbound forms

                audio = 'Magic/Audio/user_'+str(send)
                img = 'Magic/Image/user_'+str(send)

                #if my_file.is_file():
                #    os.remove(my_file)
                 # Render list page with the documents and the form  
                return render(request, 'beats/software.html',{'form': form,'my_file': my_file})
        except Customer.DoesNotExist:
                return redirect('join')
    return redirect('join')

def thanks(request):
   return render(request, 'beats/thanks.html')

def downloadFile(request):
    current_user = request.user
    return download(current_user)

def deleteFile(request):
    current_user = request.user
    deleteTheFile(current_user)
    return HttpResponse()

@login_required
def checkout(request):

    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    coupons = {'halloween':31, 'welcome':10}

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        plan = ''
        if request.POST['plan'] == 'yearly':
            plan = ''
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]
            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(),
                percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'plan':plan}], coupon=request.POST['coupon'].lower())
        else:
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'plan':plan}])

        customer = Customer()
        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()

        return redirect('home')
    else:
        coupon = 'none'
        plan = 'monthly'
        price = 500
        og_dollar = 5
        coupon_dollar = 0
        final_dollar = 5
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'yearly':
                plan = 'yearly'
                price = 5000
                og_dollar = 50
                final_dollar = 50
        if request.method == 'GET' and 'coupon' in request.GET:
            print(coupons)
            if request.GET['coupon'].lower() in coupons:
                print('fam')
                coupon = request.GET['coupon'].lower()
                percentage = coupons[request.GET['coupon'].lower()]


                coupon_price = int((percentage / 100) * price)
                price = price - coupon_price
                coupon_dollar = str(coupon_price)[:-2] + '.' + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + '.' + str(price)[-2:]

        return render(request, 'beats/checkout.html',
        {'plan':plan,'coupon':coupon,'price':price,'og_dollar':og_dollar,
        'coupon_dollar':coupon_dollar,'final_dollar':final_dollar})

def create(request):
    return render(request, 'beats/create.html')

def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.POST.get("cancel") == 'Cancel Membership?':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    
    if request.POST.get("download") == 'download':
        current_user = request.user
        send = current_user.username
        random_value = Customer.objects.get(user = request.user).random_id
        #5
        file_path = './Magic/Video/'+random_value+'user_'+str(send)+'.mp4'
        my_file = Path(file_path)

        if my_file.is_file():
            #exists
            try:
                wrapper = FileWrapper(open(file_path, 'rb'))
                response = HttpResponse(wrapper, content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
            except Exception as e:
                return HttpResponse(content=204)
    
    if request.POST.get('deleteAcc') == 'Delete Account':

        try:
            subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
            subscription.cancel_at_period_end = True
            request.user.customer.cancel_at_period_end = True
            cancel_at_period_end = True
            subscription.save()
            request.user.customer.save()
        except:
            print('meh')
        context = {}
        current_user = request.user
        send = current_user.username
        try:
            user = User.objects.get(username=send)
            user.is_active = False
            user.save()
            context['msg'] = 'Profile successfully disabled.'
            return redirect(home)
        except User.DoesNotExist:
            # ...
            print('nouser')
        except Exception as e:
            # ...
            print(e)
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False

    return render(request, 'registration/settings.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})

def terms_and_conditions(request):
    return render(request, 'registration/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'registration/privacy_policy.html')

@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')

def email_change(request):
    form = ChangeEmail
    if request.method == 'POST':
        form = ChangeEmail(request.user, request.POST)
        if form.is_valid():
            form.save()
        else:
            ctx = {"form": form} 
            # You may need other context here - use your get view as a template
            # The template should be the same one that you use to render the form
             # in the first place.
            return render(request, 'registration/email_change.html', ctx)
        return HttpResponseRedirect('/')
    else:
        user = User.objects.get(username=request.user)
        email = user.email
        form = ChangeEmail(User)
        variables = {
            'form': form,
            'email': email
        }
    return render(request, 'registration/email_change.html', variables)

class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

