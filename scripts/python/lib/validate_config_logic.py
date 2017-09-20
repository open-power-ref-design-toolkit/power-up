#!/usr/bin/env python
"""Config logic validation"""

# Copyright 2017 IBM Corp.
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import nested_scopes, generators, division, absolute_import, \
    with_statement, print_function, unicode_literals

import sys


class ValidateConfigLogic(object):
    """Config logic validation

    Args:
        log (object): Log
        config (object): Config
    """

    CONFIG_VERSION = 'v2.0'

    def __init__(self, log, config):
        self.log = log
        self.config = config

    def _validate_version(self):
        """Validate version

        Exception:
            If config version is not supported
        """

        if self.config.version != self.CONFIG_VERSION:
            try:
                raise Exception()
            except Exception:
                self.log.error(
                    'Config version %s is not supported' % self.config.version)
                sys.exit(1)

    def _validate_netmask_prefix(self):
        """Validate netmask and prefix

        The netmask or prefix needs to be specified, but not both.

        Exception:
            If both or neither the netmask and prefix are specified.
        """

        for element in (
                'deployer.networks.mgmt',
                'deployer.networks.external',
                'deployer.networks.client'):

            try:
                netmask = eval('self.config.' + element).netmask
            except AttributeError:
                netmask = None
            try:
                prefix = eval('self.config.' + element).prefix
            except AttributeError:
                prefix = None

            if netmask is None and prefix is None:
                try:
                    raise Exception()
                except Exception:
                    msg = "Either 'netmask' or 'prefix' needs to be specified"
                    self.log.error("%s - %s" % (element, msg))
                    sys.exit(1)
            if netmask is not None and prefix is not None:
                try:
                    raise Exception()
                except Exception:
                    msg = "Both 'netmask' and 'prefix' can not be specified"
                    self.log.error("%s - %s" % (element, msg))
                    sys.exit(1)

    def validate_config_logic(self):
        """Config logic validation"""

        self._validate_version()
        self._validate_netmask_prefix()
        self.log.info('Config logic validation completed successfully')