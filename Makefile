.PHONY: setup start stop test

setup:
	cp .env.example .env
	python3 -m venv venv
	./venv/bin/pip install -r backend/requirements.txt
	cd frontend && npm install

start:
	docker compose up -d

test:
	PYTHONPATH=backend ./venv/bin/pytest backend/tests
	cd frontend && npm run build
