#!/bin/bash

install() {
    python3 -m venv .env
    . .env/bin/activate
    pip install -r requirements.txt
}

run(){
    . .env/bin/activate
    python run.py
}

install
run
