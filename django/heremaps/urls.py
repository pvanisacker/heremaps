from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'heremaps.views.home', name='home'),
    url(r'^heremarkermap_django/$', render('heremaps:heremarkermap_django.html'), name='heremarkermap_django'),
    url(r'^heremarkermap_js/$', render('heremaps:heremarkermap_js.html'), name='heremarkermap_js'),
    url(r'^heremarkermap_js_custom/$', render('heremaps:heremarkermap_js_custom.html'), name='heremarkermap_js_custom'),
    url(r'^hereclustermap_django/$', render('heremaps:hereclustermap_django.html'), name='hereclustermap_django'),
    url(r'^hereclustermap_js/$', render('heremaps:hereclustermap_js.html'), name='hereclustermap_js'),
    url(r'^hereclustermap_js_custom/$', render('heremaps:hereclustermap_js_custom.html'), name='hereclustermap_js_custom'),
    url(r'^geocode/$', render('geocode.html'), name='geocode'),
    url(r'^reversegeocode/$', render('reversegeocode.html'), name='reversegeocode'),
    url(r'^setup/$', 'heremaps.views.setup', name='setup')
)