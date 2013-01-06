"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_templates_identified(self):
        pass
        
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

        
class UtilsTest(TestCase):
    def test_get_flexi_template(self):
        pass
        
class FlexiPageTest(TestCase):
    
    
    def test_templates_available(self):
        pass

class FormsTest(TestCase):
    def test_modelforms_render(self):
        pass

    def test_modelforms_save(self):
        pass
        
