from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe
from django.core.mail import EmailMessage
from .forms import SignupForm
from .tokens import account_activation_token
from .decorators import user_not_authenticated


# Create your views here.

def activate(request, domain, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for email conformation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    context = {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    }
    message = render_to_string('registration/active_accounts.html', context)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, mark_safe(f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'))
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@user_not_authenticated
def home_view(request):
    return render(request, 'home.html')

@login_required
def chat_view(request):
    return render(request, 'chat.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html') 

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, email)
            login(request, user)
            return redirect('chat')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')