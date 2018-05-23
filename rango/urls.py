from django.conf.urls import url
from django.contrib.auth.views import password_change, password_change_done
from rango import views


urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
        url(r'^restricted/', views.restricted, name='restricted'),
        
        url(r'^accounts/password/change/$', password_change, {
                'template_name': 'registration/password_change_form.html'}, name ='password_change'), 
        url(r'^accounts/password/change/done/$', password_change_done, {
                'template_name': 'registration/password_change_done.html'}, name ='password_change_done'),              
]

## These were engulfed by -- url(r'^accounts/', include('registration.backends.simple.urls')), in the main URLS.py
        ##url(r'^register/$', views.register, name='register'),
        ##url(r'^login/$', views.user_login, name='login'),
        ##url(r'^logout/$', views.user_logout, name='logout'),
        #url(r'^register_profile/$', views.register_profile, name='register_profile'),