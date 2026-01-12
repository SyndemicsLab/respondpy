////////////////////////////////////////////////////////////////////////////////
// File: register_markov.cpp                                                  //
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

#include <respond/markov.hpp>

namespace py = pybind11;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_markov(py::module &m) {
    py::class_<respond::Markov> markov(m, "Markov");
    markov
        .def(py::init(&respond::Markov::Create),
             pybind11::arg("log_name") = "console")
        .def("set_state", &respond::Markov::SetState)
        .def("get_state", &respond::Markov::GetState)
        .def("set_transitions", &respond::Markov::SetTransitions)
        .def("get_transitions", &respond::Markov::GetTransitions)
        .def("add_transition", &respond::Markov::AddTransition)
        .def("run", &respond::Markov::Run)
        .def("get_run_results", &respond::Markov::GetRunResults);
}
