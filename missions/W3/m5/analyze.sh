#!/bin/bash

if [ ! -f "result.txt" ]; then
  echo "Error: result.txt 파일이 존재하지 않습니다."
  exit 1
fi

if [ ! -f "./data/ratings.csv" ]; then
  echo "Error: ./data/ratings.csv 파일이 존재하지 않습니다."
  exit 1
fi

echo "==============================================="
echo "         HADOOP MAPREDUCE REPORT               "
echo "==============================================="
printf "1. Total Line Count: %s\n" $(wc -l <result.txt)
echo ""

echo "2. Top 10 Data (Ordered by ID):"
echo "-----------------------------------------------"
sort -k1 -n result.txt | head -n 10
echo ""

echo "3. Top 10 Data (Ordered by Rating - DESC):"
echo "-----------------------------------------------"
sort -k2 -nr result.txt | head -n 10
echo ""

# --- 검증 섹션 (Verification) ---
echo "==============================================="
echo "   [STEP 1] RAW DATA VERIFICATION (ID: 1)      "
echo "==============================================="
# 원본 데이터(RAW)에서 ID 1의 실제 평균 계산 (소수점 4자리까지 표시)
awk -F',' 'NR > 1 && $2 == 1 {sum += $3; count++} 
  END {
    if (count > 0) 
      printf "Target: MovieID 1\nResult: Average Rating is %.4f\n", sum/count; 
    else 
      print "No data found for MovieID 1"
  }' ./data/ratings.csv

echo ""

echo "-----------------------------------------------"
echo "   [STEP 2] MAPREDUCE RESULT CHECK (ID: 1)     "
echo "-----------------------------------------------"
# 결과 파일에서 ID 1의 결과 추출
result_row=$(sort -k1 -n result.txt | head -n 1 | awk '{print $2}')

if [ -z "$result_row" ]; then
  echo "No result found in result.txt"
else
  echo "MapReduce Result for ID 1: $result_row"
  echo "(Note: Rounded to the first decimal place)"
fi
echo "==============================================="
