#!/bin/bash

# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

cd /opt/os2mo-data-import-and-export/integrations/SD_Lon

poetry run python -m sdlon.fix_departments --department-uuid="$1"
