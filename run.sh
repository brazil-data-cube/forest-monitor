#!/bin/bash
export PORT=5000
export KEYSYSTEM="Key#2019@BDC#hash"
export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost/test
export CLIENT_SECRET_KEY="fm@2020!"
export CLIENT_AUDIENCE="forest-monitor-local"
export MASK_TABLE_DETER="mascara_deter",
export MASK_TABLE_PRODES="mascara_prodes",
export DESTINATION_TABLE="deter"

python3 manage.py run

