SCYLLA_VERSION?=latest
SCYLLA_NAME?=some-scylla
NODE_IP=docker exec -it $(SCYLLA_NAME) nodetool status | grep -e "^UN" | awk '{print $$2}'

setup: venv

venv: requirements.txt
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

.PHONY: scylla-run
scylla-run:
	docker run --name $(SCYLLA_NAME) --hostname some-scylla -d scylladb/scylla:$(SCYLLA_VERSION) --smp 1

.PHONY: scylla-stop
scylla-stop:
	docker stop $(SCYLLA_NAME)
	docker rm $(SCYLLA_NAME)

.PHONY: scylla-status
scylla-status:
	docker exec -it $(SCYLLA_NAME) nodetool status

.PHONY: scylla-stress
scylla-stress:
	docker exec $(SCYLLA_NAME) cassandra-stress write duration=10s -rate threads=10 -node `$(NODE_IP)`

.PHONY: format
format:
	./venv/bin/ruff format .
	./venv/bin/ruff --fix .

.PHONY: style
style:
	./venv/bin/ruff .
