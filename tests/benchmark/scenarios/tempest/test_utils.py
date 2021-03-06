# Copyright 2014: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from rally.benchmark.scenarios.tempest import tempest
from rally.benchmark.scenarios.tempest import utils
from tests import test

TS = "rally.benchmark.scenarios.tempest"


class TempestLogWrappersTestCase(test.TestCase):

    def setUp(self):
        super(TempestLogWrappersTestCase, self).setUp()
        verifier = mock.MagicMock()
        verifier.parse_results.return_value = ({"fake": True},
                                               {"have_results": True})

        context = {"tmp_results_dir": "/tmp/dir", "verifier": verifier}
        self.scenario = tempest.TempestScenario(context)
        self.scenario._add_atomic_actions = mock.MagicMock()

    @mock.patch(TS + ".utils.tempfile")
    def test_launch_without_specified_log_file(self, mock_tmp):
        mock_tmp.NamedTemporaryFile().name = "tmp_file"
        target_func = mock.MagicMock()
        func = utils.tempest_log_wrapper(target_func)

        func(self.scenario)

        target_func.assert_called_once_with(self.scenario,
                                            log_file="/tmp/dir/tmp_file")

    @mock.patch(TS + ".utils.tempfile")
    def test_launch_with_specified_log_file(self, mock_tmp):
        target_func = mock.MagicMock()
        func = utils.tempest_log_wrapper(target_func)

        func(self.scenario, log_file='log_file')

        target_func.assert_called_once_with(self.scenario,
                                            log_file="log_file")
        self.assertEqual(0, mock_tmp.NamedTemporaryFile.call_count)
