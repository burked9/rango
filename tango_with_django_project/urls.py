from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, login
from registration.backends.simple.views import RegistrationView

# Creates a new class that redirects the user to the index page, if login is successful.
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/rango/'



urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^rango/', include('rango.urls')), 
        url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
        url(r'^accounts/', include('registration.backends.simple.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
