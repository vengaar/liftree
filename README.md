# liftree
SWGI application to browse text files and display them via jinja2 templates

# Setup

## Prerequisite

fedora 29

## Procedure
As root on your server

~~~~
useradd liftree
su - liftree
git clone https://github.com/vengaar/liftree.git
exit
ansible-playbook /home/liftree/liftree/setup/playbooks/setup.yml -v
~~~~

## Test
Test url:

* http://{your_ip}/info
* http://{your_ip}/search
* http://{your_ip}/show
* http://{your_ip}/show?path=/home/liftree/liftree/example/data/test.md

# unittest

## All unittest
python3 -m unittest discover -s test/

## One test with debug
python3 test/test_render.py
