from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.core.urlresolvers import reverse

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse('login') + '?token=' + str(token.uid))
    message_body = f'Käytä tätä linkkiä kirjautuaksesi sisään:\n\n{url}'
    send_mail('Sinun kirjautumislinkkisi Superlistaan', message_body, 'noreply@superlista', [email])

    messages.success(request, "Tarkista sähköpostisi, lähetimme sinulle linkin, jonka avulla voit kirjautua sisään.")
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

