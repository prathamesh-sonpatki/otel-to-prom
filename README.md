## Demo apps to send Otel metrics to Prometheus

### Running Prometheus locally


``` shell
prometheus --enable-feature=otlp-write-receiver
```

> Assume that you have a standard `prometheus.yml` in the same directory.

### Sending Otel metrics to Prometheus

``` shell
cd python
pip3 install Flask opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
python3 app.py
```

This will push metrics to `localhost:9090/api/v1/otlp/v1/metrics` The host is standard host where Prometheus runs by default and the URL path is the OTLP endpoint of Prometheus which accepts native OpenTelemetry metrics.
