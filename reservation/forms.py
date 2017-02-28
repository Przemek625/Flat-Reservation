import datetime
from django import forms

from reservation.models import Flat, City


class SearchForm(forms.Form):
    city = forms.ModelChoiceField(required=True, queryset=City.objects.all())
    reservation_start_date = forms.DateField(
        widget=forms.DateInput({'class': 'datepicker input-sm form-control', 'placeholder': 'From Date'}),
        required=True)
    reservation_end_date = forms.DateField(
        widget=forms.DateInput({'class': 'datepicker input-sm form-control', 'placeholder': 'To Date'}),
        required=True)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        rsd = cleaned_data.get('reservation_start_date')
        red = cleaned_data.get('reservation_end_date')
        try:
            if rsd > red:
                msg = 'Reservation start date can not be bigger than Reservation end date!'
                self.add_error('reservation_start_date', msg)
            if rsd < datetime.date.today():
                msg = 'Reservation start date can not be lower than today\'s date!'
                self.add_error('reservation_start_date', msg)
        except TypeError:
            pass


class AddFlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = '__all__'


class AddCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'


class ReserveFlat(forms.Form):
    reserved_by = forms.CharField(required=True)
