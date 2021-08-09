#!/bin/bash

main() {
    docker build -f scripts/Dockerfile.test -t gpip-test .
    docker run --rm -t gpip-test
}

main