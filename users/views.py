import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import LoginForm
from .models import EmailVerification

User = get_user_model()

def check_is_verify(request):
    if not request.user.is_verify and request.user.is_authenticated:
        return redirect('email_verify')
    

def generate_verification_token():
    token_length = 32
    return secrets.token_hex(token_length)


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = None
        if email:
            user = authenticate(request, username=email, password=password)
        elif username:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_verify:
                return redirect('data_list')
            else:
                messages.error(request, 'Your email is not verified. Please check your email to verify your account.')
                # return redirect('email_verify') 
                return render(request, 'email_verify.html', {'email': user.email})
        else:
            form = LoginForm(request.POST)
            form.add_error(None, 'Invalid username, email, or password.')
            messages.error(request, 'Invalid username, email, or password.')
            return render(request, 'auth/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})


def send_verification_email(request):
    try:
        user = request.user
        email_verification = EmailVerification.objects.get(user=user)

        current_site = get_current_site(request)
        verification_token = email_verification.verification_token
        verification_link = f"{current_site.domain}/verify-email/{verification_token}/"

        email_subject = "Almost done! Finish your registration"
        email_html_message = render_to_string('auth/verification.html', {
            'verification_link': verification_link
        })
        email_plain_message = strip_tags(email_html_message)
        send_mail(email_subject, email_plain_message, settings.EMAIL_HOST_USER, [user.email],
                  html_message=email_html_message)


        # return redirect('email_verify')
        return render(request, 'email_verify.html', {"email": user.email})
    
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, "Invalid user or verification token.")

    # Handle the case when an error occurs during sending the verification email
    return redirect('email_verify')



def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        # Save password1 value to password2 field
        request.POST = request.POST.copy()
        request.POST['password2'] = password1

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
        else:
            try:
                user = User.objects.create_user(email=email, username=email, password=password1)
                user.is_verify = False
                user.save()

                # Log in the user
                user = authenticate(request, username=email, password=password1)
                login(request, user)

                # Create an EmailVerification instance
                verification_token = generate_verification_token()  # Implement a token generation function
                email_verification = EmailVerification.objects.create(user=user, verification_token=verification_token)
                # Send the verification email
                send_verification_email(request)


                # return redirect('email_verify')
                return render(request, 'email_verify.html', {'email': email})
            except IntegrityError:
                messages.error(request, "Email already exists. Please use a different email.")

    return render(request, 'auth/register.html')


def verify_email(request, verification_token):
    try:
        email_verification = EmailVerification.objects.get(verification_token=verification_token)
        user = email_verification.user

        if not user.is_verify:
            user.is_verify = True  # Set is_verify to True upon successful verification
            user.save()
            messages.success(request, "Email verification successful.")
        elif user.is_verify:
            messages.info(request, "Email already verified.")
        else:
            messages.error(request, "Invalid verification token.")
    except EmailVerification.DoesNotExist:
        messages.error(request, "Invalid verification token.")

    return redirect('data_list')


@login_required
def logout_view(request):
    logout(request)
    return redirect('data_list')


def email_verify(request):
    return render(request, 'email_verify.html', {'email': request.user.email})



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Handle user not found error
            return render(request, 'auth/forgot_password.html', {'error': 'User with this email is not found.'})

        # Generate password reset token
        token = default_token_generator.make_token(user)

        # Build password reset link
        current_site = get_current_site(request)
        reset_link = f"{current_site.domain}/reset-password/{user.pk}/{token}/"

        # Send password reset email
        subject = 'Reset Password'
        message = render_to_string('auth/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        email_plain_message = strip_tags(message)
        send_mail(subject, email_plain_message, settings.EMAIL_HOST_USER, [email], html_message=message)

        # Redirect to a success page or show a success message
        return render(request, 'auth/forgot_password.html', {'success': "We've just sent you an reset password email."})

    return render(request, 'auth/forgot_password.html')


def reset_password(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Handle user not found error
        return render(request, 'auth/reset_password.html', {'error': 'User not found.'})

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Handle password change logic
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()

            # Authenticate the user with the new password
            new_user = authenticate(request, username=user.email, password=new_password)
            if new_user is not None:
                login(request, new_user)
                # Redirect to the 'data_list' page
                messages.success(request, "Password successfully changed.")
                return redirect('data_list')  # Replace 'data_list' with the actual name or URL pattern of your data list page
            else:
                # Handle authentication error
                return render(request, 'auth/reset_password.html', {'error': 'Failed to authenticate.'})
        else:
            return render(request, 'auth/reset_password.html', {'user_id': user_id, 'token': token})
    else:
        # Handle invalid token error
        return render(request, 'auth/reset_password.html', {'error': 'Invalid token.'})
