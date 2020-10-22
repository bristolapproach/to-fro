# Deployment

1. Install Ansible on your system and activate the Python virtual environment by following [these instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). A summary of them can be found below.

   ```bash
   # Create the Ansible virtual environment
   python3 -m venv ~/ansible-env

   # Activate the ansible environment
   source ~/ansible-env/bin/activate

   # Install Ansible
   pip install ansible
   ```

2. Clone the repository

   `git clone git@github.com:cgillions/to-fro.git`

3. Move into the directory

   `cd tofro/deployment`

4. Install the Ansible requirements

   ```bash
   # Activate the ansible environment
   source ~/ansible-env/bin/activate

   # Install project's ansible-galaxy requirements
   ansible-galaxy install -r ansible-requirements.yml
   ```

5. Get the `vault_password` file from the project administrator

   This file contains a password that's used to encrypt sensitive information in the Playbook

6. Run the Playbook, specifying the development inventory file

   ```bash
   # Activate the ansible environment
   source ~/ansible-env/bin/activate

   # Run the playbook, deploying to {dev,prod}
   ansible-playbook -i environments/dev --vault-password vault_password site.yml
   ```

## Changing variables

The following command can be used to view and edit the encrypted variables:

```bash
# Activate the ansible environment
source ~/ansible-env/bin/activate

# Run the ansible-vault command, specifying the password file and the encrypted file.
ansible-vault edit --vault-password-file vault_password environments/dev/group_vars/all.yml
```
