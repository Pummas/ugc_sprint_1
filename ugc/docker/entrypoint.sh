#!/bin/bash
set -e

echo "Waiting for Kafka"
python3 /opt/wait_for_services.py

exec "$@"