from django.contrib.auth.decorators import login_required
from splunkdj.decorators.render import render_to
from splunkdj.setup import config_required
from splunkdj.setup import create_setup_view_context
from .forms import SetupForm
from django.core.urlresolvers import reverse

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