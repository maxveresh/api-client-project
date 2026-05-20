#!/bin/bash
set -e

echo "Cleaning up old Allure results..."
rm -rf allure-results/*
if [ -n "$ALLURE_DIR" ]; then
  rm -rf "$ALLURE_DIR"/*
fi

echo "Starting test execution..."
echo "ENV: $ENV"
echo "BASE_URL: $BASE_URL"
echo "MARKERS: ${MARKERS:-ALL}"

REPORT_DIR=${ALLURE_DIR:-allure-results}

if [ -z "$MARKERS" ]; then
  echo "Running ALL tests"
  pytest --alluredir="$REPORT_DIR"
else
  echo "Running tests with markers: $MARKERS"
  pytest -m "$MARKERS" --alluredir="$REPORT_DIR"
fi

echo "Tests finished"