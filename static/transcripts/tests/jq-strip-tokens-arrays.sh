#!/bin/sh
for i in original/*.json; do
  filename=$(basename "$i" .json)
  jq '.turns[] | del(.utterances[].tokens) | del(.utterances[].offsets )' < "$i" | jq -s > "short-${filename}.json"
done