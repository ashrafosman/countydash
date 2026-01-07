-- Run in Databricks SQL. Set catalog/schema before executing.
-- Example:
-- USE CATALOG main;
-- USE SCHEMA default;

CREATE TABLE IF NOT EXISTS county_profiles (
  county_id STRING,
  name STRING,
  is_active BOOLEAN,
  population BIGINT,
  medi_cal_enrolled BIGINT,
  bh_services_annual BIGINT,
  annual_expenditures BIGINT,
  latitude DOUBLE,
  longitude DOUBLE,
  contact_department STRING,
  contact_address STRING,
  contact_city STRING,
  contact_phone STRING,
  contact_email STRING,
  demographics_json STRING,
  behavioral_health_json STRING,
  expenditures_json STRING,
  homelessness_json STRING,
  integrated_plan_json STRING,
  performance_json STRING,
  updated_at TIMESTAMP
)
USING DELTA;

CREATE TABLE IF NOT EXISTS review_comments (
  id STRING,
  element_name STRING,
  page_url STRING,
  comment_text STRING,
  selected_text STRING,
  author STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
USING DELTA;
