from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .models import Email

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'mailapp/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    return render(request, 'mailapp/register.html')

# Forgot password view
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            # Send reset email (simplified)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_link}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset email sent.')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
    return render(request, 'mailapp/forgot_password.html')

# Reset password view
def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User .DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful. Please login.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'mailapp/reset_password.html')
    else:
        messages.error(request, 'Invalid reset link.')
        return redirect('forgot_password')

# Inbox view
@login_required
def inbox_view(request):
    emails = Email.objects.filter(recipients=request.user).order_by('-timestamp')
    return render(request, 'mailapp/inbox.html', {'emails': emails})

# Sent view
@login_required
def sent_view(request):
    emails = Email.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'mailapp/sent.html', {'emails': emails})

# Compose view
@login_required
def compose_view(request):
    if request.method == 'POST':
        recipients_usernames = request.POST['recipients'].split(',')
        subject = request.POST['subject']
        body = request.POST['body']
        recipients = User.objects.filter(username__in=[r.strip() for r in recipients_usernames])
        email = Email.objects.create(sender=request.user, subject=subject, body=body, is_sent=True)
        email.recipients.set(recipients)
        email.save()
        messages.success(request, 'Email sent successfully.')
        return redirect('sent')
    return render(request, 'mailapp/compose.html')