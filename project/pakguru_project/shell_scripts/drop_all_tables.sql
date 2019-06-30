-- psql -U postgres
SELECT table_name
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME LIKE 'pak_%';
/*  
DROP TABLE pakguru_app_author CASCADE;
DROP TABLE pakguru_app_post CASCADE;
DROP TABLE pakguru_app_postcategorylist CASCADE;
DROP TABLE pakguru_app_localelist CASCADE;
DROP TABLE pakguru_app_youtubefeeds CASCADE;

*/