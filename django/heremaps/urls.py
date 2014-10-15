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
    url(r'^hereshapemap_django/$', render('heremaps:hereshapemap_django.html'), name='hereshapemap_django'),
    url(r'^hereshapemap_js/$', render('heremaps:hereshapemap_js.html'), name='hereshapemap_js'),
    url(r'^hereshapemap_js_custom/$', render('heremaps:hereshapemap_js_custom.html'), name='hereshapemap_js_custom'),
    url(r'^hereshapemap_js_custom2/$', render('heremaps:hereshapemap_js_custom2.html'), name='hereshapemap_js_custom2'),
    url(r'^hereshapemap_js_de/$', render('heremaps:hereshapemap_js_de.html'), name='hereshapemap_js_de'),
    url(r'^hereshapemap_js_fr/$', render('heremaps:hereshapemap_js_fr.html'), name='hereshapemap_js_fr'),
    url(r'^hereshapemap_js_in/$', render('heremaps:hereshapemap_js_in.html'), name='hereshapemap_js_in'),
    url(r'^hereshapemap_js_uk/$', render('heremaps:hereshapemap_js_uk.html'), name='hereshapemap_js_uk'),
    url(r'^hereshapemap_js_us/$', render('heremaps:hereshapemap_js_us.html'), name='hereshapemap_js_us'),
    url(r'^hereheatmap_django/$', render('heremaps:hereheatmap_django.html'), name='hereheatmap_django'),
    url(r'^hereheatmap_js/$', render('heremaps:hereheatmap_js.html'), name='hereheatmap_js'),
    url(r'^hereheatmap_js_custom/$', render('heremaps:hereheatmap_js_custom.html'), name='hereheatmap_js_custom'),
    url(r'^reversegeocode/$', render('reversegeocode.html'), name='reversegeocode'),
    url(r'^setup/$', 'heremaps.views.setup', name='setup')
)