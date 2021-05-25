use leverx_db;

drop table if exists students;

CREATE TABLE students(
  id INT NOT NULL,
  name VARCHAR(90) NOT NULL,
  birthday DATE NOT NULL,
  room INT NOT NULL,
  sex VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX fk_students_1_idx (room ASC) VISIBLE,
  CONSTRAINT fk_students_1
    FOREIGN KEY (room)
    REFERENCES `leverx_db`.`rooms` (`id`)
    ON DELETE cascade
    ON UPDATE NO ACTION);