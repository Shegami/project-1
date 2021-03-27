from django.http import HttpResponse
from django.shortcuts import render, redirect
from shortener.forms import ShortenerForm
from shortener.models import Shortener
from random import choices, randint
from string import ascii_letters, digits


def shortener(request):
    if request.method == 'GET':
        form = ShortenerForm()
        links = Shortener.objects.all()
        return render(request, 'main.html', {
            'form': form,
            'links': links
        })
    else:
        if request.POST['button'] == 'submit':
            form = ShortenerForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                full_url = cd['full_url']
                user_url = cd['user_url']
                short_url = is_user_url(user_url)
                while short_url is False:
                    short_url = is_user_url(user_url)
                Shortener.objects.create(
                    full_url=full_url,
                    short_url=short_url)
                return redirect('shortener')
            errors = form.errors
            return HttpResponse(f'errors in {errors}')


def create_model(full_url, short_url):
    model = Shortener(
        full_url=full_url,
        short_url=short_url
    )
    return model


def generate_url(user_url=None):
    n = randint(0, 12)
    main_url = 'http://127.0.0.1:8000/'
    if user_url is None:
        user_url = ''.join(choices(ascii_letters + digits, k=n))
    short_url = f'{main_url}{user_url}'
    return is_available(short_url)


def is_user_url(user_url):
    if user_url:
        return generate_url(user_url)
    else:
        return generate_url()


def is_available(short_url):
    check = Shortener.objects.filter(short_url=short_url).first()
    if check:
        return False
    else:
        return short_url


def click_counter(request, link_id):
    model = Shortener.objects.get(id=link_id)
    model.clicks += 1
    model.save()
    return redirect(model.full_url)
