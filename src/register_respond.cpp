////////////////////////////////////////////////////////////////////////////////
// File: register_respond.cpp                                                 //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-01-08                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/respond.hpp>

namespace py = pybind11;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_respond(py::module &m) {
    m.def("migration", &respond::Migration, "Applies the Migrating Cohort.");
    m.def("behavior", &respond::Behavior, "Applies the Behavior Transition.");
    m.def("intervention", &respond::Intervention,
          "Applies the Intervention Transition.");
    m.def("overdose", &respond::Overdose, "Applies the Overdose Transition.");
    m.def("mortality", &respond::Mortality,
          "Applies the Mortality Transition.");
}