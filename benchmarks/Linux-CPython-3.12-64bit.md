# Gramps Performance Benchmarks (v6.0.4)

## Linux-CPython-3.12-64bit

### Summary

- **Generated:** 2025-08-20 16:17:23
- **Number of benchmark runs:** 4
- **Total benchmark files:** 4

### Benchmark Files

- 0001_5.2.4.json
- 0005_6.0.4.json
- 0006_5.1.6.json
- 0007_6.1.0.json


## Benchmark: test_add_person_transaction[sqlite]

![Chart for test_add_person_transaction[sqlite]](test_add_person_transaction%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.007923 | 0.007433 | 0.010523 | 0.000541 | 50 |
| 5.2.4 | 0.001305 | 0.001163 | 0.002307 | 0.000143 | 228 |
| 6.0.4 | 0.001516 | 0.001344 | 0.002158 | 0.000166 | 213 |
| 6.1.0 | 0.000290 | 0.000240 | 0.002880 | 0.000263 | 280 |


## Benchmark: test_database_loading[sqlite]

![Chart for test_database_loading[sqlite]](test_database_loading%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 1.767124 | 1.686130 | 1.854447 | 0.075290 | 5 |
| 5.2.4 | 1.821046 | 1.734248 | 1.927586 | 0.070682 | 5 |
| 6.0.4 | 2.236641 | 2.198108 | 2.282942 | 0.031420 | 5 |
| 6.1.0 | 2.098709 | 1.994001 | 2.238927 | 0.101260 | 5 |


## Benchmark: test_descendant_filter[sqlite]

![Chart for test_descendant_filter[sqlite]](test_descendant_filter%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.020280 | 0.018680 | 0.025410 | 0.001302 | 47 |
| 5.2.4 | 0.018224 | 0.017303 | 0.020646 | 0.001045 | 49 |
| 6.0.4 | 0.002194 | 0.000626 | 0.013291 | 0.002882 | 1271 |
| 6.1.0 | 0.000629 | 0.000602 | 0.000819 | 0.000022 | 1156 |


## Benchmark: test_family_queries[sqlite]

![Chart for test_family_queries[sqlite]](test_family_queries%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.001065 | 0.000783 | 0.086076 | 0.003917 | 933 |
| 5.2.4 | 0.001112 | 0.000815 | 0.086278 | 0.004306 | 768 |
| 6.0.4 | 0.001552 | 0.001230 | 0.090487 | 0.003555 | 628 |
| 6.1.0 | 0.001666 | 0.001166 | 0.096301 | 0.005108 | 680 |


## Benchmark: test_person_has_id_filter[sqlite]

![Chart for test_person_has_id_filter[sqlite]](test_person_has_id_filter%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.016778 | 0.016514 | 0.017064 | 0.000121 | 58 |
| 5.2.4 | 0.020039 | 0.019055 | 0.022619 | 0.000733 | 52 |
| 6.0.4 | 0.000600 | 0.000583 | 0.000724 | 0.000018 | 1285 |
| 6.1.0 | 0.000592 | 0.000576 | 0.000999 | 0.000026 | 1288 |


## Benchmark: test_person_queries[sqlite]

![Chart for test_person_queries[sqlite]](test_person_queries%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.005125 | 0.002805 | 0.091558 | 0.013176 | 200 |
| 5.2.4 | 0.005134 | 0.002929 | 0.122330 | 0.013360 | 304 |
| 6.0.4 | 0.009961 | 0.005546 | 0.102974 | 0.017984 | 171 |
| 6.1.0 | 0.005352 | 0.005180 | 0.005765 | 0.000174 | 10 |


## Benchmark: test_raw_person_queries[sqlite]

![Chart for test_raw_person_queries[sqlite]](test_raw_person_queries%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.002388 | 0.001270 | 0.109009 | 0.009650 | 648 |
| 5.2.4 | 0.003613 | 0.001266 | 0.086569 | 0.013272 | 647 |
| 6.0.4 | 0.003984 | 0.001981 | 0.101316 | 0.012775 | 426 |
| 6.1.0 | 0.003759 | 0.001682 | 0.119848 | 0.013674 | 457 |


## Benchmark: test_scalable_person_queries[10-sqlite]

![Chart for test_scalable_person_queries[10-sqlite]](test_scalable_person_queries%5B10-sqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.000126 | 0.000113 | 0.000209 | 0.000006 | 4077 |
| 5.2.4 | 0.000137 | 0.000119 | 0.000271 | 0.000009 | 4495 |
| 6.0.4 | 0.000236 | 0.000206 | 0.000336 | 0.000012 | 2912 |
| 6.1.0 | 0.000222 | 0.000192 | 0.000362 | 0.000013 | 2923 |


## Benchmark: test_scalable_person_queries[100-sqlite]

![Chart for test_scalable_person_queries[100-sqlite]](test_scalable_person_queries%5B100-sqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.001781 | 0.001216 | 0.085518 | 0.005607 | 664 |
| 5.2.4 | 0.001836 | 0.001213 | 0.085979 | 0.006758 | 610 |
| 6.0.4 | 0.002919 | 0.002337 | 0.090644 | 0.006401 | 378 |
| 6.1.0 | 0.002505 | 0.002170 | 0.098393 | 0.004753 | 409 |


## Benchmark: test_scalable_person_queries[50-sqlite]

![Chart for test_scalable_person_queries[50-sqlite]](test_scalable_person_queries%5B50-sqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.000695 | 0.000646 | 0.000883 | 0.000026 | 426 |
| 5.2.4 | 0.000708 | 0.000589 | 0.085245 | 0.002327 | 1322 |
| 6.0.4 | 0.001406 | 0.001160 | 0.103931 | 0.003868 | 706 |
| 6.1.0 | 0.001275 | 0.001054 | 0.097377 | 0.003669 | 688 |


## Benchmark: test_source_queries[sqlite]

![Chart for test_source_queries[sqlite]](test_source_queries%5Bsqlite%5D.png)

| Run | Mean Time (seconds) | Min Time (seconds) | Max Time (seconds) | Standard Deviation | Rounds |
|-----|-------------------|-------------------|-------------------|-------------------|--------|
| 5.1.6 | 0.000001 | 0.000001 | 0.000009 | 0.000000 | 87728 |
| 5.2.4 | 0.000001 | 0.000000 | 0.000005 | 0.000000 | 88293 |
| 6.0.4 | 0.000001 | 0.000000 | 0.000007 | 0.000000 | 79561 |
| 6.1.0 | 0.000001 | 0.000000 | 0.000008 | 0.000000 | 81368 |


---

*Generated by Gramps Benchmark Tool on 2025-08-20 16:17:24*
