#!/bin/bash

# shell script for running alembic commands

echo $"running alembic command for table creation"

alembic stamp head
if [ $? -eq 0 ]; then
    echo $"stamp head ran successfully"
else
    echo $"failed to run alembic commands"
    exit 1
fi

alembic revision --autogenerate -m "Initial Migration Added"
if [ $? -eq 0 ]; then
  echo $"generated table changes"
else
  echo $"failed to autogenerate table changes"
  exit 1
fi

alembic upgrade head
if [ $? -eq 0 ]; then
  echo $"upgraded database"
else
  echo $"failed to upgrade db"
  exit 1
fi
