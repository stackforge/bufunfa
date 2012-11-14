#!onsusr/bin/env python
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

from bufunfa.openstack.common import setup as common_setup
from bufunfa.version import version_info as version

install_requires = common_setup.parse_requirements(['tools/pip-requires'])
install_options = common_setup.parse_requirements(['tools/pip-options'])
tests_require = common_setup.parse_requirements(['tools/test-requires'])
setup_require = common_setup.parse_requirements(['tools/setup-requires'])
dependency_links = common_setup.parse_dependency_links([
    'tools/pip-requires',
    'tools/pip-options',
    'tools/test-requires',
    'tools/setup-requires'
])

setup(
    name='bufunfa',
    version=version.canonical_version_string(always=True),
    description='Billing as a Service',
    author='Endre Karlson',
    author_email='endre.karlson@bouvet.no',
    url='https://launchpad.net/bufunfa',
    packages=find_packages(exclude=['bin']),
    include_package_data=True,
    test_suite='nose.collector',
    setup_requires=setup_require,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'optional': install_options,
    },
    dependency_links=dependency_links,
    scripts=[
        'bin/bufunfa-api',
        'bin/bufunfa-central',
        'bin/bufunfa-sync',
        'bin/bufunfa-recorder'
    ],
    cmdclass=common_setup.get_cmdclass(),
    entry_points=textwrap.dedent("""
        [bufunfa.storage]
        mongodb = bufunfa.storage.impl_mongodb:MongoDBStorage
        mysql = bufunfa.storage.impl_sqlalchemy:SQLAlchemyStorage
        postgresql = bufunfa.storage.impl_sqlalchemy:SQLAlchemyStorage
        sqlite = bufunfa.storage.impl_sqlalchemy:SQLAlchemyStorage
        [bufunfa.recorder]
        ceilometer = bufunfa.recorder.impl_ceilometer:RecordEngine
        """),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Finance :: Billing Service',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: OpenStack',
    ]
)
