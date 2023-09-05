#!/bin/bash

flask --app apps db init
flask --app apps db migrate
flask --app apps db upgrade

flask --app apps run --host 0.0.0.0 --debug