#!/bin/sh

mkdir pyconv-backup

for i in *.json; do
  filename=$(basename "$i" .json)
  cp "$i" "pyconv-backup/${filename}.json"
done
for i in pyconv-backup/*.json; do
  filename=$(basename "$i" .json)
  uv run convert-timestamps.py "$i" "./${filename}.json"
done