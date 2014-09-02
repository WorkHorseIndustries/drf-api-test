# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  #https://docs.vagrantup.com/v2/vagrantfile/machine_settings.html

  config.vm.box = "hashicorp/precise64"
  config.vm.box_check_update = true


  #####  PROVIDER SETTINGS #################
  #https://docs.vagrantup.com/v2/virtualbox/configuration.html

  config.vm.provider :virtualbox 

  #####  PROVISION VIRTUAL MACHINE #########
  #https://docs.vagrantup.com/v2/provisioning/index.html

  #Docker provisions
  #https://docs.vagrantup.com/v2/provisioning/docker.html

  #Install Docker, build an image from a Dockerfile that lives in the root vagrant
  config.vm.provision "docker"


  #Shell provision
  #https://docs.vagrantup.com/v2/provisioning/shell.html

  config.vm.provision "shell", inline: "apt-get install -y python-pip"
  config.vm.provision "shell", inline: "pip install -U fig"


  ##### NETWORKING SETTINGS ################
  #https://docs.vagrantup.com/v2/networking/

  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "private_network", ip: "192.168.50.4"

  #want a different shell when you ssh into vagrant? You can use this command.
  #config.ssh.shell 

end
