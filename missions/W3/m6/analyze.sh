#!/bin/bash

TARGET_ASIN="B00CTQ6SIG"
RAW_DATA_FILE="./data/Software.jsonl" 
RESULT_FILE="result.txt"

if [ ! -f "$RESULT_FILE" ]; then
  echo "Error: $RESULT_FILE 파일이 존재하지 않습니다."
  exit 1
fi

if [ ! -f "$RAW_DATA_FILE" ]; then
  echo "Error: $RAW_DATA_FILE 파일이 존재하지 않습니다."
  exit 1
fi

echo "==============================================="
echo "         HADOOP MAPREDUCE REPORT               "
echo "==============================================="
# 결과 파일의 전체 라인 수 (처리된 총 상품 수)
printf "1. Total Unique ASINs: %s\n" $(wc -l < "$RESULT_FILE")
echo ""

echo "2. Top 10 Data (Ordered by Number of Reviews):"
echo "-----------------------------------------------"
echo "ASIN           Count    AvgRating"
sort -k2 -nr "$RESULT_FILE" | head -n 10 | awk '{printf "%-15s %-8s %-10s\n", $1, $2, $3}'
echo ""

echo "3. Top 10 Data (Ordered by Rating):"
echo "-----------------------------------------------"
echo "ASIN           Count    AvgRating"
sort -k3 -nr "$RESULT_FILE" | head -n 10 | awk '{printf "%-15s %-8s %-10s\n", $1, $2, $3}'
echo ""

# --- 검증 섹션 (Verification) ---
echo "==============================================="
echo "        [STEP 1] RAW DATA VERIFICATION         "
echo "==============================================="

# 원본 JSON에서 해당 ASIN의 리뷰 개수와 평점 합계 계산
if command -v jq >/dev/null 2>&1; then
    # jq를 이용해 개수와 평균을 동시에 계산
    raw_stats=$(jq -s -r --arg asin "$TARGET_ASIN" \
      'map(select(.asin == $asin)) | length as $cnt | (map(.rating) | add) as $sum | "\($cnt) \($sum)"' "$RAW_DATA_FILE")
    
    raw_count=$(echo $raw_stats | awk '{print $1}')
    raw_sum=$(echo $raw_stats | awk '{print $2}')
    
    if [ "$raw_count" -gt 0 ]; then
        raw_avg=$(echo "scale=4; $raw_sum / $raw_count" | bc -l)
    else
        raw_avg=0
    fi
else
    # jq가 없을 경우 grep 사용 (개수만 검증 가능)
    raw_count=$(grep -o "\"asin\": \"$TARGET_ASIN\"" "$RAW_DATA_FILE" | wc -l)
    raw_avg="N/A (install jq for rating verify)"
fi

echo "Target ASIN  : $TARGET_ASIN"
echo "Raw Count    : $raw_count"
echo "Raw Avg Rate : $raw_avg"
echo ""

echo "-----------------------------------------------"
echo "       [STEP 2] MAPREDUCE RESULT CHECK "
echo "-----------------------------------------------"

# 결과 파일에서 해당 ASIN 행 추출
result_row=$(grep "^$TARGET_ASIN" "$RESULT_FILE")

if [ -z "$result_row" ]; then
    echo "Result: No data found for $TARGET_ASIN in $RESULT_FILE"
else
    mr_count=$(echo "$result_row" | awk '{print $2}')
    mr_avg=$(echo "$result_row" | awk '{print $3}')
    
    echo "Target ASIN  : $TARGET_ASIN"
    echo "MR Count     : $mr_count"
    echo "MR Avg Rate  : $mr_avg"
    echo "(Note: Rounded to the first decimal place)"
    echo ""

    # 검증 결과 판독
    if [ "$raw_count" -eq "$mr_count" ]; then
        echo ">> [SUCCESS] Review Counts match!"
    else
        echo ">> [FAILED] Review Counts mismatch!"
        echo "   (Raw: $raw_count vs MR: $mr_count)"
    fi
fi
echo "==============================================="