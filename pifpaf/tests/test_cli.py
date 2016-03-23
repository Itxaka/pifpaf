# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess

import testtools


class TestCli(testtools.TestCase):

    def test_cli(self):
        self.assertEqual(0, os.system(
            "pifpaf run memcached --port 11214 echo >/dev/null 2>&1"))

    def test_eval(self):
        c = subprocess.Popen(["pifpaf", "run", "memcached", "--port", "11215"],
                             stdout=subprocess.PIPE)

        env = {}
        for line in c.stdout.readlines():
            k, _, v = line.partition("=")
            env[k] = v

        self.assertEqual("memcached://localhost:11215\n",
                         env["PIFPAF_URL"])
        self.assertEqual("memcached://localhost:11215\n",
                         env["PIFPAF_MEMCACHED_URL"])
        self.assertIn("PIFPAF_PID", env)
        self.assertEqual(0, c.wait())
