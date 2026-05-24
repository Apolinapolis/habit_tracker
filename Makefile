run:
	uvicorn app.main:app --reload

test-server:
	DATABASE_URL=postgresql://postgres:example@localhost:5432/ht_test_db uvicorn app.main:app --reload

test:
	pytest