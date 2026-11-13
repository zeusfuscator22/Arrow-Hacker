#!/bin/sh
set -eu
cd "$(dirname "$0")"
PORT="${AFTERGLOW_PORT:-8000}"
exec python3 server.py "$PORT"
