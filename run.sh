#!/bin/bash

ansible-playbook -v --ask-become-pass -i hosts main.yml
