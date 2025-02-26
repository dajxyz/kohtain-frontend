#!/bin/sh
for i in audio-wav/*.wav; do
  filename=$(basename "$i" .wav)
  ffmpeg -i "$i" -ar 16000 -ac 1 -b:a 64k  "audio-mp3/${filename}.mp3"
done