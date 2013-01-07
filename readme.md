# mezzanine-flexipage

## Overview
Mezzanine-flexipage is an extension to the Mezzanine Content Management Platform designed to make it easy for template designers to add and remove content areas simply by adding or removing variables from a template.

In practice, this means that someone without knowledge of Mezzanine (or Django/Python) can create templates with an arbitrary number of content fields purely by specifying those content fields in the template and without needing to manually create the corresponding model or alter the context being provided to the template.

At its heart this application is merely a Page model (named FlexiPage) with a RichContent Model foreign keyed to it (named FlexiContent). The value in the application comes from the view and Django admin logic which generates and displays the correct FlexiContent model by introspecting the template for which the context is being generated for.

## Installation

Install the current version off PyPi:

    pip install mezzanine-flexipage

In your ``settings.py`` file, install flexipages;

    INSTALLED_APPS = (
        'django.contrib.admin',
        ...
        'flexipage', # Add the flexipage app
    )

Then tell mezzanine-flexipage what your flexi templates are (start.html comes with the package):     

     FLEXI_TEMPLATES = (
         ('start.html','start'),
     )

Add the mezzanine-flexipage database tables.

    python manage.py syncdb

The option to create Flexi Pages will now be available in the admin site from the Pages page.

## Template Introspection

In order to change the number of content areas, add or remove variables starting with ``flexi_`` from the template itself. Mezzanine-flexipage will then introspect the template and create or remove Rich Text Areas from so that the variables on the page are supported by models created in the database.  The admin will then reflect these changes and whilst logged in with ``staff`` privileges the changes will update on the site proper by refreshing the page.

For example, to add an additional field to the page:

    {{ flexi_new_content_area }}

... and to have the same content editable on the page wrap it in mezzanine's ``editable`` template tag:

    {% editable flexi_new_content_area.content %}
     {{ flexi_new_content_area.content|richtext_filter|safe }}
    {% endeditable %}

This can be repeated with an arbitrary number of variables (ensuring the prefix ``flexi_`` for each variable).

## Installation from scratch (new mezzanine app)

Assuming you are using virtualenvwrapper, first install mezzanine-flexipage (this will install all dependencies).

    mkvirtualenv mezzanine-flexipage
    pip install mezzanine-flexipage
    
Create a mezzanine project:

    mezzanine-project myproject
    cd myproject


In your ``settings.py`` file, install flexipages;

    INSTALLED_APPS = (
        'django.contrib.admin',
        ...
        'flexipage', # Add the flexipage app
    )

Then tell mezzanine-flexipage what your flexi templates are (start.html comes with the package):     

     FLEXI_TEMPLATES = (
         ('start.html','start'),
     )
    
Where the first string denotes the name of the template file and the second string denotes how the template will be displayed in the admin. 
    
Create your database (sqlite by default, as specified in ``local_settings.py``), using:

    python manage.py createdb

...and follow the prompts.

Finally, create a local copy of the Mezzanine templates, which will also copy over ``start.html`` specified earlier in ``FLEXI_TEMPLATES``:

    python manage.py collecttemplates

Run the mezzanine application with: 

    python manage.py runserver

Login to the admin site and within the ``Pages`` page, click the dropdown at the top marked "Add..." and select Flexi Page. This will take you to the ``Add Flexi Page`` page.

Add a title to the new page and select 'start' from the template name dropdown. This will refresh the page with the correct Flexi Content rich content items, and enable you to add content as desired. This will now allow you to add and remove rich content variables via the template.

Refer to the section under Template Introspection for more information.

## Todo
* Show all relevant FlexiContent elements in the admin without needing to save a FlexiPage model.
* Include the ability to automatically scan the flexi\pages directory and pickup all templates in the directory, removing the need to put FLEXI\_TEMPLATES in settings
 
