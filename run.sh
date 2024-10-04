#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Here is how to use: $0 <command> [arguments...]"
  exit 1
fi

docker compose exec app "$@"
