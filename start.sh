#!/bin/bash
ip=$(ifconfig | grep -oE 'inet ([0-9]+\.){3}[0-9]+' | grep -v '127.0.0.1')
echo $ip:8501
streamlit run main.py  --server.address 0.0.0.0