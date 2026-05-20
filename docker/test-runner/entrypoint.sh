#!/bin/bash
set -e

REPORT_DIR=${ALLURE_DIR:-allure-results}
FULL_REPORT_PATH="$PWD/$REPORT_DIR"

echo "Cleaning up old Allure results in $FULL_REPORT_PATH..."
rm -rf "$FULL_REPORT_PATH"/*

echo "Starting test execution..."
echo "ENV: $ENV"
echo "BASE_URL: $BASE_URL"
echo "MARKERS: ${MARKERS:-ALL}"
echo "Target Allure Directory: $FULL_REPORT_PATH"

if [ -z "$MARKERS" ]; then
  echo "Running ALL tests"
  pytest --alluredir="$FULL_REPORT_PATH"
else
  echo "Running tests with markers: $MARKERS"
  pytest -m "$MARKERS" --alluredir="$FULL_REPORT_PATH"
fi

echo "Tests finished"