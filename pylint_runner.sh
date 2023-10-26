#!/bin/bash

pylint game models

score=$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint.txt)
score_minimal=8.0

cat pylint.txt
rm pylint.txt

if (( $(echo "$score > $score_minimal" | bc -l) )); then
  echo "Pylint succeeded"
  exit 0
else
  echo "Pylint failed"
  exit 1
fi
