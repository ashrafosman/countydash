import json
import os
from datetime import datetime, timezone

from pyspark.sql import SparkSession


def _get_catalog_and_schema():
    catalog = os.getenv("DB_CATALOG", "main")
    schema = os.getenv("DB_SCHEMA", "default")
    return catalog, schema


def _serialize(payload):
    return json.dumps(payload, separators=(",", ":"))


def main():
    catalog, schema = _get_catalog_and_schema()
    spark = SparkSession.builder.getOrCreate()

    counties = [
        {
            "county_id": "los-angeles",
            "name": "Los Angeles",
            "is_active": True,
            "population": 10040682,
            "medi_cal_enrolled": 3524319,
            "bh_services_annual": 287000,
            "annual_expenditures": 2800000000,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "contact_department": "Los Angeles County Department of Mental Health",
            "contact_address": "550 S. Vermont Avenue",
            "contact_city": "Los Angeles, CA 90020",
            "contact_phone": "(800) 854-7771",
            "contact_email": "info@dmh.lacounty.gov",
            "demographics_json": _serialize(
                {
                    "population_by_age": [
                        {"age": "0-17", "population": 2309157, "percent": 23},
                        {"age": "18-24", "population": 1104849, "percent": 11},
                        {"age": "25-44", "population": 2911641, "percent": 29},
                        {"age": "45-64", "population": 2208932, "percent": 22},
                        {"age": "65+", "population": 1506103, "percent": 15},
                    ],
                    "population_by_ethnicity": [
                        {"ethnicity": "Hispanic/Latino", "value": 4820150, "percent": 48},
                        {"ethnicity": "White", "value": 2610977, "percent": 26},
                        {"ethnicity": "Asian", "value": 1505682, "percent": 15},
                    ],
                }
            ),
            "behavioral_health_json": _serialize(
                {
                    "penetration_rates": [
                        {"service": "Specialty MH", "rate": 5.3, "benchmark": 6.2, "status": "Below"},
                        {"service": "SUD Treatment", "rate": 2.1, "benchmark": 3.0, "status": "Below"},
                    ],
                    "access_metrics": [
                        {"quarter": "Q1", "first_contact": 72, "engagement": 68, "initiation": 55},
                        {"quarter": "Q2", "first_contact": 74, "engagement": 70, "initiation": 57},
                    ],
                }
            ),
            "expenditures_json": _serialize(
                {
                    "by_category": [
                        {"category": "Outpatient", "amount": 820000000, "percent": 29},
                        {"category": "Inpatient", "amount": 650000000, "percent": 23},
                    ],
                    "trend_data": [
                        {"year": "2022", "actual": 2500000000, "projected": 2550000000},
                        {"year": "2023", "actual": 2700000000, "projected": 2750000000},
                    ],
                }
            ),
            "homelessness_json": _serialize(
                {
                    "hdis_enrolled": 12450,
                    "housing_interventions": [
                        {"type": "Permanent Supportive", "clients": 3200},
                        {"type": "Rapid Rehousing", "clients": 1800},
                    ],
                }
            ),
            "integrated_plan_json": _serialize(
                {
                    "status": "Submitted",
                    "phase": "Draft",
                    "completion_date": "2025-06-30",
                    "budget_allocations": [
                        {"category": "Workforce", "amount": 120000000},
                        {"category": "Infrastructure", "amount": 90000000},
                    ],
                }
            ),
            "performance_json": _serialize(
                {
                    "phase2_measures": [
                        {"measure": "Follow-up 7 days", "target": 60, "actual": 54, "status": "Below"},
                        {"measure": "Engagement 30 days", "target": 70, "actual": 72, "status": "On Track"},
                    ],
                    "compliance_rate": 88,
                    "monitoring_reports": 12,
                }
            ),
            "updated_at": datetime.now(timezone.utc),
        },
        {
            "county_id": "san-diego",
            "name": "San Diego",
            "is_active": True,
            "population": 3341440,
            "medi_cal_enrolled": 1203500,
            "bh_services_annual": 110000,
            "annual_expenditures": 1200000000,
            "latitude": 32.7157,
            "longitude": -117.1611,
            "contact_department": "San Diego County Behavioral Health Services",
            "contact_address": "3851 Rosecrans Street",
            "contact_city": "San Diego, CA 92110",
            "contact_phone": "(619) 563-2700",
            "contact_email": "bhs@sdcounty.ca.gov",
            "demographics_json": _serialize(
                {
                    "population_by_age": [
                        {"age": "0-17", "population": 700000, "percent": 21},
                        {"age": "18-64", "population": 2200000, "percent": 66},
                        {"age": "65+", "population": 441440, "percent": 13},
                    ]
                }
            ),
            "behavioral_health_json": _serialize(
                {
                    "penetration_rates": [
                        {"service": "Specialty MH", "rate": 5.9, "benchmark": 6.2, "status": "Near"},
                        {"service": "SUD Treatment", "rate": 2.8, "benchmark": 3.0, "status": "Near"},
                    ]
                }
            ),
            "expenditures_json": _serialize(
                {
                    "by_category": [
                        {"category": "Outpatient", "amount": 320000000, "percent": 27},
                        {"category": "Inpatient", "amount": 260000000, "percent": 22},
                    ]
                }
            ),
            "homelessness_json": _serialize({"hdis_enrolled": 5600}),
            "integrated_plan_json": _serialize({"status": "Submitted", "phase": "Draft"}),
            "performance_json": _serialize({"compliance_rate": 90, "monitoring_reports": 8}),
            "updated_at": datetime.now(timezone.utc),
        },
    ]

    comments = [
        {
            "id": "seed-1",
            "element_name": "Total Population",
            "page_url": "county-profile",
            "comment_text": "Validate against latest census estimates.",
            "selected_text": None,
            "author": "Data Team",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
    ]

    counties_df = spark.createDataFrame(counties)
    comments_df = spark.createDataFrame(comments)

    counties_df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.county_profiles")
    comments_df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.review_comments")


if __name__ == "__main__":
    main()
