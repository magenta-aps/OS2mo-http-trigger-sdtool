# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /opt/
RUN git clone -b 2.12.1 https://github.com/OS2mo/os2mo-data-import-and-export && \
    pip install --no-cache-dir -e os2mo-data-import-and-export/os2mo_data_import && \
    pip install --no-cache-dir -r os2mo-data-import-and-export/integrations/requirements.txt

COPY ./requirements.txt /app/requirements.txt
COPY ./requirements /app/requirements
RUN pip install --no-cache-dir -r /app/requirements.txt


WORKDIR /app
COPY ./app /app
