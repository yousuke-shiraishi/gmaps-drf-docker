#!/bin/bash
set -e
set -x
# ...

# Host and port that we want to wait for
HOST=api
PORT=8000

echo "Waiting for ${HOST}:${PORT} to be ready..."

# Wait until the health_check endpoint returns a successful status
while ! curl --fail -s "http://${HOST}:${PORT}/health_check/"; do
  # If the connection attempt failed, then sleep for a second and try again
  sleep 1
done

echo "${HOST}:${PORT} is ready."


# ...
nginx -g "daemon off;"
