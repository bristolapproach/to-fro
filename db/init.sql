-- Read variables from the environment.
\set main_user `echo "$POSTGRES_USER"`


-- Create the database for tofro.
-- CREATE USER tofro;
-- CREATE DATABASE tofro;
-- GRANT ALL PRIVILEGES ON DATABASE tofro TO tofro;

-- Create the database for BCC.
CREATE USER bcc;
CREATE DATABASE bcc;
GRANT ALL PRIVILEGES ON DATABASE bcc TO bcc;
GRANT ALL PRIVILEGES ON DATABASE bcc TO :main_user;
