import os

from django.template.loader import get_template
from django.template import VariableNode
from django.template.loader_tags import ExtendsNode
from django.conf import settings
from django.template.base import TemplateDoesNotExist

try:
    FLEXI_VARIABLE_PREFIX = settings.FLEXI_VARIABLE_PREFIX
except AttributeError:
    FLEXI_VARIABLE_PREFIX = 'flexi_'

try:
    FLEXI_FORM_VARIABLE_PREFIX = settings.FLEXI_FORM_VARIABLE_PREFIX
except AttributeError:
    FLEXI_FORM_VARIABLE_PREFIX = 'flexiform_'


def get_template_variables(nodes):
    """
    Given the nodes from a Django Template() object, function finds all VariableNode's
    in the current Template object and returns them as a list.

    Upon finding an ExtendsNode the function will also search that parent template
    specified for VariableNode's, continuing to do so recursively until no more
    ExtendsNode's have been found.
    """
    variables = []
    for node in nodes:
        if hasattr(node, 'nodelist'):
            var_nodes = node.nodelist.get_nodes_by_type(VariableNode)
        else:
            var_nodes = node.get_nodes_by_type(VariableNode)

        # There should only be a single ExtendsNode per template
        try:
            extend_node = node.get_nodes_by_type(ExtendsNode)[0]
        except IndexError:
            extend_node = None

        for vn in var_nodes:
            variables += [vn.filter_expression.var.var]

        if extend_node:
            parent_template_path = extend_node.parent_name.var
            try:
                parent_template = get_template(parent_template_path)
            except TemplateDoesNotExist:
                print 'couldn\'t find template: %s' % parent_template_path
                continue

            return variables + get_template_variables(parent_template.nodelist)

    return variables


def get_flexi_template(template_name):
    """
    A wrapper around Django's inbuilt get_template() function that searches for the
    `template_name` as it is given, and on failure prefixes the path with `flexipage`
    in case the user has forgotten to add this. If this prefixed path fails then
    a TemplateDoesNotExist exception is raised.
    """

    try:
        template = get_template(template_name)
    except TemplateDoesNotExist:
        template = get_template(os.path.join('flexipage', template_name))
    return template


def get_flexi_template_location(template_name):
    """
    Return the location of the template with template_name.
    """
    try:
        template_location = template_name
        get_template(template_location)
    except TemplateDoesNotExist:
        template_location = os.path.join('flexipage', template_name)
        get_template(template_location)

    return template_location


def get_flexi_form_tags(template_name):
    """
    Returns a list of django template variables strings from the template `template_name`
    that start with FLEXI_FORM_VARIABLE_PREFIX.
    """
    template = get_flexi_template(template_name)

    # Get VariableNodes and filter on FLEXI_FORM_VARIABLE_PREFIX
    ff_raw = [x for x in get_template_variables(template)
              if x.startswith(FLEXI_FORM_VARIABLE_PREFIX)]

    flexi_forms = []
    for ff in ff_raw:
        # Only interested in first part of the dot notation, i.e. the variable name
        if len(ff.split('.')) > 1:
            flexi_forms.append(ff.split('.')[0])
        else:
            flexi_forms.append(ff)

    return flexi_forms

def get_settings_forms():
    forms_dict = {}
    try:
        for form in settings.FLEXI_FORMS:
            form_path_components = form.split('.')[0:-1]
            base = '.'.join(form_path_components)
            # No module was specified with the Form name
            if base == '':
                raise ImportError
            class_name = form.split('.')[-1]
            forms_dict[class_name] = getattr(__import__(base, fromlist=[class_name]), class_name)
    except AttributeError: # no FLEXI_FORMS specified in settings
        pass
    return forms_dict

    
def get_flexi_forms(template_path):
    """
    Returns a dictionary of unbound forms as per flexi form variables found
    in the given template. Returns:

       {'name of flexi form variable': <uninstantiated class of form>, ...}

    """

    flexi_template_forms = get_flexi_form_tags(template_path)
    # strip the flexi prefix from the form to match the actual name of the model
    template_forms = [x[len(FLEXI_FORM_VARIABLE_PREFIX):] for x in flexi_template_forms]

    settings_forms = get_settings_forms()
    
    # Remove forms found in settings but not subsequently found within the template
    matched_forms = [x for x in settings_forms if x in template_forms]

    unbound_forms = {}
    for form in matched_forms:
        # Add flexi form prefix back to the name of the form,
        # otherwise the template won't recognise it
        form_name = FLEXI_FORM_VARIABLE_PREFIX + form
        unbound_forms[form_name] = settings_forms[form]
    return unbound_forms

def get_flexi_tags(template_name):
    """
    Takes a string representing the path to the template and returns a list of
    strings from the VariableNodes in the template `template_name` that start
    with FLEXI_VARIABLE_PREFIX.
    """

    template = get_flexi_template(template_name)

    # Filter VariableNodes by the FLEXI_VARIABLE_PREFIX
    ft_raw = [x for x in get_template_variables(template)
              if x.startswith(FLEXI_VARIABLE_PREFIX)]

    # Remove dot notation method/attribute lookups from the tag string, returning
    # just the tag name
    flexi_tags = []
    for ft in ft_raw:
        if len(ft.split('.')) > 1:
            flexi_tags.append(ft.split('.')[0])
        else:
            flexi_tags.append(ft)
    return flexi_tags





