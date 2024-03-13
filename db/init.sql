-- Read variables from the environment.
\set main_user `echo "${POSTGRES_USER}"`
\set bcc_user `echo "${POSTGRES_BCC_USER}"`
\set bcc_password `echo "${POSTGRES_BCC_PASSWORD}"`

-- Change password encryption
ALTER SYSTEM SET PASSWORD_ENCRYPTION = 'SCRAM-SHA-256';
SELECT PG_RELOAD_CONF();


-- Create the database for BCC.
CREATE DATABASE bcc;
CREATE USER :bcc_user WITH PASSWORD :'bcc_password';
GRANT ALL PRIVILEGES ON DATABASE bcc TO :bcc_user;
GRANT ALL PRIVILEGES ON DATABASE bcc TO :main_user;
