#High level design of OPS-CFGD
##Table of Contents
- [cfgd daemon](#cfgd-daemon)
- [cfgdbutils](#cfgdbutils)


##CFGD Daemon
###Feature Description

cfgd daemon process is started by the systemd when the switch boots up. cfgd daemon is responsible for updating persistent startup configuration to OVSDB database and notify all other daemons waiting for configuration to be available.

###Responsibilities

cfgd daemon is responsible for updating persistent startup configuration into the OVSDB database and update the state (cur_cfg) in OVSDB database.

During initilization, the platform daemons discover all of the hardware present and populate the OVSDB database with the hardware related information.
The cfgd daemon checks if any saved configuration exists with type as "startup". If a startup configuration is available, it is applied to all the tables in the OVSDB database.

###Design choices

N/A

###Relationships to external OpenSwitch entities

```ditaa
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
```
The startup configuration is stored in the OVS database file located at "/var/local/openvswitch/config.db".
The running configuration is present in ovsdb.db file currently located (on a running system) at "/var/run/openvswitch".

###OVSDB-Schema

N/A

###Internal structure

cfgd is implemented using the API library:

1. Configuration Read/Write API: These APIs perform conversion between the startup configuration in JSON format and the running configuration in the form of OVSDB tables described in vswitchd.extschema

cfgd daemon uses the dispatcher design concept to perform it's operations. The basic flow is as follows:

1) Create the idl object and call idl.run() until idl is in sync with the running config db

2) dispatcher: This calls the next function in a function table, to allow sequencing of functionality.If the function returns True, the function pointer is incremented to call the next function during the next loop. If the function returns False, the function pointer is not incremented and the same function is executed again.

The function table contains (in the following order):

- wait_for_hw_done: This function returns False (after small sleep) until open_vswitch:cur_hw is > 0. cfgd is not supposed to push the user config until after all h/w initialization has completed by the platform daemons

- push_cfg_to_db: If save_config is not None, this function will push the configuration to ovsdb.

- mark_completion: Sets open_vswitch:cur_cfg > 0. Protocol daemons are not supposed to start processing until after the user configuration (if exists) has been pushed. This value being > 0 indicates that system config (h/w and user config) has completed.

- terminate: Sets global variable exiting to True


##cfgdbutils

###Feature Description

cfgdbutil is a python utility for performing operations like copy the startup configuration to running configuration and vice versa, show startup configuration for use by CLI applications.

###Responsibilities

cfgdbutil is responsible for providing  command for show, copy and delete startup configuration from configdb.

CLI calls cfgdbutil to perform "show startup-config", "copy startup-config running-config" and "copy running-conig startup-config" command.

###Design choices

N/A

###Relationships to external OpenSwitch entities
```ditaa

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
```

###Internal structure

cfgdbutil is implemented using two API libraries:

1. Configuration Read/Write API library: These APIs perform conversion between the startup configuration in JSON format and the running configuration in the form of OVSDB tables described in vswitchd.extschema

2. cfgdb API library : These APIs perform insert, update startup row and create idl object with configdb config tables described in configdb.ovsschema.

cfgdbutil uses the argument design concept to perform it's operations. The basic flow is as follows:

1) cfgdbutil take operation to be performed like show, copy and delete as arguments.

2) Create the idl object and call idl.run() until idl is in sync with the running config db


###The commands supported by cfgdbutil

#### Show startup-config
This command fetches the startup configuration stored in the configdb in JSON format and show it in console.

#### Copy startup-config running-config
This command is used to copy the content of startup configuration to current system's running configuration.
#### Copy running-conig startup-config
This command is used to copy the content of current system's running configuration to startup configuration.

#### Delete startup-config
This command deletes the row with "type=startup" from configdb.

##References
For Command Reference document of ops-cfgd, refer to [Config persistence Command Reference - TBL](CLI.md)
