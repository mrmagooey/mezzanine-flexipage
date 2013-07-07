from django.db import models
from django.forms import ModelForm, Form
from django.shortcuts import redirect

class FlexiModelForm(ModelForm):
    def flexi_nothing(self):
        return ''

    def flexi_intermediate(self):
        """
        To be implemented when POSTed forms need to redirect to another url on success.
        e.g. return redirect('/thanks/')
        """
        pass

        
class FlexiForm(Form):
    def __init__(self, *args, **kwargs):
        if not getattr(self, 'save', False):
            raise Exception("You need to implement a save() method on your FlexiForm derived model")
        super(Form,self).__init__(*args, **kwargs)            
            
    def flexi_nothing(self):
        return ''

    def flexi_intermediate(self):
        """
        To be implemented when POSTed forms need to redirect to another url on success.
        e.g. return redirect('/thanks/')
        """
        pass
        
        
