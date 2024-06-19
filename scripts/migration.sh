#!/bin/bash

cd ..
alembic upgrade head
exec "$@"