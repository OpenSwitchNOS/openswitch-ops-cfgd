High level design of OPS-CFGD
============================
## Contents##
- [cfgd daemon](#cfgd-daemon)
- [cfgdbutils](#cfgdbutils)


cfgd daemon
=========

cfgd is a daemon process started during the switch bootup. It is responsible for pushing persistent startup configuration to OVSDB and notify all other daemons waiting for configuration to be available.

Responsibilities
---------------
cfgd daemon is responsible for pushing persistent startup configuration into the OVSDB and update the state (cur_cfg).

After the platform daemons have discovered all of the hardware present and populated the OVSDB with the relevant information for the hardware, cfgd checks if any saved configuration exists and checks for configuration of type startup. If a startup configuration is found it is applied over the rest of the tables.

Design choices
--------------
N/A

Relationships to external OpenSwitch entities
---------------------------------------------

			+---------------------+
			|                     |
			|        CLI          |
			+---------------------+
                        |
                        |
			+-----------v--------------------------------------+
			|        Config persistence utility                |
			|                                                  |
			+--------------------------------------------------+
                        |                               |
                        |                               |
			+-----------v----------------------+        |
			|      REST API                    |        |
			|                                  |        |
			+----------------------------------+        |
                        |                               |
                        |                               |
                        |                               |
			+-----------v----------------------+  +-----v------------------+
			| +----------------+     OVSDB     |  | +---------+            |
			| |   Running      |               |  | |startup  |   Configdb |
			| |   Config       |               |  | |Config   |            |
			| +----------------+               |  | +---------+            |
			+----------------------------------+  +------------------------+


Startup configuration is present in the file config.db which is currently located (on a running system) at /var/local/openvswitch.

The running configuration is present in ovsdb.db file currently located (on a running system) at /var/run/openvswitch.



OVSDB-Schema
------------
N/A

Internal structure
------------------
cfgd is implemented using one API libraries:

1. Configuration Read/Write API: These APIs perform conversion between the startup configuration in JSON format and the running configuration in the form of OVSDB tables described in vswitchd.extschema

cfgd uses the dispatcher design concept to perform it's operations. The basic flow is as follows:

1) Create the idl object and call idl.run() until idl is in sync with the running config db

2) dispatcher: This calls the next function in a function table, to allow sequencing of functionality.If the function returns True, the function pointer is incremented to call the next function during the next loop. If the function returns False, the function pointer is not incremented and the same function is called again.

The function table contains (in the following order):

	        - wait_for_hw_done: This function returns False (after small sleep) until open_vswitch:cur_hw is > 0. cfgd is not supposed to push the user config until after all h/w initialization has completed by the platform daemons

	        - push_cfg_to_db: If save_config is not None, this function will push the configuration to ovsdb.

	        - mark_completion: Sets open_vswitch:cur_cfg > 0. Protocol daemons are not supposed to start processing until after the user configuration (if exists) has been pushed. This value being > 0 indicates that system config (h/w and user config) has completed.

	        - terminate: sets global variable exiting to True


cfgdbutils
=========

cfgdbutil commands for performing operations like copy the startup configuration to running configuration and vice versa, show startup configuration for use by CLI applications.

Responsibilities
---------------
cfgdbutil is responsible for providing  command for show, copy and delete startup configuration from configdb.

CLI calls cfgdbutil to perform "show startup-config", "copy startup-config running-config" and "copy running-conig startup-config" command.

Design choices
--------------
N/A

Relationships to external OpenSwitch entities
---------------------------------------------

			+---------------------+
			|                     |
			|        CLI          |
			+---------------------+
                        |
                        |
			+-----------v--------------------------------------+
			|        Config persistence utility                |
			|                                                  |
			+--------------------------------------------------+
                        |                               |
                        |                               |
			+-----------v----------------------+        |
			|      REST API                    |        |
			|                                  |        |
			+----------------------------------+        |
                        |                               |
                        |                               |
                        |                               |
			+-----------v----------------------+  +-----v------------------+
			| +----------------+     OVSDB     |  | +---------+            |
			| |   Running      |               |  | |startup  |   Configdb |
			| |   Config       |               |  | |Config   |            |
			| +----------------+               |  | +---------+            |
			+----------------------------------+  +------------------------+

Internal structure
------------------
cfgdbutil is implemented using two API libraries:

1. Configuration Read/Write API: These APIs perform conversion between the startup configuration in JSON format and the running configuration in the form of OVSDB tables described in vswitchd.extschema

2. cfgdb library : These APIs perform insert, update startup row and create idl object with configdb config tables described in configdb.ovsschema.

cfgdbutil uses the argument design concept to perform it's operations. The basic flow is as follows:

1) cfgdbutil take operation to be performed like show, copy and delete as arguments.

2) Create the idl object and call idl.run() until idl is in sync with the running config db


###The commands supported by cfgdbutil:

### 1) show startup-config:
This command fetches the startup config stored in configdb in JSON format and show it in console.

### 2) copy startup-config running-config:
This command is used to copy the content of startup configuration to current system running configuration.
### 3) copy running-conig startup-config:
This command is used to copy the content of current system running configuration to startup configuration.

###4) delete startup-config:
This command deletes the row withe type=startup from configdb.

References
----------
