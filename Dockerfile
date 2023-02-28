# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV POETRY_VERSION="1.3.2"

RUN apt-get update \
 && apt-get -y install --no-install-recommends unixodbc-dev=2.3.6-0.1+b1 \
    freetds-dev=1.2.3-1 unixodbc=2.3.6-0.1+b1 tdsodbc=1.2.3-1 \
    libkrb5-dev=1.18.3-6+deb11u3 libmariadb-dev=1:10.5.18-0+deb11u1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/
RUN git clone -b 3.57.5 https://github.com/OS2mo/os2mo-data-import-and-export \
 && pip3 install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /opt/os2mo-data-import-and-export/integrations/SD_Lon
RUN poetry install --no-interaction --no-root --no-dev

COPY ./requirements.txt /app/requirements.txt
COPY ./requirements /app/requirements
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# These are not used but have to be there... don't worry about it - it's just DIPEX...
ENV SD_GLOBAL_FROM_DATE=2000-01-01
ENV SD_IMPORT_RUN_DB=/not/used
ENV SD_JOB_FUNCTION=EmploymentName
ENV SD_MONTHLY_HOURLY_DIVIDE=1

ENV TZ="Europe/Copenhagen"

WORKDIR /app
COPY ./app /app
