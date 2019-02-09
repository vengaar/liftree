# liftree

SWGI application to browse text files and display them via jinja2 templates

# Setup

## Prerequisite

* For installation
  * Git
  * Ansible installed with python3
* Python => 3.6
* OS
  * Ubuntu >= 18.04.1 LTS
  * fedora >= 28

## Procedure

### Ubuntu

**CAUTION : Need to use pip3, else with apt ansible in stack python2**

As root on your server

~~~~
apt install python3-pip
pip3 install ansible
git clone https://github.com/vengaar/liftree.git
ansible-playbook /home/liftree/liftree/setup/playbooks/setup.yml
~~~~

### Fedora

* For fedora 28

~~~~
dnf install ansible-python3
git clone https://github.com/vengaar/liftree.git
ansible-playbook-3 /home/liftree/liftree/setup/playbooks/setup.yml
~~~~

* For fedora 29

~~~~
dnf install ansible
git clone https://github.com/vengaar/liftree.git
ansible-playbook /home/liftree/liftree/setup/playbooks/setup.yml
~~~~

*NB : To install devel version add `-e "git_version=devel"`to ansible command line above*

## Test

Test url:

* http://{your_ip}/info
* http://{your_ip}/mock
* http://{your_ip}/mock?query=an
* http://{your_ip}/search
* http://{your_ip}/search?query=data/test
* http://{your_ip}/show
