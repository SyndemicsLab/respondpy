################################################################################
# File: conftest.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2025-11-24                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-02-26                                                    #
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
DROP TABLE IF EXISTS "intervention";
CREATE TABLE "intervention" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "behavior";
CREATE TABLE "behavior" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "background_mortality";
CREATE TABLE "background_mortality" (
	"sample"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("sample","time")
);
DROP TABLE IF EXISTS "behavior_transition";
CREATE TABLE "behavior_transition" (
	"sample"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"initial_behavior"	INTEGER NOT NULL,
	"new_behavior"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("sample","intervention","time","initial_behavior","new_behavior"),
    FOREIGN KEY("initial_behavior") REFERENCES "behavior"("id"),
	FOREIGN KEY("intervention") REFERENCES "intervention"("id"),
	FOREIGN KEY("new_behavior") REFERENCES "behavior"("id")
);
DROP TABLE IF EXISTS "initial_population";
CREATE TABLE "initial_population" (
	"sample"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"count"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("sample","intervention","behavior")
);
DROP TABLE IF EXISTS "intervention_transition";
CREATE TABLE "intervention_transition" (
	"sample"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"initial_intervention"	INTEGER NOT NULL,
	"new_intervention"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("sample","behavior","initial_intervention","new_intervention","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
    FOREIGN KEY("initial_intervention") REFERENCES "intervention"("id"),
	FOREIGN KEY("new_intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "overdose";
CREATE TABLE "overdose" (
	"intervention"	INTEGER NOT NULL,
	"sample"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("intervention","sample","behavior","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "overdose_fatality";
CREATE TABLE "overdose_fatality" (
	"sample"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"probability"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("sample","intervention","behavior","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "population_change";
CREATE TABLE "population_change" (
	"sample"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"count"	REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("sample","intervention","behavior","time"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "smr";
CREATE TABLE "smr" (
	"sample"	INTEGER NOT NULL,
	"intervention"	INTEGER NOT NULL,
	"behavior"	INTEGER NOT NULL,
	"time"	INTEGER NOT NULL,
	"ratio"	REAL NOT NULL DEFAULT 1.0,
	PRIMARY KEY("sample","time","behavior","intervention"),
	FOREIGN KEY("behavior") REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "cohort";
CREATE TABLE "cohort" (
	"id"	INTEGER NOT NULL UNIQUE,
	"description"	TEXT,
    "background_mortality_sample" INTEGER NOT NULL,
    "behavior_transition_sample" INTEGER NOT NULL,
    "initial_population_sample" INTEGER NOT NULL,
    "intervention_transition_sample" INTEGER NOT NULL,
    "overdose_sample" INTEGER NOT NULL,
    "overdose_fatality_sample" INTEGER NOT NULL,
    "population_change_sample" INTEGER NOT NULL,
    "smr_sample" INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("background_mortality_sample") REFERENCES "background_mortality"("sample"),
    FOREIGN KEY("behavior_transition_sample") REFERENCES "behavior_transition"("sample"),
    FOREIGN KEY("initial_population_sample") REFERENCES "initial_population"("sample"),
    FOREIGN KEY("intervention_transition_sample") REFERENCES "intervention_transition"("sample"),
    FOREIGN KEY("overdose_sample") REFERENCES "overdose"("sample"),
    FOREIGN KEY("overdose_fatality_sample") REFERENCES "overdose_fatality"("sample"),
    FOREIGN KEY("population_change_sample") REFERENCES "population_change"("sample"),
    FOREIGN KEY("smr_sample") REFERENCES "smr"("sample")
);
DROP TABLE IF EXISTS "demographics";
CREATE TABLE "demographics" (
	"id"	INTEGER NOT NULL UNIQUE,
	"type"	TEXT NOT NULL,
	"value"	TEXT NOT NULL,
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
"""


@pytest.fixture(scope="module")
def db_cohort_insert():
    """Fixture to insert a cohort into the database for testing

    Returns:
        str: The cohort insertion SQL string
    """
    return """
INSERT INTO cohort (id, description, background_mortality_sample, behavior_transition_sample, initial_population_sample, intervention_transition_sample, overdose_sample, overdose_fatality_sample, population_change_sample, smr_sample) VALUES (1, "Test Cohort 1", 1, 1, 1, 1, 1, 1, 1, 1);"""


@pytest.fixture(scope="module")
def db_intervention_insert():
    return """
INSERT INTO intervention (id, name) VALUES (1, "no_treatment"), (2, "buprenorphine");"""


@pytest.fixture(scope="module")
def db_behavior_insert():
    return """
INSERT INTO behavior (id, name) VALUES (1, "active_injection"), (2, "nonactive_injection");"""


@pytest.fixture(scope="module")
def db_population_insert():
    return """
INSERT INTO initial_population (sample, intervention, behavior, count) VALUES (1, 1, 1, 100), (1, 1, 2, 150), (1, 2, 1, 200), (1, 2, 2, 250);"""


@pytest.fixture(scope="module")
def db_migration_insert():
    return """
INSERT INTO population_change (sample, intervention, behavior, time, count) VALUES (1, 1, 1, 1, 100), (1, 1, 2, 1, 150), (1, 2, 1, 1, 200), (1, 2, 2, 1, 250);"""


@pytest.fixture(scope="module")
def db_intervention_transition_insert():
    return """
INSERT INTO intervention_transition (sample, behavior, time, initial_intervention, new_intervention, probability) VALUES (1, 1, 1, 1, 1, 0.75), (1, 1, 1, 1, 2, 0.25), (1, 1, 1, 2, 1, 0.0), (1, 1, 1, 2, 2, 1.0), (1, 2, 1, 1, 1, 0.75), (1, 2, 1, 1, 2, 0.25), (1, 2, 1, 2, 1, 0.2), (1, 2, 1, 2, 2, 0.8);"""


@pytest.fixture(scope="module")
def db_behavior_transition_insert():
    return """
INSERT INTO behavior_transition (sample, intervention, time, initial_behavior, new_behavior, probability) VALUES (1, 1, 1, 1, 1, 0.75), (1, 1, 1, 1, 2, 0.25), (1, 1, 1, 2, 1, 0.0), (1, 1, 1, 2, 2, 1.0), (1, 2, 1, 1, 1, 0.75), (1, 2, 1, 1, 2, 0.25), (1, 2, 1, 2, 1, 0.2), (1, 2, 1, 2, 2, 0.8);"""


@pytest.fixture(scope="module")
def db_smr_insert():
    return """
INSERT INTO smr (sample, intervention, behavior, time, ratio) VALUES (1, 1, 1, 1, 2.0), (1, 1, 2, 1, 2.1), (1, 2, 1, 1, 2.2), (1, 2, 2, 1, 2.3);"""


@pytest.fixture(scope="module")
def db_bgm_insert():
    return """
INSERT INTO background_mortality (sample, time, probability) VALUES (1, 1, .25);"""


@pytest.fixture(scope="module")
def db_od_insert():
    return """
INSERT INTO overdose (sample, intervention, behavior, time, probability) VALUES (1, 1, 1, 1, 0.8), (1, 1, 2, 1, 0.7), (1, 2, 1, 1, 0.6), (1, 2, 2, 1, 0.5);"""


@pytest.fixture(scope="module")
def db_fod_insert():
    return """
INSERT INTO overdose_fatality (sample, intervention, behavior, time, probability) VALUES (1, 1, 1, 1, 0.1), (1, 1, 2, 1, 0.2), (1, 2, 1, 1, 0.3), (1, 2, 2, 1, 0.4);"""


@pytest.fixture
def insert_complete_sample():
    return """
INSERT INTO cohort (id, description, background_mortality_sample, behavior_transition_sample, initial_population_sample, intervention_transition_sample, overdose_sample, overdose_fatality_sample, population_change_sample, smr_sample) VALUES (1, "Test Cohort 1", 1, 1, 1, 1, 1, 1, 1, 1);

INSERT INTO intervention (id, name) VALUES (1, "no_treatment"), (2, "early_buprenorphine"), (3, "buprenorphine"), (4, "post_buprenorphine");

INSERT INTO behavior (id, name) VALUES (1, "active_injection"), (2, "nonactive_injection");

INSERT INTO initial_population (sample, intervention, behavior, count) VALUES (1, 1, 1, 100), (1, 1, 2, 150), (1, 2, 1, 200), (1, 2, 2, 250), (1, 3, 1, 0), (1, 3, 2, 0), (1, 4, 1, 0), (1, 4, 2, 0);

INSERT INTO population_change (sample, intervention, behavior, time, count) VALUES (1, 1, 1, 1, 100), (1, 1, 2, 1, 150), (1, 2, 1, 1, 200), (1, 2, 2, 1, 250), (1, 3, 1, 1, 0), (1, 3, 2, 1, 0), (1, 4, 1, 1, 0), (1, 4, 2, 1, 0);

INSERT INTO intervention_transition (sample, behavior, time, initial_intervention, new_intervention, probability) VALUES (1, 1, 1, 1, 1, 0.8),(1, 2, 1, 1, 1, 0.7),(1, 1, 1, 1, 2, 0.2),(1, 2, 1, 1, 2, 0.3),(1, 1, 1, 1, 3, 0.0),(1, 2, 1, 1, 3, 0.0),(1, 1, 1, 1, 4, 0.0),(1, 2, 1, 1, 4, 0.0),(1, 1, 1, 2, 1, 0.0),(1, 2, 1, 2, 1, 0.0),(1, 1, 1, 2, 2, 0.7),(1, 2, 1, 2, 2, 0.6),(1, 1, 1, 2, 3, 0.2),(1, 2, 1, 2, 3, 0.1),(1, 1, 1, 2, 4, 0.1),(1, 2, 1, 2, 4, 0.3),(1, 1, 1, 3, 1, 0.0),(1, 2, 1, 3, 1, 0.0),(1, 1, 1, 3, 2, 0.0),(1, 2, 1, 3, 2, 0.0),(1, 1, 1, 3, 3, 0.8),(1, 2, 1, 3, 3, 0.8),(1, 1, 1, 3, 4, 0.2),(1, 2, 1, 3, 4, 0.2),(1, 1, 1, 4, 1, 0.8),(1, 2, 1, 4, 1, 0.8),(1, 1, 1, 4, 2, 0.0),(1, 2, 1, 4, 2, 0.0),(1, 1, 1, 4, 3, 0.0),(1, 2, 1, 4, 3, 0.0),(1, 1, 1, 4, 4, 0.2),(1, 2, 1, 4, 4, 0.2);

INSERT INTO behavior_transition (sample, intervention, time, initial_behavior, new_behavior, probability) VALUES (1, 1, 1, 1, 1, 0.8),(1, 1, 1, 1, 2, 0.2),(1, 1, 1, 2, 1, 0.1),(1, 1, 1, 2, 2, 0.9),(1, 2, 1, 1, 1, 0.9),(1, 2, 1, 1, 2, 0.1),(1, 2, 1, 2, 1, 0.7),(1, 2, 1, 2, 2, 0.3),(1, 3, 1, 1, 1, 0.3),(1, 3, 1, 1, 2, 0.7),(1, 3, 1, 2, 1, 0.4),(1, 3, 1, 2, 2, 0.6),(1, 4, 1, 1, 1, 0.3),(1, 4, 1, 1, 2, 0.7),(1, 4, 1, 2, 1, 0.2),(1, 4, 1, 2, 2, 0.8);

INSERT INTO smr (sample, intervention, behavior, time, ratio) VALUES (1, 1, 1, 1, 2.0), (1, 1, 2, 1, 2.1), (1, 2, 1, 1, 2.0), (1, 2, 2, 1, 2.1), (1, 3, 1, 1, 2.0), (1, 3, 2, 1, 2.1), (1, 4, 1, 1, 2.0), (1, 4, 2, 1, 2.1);

INSERT INTO background_mortality (sample, time, probability) VALUES (1, 1, .25);

INSERT INTO overdose (sample, intervention, behavior, time, probability) VALUES (1, 1, 1, 1, 0.8), (1, 1, 2, 1, 0.7),(1, 2, 1, 1, 0.8), (1, 2, 2, 1, 0.7),(1, 3, 1, 1, 0.8), (1, 3, 2, 1, 0.7),(1, 4, 1, 1, 0.8), (1, 4, 2, 1, 0.7);

INSERT INTO overdose_fatality (sample, intervention, behavior, time, probability) VALUES (1, 1, 1, 1, 0.1), (1, 1, 2, 1, 0.2), (1, 2, 1, 1, 0.1), (1, 2, 2, 1, 0.2), (1, 3, 1, 1, 0.1), (1, 3, 2, 1, 0.2), (1, 4, 1, 1, 0.1), (1, 4, 2, 1, 0.2);
"""
