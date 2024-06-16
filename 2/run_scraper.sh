#!/bin/bash

# Check if at least two arguments are provided
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 [phrase] [proxy_url (optional)]"
  exit 1
fi

# Initialize an empty phrase variable
PHRASE="$1"
shift

# Loop through all arguments except the last one
while [ "$#" -gt 1 ]; do
  PHRASE="$PHRASE $1"
  shift
done

# Check if the last argument is a URL or phrase
if [ "$#" -eq 1 ]; then
  if [[ $1 == http* ]]; then
    PROXY_URL=$1
  else
    PHRASE="$PHRASE $1"
    PROXY_URL=""
  fi
else
  PROXY_URL=""
fi

# Run the Python script with the provided arguments
python scraper.py "$PHRASE" "$PROXY_URL"
