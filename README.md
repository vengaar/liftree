# liftree
SWGI application to browse text files and display them via jinja2 templates

# Setup

rpm dependencies :

On root on server

~~~~
useradd liftree
su - liftree
git clone https://github.com/vengaar/liftree.git
exit
ansible-playbook /home/liftree/liftree/setup/setup.yml
~~~~

go on `http://{your_ip}/info`
go on `http://{your_ip}/search`
go on `http://{your_ip}/show?path=/home/liftree/liftree/example/data/test.md`
