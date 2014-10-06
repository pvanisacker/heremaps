from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'heremaps.views.home', name='home'),
    #url(r'^heremarkermap/$',render('heremaps:heremarkermap.html'), name='heremarkermap'),
    url(r'^heremarkermap/$', 'heremaps.views.heremarkermap', name='heremarkermap'),
    url(r'^setup/$', 'heremaps.views.setup', name='setup')
)
