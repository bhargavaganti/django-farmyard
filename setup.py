from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

#APP_NAME should be the module name as python sees it.
APP_NAME = 'farmyard'
DESCRIPTION = 'Collection of apps for a church website'
VERSION = __import__('farmyard').__version__
REQUIREMENTS = [
    'setuptools',
    'django==1.6.2',
    'django-extensions==1.3.3',
    'notes==0.3.0',
    'django-attributes==0.2.0',
    'django-filer==0.9.5',
    'django-localflavor==1.0',
    'django-zurb-foundation==5.1.1',
    'werkzeug==0.9.4',
    'python-dateutil==1.4.1',
    'django-uuidfield==0.5.0',
    'easy-thumbnails==1.4',
    'south==0.8.2',
]


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

setup(
    name=APP_NAME,
    version=VERSION,
    url='http://github.com/powellc/django-farmyard',
    license='BSD',
    platforms=['OS Independent'],
    description=DESCRIPTION,
    author='Colin Powell',
    author_email='info@timberwyckfarm.com',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
    tests_require=['tox'],
    cmdclass={'test': Tox},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    package_dir={
        'farmyard': 'farmyard',
    },
)
