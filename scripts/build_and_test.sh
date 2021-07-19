#!/bin/bash

main() {
    docker build -f scripts/Dockerfile.test -t gpip-test . > /dev/null 2>&1
    docker run --rm -t gpip-test
}

main