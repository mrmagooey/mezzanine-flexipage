from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import RichTextField
from django.conf import settings
from .utils import get_flexi_tags
from django.utils.translation import ugettext, ugettext_lazy as _


try:
    TEMPLATE_CHOICES = settings.FLEXI_TEMPLATES
except AttributeError:
    raise Exception("FLEXI_TEMPLATES not set in settings")

    
class FlexiPage(Page):
    template_name = models.CharField(max_length=100, choices=TEMPLATE_CHOICES)

    def check_for_flexicontent(self):
        flexi_tags = get_flexi_tags(self.template_name)
        if len(flexi_tags) == 0:
            return False
    
    def update_flexicontent(self):
        flexi_tags = get_flexi_tags(self.template_name)
        print 'update_flexicontent()'
        print self.template_name
        # For each flexi tag, check if a FlexiContent already exists with that name
        for ft in flexi_tags:
            try:
                FlexiContent.objects.get(name=ft)
            except FlexiContent.DoesNotExist:
                f = FlexiContent()
                f.name = ft
                f.page = self
                f.save()
    
    def save(self, *args, **kwargs):
        # Need to ignore the fact that there is no title when users
        # change the template name in the admin
        super(FlexiPage, self).save(*args, **kwargs)
        self.update_flexicontent()

    class Meta:
        verbose_name = "Flexi Page"

        
class FlexiContent(models.Model):
    name = models.CharField(max_length=50)
    page = models.ForeignKey("FlexiPage", related_name='flexi_content')

    content = RichTextField(_("Content"), blank=True)

    search_fields = ("content",)

    def __unicode__(self):
        return self.name


