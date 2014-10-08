from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'heremaps.views.home', name='home'),
    #url(r'^heremarkermap/$',render('heremaps:heremarkermap.html'), name='heremarkermap'),
    url(r'^heremarkermap1/$', render('heremaps:heremarkermap1.html'), name='heremarkermap1'),
    url(r'^heremarkermap2/$', render('heremaps:heremarkermap2.html'), name='heremarkermap2'),
    url(r'^setup/$', 'heremaps.views.setup', name='setup')
)
