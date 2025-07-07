#!/bin/bash

BASE_URL="http://localhost:5000/api/timeline_post"

# Generate random test data
NAME="Test User $(date +%s)"
EMAIL="testuser@example.com"
CONTENT="This is a test post"

echo "Creating post."

# Send POST request
RESPONSE=$(curl -s -X POST "$BASE_URL" \
  --data-urlencode "name=$NAME" \
  --data-urlencode "email=$EMAIL" \
  --data-urlencode "content=$CONTENT")

# Extract the ID from the response using grep/sed
ID=$(echo "$RESPONSE" | grep -o '"id": [0-9]*' | sed 's/[^0-9]*//')

if [ -z "$ID" ]; then
  echo "Failed to create timeline post."
  exit 1
fi

echo "Created timeline post"
echo ""
echo "Fetching timeline posts."

# Send GET request
curl -s "$BASE_URL" | grep "$NAME" > /dev/null

# If exit code is 0, post was created and found
if [ $? -eq 0 ]; then
  echo "Successfully found post."
else
  echo "Post not found."
  exit 1
fi