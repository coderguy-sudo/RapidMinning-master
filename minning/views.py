from django .views import generic
from .forms import *
from django.http import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import auth


class IndexView(generic.ListView):
    template_name = 'minning/index.html'

    def get_queryset(self):
        return


def registration(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.is_active = False
            user.save()
            #user = User.objects.create_user(username=username, email=email, password=password)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Account.'
            message = render_to_string('minning/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return HttpResponseRedirect('/registration/')

    else:
        form = userForm()
    return render(request, 'minning/registration.html', {'frm': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'minning/confirmed.html')
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['pas']
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.error(request, 'Username or Password is not Correct.')
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid User')

    return render(request, 'minning/login.html')


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'minning/dashboard.html')


def logout(request):
    auth.logout(request)
    return render(request, 'minning/login.html')
