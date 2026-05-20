#!/bin/bash
set -e

echo "Cleaning up old Allure results..."
rm -rf allure-results/*

echo "Starting test execution..."
echo "ENV: $ENV"
echo "BASE_URL: $BASE_URL"
echo "MARKERS: ${MARKERS:-ALL}"

if [ -z "$MARKERS" ]; then
  echo "Running ALL tests"
  pytest --alluredir=allure-results
else
  echo "Running tests with markers: $MARKERS"
  pytest -m "$MARKERS" --alluredir=allure-results
fi

echo "Tests finished"