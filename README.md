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

  _pip install psycopg2_

- **bcrypt**

  _pip install bcrypt_
  
# Auto Back-up

**Make sure that the location of these folders are set in Path!**

- C:\Program Files\PostgreSQL\14\bin
- C:\Program Files\PostgreSQL\14\lib

Script back_up.bat is set to back up the database into the windows temp folder.

You need to add this script to task scheduler and set it to midnight everyday. There are pictures in the autobackup folder, as well as the script itself.

```console
set PGPASSWORD=postgres
pg_dump -h "localhost" -U "postgres" -f "C:\Windows\Temp\library" "librarydb"
```

# Podmienky

- ~~Bcrypt - skutočná validácia usera na základe hesla (Pop up s nesprávnym heslom)~~

- ~~User rola do databáze (nemôže byť superuser)~~

- ~~Iná schema ako public~~

- ~~CRUD (Create, read, update, delete) tlačítka do treeview na aspoň jednu entitu~~

  - ~~findAll operáciu na jednu operáciu~~

- ~~Detailný view na jednu entitu (použiť JOIN)~~

- ~~Transaction rollback atd.~~

- ~~Filter napríklad by Family Name~~

- SQL Injection na dummy table

  - ~~Spôsob cez Drop Table~~
  - Spôsob retrieve viac dát ako treba
  - ~~Vysvetli dôležitosť preparedStatements~~

- Back up DB every midnight script

- ~~Logging (SLF4J Logback), loguj exceptions (avoid log-and-throw antipattern)~~

- ~~GitHub~~

  - ~~.gitignore file~~
  - ~~readme ako spustiť~~

- ~~License file (MIT)~~
  - ~~https://github.com/licenses/lice~~
  - ~~pip install lice~~
  - ~~lice mit~~

- ~~Licenses of external libraries~~
  - ~~https://github.com/raimon49/pip-licenses~~
  - ~~pip install -U pip-licenses~~
  - ~~pip-licenses --order=license --format=html~~

# Some Info

**pip-licenses** has been used to generate licenses of external libraries. Unused libraries have been removed from the .html

# Obhajoba - Prezentácia

1. Title slide:
   – your project name
   – your name
   – your study programme and your year of study
2. Motivation slide:
   – describe your project
   – what your project is dealing with?
3. Project intro:
   – show your ERD
4. Project changes:
   – describe what did you change in your project during the development (e.g., based on
   evaluations)
5. Project DEMO:
   – show several screens from the application
   – run the project and show the project to your seminar tutor (show several project functionalities)
6. Conclusion:
   – describe what would you change if you would develop such a project next time
   – where did you stuck and what was the most difficult part

# Licenses of external libraries in markdown format (because it looks pretty)

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


