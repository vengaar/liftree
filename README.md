# liftree
SWGI application to browse text files and display them via jinja2 templates

# Setup

## Prerequisite

python => 3.6
fedora => 28

## Procedure
As root on your server

on fedora 28

~~~~
dnf install ansible-python3
git clone https://github.com/vengaar/liftree.git
ansible-playbook-3 /home/liftree/liftree/setup/playbooks/setup.yml -v
~~~~

on fedora 29

~~~~
dnf install ansible
git clone https://github.com/vengaar/liftree.git
ansible-playbook /home/liftree/liftree/setup/playbooks/setup.yml -v
~~~~

## Test
Test url:

* http://{your_ip}/info
* http://{your_ip}/mock
* http://{your_ip}/mock?query=an
* http://{your_ip}/search
* http://{your_ip}/search?query=data/test
* http://{your_ip}/show
