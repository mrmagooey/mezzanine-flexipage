from django.shortcuts import render
from mezzanine.pages.page_processors import processor_for
from .models import FlexiPage
from .utils import get_flexi_template_location, get_flexi_forms

from django.conf import settings

try:
    FLEXI_PREFIX = settings.VARIABLE_PREFIX
except AttributeError:
    VARIABLE_PREFIX = 'flexi_'

try:
    FLEXI_FORMS = settings.FLEXI_FORMS
except AttributeError:
    FLEXI_FORMS = None

def get_flexi_variables_context(page):
    variables_context = {}
    variables_context['page'] = page
    # Get every FlexiContent model fk'd to the FlexiPage
    # TODO potentially should introspect the template and only retrieve FlexiContent models
    # that exist on the page rather than just getting everything fk'd to the page
    flexi_contents = page.flexipage.flexi_content.all()
    # Use the name of the FlexiContent and inject that into the context
    for fc in flexi_contents:
        variables_context[fc.name] = fc
    return variables_context
    
def get_flexi_forms_context(page):
    forms_context = {}
    template_path = get_flexi_template_location(page.flexipage.template_name)
    template_forms = get_flexi_forms(template_path)    
    for form_name, form_class in template_forms.iteritems():
        forms_context[form_name] = form_class(prefix=form_name)
    return forms_context
    
@processor_for(FlexiPage)
def flexi_page_view(request, page):
    # Get the template from the flexipage model, or raise exception    
    template_path = get_flexi_template_location(page.flexipage.template_name)
    if request.user.is_staff:
        # Calling save ensures that the FlexiContent models are created
        page.flexipage.save()
        
    variables_context = get_flexi_variables_context(page)
    forms_context = get_flexi_forms_context(page)
    
    if request.method == "POST":
        # Get all forms on the page
        # Check each form for integrity
        # If each form is_valid() then save everything
        # If a form fails validation, re-render all bound forms
        template_forms = get_flexi_forms(template_path)
        bound_forms_success = {}
        bound_forms_errors = {}
        for form_name, form_class in template_forms.iteritems():
            bound_form = form_class(request.POST, prefix=form_name)
            if bound_form.is_valid():
                bound_forms_success[form_name] = bound_form
                bound_form.save()
            else:
                bound_forms_errors[form_name] = bound_form

        # If there are errors, re-render with bound forms
        # If there are no errors
        #  1. Check each form for an flexi_intermediate() method
        #  1. re-render with success markings on forms
        if bound_forms_errors:
            context = dict(variables_context.items() +
                           bound_forms_success.items() + bound_forms_errors.items())
            return render(request, template_name=template_path, dictionary=context)
        else: # All forms saved successfully
            for form_name, form_class in bound_forms_success.iteritems():
                # Try calling the forms intermediate method
                if hasattr(form_class,'flexi_intermediate'):
                    return form_class.flexi_intermediate()
            # No flexi_intermediate methods found, render page as per normal GET request
            context = dict(variables_context.items() + forms_context.items())
            return render(request, template_name=template_path, dictionary=context)
            
    elif request.method == "GET":
        context = dict(variables_context.items() + forms_context.items())
        return render(request, template_name=template_path, dictionary=context)

