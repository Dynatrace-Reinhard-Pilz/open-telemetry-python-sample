# open-telemetry-python-sample
A quick sample for how to integrate Python via OpenTelemetry with Dynatrace.
This sample works with and without OneAgent installed. It just adds a few additional features (Resource Attributes, Log Enrichment) in case the Agent is present.
## How to launch
* Fill out the environment endpoint and API Token in `setenv.cmd` and launch that script
* Execute `pip install -r requirements.txt`
* Execute `python main.py`
