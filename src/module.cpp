////////////////////////////////////////////////////////////////////////////////
// File: module.cpp                                                           //
// Project: respondpy                                                         //
// Created Date: 2025-08-01                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-09                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center             //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

namespace py = pybind11;

void register_cost_effectiveness(py::module &m);
void register_history(py::module &m);
void register_logging(py::module &m);
void register_model(py::module &m);
void register_simulation(py::module &m);
void register_transition(py::module &m);

PYBIND11_MODULE(_core, m, py::mod_gil_not_used()) {
    py::module cost_effectiveness = m.def_submodule("cost_effectiveness");
    register_cost_effectiveness(cost_effectiveness);

    py::module history_mod = m.def_submodule("history");
    register_history(history_mod);

    py::module logging = m.def_submodule("logging");
    register_logging(logging);

    py::module model_mod = m.def_submodule("model");
    register_model(model_mod);

    py::module sim_mod = m.def_submodule("simulation");
    register_simulation(sim_mod);

    py::module t_mod = m.def_submodule("transition");
    register_transition(t_mod);
}