# -*- encoding: utf-8 -*-
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
import abc
from bufunfa.plugin import Plugin


class StorageEngine(Plugin):
    """
    Base class for storage engines
    """

    __plugin_type__ = 'storage'

    @abc.abstractmethod
    def get_connection(self, conf):
        """
        Return a Connection instance based on the configuration settings.
        """


class Connection(object):
    """
    A Connection
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, conf):
        """
        Constructor...
        """

    @abc.abstractmethod
    def add_rate(self, context, values):
        """
        Add a new rate
        """

    @abc.abstractmethod
    def get_rates(self, context):
        """
        Get all rates
        """

    @abc.abstractmethod
    def update_rate(self, context, rate_id, values):
        """
        Update a rate
        """

    @abc.abstractmethod
    def delete_rate(self, context, rate_id):
        """
        Delete a rate
        """
