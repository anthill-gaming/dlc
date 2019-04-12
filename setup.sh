#!/usr/bin/env bash

# Setup postgres database
createuser -d anthill_dlc -U postgres
createdb -U anthill_dlc anthill_dlc