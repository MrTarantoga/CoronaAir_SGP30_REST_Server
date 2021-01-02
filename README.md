# CoronaAir_SGP30_REST_Server

This project conatins all needed files for the rest server that collects data.

Requirements (tested with version):

- [x] Flask==1.1.2

- [x] requests==2.21.0

- [x] SQLAlchemy==1.3.22

- [x] systemd==0.16.1

- [x] pyzbar==0.1.8

- [x] seaborn==0.11.1

- [x] matplotlib==3.3.3

- [x] pandas==1.2.0

- [x] numpy==1.19.4

- [x] Pillow==8.0.1

# sgp_30

| Field       | Type                | Null | Key | Default | Extra          |
| ----------- | ------------------- | ---- | --- | ------- | -------------- |
| id          | int(10) unsigned    | NO   | PRI | NULL    | auto_increment |
| sensor_id   | bigint(16) unsigned | NO   |     | NULL    |                |
| temperature | float               | NO   |     | NULL    |                |
| eCO2        | int(5)              | NO   |     | NULL    |                |
| raw_Ethanol | int(5)              | NO   |     | NULL    |                |
| raw_H2      | int(5)              | NO   |     | NULL    |                |
| pressure    | float               | NO   |     | NULL    |                |
| humidity    | float               | NO   |     | NULL    |                |
| TVOC        | int(5)              | NO   |     | NULL    |                |
| timestamp   | varchar(45)         | NO   |     | NULL    |                |

For the **sgp_30_db.service** you need a databse URI. Please refer:  [Engine Configuration](https://docs.sqlalchemy.org/en/13/core/engines.html)

For the gunicorn config please refer: [Running Gunicorn &mdash; Gunicorn 20.0.4 documentation](https://docs.gunicorn.org/en/latest/run.html)
