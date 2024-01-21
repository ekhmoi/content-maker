#!/bin/sh

# Navigate to the ui directory
cd ui

# Run npm install
npm start & (cd ../ && python3 main.py serve -o ./outputs)
