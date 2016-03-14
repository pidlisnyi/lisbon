from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from .models import Offer
from .forms import OfferForm
from helpers.models import Helpers


def get_lang(request):
    lang = request.LANGUAGE_CODE
    return lang


def get_company():
    return Helpers.objects.get(id=1).company_name


def offer_list(request):
    queryset_list = Offer.objects.all()
    lang = get_lang(request)
    breadcrumbs = [
        {'url': '/', 'name': _('Home')},
        {'url': '#', 'name': _('Offers'), 'active': True}
    ]
    query = request.GET.get('q')
    if query:
        if 'pt' in lang:
            queryset_list = queryset_list.filter(
                Q(title_PT__icontains=query) |
                Q(description_PT__icontains=query)
            ).distinct()
        else:
            if 'en' in lang:
                queryset_list = queryset_list.filter(
                    Q(title_EN__icontains=query) |
                    Q(description_EN__icontains=query)
                ).distinct()
            else:
                if 'de' in lang:
                    queryset_list = queryset_list.filter(
                        Q(title_DE__icontains=query) |
                        Q(description_DE__icontains=query))

    paginator = Paginator(queryset_list, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('accounts:signup')
    else:
        form = OfferForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Offer Created')
            return redirect('offer:list')

    context = {
        'company': get_company(),
        'title': _('Offers'),
        'object_list': queryset,
        'breadcrumbs': breadcrumbs,
        'page_request_var': page_request_var,
        'value': _('Add'),
        'form': form
    }

    return render(request, 'partials/offer.html', context)


def offer_detail(request, pk=None):
    offer = Offer.objects.get(pk=pk)
    lang = get_lang(request)
    title = {
        'pt': offer.title_PT,
        'en': offer.title_EN,
        'de': offer.title_DE
    }
    description = {
        'pt': offer.description_PT,
        'en': offer.description_EN,
        'de': offer.description_DE
    }
    breadcrumbs = [
        {'url': '/', 'name': _('Home'), 'active': False},
        {'url': '/offer', 'name': _('Offers'), 'active': False},
        {'url': '#', 'name': title[lang], 'active': True}]
    context = {
        'company': get_company(),
        'breadcrumbs': breadcrumbs,
        'title': title[get_lang(request)],
        'object': {
            'id': offer.id,
            'keywords_SEO': offer.keywords_SEO,
            'description_SEO': offer.description_SEO,
            'title': title[lang],
            'description': description[lang],
            'img': offer.img,
        },
    }

    return render(request, 'templates/_offer_details.html', context)


def offer_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('accounts:signup')
    else:
        form = OfferForm(request.POST or None, request.FILES or None)
        breadcrumbs = [{'url': '/', 'name': _('Home'), 'active': False},{'url': '/offer', 'name': _('Offers'), 'active': False},{'url': '#', 'name': _('Create Offer'), 'active': True}]
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Offer Created')
            return redirect('offer:list')

    context = {
        'company': get_company(),
        'title': _('Create Offer'),
        'breadcrumbs': breadcrumbs,
        'value': _('Add'),
        'form': form
    }

    return render(request, 'templates/_form.html', context)


def offer_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('accounts:signup')
    else:
        offer = get_object_or_404(Offer, pk=pk)
        lang = get_lang(request)
        title = {
            'pt': offer.title_PT,
            'en': offer.title_EN,
            'de': offer.title_DE
        }
        breadcrumbs = [{'url': '/', 'name': _('Home')},
                       {'url': '/offer', 'name': _('Offers')},
                       {'url': '#', 'name': _('Edit') + ' ' + title[lang], 'active': True}]
        form = OfferForm(request.POST or None, request.FILES or None, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.save()
            messages.success(request, _('Offer saved'))
            return redirect('offer:list')

        context = {
            'company': get_company(),
            'title': _('Edit') + ' ' + title[lang],
            'breadcrumbs': breadcrumbs,
            'instance': offer,
            'form': form
        }
        return render(request, 'templates/_form.html', context)


def offer_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('accounts:signup')
    instance = get_object_or_404(Offer, pk=pk)
    instance.delete()
    messages.success(request, 'Offer deleted')
    return redirect('offer:list')
