from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from copy import deepcopy
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import  StackedDynamicInlineAdmin
from .models import FlexiPage, FlexiContent
from .utils import get_flexi_tags

flexi_page_fieldsets = ((None, {"fields":("template_name",)}),)

#http://stackoverflow.com/questions/442040/pre-populate-an-inline-formset
#http://stackoverflow.com/questions/2101979/django-admin-filter-objects-for-inline-formset
class FlexiContentInlineFormset(BaseInlineFormSet):
    def get_queryset(self):
        if not hasattr(self, '_queryset'):
            qs_all = super(FlexiContentInlineFormset, self).get_queryset()
            try:
                flexi_content = qs_all[0]
            except IndexError:
                return qs_all
            # Save the parent page to trigger its custom save function
            flexi_content.page.update_flexicontent()
            # Get the FlexiPages template tags
            tags = get_flexi_tags(flexi_content.page.template_name)
            # Return a queryset filtered by tags
            qs = qs_all.filter(name__in=tags)
            self._queryset = qs
        return self._queryset


class FlexiContentInline(StackedDynamicInlineAdmin):
    model = FlexiContent
    fk_name = 'page'
    formset = FlexiContentInlineFormset
    extra = 0
    
    class Media:
        js = ('js/admin/save_modelform_onchange.js',)
        

class FlexiPageAdmin(PageAdmin):
    inlines = (FlexiContentInline,)
    fields = ('')
    
admin.site.register(FlexiPage, FlexiPageAdmin)