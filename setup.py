#!/usr/bin/env python
# Copyright 2012 Bouvet ASA
#
# Author: Endre Karlson <endre.karlson@bouvet.no>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from setuptools import setup, find_packages
import textwrap

from billistix.openstack.common import setup as common_setup

install_requires = common_setup.parse_requirements(['tools/pip-requires'])
tests_require = common_setup.parse_requirements(['tools/test-requires'])
setup_require = common_setup.parse_requirements(['tools/setup-requires'])
dependency_links = common_setup.parse_dependency_links([
    'tools/pip-requires',
    'tools/test-requires',
    'tools/setup-requires'
])

version = '0.1'

setup(
    name='billistix',
    version=version,
    description='Billing as a Service',
    author='Endre Karlson',
    author_email='endre.karlson@bouvet.no',
    url='https://launchpad.net/billistix',
    packages=find_packages(exclude=['bin']),
    include_package_data=True,
    test_suite='nose.collector',
    setup_requires=setup_require,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    dependency_links=dependency_links,
    scripts=[
        'bin/billistix-api',
        'bin/billistix-central',
        'bin/billistix-sync',
        'bin/billistix-meter-sync'
    ],
    cmdclass=common_setup.get_cmdclass(),
    entry_points=textwrap.dedent("""
        [billistix.storage]
        mongodb = billistix.storage.impl_mongodb:MongoDBStorage
        mysql = billistix.storage.impl_sqlalchemy:SQLAlchemyStorage
        postgresql = billistix.storage.impl_sqlalchemy:SQLAlchemyStorage
        sqlite = billistix.storage.impl_sqlalchemy:SQLAlchemyStorage
        """)
)
