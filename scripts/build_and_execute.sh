#!/bin/bash

main() {
    docker build -f scripts/Dockerfile -t gpip . > /dev/null 2>&1
    docker run --rm -t gpip
}

main