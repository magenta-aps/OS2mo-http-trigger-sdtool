# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /opt/
RUN git clone --single-branch --branch feature/41894_sdtool_disable_cache https://github.com/OS2mo/os2mo-data-import-and-export
RUN pip install --no-cache-dir -e os2mo-data-import-and-export/os2mo_data_import
RUN pip install --no-cache-dir more-itertools==8.6.0

COPY ./requirements.txt /app/requirements.txt
COPY ./requirements /app/requirements
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple os2mo-fastapi-utils==0.0.1

WORKDIR /app
COPY ./app /app
