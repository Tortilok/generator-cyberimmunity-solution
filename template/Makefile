SHELL := bash

MODULES := monitor \
{% for item in tags %}{{ item }} \
{% endfor %}
SLEEP_TIME := 10

all:
	docker-compose up --build -d
	sleep ${SLEEP_TIME}

	for MODULE in ${MODULES}; do \
		echo Creating $${MODULE} topic; \
		docker exec broker \
			kafka-topics --create --if-not-exists \
			--topic $${MODULE} \
			--bootstrap-server localhost:9092 \
			--replication-factor 1 \
			--partitions 1; \
	done

test:
	python3 tests/operation.py

logs:
	docker-compose logs -f --tail 100

clean:
	docker-compose down
