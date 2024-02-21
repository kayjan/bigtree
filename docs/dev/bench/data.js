window.BENCHMARK_DATA = {
  "lastUpdate": 1708525197044,
  "repoUrl": "https://github.com/kayjan/bigtree",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "name": "kayjan",
            "username": "kayjan"
          },
          "committer": {
            "name": "kayjan",
            "username": "kayjan"
          },
          "id": "098d71bb5d4259c105f1810e8c12d66d74c22a0e",
          "message": "Added: benchmark dir path",
          "timestamp": "2024-02-15T12:50:01Z",
          "url": "https://github.com/kayjan/bigtree/pull/205/commits/098d71bb5d4259c105f1810e8c12d66d74c22a0e"
        },
        "date": 1708525195913,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10",
            "value": 13759.852053964616,
            "unit": "iter/sec",
            "range": "stddev: 0.000018120318373713585",
            "extra": "mean: 72.67520000056038 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100",
            "value": 446.3545841711644,
            "unit": "iter/sec",
            "range": "stddev: 0.000026382719692861725",
            "extra": "mean: 2.240371299998855 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000",
            "value": 6.570487329970291,
            "unit": "iter/sec",
            "range": "stddev: 0.0010947628004656506",
            "extra": "mean: 152.19571239999965 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10",
            "value": 54.938757816336825,
            "unit": "iter/sec",
            "range": "stddev: 0.00040141815571895163",
            "extra": "mean: 18.202086099999804 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10_no_assertions",
            "value": 22314.95324970347,
            "unit": "iter/sec",
            "range": "stddev: 0.000007149556662764809",
            "extra": "mean: 44.81300000094279 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100_no_assertions",
            "value": 1365.2273188819292,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016689841327954604",
            "extra": "mean: 732.4787499996432 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000_no_assertions",
            "value": 130.159694621401,
            "unit": "iter/sec",
            "range": "stddev: 0.00001682687865207749",
            "extra": "mean: 7.682869900000355 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10_no_assertions",
            "value": 80.61362381044749,
            "unit": "iter/sec",
            "range": "stddev: 0.00012793682992144064",
            "extra": "mean: 12.404851099999803 msec\nrounds: 2"
          }
        ]
      }
    ]
  }
}