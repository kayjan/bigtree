window.BENCHMARK_DATA = {
  "lastUpdate": 1708532466240,
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
          "id": "0b71cbefb5cb8989b176f8c06cab325a58ffd7a3",
          "message": "Changed: Change benchmark save dir from gh-pages to master",
          "timestamp": "2024-02-15T12:50:01Z",
          "url": "https://github.com/kayjan/bigtree/pull/207/commits/0b71cbefb5cb8989b176f8c06cab325a58ffd7a3"
        },
        "date": 1708532464866,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10",
            "value": 13763.336673418606,
            "unit": "iter/sec",
            "range": "stddev: 0.000015384239395806767",
            "extra": "mean: 72.65679999903796 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100",
            "value": 452.6237683287322,
            "unit": "iter/sec",
            "range": "stddev: 0.000041075479366656276",
            "extra": "mean: 2.209340449999786 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000",
            "value": 6.456552622105892,
            "unit": "iter/sec",
            "range": "stddev: 0.0013583800573773318",
            "extra": "mean: 154.88141405000064 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10",
            "value": 56.86340793582935,
            "unit": "iter/sec",
            "range": "stddev: 0.00017576595686372493",
            "extra": "mean: 17.586001900000525 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10_no_assertions",
            "value": 22199.455447278593,
            "unit": "iter/sec",
            "range": "stddev: 0.000007242965470510293",
            "extra": "mean: 45.04615000016088 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100_no_assertions",
            "value": 1596.0432173392508,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036504387577027664",
            "extra": "mean: 626.5494499999136 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000_no_assertions",
            "value": 138.14268813514244,
            "unit": "iter/sec",
            "range": "stddev: 0.000011322900886970027",
            "extra": "mean: 7.238892000000163 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10_no_assertions",
            "value": 92.09873020718089,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034287607828024053",
            "extra": "mean: 10.857912999999542 msec\nrounds: 2"
          }
        ]
      }
    ]
  }
}