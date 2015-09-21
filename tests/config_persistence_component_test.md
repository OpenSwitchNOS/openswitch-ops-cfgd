Config Persistence Component Test Cases
=====
## Contents##
- [1. Test cases to verify Config Persistence daemon](#1.-test-cases-to-verify-config-persistence-daemon)
	- [1.01 Test to verify no configdb detection](#1.01-test-to-verify-no-configdb-detection)
	- [1.02 Test to verify configdb detection and connection](#1.02-test-to-verify-configdb-detection-and-connection)
	- [1.03 Test to verify configdb detect startup row](#1.03-test-to-verify-configdb-detect-startup-row)
	- [1.04 Test to verify configdb mark completion](#1.04-test-to-verify-configdb-mark-completion)
	- [1.05 Test to verify startup config push during boot](#1.05-test-to-verify-startup-config-push-during-boot)
- [Test cases to verify Config Persistence utility](#test-cases-to-verify-config-persistence-utility)
	- [2.01 Test to verify show startup configuration](#2.01-test-to-verify-show-startup-configuration)
	- [2.02 Test to verify delete startup configuration](#2.02-test-to-verify-delete-startup-configuration)
	- [2.03 Test to verify running configuration to startup configuration](#2.03-test-to-verify-running-configuration-to-startup-configuration)
	- [2.04 Test to verify startup configuration to running configuration](#2.04-test-to-verify-startup-configuration-to-running-configuration)

##1. Test cases to verify Config Persistence daemon ##
### Objective ###
Test cases to verify that configdb and working of cfgd daemon.
### Requirements ###
The requirements for this test case are:

 - AS5712 switch

### Setup ###
#### Topology Diagram ####
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+

### 1.01 Test to verify no configdb detection  ###
#### Description ####
Test to verify that config persistence daemon detect that configdb is not present and log correct error.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if "No rows found in the config table" error message is received.
#### Test Fail Criteria ####
Testcase result is fail if "No rows found in the config table" error message is not received.

### 1.02 Test to verify configdb detection and connection  ###
#### Description ####
Test to verify that config persistence daemon detect configdb and connect to db.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if cfgd is able to detect a empty configdb with no row present.
#### Test Fail Criteria ####
Testcase result is fail if cfgd is not able connect to configdb.


### 1.03 Test to verify configdb detect startup row  ###
#### Description ####
Test to verify that config persistence daemon detect startup row in configdb.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if "Config data found" message is received.
#### Test Fail Criteria ####
Testcase result is fail if  "Config data found" message is not received.


### 1.04 Test to verify configdb mark completion  ###
#### Description ####
Test to verify that config persistence daemon mark completion in configdb after pushing startup config to running config.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if cur_cfg and next_cfg in System table is greater than 1
#### Test Fail Criteria ####
Testcase result is fail if if cur_cfg and next_cfg in System table is zero or empty


### 1.05 Test to verify startup config push during boot ###
#### Description ####
Test to verify that config persistence daemon copy the startup config saved in configdb to the running db during boot up time. Save a startup config with hostname configured to "CT-TEST" and system is rebooted.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if the hostname in System table is "CT-TEST"
#### Test Fail Criteria ####
Testcase result is fail if  the hostname in System table is not "CT-TEST".


## Test cases to verify Config Persistence utility ##
### Objective ###
Test cases to verify that cfgdbutil perform copy configuration and show configuration correctly.
### Requirements ###
The requirements for this test case are:

 - AS5712 switch

### Setup ###
#### Topology Diagram ####
              +------------------+
              |                  |
              |  AS5712 switch   |
              |                  |
              +------------------+
#### Test Setup ####
### 2.01 Test to verify show startup configuration  ###
#### Description ####
Test to verify that config persistence utility to fetch startup configuration in JSON format from startup row in configdb. Save a dummy JSON string in startup row and execute show command, compare the output of show command and configured dummy JSON string are same.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if show command output match with JSON string configured during setup.
#### Test Fail Criteria ####
Testcase result is fail if show command output doesn't match with JSON string configured during setup.

### 2.02 Test to verify delete startup configuration ###
#### Description ###
Test to verify that config persistence utility to fetch startup row in configdb and delete it. Insert a dummy row with type = startup and execute delete command.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if show command output match with JSON string configured during setup.

#### Test Fail Criteria ####
Testcase result is fail if show command output doesn't match with JSON string configured during setup.

### 2.03 Test to verify running configuration to startup configuration ###
#### Description ###
Test to verify that config persistence utility copy the current system running configuration and save it in JSON format in startup row of configdb. Configure hostname as "CT-TEST" in running configuration and execute copy running configuration to startup configuration.
### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if the saved JSON string in startup row contain hostname key value as "CT-TEST" in System table.
#### Test Fail Criteria ####
Testcase result is fail if the saved JSON string in startup row doesn't contain hostname key value as "CT-TEST" in System table.

### 2.04 Test to verify startup configuration to running configuration###
#### Description ###
Test to verify that config persistence utility copy the saved JSON format configuration in startup row of configdb to current system running configuration. Save a startup JSON string in startup row with hostname configured to "CT-TEST" and execute copy startup config to running config.

### Test Result Criteria ###
#### Test Pass Criteria ####
Testcase result is success if "show running-config" command has hostname configured as "CT-TEST"

#### Test Fail Criteria ####
Testcase result is success if "show running-config" command has hostname not configured as "CT-TEST"
