test:
#	uv run pytest --cov=dbconn
	ruff check

fmt:
	ruff check --select I,F401 --fix
	ruff format
