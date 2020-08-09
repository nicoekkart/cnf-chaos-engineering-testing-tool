This CLI tests a CNF application with chaos experiments.

Litmus operators should be installed prior to running the CLI.

```
kubectl apply -f https://litmuschaos.github.io/pages/litmus-operator-v1.4.0.yaml
kubectl apply -f https://hub.litmuschaos.io/api/chaos/1.4.0?file=charts/generic/experiments.yaml 
```

To install prerequsites, run:

```
pip install -r requirements.txt
```

To view all the options:

```
$ python main.py --help
usage: main.py [-h] config_file

Run chaos experiments on a NSM helm installation

positional arguments:
  config_file

optional arguments:
  -h, --help   show this help message and exit

```

