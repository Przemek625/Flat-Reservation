from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from reservation.forms import SearchForm, AddFlatForm, AddCityForm, ReserveFlat
from reservation.models import Flat, Reservation


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            rsd = form.cleaned_data['reservation_start_date']
            red = form.cleaned_data['reservation_end_date']

            available_flats = Flat.objects.filter(city__name=city).\
                filter(available_from__gt=rsd, available_to__lte=red)

            unavailable_reservations = Reservation.objects. \
                filter(Q(reservation_start_date__gte=rsd,
                         reservation_end_date__lte=red) |
                       Q(reservation_start_date__lte=rsd,
                         reservation_end_date__gte=red)).all()

            unavailable_flats_pk_set = [e.flat.pk for e in unavailable_reservations]

            available_flats.exclude(pk__in=unavailable_flats_pk_set)

            if available_flats:
                return render(request, 'index.html',
                              {'form': form,
                               'available_flats': available_flats, 'rsd': rsd.isoformat(), 'red': red.isoformat()})
            else:
                message = 'There are no available flats for your query! ' \
                          'Maybe try another city or date ranges'
                return render(request, 'index.html',
                              {'form': form, 'message': message})
        else:
            return render(request, 'index.html', {'form': form})
    else:
        form = SearchForm()
        return render(request, 'index.html', {'form': form})


def add_flat(request):
    if request.method == 'POST':
        form = AddFlatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'add_flat.html', {'form': form})
    else:
        form = AddFlatForm()
        return render(request, 'add_flat.html', {'form': form})


def add_city(request):
    if request.method == 'POST':
        form = AddCityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_flat')
        else:
            return render(request, 'add_city.html', {'form': form})
    else:
        form = AddCityForm()
        return render(request, 'add_city.html', {'form': form})


def reserve_flat(request):
    # data from url
    flat_id = request.GET.get('flat_id', '')
    rsd = request.GET.get('rsd', '')
    red = request.GET.get('red', '')

    if not (flat_id and rsd and red):
        raise Http404('Something went wrong')

    try:
        flat = Flat.objects.get(pk=flat_id)
    except Flat.DoesNotExist:
        request.session['message'] = 'It seems that such flat does not exist'
        return redirect('reserve_flat_result')

    if request.method == 'POST':
        form = ReserveFlat(request.POST)
        if form.is_valid():
            rb = form.cleaned_data['reserved_by']
            try:
                flat_is_reserved = Reservation.objects.filter(flat__id=flat_id). \
                    filter(Q(reservation_start_date__gte=rsd,
                             reservation_end_date__lte=red) |
                           Q(reservation_start_date__lte=rsd,
                             reservation_end_date__gte=red)).all()
            except ValidationError:
                raise Http404('Something went wrong')
            if flat_is_reserved:
                request.session['message'] = 'It seems that this flat is no longer available for this time frame'
                return redirect('reserve_flat_result')
            else:
                Reservation(reservation_start_date=rsd, reservation_end_date=red,
                            reserved_by=rb, flat=flat).save()
                request.session['message'] = 'You have reserved the flat successfully'
                return redirect('reserve_flat_result')

        else:
            return render(request, 'reserve_flat.html', {'form': form, 'rsd': rsd, 'red': red, 'flat': flat})
    else:
        form = ReserveFlat()
        return render(request, 'reserve_flat.html', {'form': form, 'rsd': rsd, 'red': red, 'flat': flat})


def reserve_flat_result(request):
    try:
        message = request.session['message']
        del request.session['message']
        return render(request, 'reserve_flat_result.html', {'message': message})
    except KeyError:
        raise Http404('This page is not available for you')
