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

from flexipage.models import FlexiPage

from flexipage.tests.test_flexi_app import models
from django.test import TestCase

from django.template.base import TemplateDoesNotExist

test_template_location = 'tests/test.html'

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
        
            
class TestFlexiAdmin(TestCase):
    def test_template_changes_reflected_in_admin(self):
        pass

        
class TestFlexiForms(TestCase):
    def test_modelforms_render(self):
        pass

    def test_modelforms_save(self):
        pass

        
@override_settings(FLEXI_TEMPLATES=('test','tests/test.html'))
class TestFlexiFormView(TestCase):
    def test_context(self):
        pass
