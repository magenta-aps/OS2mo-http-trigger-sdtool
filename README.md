[//]: # (SPDX-FileCopyrightText: Magenta ApS)
[//]: # ()
[//]: # (SPDX-License-Identifier: MPL-2.0)

# OS2mo HTTP Trigger Example

This repository contains an example implementation of an OS2mo HTTP Trigger receiver.

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
    "http_trigger_example:5011"
]
```
To `MO`'s `.toml` configuration file.

Finally (re)start `MO` using its `docker-compose.yml` file.
