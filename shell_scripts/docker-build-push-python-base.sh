#!/bin/bash
docker build -t bilgrami/python-base:latest -f Dockerfile.base .;
docker push bilgrami/python-base:latest
