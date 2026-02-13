////////////////////////////////////////////////////////////////////////////////
// File: register_simulation.cpp                                              //
// Project: respondpy                                                         //
// Created Date: 2026-02-09                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-12                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/simulation.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_simulation(py::module &m) {
    py::class_<Simulation>(m, "Simulation")
        .def(py::init<>())
        .def(py::init<const std::string &>())
        .def("run", &Simulation::Run)
        .def("add_model", &Simulation::AddModel)
        .def("get_models", &Simulation::GetModels)
        .def("get_model_names", &Simulation::GetModelNames)
        .def("clear_models", &Simulation::ClearModels)
        .def("get_model_histories", &Simulation::GetModelHistories)
        .def("get_model_history_names", &Simulation::GetModelHistoryNames)
        .def("get_log_name", &Simulation::GetLogName)
        .def("__repr__",
             [](const Simulation &m) {
                 return "<respondpy.Simulation with " +
                        std::to_string(m.GetModelNames().size()) + " models>";
             })
        .def("__copy__",
             [](const Simulation &self) { return Simulation(self); });
}