1. Move pk-reliant activities from Action.save method into m2m signals

2. Upgrade postgres passwords to scram-sha-256

Steps
  * Take backup of current database
  * Edit out postgis lines from backup dump file
  * Stop docker containers
  * Edit docker-compose.yml and environment configuration
    to switch on scram-sha-256 as default and rename 
    data volume
  * Edit db container's Dockerfile to change container base 
    from postgis to postgres 13
  * Edit Django settings file to use postresql database 
    engine rather than postgis
  * Rebuild containers
  * Spin up containers
  * Load data back in 
  * Test password encryption
  * Test data still in database