from django.contrib.auth.decorators import login_required
from splunkdj.decorators.render import render_to
from splunkdj.setup import config_required
from splunkdj.setup import create_setup_view_context
from .forms import SetupForm
from django.core.urlresolvers import reverse

def get_app_id(request):
    print("get_app_id")
    service = request.service
    app_id="none"
    app_code="none"
    for conf in service.confs:
        if conf.name == "setup":
            for stanza in conf.iter():
                if stanza.name == "heremaps":
                    app_id=stanza.content["app_id"]
                    app_code=stanza.content["app_code"]
    return {'app_id':app_id,'app_code':app_code}

@render_to('heremaps:home.html')
@login_required
@config_required
def home(request):
    return {}

@render_to('heremaps:setup.html')
@login_required
def setup(request):
    return create_setup_view_context(
        request,
        SetupForm,
        reverse('heremaps:home'))