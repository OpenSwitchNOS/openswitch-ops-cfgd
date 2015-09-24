"""
Copyright (C) 2015 Hewlett Packard Enterprise Development LP
All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

#!/usr/bin/python

import os
import sys
import time
import pytest
import subprocess
import json
from halonvsi.docker import *
from halonvsi.halon import *

class cfgdbUtilTests( HalonTest ):

  def setupNet(self):
    # if you override this function, make sure to
    # either pass getNodeOpts() into hopts/sopts of the topology that
    # you build or into addHost/addSwitch calls
    self.net = Mininet(topo=SingleSwitchTopo(
      k=1,
      hopts=self.getHostOpts(),
      sopts=self.getSwitchOpts()),
      switch=HalonSwitch,
      host=HalonHost,
      link=HalonLink, controller=None,
      build=True)

  def cfgdbutils_delete_command(self):
    info('\n########## Test cfgdbutils delete commands ##########')
    s1 = self.net.switches[ 0 ]

    info('\n### Delete startup config saved in configdb ###')

    # Note: I have to use the extra "echo" command to flush out
    #       the buffer
    output = s1.cmd("cfgdbutil delete startup-config")
    output += s1.cmd("echo")
    debug(output)

    if 'success' in output:
      info('\n### Passed: Delete startup configuration ###')
    else:
      assert ('success' in out), \
            "Failed: Delete startup configuration"

  def cfgdbutils_show_command(self):
    info('\n########## Test cfgdbutils show commands ##########')

    s1 = self.net.switches[ 0 ]

    # Note: I have to use the extra "end" CLI command to flush out
    #       the buffer.
    s1.cmdCLI("configure terminal")
    s1.cmdCLI("lldp holdtime 9")
    s1.cmdCLI("radius-server host 1.1.1.1")
    s1.cmdCLI("exit")
    s1.cmdCLI("copy running-config startup-config")
    output = s1.cmdCLI("show startup-config")
    output += s1.cmdCLI("end")

    if "lldp holdtime 9" in output and "radius-server host 1.1.1.1" in output:
      info('\n### Passed: Fetch startup configuration success ###')
    else:
      assert ("lldp holdtime 9" in output and "radius-server host 1.1.1.1" in output), \
           "Failed: To fetch startup configuration"

  def cfgdbutils_copy_running_startup(self):
    info('\n########## Test copy running to startup config ##########')

    s1 = self.net.switches[ 0 ]

    # Change hostname as CT-TEST in running db and copy the running
    # config to startup config and verify in show startup config has
    # hostname as CT-TEST.
    s1.cmdCLI("configure terminal")
    s1.cmdCLI("hostname CT-TEST")
    s1.cmdCLI("exit")
    s1.cmdCLI("copy running-config startup-config")

    output = s1.cmdCLI("show startup-config")
    output += s1.cmdCLI("end")

    if "CT-TEST" in output:
      info('\n### Passed: copy running to startup configuration ###')
    else:
      assert ("CT-TEST" in output), \
           "Failed: copy running to startup configuration"

  def cfgdbutils_copy_startup_running(self):
    info('\n########## Test copy startup to running config ##########')

    s1 = self.net.switches[ 0 ]

    # Add one more radius server in running db and copy the startup
    # configuration to running config and verify in show running config
    # that hostname is again changed to CT-TEST.
    s1.cmdCLI("configure terminal")
    s1.cmdCLI("radius-server host 2.2.2.2")
    s1.cmdCLI("exit")
    s1.cmdCLI("copy startup-config  running-config")

    output = s1.cmdCLI("show running-config")
    output += s1.cmdCLI("end")

    if "radius-server host 2.2.2.2" not in output:
      info('\n### Passed: copy startup to running configuration ###\n')
    else:
      assert ("radius-server host 2.2.2.2" not in output), \
           "Failed: copy startup to running configuration"

class Test_cfgdbutil:
  def setup(self):
    pass

  def teardown(self):
    pass

  def setup_class(cls):
    Test_cfgdbutil.test = cfgdbUtilTests()
    pass

  def teardown_class(cls):
    # Stop the Docker containers, and
    # mininet topology
    Test_cfgdbutil.test.net.stop()

  def setup_method(self, method):
    pass

  def teardown_method(self, method):
    pass

  def __del__(self):
    del self.test

  # Show command tests.
  def test_show_config_commands(self):
    self.test.cfgdbutils_show_command()

  # Delete command tests.
  def test_delete_config_commands(self):
      self.test.cfgdbutils_delete_command()

  # Copy running to startup config tests.
  def test_cfgdbutils_copy_running_startup(self):
      self.test.cfgdbutils_copy_running_startup()

  # Copy startup to  running config tests.
  def test_cfgdbutils_copy_startup_running(self):
      self.test.cfgdbutils_copy_startup_running()
