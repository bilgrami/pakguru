#!/bin/bash
docker build -t bilgrami/python-base:latest -f Dockerfile.base .;
docker build --rm -t bilgrami/pakguru:latest .;
