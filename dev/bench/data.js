window.BENCHMARK_DATA = {
  "lastUpdate": 1708529374466,
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
      },
      {
        "commit": {
          "author": {
            "email": "kayjanw@gmail.com",
            "name": "Kay Jan W",
            "username": "kayjan"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c976626a5cebf9e4420187e8c547573f1833623c",
          "message": "Merge pull request #206 from kayjan/benchmark-dir\n\nChanged: Save benchmark result for comparison and gh-pages",
          "timestamp": "2024-02-21T23:28:43+08:00",
          "tree_id": "d5339b366c4c1dc93b5b151e5d237de9572564f2",
          "url": "https://github.com/kayjan/bigtree/commit/c976626a5cebf9e4420187e8c547573f1833623c"
        },
        "date": 1708529373376,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10",
            "value": 13979.092868558011,
            "unit": "iter/sec",
            "range": "stddev: 0.000014858576214890498",
            "extra": "mean: 71.53540000075508 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100",
            "value": 454.7856226983139,
            "unit": "iter/sec",
            "range": "stddev: 0.00003956856410443591",
            "extra": "mean: 2.1988382000003526 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000",
            "value": 6.6748235636044795,
            "unit": "iter/sec",
            "range": "stddev: 0.0021611615680394375",
            "extra": "mean: 149.81669409999938 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10",
            "value": 54.645571392293064,
            "unit": "iter/sec",
            "range": "stddev: 0.00026585928038314955",
            "extra": "mean: 18.29974459999946 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_10_no_assertions",
            "value": 22683.581056841085,
            "unit": "iter/sec",
            "range": "stddev: 0.000005652540897304884",
            "extra": "mean: 44.08475000019507 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_100_no_assertions",
            "value": 1550.1579572204273,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028400943867403994",
            "extra": "mean: 645.0955500000077 usec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_1_depth_1000_no_assertions",
            "value": 139.58604850008427,
            "unit": "iter/sec",
            "range": "stddev: 0.000007687877056865106",
            "extra": "mean: 7.164039749999773 msec\nrounds: 2"
          },
          {
            "name": "tests/node/test_node_benchmark.py::test_node_benchmark_width_2_depth_10_no_assertions",
            "value": 80.87561406983694,
            "unit": "iter/sec",
            "range": "stddev: 0.0006177243121153965",
            "extra": "mean: 12.364666549999725 msec\nrounds: 2"
          }
        ]
      }
    ]
  }
}