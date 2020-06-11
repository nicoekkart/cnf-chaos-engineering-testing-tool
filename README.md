To run the chaos experiments, do the following:

```
kubectl apply -f https://litmuschaos.github.io/pages/litmus-operator-v1.4.0.yaml
kubectl apply -f https://hub.litmuschaos.io/api/chaos/1.4.0?file=charts/generic/experiments.yaml 
```