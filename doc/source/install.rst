..
    Copyright 2012 Endre Karlson for Bouvet ASA

    Licensed under the Apache License, Version 2.0 (the "License"); you may
    not use this file except in compliance with the License. You may obtain
    a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.

.. _install:

========================
Install
========================

bufunfa is comprised of three components for more info on these please
consolidate :architecture:.

.. note::
    bufunfa makes extensive use of the messaging bus, but has not
    yet been tested with ZeroMQ. We recommend using Rabbit or qpid
    for now.


From Packages
+++++++++++++


From Source / GIT
+++++++++++++++++

Common steps
================

.. index::
    double: installing; rename_configs

.. note::
   The below operations should take place underneath your <project>/etc folder.

** Renaming configuration files is easy if you want to do it one by one then
   do::
   $ mv bufunfa-central.conf.sample bufunfa-central.conf

** You can also do it in one swoop::
   $ rename 's/\.sample$//' *.sample


Installing the Central
======================

.. index::
   double: installing; central

1. Clone the bufunfa repo off of github::
   $ cd /opt/stack
   $ git clone https://github.com/ekarlso/bufunfa.git

2. As a user with ``root`` permissions or ``sudo`` privileges, run the
   bufunfa installer::
   $ cd bufunfa
   $ sudo python setup.py install

3. See :rename_configs:

4. Configure the :term:`central` service

   Change the wanted configuration settings to match your environment
   ::
    $ vi bufunfa-central.conf

   Refer to :doc:`configuration` details on configuring the service.

5. Start the central service::
   $ bufunfa-central


Installing the Recorder
====================

.. index::
   double: installing; recorder


1. Clone the bufunfa repo off of github::
   $ cd /opt/stack
   $ git clone https://github.com/ekarlso/bufunfa.git

2. As a user with ``root`` permissions or ``sudo`` privileges, run the
   bufunfa installer::
   $ cd bufunfa
   $ sudo python setup.py install

3. See :rename_configs:

4. Configure the :term:`recorder` service

   Change the wanted configuration settings to match your environment
   ::
    $ vi bufunfa-recorder.conf

   Refer to :doc:`configuration` details on configuring the service.

5. Start the Recorder service::
   $ bufunfa-recorder


Installing the API
====================

.. index::
   double: installing; api

.. note::
   The API Server needs to able to talk to Keystone for AuthN + Z and
   communicates via MQ to other services.

1. Clone the bufunfa repo off of github::
   $ cd /opt/stack
   $ git clone https://github.com/ekarlso/bufunfa.git

2. As a user with ``root`` permissions or ``sudo`` privileges, run the
   bufunfa installer::
   $ cd bufunfa
   $ sudo python setup.py install

3. See :rename_configs:

4. Configure the :term:`api` service

   Change the wanted configuration settings to match your environment
   ::
    $ vi bufunfa-api.conf
    $ vi bufunfa-api-paste.ini

   Refer to :doc:`configuration` details on configuring the service.

5. Start the API service::
   $ bufunfa-api
