#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Download only if the raw data isn't there yet
if [ ! -d data/raw ]; then
    make download
fi

make concat csv features
