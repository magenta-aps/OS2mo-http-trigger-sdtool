#!/bin/bash

cd /opt/os2mo-data-import-and-export/
export PYTHONPATH=$PWD:$PYTHONPATH

python integrations/SD_Lon/fix_departments.py --department-uuid="$1"
