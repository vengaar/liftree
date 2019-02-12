# liftree

SWGI application to browse text files and display them via jinja2 templates

# Setup

## Prerequisite

* For installation
  * Git
  * Ansible
* Python => 3.6

## Procedure


### Ubuntu >= 18

As root on your server

~~~~
apt install ansible
git clone https://github.com/vengaar/liftree.git
ansible-playbook liftree/setup/playbooks/setup.yml
~~~~

### Fedora >= 28

As root on your server

~~~~
dnf install ansible
git clone https://github.com/vengaar/liftree.git
ansible-playbook liftree/setup/playbooks/setup.yml
~~~~

### To test devel

~~~~
git clone https://github.com/vengaar/liftree.git
cd liftree
git chekout devel
git pull
ansible-playbook setup/playbooks/setup.yml -e "git_version=devel"
~~~~


## Test

Test url:

* http://{your_ip}/info
* http://{your_ip}/mock
* http://{your_ip}/mock?query=an
* http://{your_ip}/search
* http://{your_ip}/search?query=data/test
* http://{your_ip}/show
