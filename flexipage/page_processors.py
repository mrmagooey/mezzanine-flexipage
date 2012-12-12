from django.shortcuts import render
from mezzanine.pages.page_processors import processor_for
from .models import FlexiPage
from .utils import get_flexi_template_location
import os

from django.conf import settings

try:
    FLEXI_PREFIX = settings.VARIABLE_PREFIX
except AttributeError:
    VARIABLE_PREFIX = 'flexi_'


    
@processor_for(FlexiPage)
def flexi_page_view(request, page):
    if request.user.is_staff:
        # Calling save ensures that the FlexiContent models are created
        page.flexipage.save()
    
    # Get the template from the flexipage model, or raise exception
    template_path = get_flexi_template_location(page.flexipage.template_name)
    
    context = {}
    # Get every FlexiContent model fk'd to the FlexiPage
    flexi_contents = page.flexipage.flexi_content.all()
    # Use the name of the FlexiContent and inject that into the FlexiPage context

    for fc in flexi_contents:
        context[fc.name] = fc
    
    # TODO add in metadata context
    return render(request, template_name=template_path, dictionary=context)
    
