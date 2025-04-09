#!/bin/bash
airflow db init
airflow scheduler &
airflow webserver
