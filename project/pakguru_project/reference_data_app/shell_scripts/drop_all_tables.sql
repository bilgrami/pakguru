-- psql -U postgres
/*  
SELECT concat('DROP TABLE ',table_name, ' CASCADE;')
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME LIKE 'reference_data_app_%';
*/
