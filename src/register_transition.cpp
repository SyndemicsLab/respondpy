////////////////////////////////////////////////////////////////////////////////
// File: register_transition.cpp                                              //
// Project: respondpy                                                         //
// Created Date: 2026-02-02                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-02                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/transition.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_transition(py::module &m) {
    py::class_<Transition> t(m, "Transition");
    t.def(py::init())
        .def_readwrite("transition_matrices", &Transition::transition_matrices)
        .def("set_callback", &Transition::SetCallback)
        .def("execute", &Transition::Execute);
}