#!/bin/sh

for i in audio-wav/*.wav; do
  filename=$(basename "$i" .wav)
  audiowaveform -i "$i" -o "waveforms/${filename}.json" -z 2048
done