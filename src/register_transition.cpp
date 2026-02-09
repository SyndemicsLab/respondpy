////////////////////////////////////////////////////////////////////////////////
// File: register_transition.cpp                                              //
// Project: respondpy                                                         //
// Created Date: 2026-02-02                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-09                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/transition.hpp>
#include <respond/transition_factory.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_transition(py::module &m) {
    py::class_<Transition, py::smart_holder> t(m, "Transition");
    t.def(py::init(&TransitionFactory::CreateTransition), py::arg("type"),
          py::arg("log_name") = "console")
        .def("execute", &Transition::Execute)
        .def("add_transition_matrix", &Transition::AddTransitionMatrix)
        .def("get_transition_name", &Transition::GetTransitionName)
        .def("clear_transition_matrices", &Transition::ClearTransitionMatrices)
        .def("get_log_name", &Transition::GetLogName)
        .def("__repr__",
             [](const Transition &m) {
                 return "<respondpy.Transition named " + m.GetTransitionName() +
                        " >";
             })
        .def("__copy__", [](const Transition &self) { return self.clone(); })
        .def(
            "__deepcopy__",
            [](const Transition &self, py::dict) { return self.clone(); },
            "memo");
}