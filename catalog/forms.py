from django.forms import ModelForm
from django import forms

from catalog.models import BuyingModel
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BuyingModelForm(ModelForm):
    def clean_meat_num(self):
       data = self.cleaned_data['meat_num']
       if data < 0:
           raise ValidationError(_('訂購數量不可小於0'))
       # Remember to always return the cleaned data.
       return data

    def clean_vege_num(self):
       data = self.cleaned_data['vege_num']
       if data < 0:
           raise ValidationError(_('訂購數量不可小於0'))
       # Remember to always return the cleaned data.
       return data

    def clean(self):
        cleaned_data = super().clean()
        meat_num = cleaned_data.get('meat_num')
        vege_num = cleaned_data.get('vege_num')

        if meat_num == 0 and vege_num == 0:
            raise ValidationError(_('葷食便當數量和素食便當數量不能皆為0'))

    class Meta:
        model = BuyingModel
        fields = ['customer_name', 'customer_phone', 'meat_num', 'vege_num']
        labels = {'customer_name': _('訂購人'), 'customer_phone': _('電話'), 
                   'meat_num': _('葷食便當數量'), 'vege_num': _('素食便當數量'), }
        #help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
        help_texts = {'customer_name': _(''), 'customer_phone': _(''), 
                   'meat_num': _(''), 'vege_num': _(''), }

class CheckOrderForm(forms.Form):
    phone = forms.CharField(max_length=10, help_text='請輸入欲查詢之電話')