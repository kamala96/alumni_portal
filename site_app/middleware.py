from django.utils import timezone
from django.contrib.auth import logout
from site_app.models import TrafficLog
from django.utils.deprecation import MiddlewareMixin
import re

class InactivityTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Set your desired inactivity timeout period in seconds
            inactivity_timeout_seconds = 3600  # 30 minutes

            # Check the last activity time
            last_activity_time_str = request.session.get('last_activity_time')

            # If last activity time is not set, set it
            if not last_activity_time_str:
                request.session['last_activity_time'] = timezone.now().isoformat()
            else:
                # Convert the stored string to a datetime object
                last_activity_time = timezone.datetime.fromisoformat(last_activity_time_str)

                # Calculate the inactivity time difference
                inactivity_time_difference = timezone.now() - last_activity_time

                # If the user has been inactive, log them out
                if inactivity_time_difference.total_seconds() > inactivity_timeout_seconds:
                    logout(request)

            # Update the last activity time for the user
            request.session['last_activity_time'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response





class TrafficMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the user is already counted in the session
        if not request.session.get('is_counted'):
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            device_type = self.get_device_type(user_agent)
            ip_address = self.get_ip_address(request)
            
            # Log the traffic
            now = timezone.now()
            today = timezone.now().date()
            if not TrafficLog.objects.filter(ip_address=ip_address, user_agent=user_agent, timestamp__date=today).exists():
                traffic_log, created = TrafficLog.objects.get_or_create(ip_address=ip_address, user_agent=user_agent, device_type=device_type)

            if not created:
                # Update last activity timestamp if entry already exists
                traffic_log.last_activity = now
                traffic_log.save()

            # Mark this session as counted
            request.session['is_counted'] = True

    def get_ip_address(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_device_type(self, user_agent):
        if re.search(r'mobile|android|iphone|ipad', user_agent):
            return 'mobile'
        elif re.search(r'tablet|ipad', user_agent):
            return 'tablet'
        elif re.search(r'windows|macintosh|linux', user_agent):
            return 'desktop'
        elif re.search(r'bot|spider', user_agent):
            return 'bot'
        return 'other'
    