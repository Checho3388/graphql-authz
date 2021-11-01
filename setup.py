#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ["casbin==1.9.3"]

test_requirements = ['pytest>=3', ]

setup(
    author="Ezequiel Grondona",
    author_email='ezequiel.grondona@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Authorization middleware for GraphQL.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='graphql',
    name='graphql-authz',
    packages=find_packages(include=['authz', 'authz.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Checho3388/graphql_authz',
    version='0.1.0',
    zip_safe=False,
)
