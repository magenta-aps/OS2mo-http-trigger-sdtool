#!/bin/bash

# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

cd /opt/os2mo-data-import-and-export/
export PYTHONPATH=$PWD:$PYTHONPATH

python integrations/SD_Lon/fix_departments.py --department-uuid="$1"
