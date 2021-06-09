SELECT 
IF (LAST_UPDATE_TIME IS NOT NULL,'In Use','') Status,
DATABASE_NAME,
APP_NAME,
`DB Size in MB`,
IFNULL(LAST_UPDATE_TIME,'N/A') LAST_UPDATE_TIME
FROM
(SELECT
TABLE_SCHEMA DATABASE_NAME,
CASE
WHEN TABLE_SCHEMA = 'db_comwave_call_tracker_ties' THEN 'Comwave Call Tracker'
WHEN TABLE_SCHEMA = 'db_pbx_lrt_global' THEN 'PBX'
WHEN TABLE_SCHEMA = 'db_benefits_calendar_gt' THEN 'Benefits Calendar TIGT'
WHEN TABLE_SCHEMA = 'db_vap_global' THEN 'Global Entrance'
WHEN TABLE_SCHEMA = 'db_lunch_card' THEN 'Lunch Card GT'
WHEN TABLE_SCHEMA = 'db_performance_follow_up' THEN 'Performance Follow Up'
WHEN TABLE_SCHEMA = 'db_fitbit_logger' THEN 'FitBit Logger'
WHEN TABLE_SCHEMA = 'db_gaia_global' THEN 'Global Coffe Orders'
WHEN TABLE_SCHEMA = 'db_success_factor' THEN 'Success Factors'
WHEN TABLE_SCHEMA = 'db_question2answer' THEN 'Knowledge Database for IS'
WHEN TABLE_SCHEMA = 'db_dba_knowledge' THEN 'Knowledge Database for DBA'
WHEN TABLE_SCHEMA = 'db_badger_global' THEN 'Global Badger'
WHEN TABLE_SCHEMA = 'db_thecore_global' THEN 'Global Thecore'
WHEN TABLE_SCHEMA = 'db_mapping_layer_global' THEN 'Mapping Layer Global'
WHEN TABLE_SCHEMA = 'db_success_factors' THEN 'Success Factors'
WHEN TABLE_SCHEMA = 'db_automatic_creation' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_core' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_araneta' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_arizona' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_austin' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_cascadas' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_cocopat' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_information_services' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_is' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_las_vegas' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_market' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_mckinley' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_mckinley_west' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_merliot' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_ortigas_center' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_pradera_west' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_torre_pradera' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_wfc' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_wtc' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_instance_xela' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_global_logger' THEN 'Glogger'
WHEN TABLE_SCHEMA = 'db_glogger_avaya_integrator' THEN 'Avaya Integrator'
WHEN TABLE_SCHEMA = 'db_mapping_layer' THEN 'Mapping Layer'
WHEN TABLE_SCHEMA = 'db_r2w_global' THEN ''
WHEN TABLE_SCHEMA = 'db_tracmor' THEN ''
WHEN TABLE_SCHEMA = 'db_osticket_workday_global' THEN ''
WHEN TABLE_SCHEMA = 'db_payroll_dispute_global' THEN ''
WHEN TABLE_SCHEMA = 'db_hr_osticket_us' THEN ''
WHEN TABLE_SCHEMA = 'db_asset_osticket' THEN ''
WHEN TABLE_SCHEMA = 'db_global_roster' THEN ''
WHEN TABLE_SCHEMA = 'db_benefits' THEN ''
WHEN TABLE_SCHEMA = 'db_global_coaching_reports' THEN ''
WHEN TABLE_SCHEMA = 'db_ticket_central' THEN ''
WHEN TABLE_SCHEMA = 'db_anniversary' THEN ''
WHEN TABLE_SCHEMA = 'db_donations_global' THEN ''
WHEN TABLE_SCHEMA = 'db_hermes' THEN ''
WHEN TABLE_SCHEMA = 'db_reader_esb' THEN ''
WHEN TABLE_SCHEMA = 'mysql' THEN 'system'
WHEN TABLE_SCHEMA = 'sys' THEN 'system'
WHEN TABLE_SCHEMA = 'information_schema' THEN 'system'
WHEN TABLE_SCHEMA = 'performance_schema' THEN 'system'
ELSE ''
END AS APP_NAME,
ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) 'DB Size in MB',
DATE_FORMAT(MAX(UPDATE_TIME), "%d %M %Y") LAST_UPDATE_TIME
FROM   INFORMATION_SCHEMA.TABLES
GROUP BY DATABASE_NAME,APP_NAME
) TEMP
ORDER BY 4 DESC;
