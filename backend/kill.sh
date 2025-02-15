#!/bin/bash

PID=$(sudo lsof -t -i :8080)

if [ -n "$PID" ]; then
  echo "Killing process $PID running on port 8080..."
  kill -9 $PID
  echo "Process $PID has been terminated."
else
  echo "No process found running on port 8080."
fi
