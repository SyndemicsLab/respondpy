////////////////////////////////////////////////////////////////////////////////
// File: module.cpp                                                           //
// Project: respondpy                                                         //
// Created Date: 2025-08-01                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-01-08                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center             //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

namespace py = pybind11;

void register_markov(py::module &m);
void register_cost_effectiveness(py::module &m);
void register_logging(py::module &m);
void register_types(py::module &m);
void register_respond(py::module &m);

PYBIND11_MODULE(_core, m, py::mod_gil_not_used()) {
    py::module markov = m.def_submodule("markov");
    register_markov(markov);

    py::module cost_effectiveness = m.def_submodule("cost_effectiveness");
    register_cost_effectiveness(cost_effectiveness);

    py::module logging = m.def_submodule("logging");
    register_logging(logging);

    py::module types = m.def_submodule("types");
    register_types(types);

    py::module respond = m.def_submodule("respond");
    register_respond(respond);
}