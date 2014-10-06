from splunkdj.setup import forms

class SetupForm(forms.Form):
    app_id = forms.CharField(
        endpoint='configs/conf-setup', entity='heremaps', field='app_id',
        max_length=100)
    app_code = forms.CharField(
        endpoint='configs/conf-setup', entity='heremaps', field='app_code',
        max_length=100)