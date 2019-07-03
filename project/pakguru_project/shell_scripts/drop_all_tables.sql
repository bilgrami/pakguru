-- psql -U postgres
/*  
SELECT concat('DROP TABLE ',table_name, ' CASCADE;')
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME LIKE 'pakguru_app_%';
*/
/*
DROP TABLE pakguru_app_author CASCADE;
DROP TABLE pakguru_app_showsourcefeed_country CASCADE;
DROP TABLE pakguru_app_showchannel CASCADE;
DROP TABLE pakguru_app_showsourcefeed CASCADE;
DROP TABLE pakguru_app_show_additional_feeds CASCADE;
DROP TABLE pakguru_app_show_country CASCADE;
DROP TABLE pakguru_app_poststatistic CASCADE;
DROP TABLE pakguru_app_postcategorylist CASCADE;
DROP TABLE pakguru_app_countrylist CASCADE;
DROP TABLE pakguru_app_post_country CASCADE;
DROP TABLE pakguru_app_localelist CASCADE;
DROP TABLE pakguru_app_show CASCADE;
DROP TABLE pakguru_app_post CASCADE;
DROP TABLE pakguru_app_showfeed_harvestjoblog CASCADE;
*/
/*
DROP TABLE auth_permission CASCADE;
DROP TABLE auth_group CASCADE;
DROP TABLE auth_group_permissions CASCADE;
DROP TABLE auth_user_groups CASCADE;
DROP TABLE auth_user CASCADE;
DROP TABLE auth_user_user_permissions CASCADE;

DROP TABLE django_migrations CASCADE;
DROP TABLE django_content_type CASCADE;
DROP TABLE django_admin_log CASCADE;
DROP TABLE django_session CASCADE;

*/
