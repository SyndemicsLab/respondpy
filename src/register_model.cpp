////////////////////////////////////////////////////////////////////////////////
// File: register_model.cpp                                                   //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-07-20                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/constants.hpp>
#include <respond/model.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_model(py::module &m) {
    py::class_<Model, py::smart_holder>(m, "Model")
        .def(py::init(&Model::Create), py::arg("name"),
             py::arg("log_name") = "respond",
             py::arg("log_filepath") = "respond.log",
             "Factory method to create a Model instance. Initializes logging "
             "for the model and returns a unique_ptr to the created instance. "
             "Throws an exception if the model name is unsupported.")
        .def("__copy__", [](const Model &self) { return self.clone(); })
        .def(
            "__deepcopy__",
            [](const Model &self, py::dict) { return self.clone(); },
            "memo") // memo argument is required by Python's deepcopy protocol;
        .def("add_timestep", &Model::AddTimestep, py::arg("timestep"),
             "Add a single timestep to the model. The model gains an ownership "
             "reference to this timestep and will manage its lifecycle.")
        .def("run_timestep", py::overload_cast<>(&Model::RunTimestep),
             "Execute the next timestep in the model's sequence.")
        .def("run_timestep", py::overload_cast<size_t>(&Model::RunTimestep),
             py::arg("idx"),
             "Execute the timestep at the specified index in the model's "
             "sequence.")
        .def("run_timesteps", &Model::RunTimesteps,
             "Execute all registered timesteps in sequence, applying their "
             "transitions to the model's state.")
        .def("clear_timesteps", &Model::ClearTimesteps,
             "Clear all timesteps from the model.")
        .def("clear_histories", &Model::ClearHistories,
             "Clear all history records and reset the history tracking state.")
        .def("create_default_histories", &Model::CreateDefaultHistories,
             "Create default history tracking for the model. Initializes "
             "standard history records based on the model's state.")
        .def("get_timestep_at_index", &Model::GetTimestepAtIndex,
             py::arg("idx"),
             "Get the timestep at the specified index in the model's sequence.")
        .def("get_state", &Model::GetState,
             "Get the current state vector of the model.")
        .def("get_name", &Model::GetName, "Get the name of the model.")
        .def("get_histories", &Model::GetHistories,
             "Get the list of histories associated with the model.")
        .def("get_timestep", &Model::GetTimestep,
             "Get the current timestep index.")
        .def(
            "get_history_capture_interval", &Model::GetHistoryCaptureInterval,
            "Get the active capture interval. A value of 1 means full capture.")
        .def("get_final_timestep", &Model::GetFinalTimestep,
             "Get the configured final simulation timestep, or -1 if unset.")
        .def("get_initial_history_recorded", &Model::GetInitialHistoryRecorded,
             "Check if the initial history has been recorded.")
        .def("set_state", &Model::SetState, py::arg("state"),
             "Set the current state vector of the model.")
        .def("set_history_capture_interval", &Model::SetHistoryCaptureInterval,
             py::arg("interval"),
             "Set the global history capture interval. Records every "
             "interval timesteps; values less than 1 default to full capture.")
        .def("set_final_timestep", &Model::SetFinalTimestep,
             py::arg("final_timestep"),
             "Set the final timestep that must always be recorded.")
        .def("set_initial_history_recorded", &Model::SetInitialHistoryRecorded,
             py::arg("recorded"),
             "Set whether the initial history has been recorded.")
        .def("serialize", &Model::Serialize,
             "Serialize the model's state and history into a string.")
        .def("__repr__", [](const Model &m) {
            std::stringstream ss;
            ss << m;
            return ss.str();
        });
}
