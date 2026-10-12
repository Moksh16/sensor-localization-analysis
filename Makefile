PYTHON ?= python3

.PHONY: all download concat csv features clean

all: features

download:
	$(PYTHON) scripts/download_data.py

concat:
	$(PYTHON) scripts/concatenate_data.py

csv:
	$(PYTHON) scripts/build_csv.py

features:
	$(PYTHON) scripts/feature_engineering.py

clean:
	rm -rf data/processed data/csv data/cleaned
