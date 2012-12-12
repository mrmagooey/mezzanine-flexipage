
from django.core.management import setup_environ

import sys
import os

## For testing functions in this module ##
# sys.path = [os.path.dirname(\
#                             os.path.dirname(os.path.dirname\
#                                             (os.path.abspath(__file__))))] + sys.path
# sys.path = [os.path.dirname(os.path.dirname\
#                             (os.path.abspath(__file__)))] + sys.path

# from oddsocks import settings

# setup_environ(settings)

from django.template.loader import get_template
from django.template import VariableNode
from django.template.loader_tags import ExtendsNode
from django.conf import settings
from django.template.base import TemplateDoesNotExist


try:
    FLEXI_PREFIX = settings.VARIABLE_PREFIX
except AttributeError:
    FLEXI_PREFIX = 'flexi_'

def get_flexi_template(template_name):
    try:
        template = get_template(template_name)
    except TemplateDoesNotExist:
        template = get_template(os.path.join('flexipage', template_name))
    return template

def get_flexi_template_location(template_name):
    try:
        template_location = template_name        
        get_template(template_location)
    except TemplateDoesNotExist:
        template_location = os.path.join('flexipage', template_name)
        get_template(template_location)
                                         
    return template_location
    
def get_flexi_tags(template_name):
    template = get_flexi_template(template_name)
    ft_raw = [x for x in get_template_variables(template)
              if x.startswith(FLEXI_PREFIX)]
    
    flexi_tags = []
    for ft in ft_raw:
        if len(ft.split('.')) > 1:
            flexi_tags.append(ft.split('.')[0])
        else:
            flexi_tags.append(ft)
    print 'get_flexi_tags(): flexi tags', flexi_tags
    return flexi_tags
    
def get_template_variables(nodes):
    variables = []    
    for node in nodes:
        # Check if its a nodelist rather than a single node
        # TODO check if a VariableNode can have a nodelist
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




