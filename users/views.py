from django.shortcuts import render,reverse ,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from users.models import *
from django.contrib import messages
from .models import Event
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Count


# Create your views here.

@login_required(login_url='/login')
def index(request):
    events = Event.objects.annotate(registration_count=Count('registration'))

    context = {
        "events": events,
    }

    return render(request, 'index.html', context=context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('users:index'))

        else:
            context = {
                "error" : True,
                "message": "Invalid Email or Password"
            }
            return render(request, 'login.html', context=context)
    else:         
        return render(request, 'login.html')
    


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            context = {
                "error" : True,
                "message": "Email already exists"
            }
            return render(request, 'register.html', context=context)

        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_customer=True
            )
            user.save()

            customer = Customer.objects.create(
                user=user
            )
            customer.save()
            return HttpResponseRedirect(reverse('users:login'))

    else:
        return render(request, 'register.html')
    

@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('users:login'))


@login_required(login_url='/login')
def createevent(request):
    if request.method == 'POST':
        name = request.POST.get('eventname')
        event_type = request.POST.get('eventtype')
        image = request.FILES.get('Image')
        description = request.POST.get('Description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        capacity = request.POST.get('capacity')

        # Save event
        Event.objects.create(
            user=request.user,
            name=name,
            type=event_type,
            img=image,
            description=description,
            date=date,
            time=time,
            venue=venue,
            capacity=capacity
        )

        return redirect('users:manageevent')  # You must name your URL this in urls.py

    return render(request, 'createevent.html')

@login_required(login_url='/login')
def manageevent(request):
    user = request.user
    events = Event.objects.filter(user=user)

    
    context = {
        "events" : events,

    }

    return render(request, 'manageevent.html', context = context)


@login_required(login_url='/login')
def editevent(request, id):
    event = get_object_or_404(Event, id=id, user=request.user)

    if request.method == 'POST':
        event.name = request.POST.get('eventname')
        event.type = request.POST.get('eventtype')

        if 'Image' in request.FILES:
            event.img = request.FILES.get('Image')

        event.description = request.POST.get('Description')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time')
        event.venue = request.POST.get('venue')
        event.capacity = request.POST.get('capacity')
        event.save()

        return redirect('users:manageevent')

    return render(request, 'createevent.html', {'event': event, 'edit': True})


@login_required(login_url='/login')
def deleteevent(request, id):
    event = get_object_or_404(Event, id=id, user=request.user)
    event.delete()
    return redirect('users:manageevent')


@login_required(login_url='/login')
def allevent(request):
    query = request.GET.get('q')  # Get the search query from URL

    events = Event.objects.all().annotate(
        total_registered=Count('registration')
    )

    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(type__icontains=query) |
            Q(venue__icontains=query)
        )

    context = {
        "events": events
    }

    return render(request, 'allevent.html', context=context)

@login_required(login_url='/login')
def singleevent(request, id):
    event = get_object_or_404(Event, id=id)
    is_registered = Registration.objects.filter(user=request.user, event=event).exists()

    total_registered = Registration.objects.filter(event=event).count()

    context = {
        'event': event,
        'is_registered': is_registered,
        'total_registered': total_registered,
    }
    return render(request, 'singleevent.html', context = context)

@login_required(login_url='/login')
def singleeventstatus(request, id):
    event = get_object_or_404(Event, id=id)

    # Ensure only the creator can access
    if request.user != event.user:
        return redirect('users:index')  # Or raise 403

    registrations = Registration.objects.filter(event=event).select_related('user')

    context = {
        "event": event,
        "registrations": registrations,
        "total_attendees": registrations.count()
    }

    return render(request, 'singleeventstatus.html', context=context)

@login_required(login_url='/login')
def register_event(request, id):
    event = get_object_or_404(Event, id=id)

    # Check if already registered
    already_registered = Registration.objects.filter(user=request.user, event=event).exists()
    if not already_registered:
        Registration.objects.create(user=request.user, event=event)

    return redirect('users:singleevent', id=id)  

@login_required(login_url='/login')
def registeredevent(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    events = [r.event for r in registrations]

    context = {
        'events': events
    }
    return render(request, 'registeredevent.html', context)

@login_required(login_url='/login')
@require_POST
def unregister_event(request, id):
    event = get_object_or_404(Event, id=id)
    Registration.objects.filter(user=request.user, event=event).delete()
    return redirect('users:singleevent', id=id)

@login_required(login_url='/login')
def delete_registration(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)

    # Only event creator can delete
    if request.user != event.user:
        return redirect('users:index')

    Registration.objects.filter(event=event, user_id=user_id).delete()
    return redirect('users:singleeventstatus', id=event_id)