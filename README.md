# bpc-bds-project3

# Set Up

Download PostgreSQL
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

Set up pgAdmin

File -> Preferences -> Binary paths -> Add pgAdmin paths

Make sure the port is set to 5432

Create a server named BPC-BDS, set the following login information:
- Username: postgres
- Password: postgres

Create a database named librarydb

Within the database, restore the file named 'library'

Start the application

## Alternatively

Clone https://gitlab.com/but-courses/bpc-bds/bpc-bds-db-setup

Run the repository with docker-compose up

Go to the web page: http://localhost/pgadmin4/

Login with the following credentials:
- Username: johndoe@email.cz
- Password: postgres

Afterwards follow the steps from the previous method

# Log In

E-mail: kibo@email.com

Password: batman

# Requirements

- **ttkbootstrap**

  _python -m pip install git+https://github.com/israel-dryer/ttkbootstrap_

  _python -m pip install ttkbootstrap_

- **psycopg2**

  _pip install psycopg2_ **or** *pip install psycopg2-binary*

- **bcrypt**

  _pip install bcrypt_
  
# Auto Back-up

**Make sure that the location of these folders are set in Path!**

- C:\Program Files\PostgreSQL\14\bin
- C:\Program Files\PostgreSQL\14\lib

Script [back_up.bat](/autobackup/back_up.bat) is set to back up the database into the windows temp folder with the filename '*library*'.

You need to add this script to task scheduler and set it to midnight. There are pictures in the [autobackup](/autobackup/) folder, as well as the script itself.

```bat
set PGPASSWORD=postgres
pg_dump -h "localhost" -U "postgres" -f "C:\Windows\Temp\library" "librarydb"
```

# Some Info

[pip-licenses](https://github.com/raimon49/pip-licenses) has been used to generate licenses of external libraries. Unused libraries have been removed from the .html

# Licenses of external libraries in markdown format

| Name              | Version | License                                             |
|-------------------|---------|-----------------------------------------------------|
| Pillow            | 8.4.0   | Historical Permission Notice and Disclaimer (HPND)  |
| bcrypt            | 3.2.0   | Apache Software License                             |
| lice              | 0.6     | BSD License                                         |
| psycopg2          | 2.9.2   | GNU Library or Lesser General Public License (LGPL) |
| psycopg2-binary   | 2.9.2   | GNU Library or Lesser General Public License (LGPL) |
| ttkbootstrap      | 1.0.0   | MIT License                                         |

# License

Copyright 2021 Michal Žernovič

Licensed under the [MIT License](LICENSE)


