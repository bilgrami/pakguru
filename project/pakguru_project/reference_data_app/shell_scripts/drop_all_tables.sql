-- psql -U postgres
/*  
SELECT concat('DROP TABLE ',table_name, ' CASCADE;')
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME LIKE 'reference_data_%';
*/
/*
 DROP TABLE reference_data_source_type CASCADE;
 DROP TABLE reference_data_show_info CASCADE;
 DROP TABLE reference_data_show_episode_info CASCADE;
*/