# W5M1

## RDD (Resilient Distributed Dataset)

- Immutable - transformation은 새로운 RDD 만들고 원본 수정 x
- Fault Tolerance - lineage 구축

## Transformation vs Actions

 - Transformation은 새로운 RDD를 만들지만 즉시 실행되지 않음
 - Narrow  Transformation - 셔플 x (map, filter)
```python
# map() - 1 대 1 변환
parsed_rdd = raw_rdd.map(parse_parquet_row)
# 각 입력 파티션 → 하나의 출력 파티션

# filter() - 1 대 0 또는 1 변환
cleaned_rdd = parsed_rdd.filter(is_valid_record)
# 각 파티션 내에서 유효하지 않은 레코드 제거
# 셔플 필요 없음
```
 - Wide Transformation - 셔플 필요 (reduceByKey, sortBy)
```python
# reduceByKey() - 키로 집계
daily_metrics = daily_data.reduceByKey(
    lambda a, b: (a[0] + b[0], a[1] + b[1], a[2] + b[2])
)
# 같은 키를 가진 모든 레코드가 같은 파티션에 있어야 하므로 셔플이 필요

# sortBy() - 전역 정렬
top_revenue_days = daily_metrics.sortBy(lambda x: x[1], ascending=False)
# 모든 파티션에 걸쳐 비교 필요
# 데이터를 모아 정렬하기 위해 셔플 필요
```
- Action은 실제 계산을 실행시킴
```python
# count() - 요소 수 반환
cleaned_count = cleaned_rdd.count()  
# reduce() - 모든 요소 집계
totals = metrics_rdd.reduce(lambda a, b: (a[0] + b[0], ...))  
# saveAsTextFile() - 결과 저장
daily_results.saveAsTextFile(output_path)  
```

## Lazy Evaluation

Action 호출될 때까지 실행 x

```python
# Transformations
parsed_rdd = raw_rdd.map(parse_parquet_row)        # 실행x
cleaned_rdd = parsed_rdd.filter(is_valid_record)   # 실행x
metrics_rdd = cleaned_rdd.map(lambda x: ...)       # 실행x

# Actions
total_trips = metrics_rdd.count()  # 실행
```

- Spark는 DAG를 만들어 실행 계획을 나타냄
- shuffle - 파티션 간의 데이터 재분배
- Stage가 Shuffle이 발생하는 경계에서 생성

## Cache

RDD를 메모리에 저장하여 재사용
### Without Caching
```
Action 1: count()
raw_rdd → map → filter → count

Action 2: reduce()
raw_rdd → map → filter → reduce (재계산 필요)
```
### With Caching
```
Action 1: count()
raw_rdd → map → filter → [CACHE] → count

Action 2: reduce()
[CACHE] → reduce (재사용)
```

# W5M2

## DataFrame

| 특성     | RDD    | DataFrame      |
| ------ | ------ | -------------- |
| 구조     | 비구조화   | 구조화 (스키마 있음)   |
| 최적화    | 수동     | 자동 (Catalyst)  |
| API    | 저수준    | 고수준 (SQL-like) |
| 성능     | 사용자 의존 | 최적화됨           |
| 사용 편의성 | 낮음     | 높음             |

## AQE(Adaptive Query Execution )

- 실행 중 통계를 기반으로 쿼리 계획을 동적으로 최적화
```python
spark = SparkSession.builder \
	.config("spark.sql.adaptive.enabled", "true")\
	.config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
	.getOrCreate()
```

## 최적화

**불필요한 Shuffle 최소화**
  `groupBy()` 전에 `filter()`로 데이터 축소
- 조인 전 `groupBy`와 `select`로 양쪽 데이터 축소

**캐싱 활용**
- `df_cleaned.cache()`: 일별 집계와 시간별 집계 양쪽에서 재사용
- `weather_analysis.cache()`: `show()`와 `write()` 양쪽에서 재사용
- 분석 완료 후 `unpersist()`로 메모리 해제

 **파티션 설정**
- `spark.sql.shuffle.partitions` 값 조정
- `coalesce(1)`로 출력 시 단일 파일 생성
