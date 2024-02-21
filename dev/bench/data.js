window.BENCHMARK_DATA = {
  "lastUpdate": 1708510234242,
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
          "id": "5e073dc2f0211cabe5e807e799b8045db2cdecac",
          "message": "Changed: Auto push benchmark",
          "timestamp": "2024-02-15T12:50:01Z",
          "url": "https://github.com/kayjan/bigtree/pull/204/commits/5e073dc2f0211cabe5e807e799b8045db2cdecac"
        },
        "date": 1708510233304,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10",
            "value": 13374.777310155845,
            "unit": "iter/sec",
            "range": "stddev: 0.000018380675090484013",
            "extra": "mean: 74.76759999889282 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100",
            "value": 457.2962160018889,
            "unit": "iter/sec",
            "range": "stddev: 0.000039604909390469214",
            "extra": "mean: 2.1867663999998403 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000",
            "value": 6.5411368411645645,
            "unit": "iter/sec",
            "range": "stddev: 0.002489996980434288",
            "extra": "mean: 152.8786240499997 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10",
            "value": 48.49261741361179,
            "unit": "iter/sec",
            "range": "stddev: 0.0005288342722048427",
            "extra": "mean: 20.62169569999952 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10_no_assertions",
            "value": 20615.411256377858,
            "unit": "iter/sec",
            "range": "stddev: 0.000006725009753393029",
            "extra": "mean: 48.507400001085436 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100_no_assertions",
            "value": 1579.7672260393158,
            "unit": "iter/sec",
            "range": "stddev: 0.00000906489680343641",
            "extra": "mean: 633.0046499996911 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000_no_assertions",
            "value": 131.21449995803002,
            "unit": "iter/sec",
            "range": "stddev: 0.000046972467077592014",
            "extra": "mean: 7.6211089500006315 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10_no_assertions",
            "value": 70.1225777369504,
            "unit": "iter/sec",
            "range": "stddev: 0.00022790299044748871",
            "extra": "mean: 14.260742150000283 msec\nrounds: 2"
          }
        ]
      }
    ]
  }
}