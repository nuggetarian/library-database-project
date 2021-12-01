# bpc-bds-project3

# Treba nainštalovať

**ttkbootstrap**

python -m pip install git+https://github.com/israel-dryer/ttkbootstrap

python -m pip install ttkbootstrap

**psycopg2**

pip install psycopg2

**bcrypt**

pip install bcrypt

# Podmienky

- Bcrypt - skutočná validácia usera na základe hesla (Pop up s nesprávnym heslom)

- User rola do databáze (nemôže byť superuser)

- Iná schema ako public

- CRUD (Create, read, update, delete) tlačítka do treeview na aspoň jednu entitu

  - findAll operáciu na jednu operáciu

- Detailný view na jednu entitu (použiť JOIN)

- Transaction rollback atd.

- Filter napríklad by Family Name

- SQL Injection na dummy table

  - Spôsob cez Drop Table
  - Spôsob retrieve viac dát ako treba
  - Vysvetli dôležitosť preparedStatements

- Back up DB every midnight script

- Logging (SLF4J Logback), loguj exceptions (avoid log-and-throw antipattern)

- GitHub

  - .gitignore file
  - readme ako spustiť

- License file (MIT)
  https://github.com/licenses/lice
  pip install lice
  lice mit
