from django.conf.urls.defaults import patterns, include, url
from eventdemo.htmlembeded import hello, getparam, current_datetime
from eventdemo.ftproxy import ftproxy
from eventdemo.lookuptable.lookupservice import lookupService
from eventdemo.fusionservice import authStepInit
from eventdemo.fusionservice import AuthStepValidToken
from eventdemo.admin import adminPage, processAdminCmd
from eventdemo.jqueryeg.jqueryeg import jqueryEg
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djtest.views.home', name='home'),
    # url(r'^djtest/', include('djtest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
                       ( r'^resources/(.*)$',
                         'django.views.static.serve',
                         { 'document_root': settings.MEDIA_ROOT } ),
                       url(r'^hello\.html$', hello),
                       url(r'^embeded/(\d{1,2})$', getparam),
                       url(r'^curdate\.html$',current_datetime),
                       url(r'^ftproxy',ftproxy),
                       url(r'^partservice', lookupService),
                      
                       # auth
                       url(r'^AuthStepValidToken',AuthStepValidToken),
                       url(r'^authStepInit', authStepInit),
                      
                       #admin
                       url(r'^admin/index\.html', adminPage),
                       url(r'^admin/processAdminCmd', processAdminCmd),
                       
                       #jquery example
                        url(r'^jquery/jqueryeg\.html', jqueryEg),
)
