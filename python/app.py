from flask import Flask, jsonify, request
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Configure the OTLP metrics exporter
otlp_exporter = OTLPMetricExporter(endpoint="http://localhost:9090/api/v1/otlp/v1/metrics")
reader = PeriodicExportingMetricReader(otlp_exporter, 1000)
resource = Resource.create({"service.name": "calculator"})
provider = MeterProvider(metric_readers=[reader], resource=resource)

metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Example metric recording
calc_metric = meter.create_counter(
    name="calc_operation",
    description="Records every Calculator Operation",
)

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    result = data['num1'] + data['num2']
    calc_metric.add(1, {"operation": "add"})
    return jsonify({"result": result})

@app.route('/subtract', methods=['POST'])
def subtract():
    data = request.json
    result = data['num1'] - data['num2']
    calc_metric.add(1, {"operation": "sub"})
    return jsonify({"result": result})

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.json
    result = data['num1'] * data['num2']
    calc_metric.add(1, {"operation": "mult"})
    return jsonify({"result": result})

@app.route('/divide', methods=['POST'])
def divide():
    data = request.json
    if data['num2'] == 0:
        return jsonify({"error": "Division by zero is not allowed."}), 400
    result = data['num1'] / data['num2']
    calc_metric.add(1, {"operation": "div"})
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
