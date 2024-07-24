from django.utils import timezone
from django.contrib.auth import logout

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
