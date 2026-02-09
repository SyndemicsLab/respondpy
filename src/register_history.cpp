////////////////////////////////////////////////////////////////////////////////
// File: register_history.cpp                                                 //
// Project: respondpy                                                         //
// Created Date: 2026-02-09                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-09                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/history.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_history(py::module &m) {
    py::class_<History>(m, "History")
        .def(py::init(), pybind11::arg("name") = "state",
             pybind11::arg("log_name") = "console")
        .def("__copy__", [](const History &self) { return History(self); })
        .def("get_state_map", &History::GetStateMap,
             "Get the state map (timestep -> state vector).")
        .def("get_history_name", &History::GetHistoryName,
             "Get the name of the history object.")
        .def("get_log_name", &History::GetLogName,
             "Get the log name used for logging.")
        .def("get_state_as_vector", &History::GetStateAsVector,
             "Get the state as a vector, padding missing timesteps with zero "
             "vectors.")
        .def("add_state", &History::AddState, pybind11::arg("state"),
             pybind11::arg("timestep") = -1,
             "Add a state vector at a given timestep (-1 for auto-increment).")
        .def("clear", &History::Clear, "Clear all stored state history.")
        .def("__eq__", &History::operator==,
             "Check equality of History objects (name, log_name, and state).")
        .def("__ne__", &History::operator!=,
             "Check inequality of History objects.");
}