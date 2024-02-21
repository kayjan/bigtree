window.BENCHMARK_DATA = {
  "lastUpdate": 1708529280956,
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
          "id": "020749d8442c9d31c24bfac6e3058ea9ddf96dcd",
          "message": "Changed: Save benchmark result for comparison and gh-pages",
          "timestamp": "2024-02-15T12:50:01Z",
          "url": "https://github.com/kayjan/bigtree/pull/206/commits/020749d8442c9d31c24bfac6e3058ea9ddf96dcd"
        },
        "date": 1708529279431,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10",
            "value": 14165.379387705663,
            "unit": "iter/sec",
            "range": "stddev: 0.000013591370152735988",
            "extra": "mean: 70.5946500005439 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100",
            "value": 447.95184768523853,
            "unit": "iter/sec",
            "range": "stddev: 0.00003759375628532879",
            "extra": "mean: 2.2323827999983337 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000",
            "value": 6.585063304450859,
            "unit": "iter/sec",
            "range": "stddev: 0.0015010190514927974",
            "extra": "mean: 151.8588286499991 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10",
            "value": 56.598474419249484,
            "unit": "iter/sec",
            "range": "stddev: 0.000044495330599761786",
            "extra": "mean: 17.668320750000532 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10_no_assertions",
            "value": 19535.905039967314,
            "unit": "iter/sec",
            "range": "stddev: 0.00001661842357080856",
            "extra": "mean: 51.187799999752315 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100_no_assertions",
            "value": 1472.9415843887543,
            "unit": "iter/sec",
            "range": "stddev: 0.000007691554010421899",
            "extra": "mean: 678.9135500000043 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000_no_assertions",
            "value": 136.45478754149568,
            "unit": "iter/sec",
            "range": "stddev: 0.000002364565076990495",
            "extra": "mean: 7.328434699998354 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10_no_assertions",
            "value": 85.30122185897109,
            "unit": "iter/sec",
            "range": "stddev: 0.00006262632628750863",
            "extra": "mean: 11.723161499999433 msec\nrounds: 2"
          }
        ]
      }
    ]
  }
}