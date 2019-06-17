#!/usr/bin/env bash
docker build --rm -f "Dockerfile" -t bilgrami/pakguru:latest .
docker push bilgrami/pakguru:latest
# docker run --rm -it -p 5000:5000/tcp bilgrami/pakguru:latest
