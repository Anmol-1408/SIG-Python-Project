from django import forms
from .models import FinanceRecord

class FinanceRecordForm(forms.ModelForm):
    include_as_expense = forms.BooleanField(required=False, label="Include as Expense")

    class Meta:
        model = FinanceRecord
        fields = ['description', 'amount', 'category', 'date', 'include_as_expense']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(FinanceRecordForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        
