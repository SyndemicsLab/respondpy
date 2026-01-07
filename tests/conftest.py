################################################################################
# File: data_definitions.py                                                    #
# Project: respondpy                                                           #
# Created Date: 2025-11-24                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-01-07                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center               #
################################################################################
import pytest


@pytest.fixture(scope="module")
def db_schema():
    """Fixture to provide the database schema for testing

    Returns:
        str: The database schema SQL string
    """
    return """
DROP TABLE IF EXISTS "background_mortality";
CREATE TABLE "background_mortality" (
	"cohort"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("cohort","time"),
	FOREIGN KEY("cohort") REFERENCES "cohort"("id")
);
DROP TABLE IF EXISTS "behavior";
CREATE TABLE "behavior" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "behavior_transition";
CREATE TABLE "behavior_transition" (
	"cohort"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"initial_behavior"	INTEGER NOT NULL,
	"new_behavior"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("cohort","intervention","time","initial_behavior","new_behavior"),
	FOREIGN KEY("cohort") REFERENCES "cohort"("id"),
	FOREIGN KEY("initial_behavior") REFERENCES "behavior"("id"),
	FOREIGN KEY("intervention") REFERENCES "intervention"("id"),
	FOREIGN KEY("new_behavior") REFERENCES "behavior"("id")
);
DROP TABLE IF EXISTS "cohort";
CREATE TABLE "cohort" (
	"id"	INTEGER NOT NULL UNIQUE,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "cohort_demographics";
CREATE TABLE "cohort_demographics" (
	"cohort_id"	INTEGER NOT NULL,
	"demographic_id"	INTEGER NOT NULL,
	PRIMARY KEY("cohort_id","demographic_id"),
	FOREIGN KEY("cohort_id") REFERENCES "cohort"("id"),
	FOREIGN KEY("demographic_id") REFERENCES "demographics"("id")
);
DROP TABLE IF EXISTS "demographics";
CREATE TABLE "demographics" (
	"id"	INTEGER NOT NULL UNIQUE,
	"type"	TEXT NOT NULL,
	"value"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "initial_population";
CREATE TABLE "initial_population" (
	"cohort"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"count"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("cohort","intervention","behavior")
);
DROP TABLE IF EXISTS "intervention";
CREATE TABLE "intervention" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "intervention_transition";
CREATE TABLE "intervention_transition" (
	"cohort"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"initial_intervention"	INTEGER NOT NULL,
	"new_intervention"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("cohort","behavior","initial_intervention","new_intervention","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
	FOREIGN KEY("cohort") REFERENCES "cohort"("id"),
	FOREIGN KEY("initial_intervention") REFERENCES "intervention"("id"),
	FOREIGN KEY("new_intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "overdose";
CREATE TABLE "overdose" (
	"intervention"	INTEGER NOT NULL,
	"cohort"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("intervention","cohort","behavior","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
	FOREIGN KEY("cohort") REFERENCES "cohort"("id"),
	FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "overdose_fatality";
CREATE TABLE "overdose_fatality" (
	"cohort"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("cohort","intervention","behavior","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
	FOREIGN KEY("cohort") REFERENCES "cohort"("id"),
	FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "population_change";
CREATE TABLE "population_change" (
	"cohort"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"count"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("cohort","intervention","behavior","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
	FOREIGN KEY("cohort") REFERENCES "cohort"("id"),
	FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "smr";
CREATE TABLE "smr" (
	"cohort"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"ratio"	REAL NOT NULL DEFAULT 1.0,
	PRIMARY KEY("time","behavior","intervention","cohort"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
	FOREIGN KEY("cohort") REFERENCES "cohort"("id"),
	FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
"""


@pytest.fixture(scope="module")
def db_cohort_insert():
    """FIxture to insert a cohort into the database for testing

    Returns:
        str: The cohort insertion SQL string
    """
    return """
INSERT INTO cohort (id, description) VALUES (1, "Test Cohort 1");"""


@pytest.fixture(scope="module")
def db_intervention_insert():
    return """
INSERT INTO intervention (id, name) VALUES (1, "No_Treatment), (2, Buprenorphine);"""


@pytest.fixture(scope="module")
def db_behavior_insert():
    return """
INSERT INTO behavior (id, name) VALUES (1, "Active_Injection"), (2, "Nonactive_Injection");"""


@pytest.fixture(scope="module")
def db_population_insert():
    return """
INSERT INTO initial_population (cohort, intervention, behavior, count) VALUES (1, 1, 1, 100), (1, 1, 2, 150), (1, 2, 1, 200), (1, 2, 2, 250);"""
