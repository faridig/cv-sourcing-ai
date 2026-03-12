.PHONY: setup start stop test seed clean-storage

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

seed:
	PYTHONPATH=backend ./venv/bin/python backend/scripts/seed_cvs.py

clean-storage:
	PYTHONPATH=backend ./venv/bin/python backend/scripts/clear_storage.py
