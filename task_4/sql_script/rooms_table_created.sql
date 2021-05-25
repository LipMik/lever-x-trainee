use leverx_db;

drop table if exists rooms;

CREATE TABLE rooms(
  id INT NOT NULL,
  name VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));