################################################################################
# File: conftest.py                                                            #
# Project: respondpy                                                           #
# Created Date: 2026-05-06                                                     #
# Author: Matthew Carroll                                                      #
# -----                                                                        #
# Last Modified: 2026-06-16                                                    #
# Modified By: Matthew Carroll                                                 #
# -----                                                                        #
# Copyright (c) 2026 Syndemics Lab at Boston Medical Center                    #
################################################################################

"""
Shared fixtures for respondpy benchmarks.

The database is created once per session (scope="session") so DB setup cost
is paid only once across all benchmark functions.
"""

from __future__ import annotations

import sqlite3
from configparser import ConfigParser
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Schema & seed data
# ---------------------------------------------------------------------------

_DB_SCHEMA = """
DROP TABLE IF EXISTS "intervention";
CREATE TABLE "intervention" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"  TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "behavior";
CREATE TABLE "behavior" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"  TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "background_mortality";
CREATE TABLE "background_mortality" (
    "sample"        INTEGER NOT NULL,
    "time"          INTEGER NOT NULL,
    "probability"   REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY("sample","time")
);
DROP TABLE IF EXISTS "behavior_transition";
CREATE TABLE "behavior_transition" (
    "sample"            INTEGER NOT NULL,
    "intervention"      INTEGER NOT NULL,
    "time"              INTEGER NOT NULL,
    "initial_behavior"  INTEGER NOT NULL,
    "new_behavior"      INTEGER NOT NULL,
    "probability"       REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY("sample","intervention","time","initial_behavior","new_behavior"),
    FOREIGN KEY("initial_behavior") REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention")     REFERENCES "intervention"("id"),
    FOREIGN KEY("new_behavior")     REFERENCES "behavior"("id")
);
DROP TABLE IF EXISTS "initial_population";
CREATE TABLE "initial_population" (
    "sample"        INTEGER NOT NULL,
    "intervention"  INTEGER NOT NULL,
    "behavior"      INTEGER NOT NULL,
    "count"         REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY("sample","intervention","behavior")
);
DROP TABLE IF EXISTS "intervention_transition";
CREATE TABLE "intervention_transition" (
    "sample"                INTEGER NOT NULL,
    "behavior"              INTEGER NOT NULL,
    "time"                  INTEGER NOT NULL,
    "initial_intervention"  INTEGER NOT NULL,
    "new_intervention"      INTEGER NOT NULL,
    "probability"           REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY("sample","behavior","initial_intervention","new_intervention","time"),
    FOREIGN KEY("behavior")             REFERENCES "behavior"("id"),
    FOREIGN KEY("initial_intervention") REFERENCES "intervention"("id"),
    FOREIGN KEY("new_intervention")     REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "overdose";
CREATE TABLE "overdose" (
    "intervention"  INTEGER NOT NULL,
    "sample"        INTEGER NOT NULL,
    "behavior"      INTEGER NOT NULL,
    "time"          INTEGER NOT NULL,
    "probability"   REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY("intervention","sample","behavior","time"),
    FOREIGN KEY("behavior")     REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "overdose_fatality";
CREATE TABLE "overdose_fatality" (
    "sample"        INTEGER NOT NULL,
    "intervention"  INTEGER NOT NULL,
    "behavior"      INTEGER NOT NULL,
    "time"          INTEGER NOT NULL,
    "probability"   REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY("sample","intervention","behavior","time"),
    FOREIGN KEY("behavior")     REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "population_change";
CREATE TABLE "population_change" (
    "sample"        INTEGER NOT NULL,
    "intervention"  INTEGER NOT NULL,
    "behavior"      INTEGER NOT NULL,
    "time"          INTEGER NOT NULL,
    "count"         REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY("sample","intervention","behavior","time"),
    FOREIGN KEY("behavior")     REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "smr";
CREATE TABLE "smr" (
    "sample"        INTEGER NOT NULL,
    "intervention"  INTEGER NOT NULL,
    "behavior"      INTEGER NOT NULL,
    "time"          INTEGER NOT NULL,
    "ratio"         REAL NOT NULL DEFAULT 1.0,
    PRIMARY KEY("sample","time","behavior","intervention"),
    FOREIGN KEY("behavior")     REFERENCES "behavior"("id"),
    FOREIGN KEY("intervention") REFERENCES "intervention"("id")
);
DROP TABLE IF EXISTS "cohort";
CREATE TABLE "cohort" (
    "id"                            INTEGER NOT NULL UNIQUE,
    "description"                   TEXT,
    "background_mortality_sample"   INTEGER NOT NULL,
    "behavior_transition_sample"    INTEGER NOT NULL,
    "initial_population_sample"     INTEGER NOT NULL,
    "intervention_transition_sample" INTEGER NOT NULL,
    "overdose_sample"               INTEGER NOT NULL,
    "overdose_fatality_sample"      INTEGER NOT NULL,
    "population_change_sample"      INTEGER NOT NULL,
    "smr_sample"                    INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "demographics";
CREATE TABLE "demographics" (
    "id"    INTEGER NOT NULL UNIQUE,
    "type"  TEXT NOT NULL,
    "value" TEXT NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "cohort_demographics";
CREATE TABLE "cohort_demographics" (
    "cohort_id"     INTEGER NOT NULL,
    "demographic_id" INTEGER NOT NULL,
    PRIMARY KEY("cohort_id","demographic_id"),
    FOREIGN KEY("cohort_id")      REFERENCES "cohort"("id"),
    FOREIGN KEY("demographic_id") REFERENCES "demographics"("id")
);
"""


def _seed_benchmark_database(conn: sqlite3.Connection) -> None:
    """Seed a valid benchmark database across timesteps 1..52.

    The benchmark is intentionally generated programmatically so that
    time-varying rows exist for multiple parameter-change schedules without
    requiring a huge static SQL file.
    """
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO cohort (
            id, description, background_mortality_sample,
            behavior_transition_sample, initial_population_sample,
            intervention_transition_sample, overdose_sample,
            overdose_fatality_sample, population_change_sample, smr_sample
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (1, "Benchmark Cohort", 1, 1, 1, 1, 1, 1, 1, 1),
    )

    cursor.executemany(
        "INSERT INTO intervention (id, name) VALUES (?, ?)",
        [
            (1, "no_treatment"),
            (2, "early_buprenorphine"),
            (3, "buprenorphine"),
            (4, "post_buprenorphine"),
        ],
    )
    cursor.executemany(
        "INSERT INTO behavior (id, name) VALUES (?, ?)",
        [
            (1, "active_injection"),
            (2, "nonactive_injection"),
        ],
    )
    cursor.executemany(
        "INSERT INTO initial_population (sample, intervention, behavior, count) VALUES (?, ?, ?, ?)",
        [
            (1, 1, 1, 100),
            (1, 1, 2, 150),
            (1, 2, 1, 200),
            (1, 2, 2, 250),
            (1, 3, 1, 0),
            (1, 3, 2, 0),
            (1, 4, 1, 0),
            (1, 4, 2, 0),
        ],
    )

    behavior_transition_rows = []
    intervention_transition_rows = []
    population_change_rows = []
    smr_rows = []
    background_mortality_rows = []
    overdose_rows = []
    overdose_fatality_rows = []

    for t in range(1, 53):
        population_change_rows.extend([
            (1, 1, 1, t, 100),
            (1, 1, 2, t, 150),
            (1, 2, 1, t, 200),
            (1, 2, 2, t, 250),
            (1, 3, 1, t, 0),
            (1, 3, 2, t, 0),
            (1, 4, 1, t, 0),
            (1, 4, 2, t, 0),
        ])

        background_mortality_rows.append((1, t, 0.25))

        smr_rows.extend([
            (1, 1, 1, t, 2.0),
            (1, 1, 2, t, 2.1),
            (1, 2, 1, t, 2.0),
            (1, 2, 2, t, 2.1),
            (1, 3, 1, t, 2.0),
            (1, 3, 2, t, 2.1),
            (1, 4, 1, t, 2.0),
            (1, 4, 2, t, 2.1),
        ])

        overdose_rows.extend([
            (1, 1, 1, t, 0.8),
            (1, 1, 2, t, 0.7),
            (1, 2, 1, t, 0.8),
            (1, 2, 2, t, 0.7),
            (1, 3, 1, t, 0.8),
            (1, 3, 2, t, 0.7),
            (1, 4, 1, t, 0.8),
            (1, 4, 2, t, 0.7),
        ])

        overdose_fatality_rows.extend([
            (1, 1, 1, t, 0.1),
            (1, 1, 2, t, 0.2),
            (1, 2, 1, t, 0.1),
            (1, 2, 2, t, 0.2),
            (1, 3, 1, t, 0.1),
            (1, 3, 2, t, 0.2),
            (1, 4, 1, t, 0.1),
            (1, 4, 2, t, 0.2),
        ])

        for intervention in range(1, 5):
            for initial_behavior in (1, 2):
                for new_behavior in (1, 2):
                    behavior_transition_rows.append(
                        (
                            1,
                            intervention,
                            t,
                            initial_behavior,
                            new_behavior,
                            {
                                1: {(1, 1): 0.8, (1, 2): 0.2, (2, 1): 0.1, (2, 2): 0.9},
                                2: {(1, 1): 0.9, (1, 2): 0.1, (2, 1): 0.7, (2, 2): 0.3},
                                3: {(1, 1): 0.3, (1, 2): 0.7, (2, 1): 0.4, (2, 2): 0.6},
                                4: {(1, 1): 0.3, (1, 2): 0.7, (2, 1): 0.2, (2, 2): 0.8},
                            }[intervention][(initial_behavior, new_behavior)],
                        )
                    )

        for behavior in (1, 2):
            for initial_intervention in range(1, 5):
                for new_intervention in range(1, 5):
                    intervention_transition_rows.append(
                        (
                            1,
                            behavior,
                            t,
                            initial_intervention,
                            new_intervention,
                            {
                                1: {
                                    (1, 1): 0.8, (1, 2): 0.2, (1, 3): 0.0, (1, 4): 0.0,
                                    (2, 1): 0.0, (2, 2): 0.7, (2, 3): 0.2, (2, 4): 0.1,
                                    (3, 1): 0.0, (3, 2): 0.0, (3, 3): 0.8, (3, 4): 0.2,
                                    (4, 1): 0.8, (4, 2): 0.0, (4, 3): 0.0, (4, 4): 0.2,
                                },
                                2: {
                                    (1, 1): 0.7, (1, 2): 0.3, (1, 3): 0.0, (1, 4): 0.0,
                                    (2, 1): 0.0, (2, 2): 0.6, (2, 3): 0.1, (2, 4): 0.3,
                                    (3, 1): 0.0, (3, 2): 0.0, (3, 3): 0.8, (3, 4): 0.2,
                                    (4, 1): 0.8, (4, 2): 0.0, (4, 3): 0.0, (4, 4): 0.2,
                                },
                            }[behavior][(initial_intervention, new_intervention)],
                        )
                    )

    cursor.executemany(
        "INSERT INTO population_change (sample, intervention, behavior, time, count) VALUES (?, ?, ?, ?, ?)",
        population_change_rows,
    )
    cursor.executemany(
        "INSERT INTO intervention_transition (sample, behavior, time, initial_intervention, new_intervention, probability) VALUES (?, ?, ?, ?, ?, ?)",
        intervention_transition_rows,
    )
    cursor.executemany(
        "INSERT INTO behavior_transition (sample, intervention, time, initial_behavior, new_behavior, probability) VALUES (?, ?, ?, ?, ?, ?)",
        behavior_transition_rows,
    )
    cursor.executemany(
        "INSERT INTO smr (sample, intervention, behavior, time, ratio) VALUES (?, ?, ?, ?, ?)",
        smr_rows,
    )
    cursor.executemany(
        "INSERT INTO background_mortality (sample, time, probability) VALUES (?, ?, ?)",
        background_mortality_rows,
    )
    cursor.executemany(
        "INSERT INTO overdose (sample, intervention, behavior, time, probability) VALUES (?, ?, ?, ?, ?)",
        overdose_rows,
    )
    cursor.executemany(
        "INSERT INTO overdose_fatality (sample, intervention, behavior, time, probability) VALUES (?, ?, ?, ?, ?)",
        overdose_fatality_rows,
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def benchmark_db(tmp_path_factory) -> Path:
    """Create and seed a SQLite database once for the entire benchmark session."""
    db_path = tmp_path_factory.mktemp("bench-data") / "benchmark.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(_DB_SCHEMA)
    _seed_benchmark_database(conn)
    conn.close()
    return db_path


@pytest.fixture(scope="session")
def benchmark_config(tmp_path_factory) -> str:
    """Fixed simulation config used across all benchmarks."""
    conf_path = tmp_path_factory.mktemp("bench-data") / "sim.conf"
    cfg = ConfigParser()
    cfg["simulation"] = {
        "duration": "52",
        "parameter_change_times": "1",
        "stratify_entering_cohort": "false",
    }
    cfg["output"] = {
        "build_summary_stats": "true",
        "save_state_history": "true",
        "timesteps_to_report": "52",
    }
    with open(conf_path, "w", encoding='utf-8') as f:
        cfg.write(f)
    return conf_path
