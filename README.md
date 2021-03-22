<!--
SPDX-FileCopyrightText: Magenta ApS

SPDX-License-Identifier: MPL-2.0
-->

# OS2mo HTTP Trigger SDTool

This repository contains an OS2mo HTTP Trigger receiver for SDTool.

The receiver will register itself to listen for the refresh event on orgunits.
Upon receiving a refresh event, it will query SD for information about the orgunit
using the UUID in the event payload, and then update MO accordingly.


## Usage
Start the container using `docker-compose`:
```
docker-compose up -d
```

Configure `MO`'s HTTP Trigger support to connect to our container, by adding:
```
[triggers.http_trigger]
enabled = true
http_endpoints = [
    "http_trigger_sdtool:5011"
]
```
To `MO`'s `.toml` configuration file.

OR configure `MO`'s SDTool specific code to connect to our container, by adding:
```
[external_integration]
org_unit = "http://http_trigger_sdtool:5011/sdtool"
```
To `MO`'s `.toml` configuration file.

Finally (re)start `MO` using its `docker-compose.yml` file.
