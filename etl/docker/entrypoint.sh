#!/bin/bash
set -e

python3 /opt/wait_for_services.py

exec "$@"