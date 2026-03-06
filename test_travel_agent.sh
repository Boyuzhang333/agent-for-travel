#!/usr/bin/env bash

OUTPUT_FILE="test_results.log"

echo "=== Travel Agent Test Run ===" | tee $OUTPUT_FILE
echo "Date: $(date)" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

run_test () {
  TEST_INPUT="$1"

  echo "----------------------------------" | tee -a $OUTPUT_FILE
  echo "TEST INPUT: $TEST_INPUT" | tee -a $OUTPUT_FILE
  echo "----------------------------------" | tee -a $OUTPUT_FILE

  printf "%s\nexit\n" "$TEST_INPUT" | python -u -m my_agent.main | tee -a $OUTPUT_FILE

  echo "" | tee -a $OUTPUT_FILE
}

run_test "Plan a 3 day trip from Paris to Rome with 800 euros"
run_test "Plan a 5 day trip from Berlin to Madrid with 1500 euros"
run_test "Plan a 2 day trip from Lyon to Milan with 400 euros"
run_test "Plan a 7 day trip from London to Tokyo with 3000 euros"
run_test "Plan a 4 day trip from Nice to Barcelona with 900 euros"

echo "Tests completed."