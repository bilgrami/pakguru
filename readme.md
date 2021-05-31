# Welcome to pak.guru official github repository

----

| [![Build Status](https://travis-ci.org/bilgrami/pakguru.svg?branch=master)](https://travis-ci.org/bilgrami/pakguru)
| [![Coverage Status](https://coveralls.io/repos/github/bilgrami/pakguru/badge.svg)](https://coveralls.io/github/bilgrami/pakguru)
| [![CircleCI](https://circleci.com/gh/bilgrami/pakguru.svg?style=svg)](https://circleci.com/gh/bilgrami/pakguru)

## Demo Link

* [https://pakguru.azurewebsites.net/] - pak.guru old website is a multi-container django app hosted on Azure. We make heavy use of serverless lambdas to harvest data.

----

## Installation

### 1) Pre-requisites

#### Required

* Python v3.7.4 with pip
* Docker and docker-compose
* git

#### Optional

* VS Code
* Azure Cli

Make sure your local volumne drives are mounted and shared within docker.

For example:

```sh
docker run --rm -v c:/Users:/data alpine ls /data
```

#### Method 1: Pull image from docker hub

```sh
docker pull bilgrami/pakguru:latest
```

#### Method 2: Build image on your local machine

```sh
git clone https://github.com/bilgrami/pakguru.git
cd pakguru

## setup python environment
./shell_scripts/setup-environment.sh

docker build -t bilgrami/pakguru:latest .
```

### 2) Run Docker Container

After building docker image, launch the website using any of the following methods:

#### Method 1: Use multi-container Django app with postgres database and redis cache

```sh
docker-compose up
```

#### Method 2: Use stand-alone docker container app running Django with sqllite database and dummy cache

```sh
docker run --rm -it -p 5000:5000/tcp bilgrami/pakguru:latest
```

### 3) Run init script

Run init script to create users, migrate database and load sample fixture data

```sh
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && chmod +x ./shell_scripts/init_script.sh && ./shell_scripts//init_script.sh'

```

### 4) Launch Website

Verify the deployment by navigating to your server address in your preferred browser.

```sh
http://localhost:5000

```

> version 0.1.1

----

[pak.guru]: <https://www.pak.guru>
