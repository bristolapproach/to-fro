# Deployment

1. Install Ansible on your system and activate the Python virtual environment by following [these instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

2. Clone the repository

   `git clone git@github.com:cgillions/to-fro.git`

3. Move into the directory

   `cd tofro/deployment`

4. Install the Ansible requirements

   `ansible-galaxy install -r requirements.yml`

5. Get the `vault_password` file from the project administrator

   This file contains a password that's used to encrypt sensitive information in the Playbook

6. Run the Playbook, specifying the development inventory file
  
   `ansible-playbook -i environments/prod --vault-password vault_password site.yml`

## Changing variables

The following command can be used to view and edit the encrypted variables:

    ansible-vault edit --vault-password-file vault_password tofro/vars/main.yml
