from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'heremaps.views.home', name='home'),
    url(r'^heremarkermap_django/$', render('heremaps:heremarkermap_django.html'), name='heremarkermap_django'),
    url(r'^heremarkermap_js/$', render('heremaps:heremarkermap_js.html'), name='heremarkermap_js'),
    url(r'^setup/$', 'heremaps.views.setup', name='setup')
)
