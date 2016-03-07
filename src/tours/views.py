from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import TourForm
from .models import Tour, Offer


def tour_list(request):
    queryset_list = Tour.objects.all()
    breadcrumbs_list = [{'url': '/', 'name': 'Home'}, {'url': '/tours', 'name': 'Tours'}]
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        'title': 'Tours',
        'breadcrumbs_list': breadcrumbs_list,
        'page_request_var': page_request_var,
    }

    return render(request, 'partials/tours.html', context)


def tour_detail(request, pk=None):
    breadcrumbs_list = [{'url': '/', 'name': 'Home'}, {'url': '/tours', 'name': 'Tour detail'}]
    model = Tour.objects.get(pk=pk)
    context = {
        'breadcrumbs_list': breadcrumbs_list,
        'title': 'Tour detail',
        'object': model,
    }

    return render(request, 'partials/detail.html', context)


def tour_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('accounts:signup')
    else:
        instance = get_object_or_404(Tour, pk=pk)
        breadcrumbs_list = [{'url': '/', 'name': 'Home'}, {'url': '/tours', 'name': 'Tour edit'}]
        form = TourForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Tour saved')
            return redirect('tour_list')

        context = {
            'title': 'Tout Edit',
            'breadcrumbs_list': breadcrumbs_list,
            'instance': instance,
            'form': form
        }
        return render(request, 'templates/_edit_form.html', context)


def tour_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect('accounts:signup')
    else:
        # breadcrumbs_list = [{'url': '/', 'name': 'Home'}, {'url': '/tours', 'name': 'Tour create'}],
        form = TourForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # message success
            #  messages.success(request, "Successfully Created")
            return redirect('tour_list')

        context = {
            'title': 'Tour create',
            'breadcrumbs_list': [{'url': '/', 'name': 'Home'}, {'url': '/tours', 'name': 'Tour create'}],
            'value': 'Create Tour',
            'form': form
        }

        return render(request, 'templates/_form.html', context)


class ServiceDetailView(generic.DetailView):
    model = Offer
    template_name = 'partials/detail.html'
    context_object_name = 'object'
