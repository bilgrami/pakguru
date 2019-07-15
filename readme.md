# Welcome to pak.guru official github repository

----

| [![Build Status](https://travis-ci.org/bilgrami/pakguru.svg?branch=master)](https://travis-ci.org/bilgrami/pakguru)
| [![Coverage Status](https://coveralls.io/repos/github/bilgrami/pakguru/badge.svg)](https://coveralls.io/github/bilgrami/pakguru)
| [![CircleCI](https://circleci.com/gh/bilgrami/pakguru.svg?style=svg)](https://circleci.com/gh/bilgrami/pakguru)

## Demo Link

* [pak.guru] - pak.guru website is a multi-container django app hosted as an Azure. We also make heavy use of serverless lambdas to harvest web data and publish to the website.

----

## Installation

### 1) Pre-requisites

You need docker and docker-compose to run the website.

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

#### Method 1: Use docker with sqllite database

```sh
docker run --rm -it -p 5000:5000/tcp bilgrami/pakguru:latest
```

#### Method 2: Use docker-compose with postgrs database

```sh
docker-compose up
```

### 3) Launch Website

Verify the deployment by navigating to your server address in your preferred browser.

```sh
http://127.0.0.1:5000
```

> version 0.1.1

----

[pak.guru]: <https://www.pak.guru>
