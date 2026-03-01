#!/bin/bash
echo "Запуск тестов с генерацией отчётов..."

mkdir -p reports/coverage

pytest \
  --cov=src \
  --cov-report=term \
  --cov-report=html:reports/coverage \
  --html=reports/test_results.html \
  --self-contained-html \
  tests/

echo "Отчёты сгенерированы в папке reports/"