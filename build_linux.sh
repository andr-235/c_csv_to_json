#!/bin/bash
echo "Building Linux RPM package..."
briefcase create
briefcase build
briefcase package --format rpm
echo "Build complete! Check dist/ folder"

