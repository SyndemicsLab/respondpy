////////////////////////////////////////////////////////////////////////////////
// File: register_model.cpp                                                   //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-09                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/model.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_model(py::module &m) {
    py::class_<Model>(m, "Model")
        .def(py::init(&Model::Create), py::arg("name"),
             py::arg("log_name") = "console")
        .def("set_state", &Model::SetState)
        .def("get_state", &Model::GetState)
        .def("run_transitions", &Model::RunTransitions)
        .def("add_transition", &Model::AddTransition)
        .def("get_transition_names", &Model::GetTransitionNames)
        .def("clear_transitions", &Model::ClearTransitions)
        .def("get_histories", &Model::GetHistories)
        .def("set_histories", &Model::SetHistories)
        .def("get_model_name", &Model::GetModelName)
        .def("get_log_name", &Model::GetLogName)
        .def("__repr__",
             [](const Model &m) {
                 return "<respondpy.Model named " + m.GetModelName() +
                        " with " + len(m.GetTransitionNames()) +
                        " transitions>";
             })
        .def("__copy__", [](const Model &self) { return self.clone(); })
        .def(
            "__deepcopy__",
            [](const Model &self, py::dict) { return self.clone(); },
            "memo") // memo argument is required by Python's deepcopy protocol;
}
