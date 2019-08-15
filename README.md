[defaults setup role]: https://github.com/vengaar/liftree/tree/master/setup/playbooks/roles/setup/defaults

# liftree

SWGI application to browse text files and display them via jinja2 templates

# Setup

## Prerequisite

* For installation
  * Git
  * Ansible
* Python => 3.6

### Defaults

* The default settings are available in defaults of ansible setup role
* See [defaults setup role]
* By default liftree run on port 8043 but you override it with an ansible extra_vars as `-e "wsgi_port=80"`


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

* http://{your_ip}:8043/info
* http://{your_ip}:8043/mock
* http://{your_ip}:8043/mock?query=an
* http://{your_ip}:8043/search
* http://{your_ip}:8043/search?query=data/test
* http://{your_ip}:8043/show
