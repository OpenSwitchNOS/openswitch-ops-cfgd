OPS-CFGD
=====

What is ops-cfgd?
----------------

ops-cfgd is a module responsible for pushing startup configuration of the switch into the OVSDB which contains the running configuration of the switch.

What is the structure of the repository?
----------------------------------------
* src/ops-cfgd/ contains the cfgd and cfgdbutil source code.
	* tests/ contains all the component tests
	* doc/ contains documentation
* src/ops-restd/runconfig contains the source code of the configuration read-write APIs which are used by cfgd and cfgdbutil
* src/ops-cli/vtysh contains the CLI code for copy operations between running configuration and startup configuration.

What is the license?
--------------------
N/A

What other documents are available?
-----------------------------------
DESIGN-cfgd.md: Contains the high level design


For general information about OpenSwitch project refer to http://www.openswitch.net
