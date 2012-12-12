from setuptools import setup

setup(name='mezzanine-flexipage',
      version='0.1',
      description='',
      url='http://github.com/mrmagooey/flexipage',
      author='Peter Davis',
      author_email='peter.davis8@gmail.com',
      license='MIT',
      packages=['flexipage'],
      install_requires=[
          'mezzanine'
      ],
      include_package_data=True,
      package_data = {'flexipage':['*.html']},
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: "
                              "Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",],
      zip_safe=False)