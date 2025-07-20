
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from users.models import Event, Customer, Registration
from django.contrib.auth.models import User

def index(request):
    # Get current date for filtering
    today = timezone.now().date()
    
    # Calculate stats
    total_events = Event.objects.count()
    total_users = Customer.objects.count()  # Or User.objects.count() if you want all users
    
    # Upcoming events (date >= today)
    upcoming_events = Event.objects.filter(date__gte=today).count()
    
    # Completed events (date < today)
    completed_events = Event.objects.filter(date__lt=today).count()
    
    # Get recent events with additional info
    recent_events = Event.objects.all().order_by('-date')[:10]  # Get 10 most recent
    
    # Prepare event data for table
    events_data = []
    for event in recent_events:
        # Get host name (user who created the event)
        host_name = event.user.get_full_name() or event.user.username
        
        # Get number of attendees
        attendees_count = Registration.objects.filter(event=event).count()
        
        # Determine status
        if event.date < today:
            status = ('Inactive', 'bg-red-600')
        else:
            status = ('Active', 'bg-green-600')
        
        events_data.append({
            'id': event.id,
            'name': event.name,
            'host_name': host_name,
            'date': event.date.strftime('%b %d, %Y'),
            'attendees': attendees_count,
            'status': status,
        })
    
    context = {
        'total_events': total_events,
        'total_users': total_users,
        'upcoming_events': upcoming_events,
        'completed_events': completed_events,
        'events_data': events_data,
    }
    
    return render(request, 'manager/index.html', context)

def manager_logout(request):
    logout(request)
    return redirect('users:login') 


# views.py (inside manager app)

def view_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Get all registrations for this event
    registrations = Registration.objects.filter(event=event).select_related('user')
    
    # Count total attendees
    total_attendees = registrations.count()
    
    context = {
        'event': event,
        'registrations': registrations,
        'total_attendees': total_attendees,
    }
    return render(request, 'manager/singlevent.html', context = context)


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('manager:index')