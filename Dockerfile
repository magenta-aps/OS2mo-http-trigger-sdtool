# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV POETRY_VERSION="1.3.2"

RUN apt-get update \
 && apt-get -y install --no-install-recommends unixodbc-dev \
    freetds-dev unixodbc tdsodbc libkrb5-dev libmariadb-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# These need to be installed manually ALL THE TIME for debugging, so let's
# include them here for now until we have a more stable application
RUN apt install -y vim sqlite3 screen

WORKDIR /opt/
RUN git clone -b 4.54.6 https://github.com/OS2mo/os2mo-data-import-and-export \
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
