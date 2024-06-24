#!/bin/bash
alembic downgrade base
alembic upgrade head
exec "$@"