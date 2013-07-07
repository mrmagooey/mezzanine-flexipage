"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test.utils import override_settings
from django.template import Template
from django.forms import ModelForm
from django.db import models
from flexipage.utils import get_flexi_template, get_flexi_template_location,\
    get_template_variables, get_flexi_tags, get_flexi_forms, get_settings_forms,\
    get_flexi_form_tags

import flexipage
from flexipage.models import FlexiPage, FlexiContent

from flexipage.tests.test_flexi_app import models
from django.test import TestCase
from django.template.base import TemplateDoesNotExist
from django.conf import settings
from flexipage.page_processors import get_flexi_variables_context, get_flexi_forms_context
import os

# in case of emergency, break glass - makes interactive shell in execution
# import readline # optional, will allow Up/Down/History in the console
# import code
# vars = globals().copy()
# vars.update(locals())
# shell = code.InteractiveConsole(vars)
# shell.interact()

test_template_location = 'flexipage/tests/test.html'
flexipage_module_directory = flexipage.__path__[0]

@override_settings(FLEXI_TEMPLATES=('test',test_template_location))
class TestFlexiPage(TestCase):
    def setUp(self):
        pass
        
    def test_save_flexipage(self):
        "Tests that using the test template available new flexipages can be created"
        fp = FlexiPage()
        fp.title = 'some title here'
        fp.template_name = test_template_location
        fp.save()
        
        
    def test_save_flexipage_raise_error_on_no_template_name(self):
        "Tests that a FlexiPage without a template raises an error"
        fp = FlexiPage()
        fp.title = 'some title here'
        with self.assertRaises(AttributeError) as ex:
            fp.save()

    def test_check_for_flexicontent(self):
        "Tests the check_for_flexicontent method on the FlexiPage model"
        fp = FlexiPage()
        fp.title = 'some title here'
        fp.template_name = test_template_location
        fp.save()
        self.assertEqual(['flexi_second_variable'], fp.check_for_flexicontent())
        
    def test_update_flexicontent(self):
        "Test the update_flexicontent method"
        # check that it will create new FlexiContent items from the template
        fp = FlexiPage()
        fp.title = 'some title here'
        fp.template_name = test_template_location
        fp.save()
        flexi_contents = FlexiContent.objects.all()
        self.assertEqual(len(flexi_contents), 1)
        # add flexicontent to the template, check that this creates a new FlexiContent model
        test_html_location = os.path.join(flexipage_module_directory,
                                          'templates/flexipage/tests/test.html')
        with open(test_html_location, 'r') as original_test_html_file:
            original_html_string = original_test_html_file.read()
        with open(test_html_location, 'a') as test_html_file:
            test_html_file.write('\n {{ flexi_new_variable }} \n')
        fp.save()
        # Additional FlexiContent now fk'd to page model
        flexi_contents = FlexiContent.objects.all()
        self.assertEqual(len(flexi_contents), 2)
        # remove flexicontent item to return template to original format
        with open(test_html_location, 'w') as test_html_file_out:
            test_html_file_out.write(original_html_string)

    def test_flexipage_variables_context(self):
        """
        Tests that all flexicontent models fk'd to the page are 
        included in the page context even if no longer present in the template
        """
        fp = FlexiPage()
        fp.title = 'some title here'
        fp.template_name = test_template_location
        fp.save()
        flexi_contents = FlexiContent.objects.all()
        self.assertEqual(len(flexi_contents), 1)
        # add flexicontent to the template, check that this creates a new FlexiContent model
        test_html_location = os.path.join(flexipage_module_directory,
                                          'templates/flexipage/tests/test.html')
        with open(test_html_location, 'r') as original_test_html_file:
            original_html_string = original_test_html_file.read()
        with open(test_html_location, 'a') as test_html_file:
            test_html_file.write('\n {{ flexi_new_variable }} \n')
        fp.save()
        # Additional FlexiContent now fk'd to page model
        flexi_contents = FlexiContent.objects.all()
        self.assertEqual(len(flexi_contents), 2)
        # remove flexicontent item to return template to original format
        with open(test_html_location, 'w') as test_html_file_out:
            test_html_file_out.write(original_html_string)
        # The quantity of FlexiContent models stays the same
        flexi_contents = FlexiContent.objects.all()
        self.assertEqual(len(flexi_contents), 2)
        # And the flexi_new_variable variable is still in the template context
        self.assertIn('flexi_new_variable', get_flexi_variables_context(fp))
        
        
            
class TestFlexiAdmin(TestCase):
    def test_template_changes_reflected_in_admin(self):
        pass

        
@override_settings(FLEXI_TEMPLATES=('test',test_template_location))        
class TestFlexiForms(TestCase):
    def test_modelforms_render(self):
        pass

    def test_modelforms_save(self):
        pass

        
@override_settings(FLEXI_TEMPLATES=('test','tests/test.html'))
class TestFlexiFormView(TestCase):
    def test_context(self):
        pass
