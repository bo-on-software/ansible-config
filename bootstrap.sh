#!/bin/bash

Fail() {
	echo $@
	exit 1
}

Try() {
	"$@" || Fail "$* failed!"
}

Try sudo apt-add-repository ppa:ansible/ansible
Try sudo apt-get update
Try sudo apt-get install -y git ansible
Try mkdir -p ~/Projects/
Try git clone https://github.com/bo-on-software/ansible-config.git ~/Projects/ansible-config
Try cd ~/Projects/ansible-config
./run.sh

