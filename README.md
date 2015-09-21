#Read me for OPS-CFGD repository
#Table of Contents
[toc]

##What is ops-cfgd?

The OVSDB database contains the running configuration of the switch. The ops-cfgd module is responsible for updating the OVSDB database with the startup configuration during system bootup.

##What is the structure of the repository?

* src/ops-cfgd/ contains the cfgd and cfgdbutil source code.
    * tests/ contains all the component tests

##What is the license?

N/A

##What other documents are available?

For the high level design of ops-cfgd, refer to [Config persistence design - TBL](DESIGN.md)
For Command Reference document of ops-cfgd, refer to [Config persistence Command Reference - TBL](CLI.md)

For general information about OpenSwitch project refer to http://www.openswitch.net
