use leverx_db;

ALTER TABLE `leverx_db`.`students`
ADD INDEX `ind_sex` USING BTREE (`sex`) VISIBLE;