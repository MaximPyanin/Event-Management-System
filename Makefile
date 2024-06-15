apply-migrations:
	@echo "applying migrations"
	alembic upgrade head
rollback-migrations:
	@echo "migrations rollback"
	alembic downgrade base
new-migration:
	@echo "creating new migration"
	alembic revision
autogenerate-migration:
	@echo "generating new migration"
	alembic revision --autogenerate