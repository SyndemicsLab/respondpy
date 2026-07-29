////////////////////////////////////////////////////////////////////////////////
// File: register_simulation.cpp                                              //
// Project: respondpy                                                         //
// Created Date: 2026-02-09                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-07-22                                                  //
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
        .def(py::init<>(),
             "Default constructor for a Simulation instance. Initializes the "
             "simulation with the default logger.")
        .def(py::init<const std::string &>(), py::arg("log_name"),
             "Constructs a Simulation with a specified logger.")
        .def(py::init<const std::string &, const std::string &>(),
             py::arg("log_name"), py::arg("log_filepath"),
             "Constructs a Simulation with a specified logger and log file.")
        .def("__copy__",
             [](const Simulation &self) { return Simulation(self); })
        .def(
            "__deepcopy__",
            [](const Simulation &self, py::dict) { return Simulation(self); },
            "memo")
        .def("create_new_model", &Simulation::CreateNewModel,
             py::arg("model_name"),
             "Create a new model instance and add it to the simulation. "
             "Initializes logging for the model and returns a cloned model. "
             "Throws an exception if the model name is unsupported.")
        .def("clear_models", &Simulation::ClearModels,
             "Clear all models from the simulation.")
        .def(
            "add_model",
            [](Simulation &self, const Model &model) {
                const auto cloned_model = model.clone();
                self.AddModel(cloned_model);
            },
            py::arg("model"),
            "Add an existing model instance to the simulation. The simulation "
            "takes ownership of the model.")
        .def("run", &Simulation::Run, py::arg("duration") = -1,
             "Run the simulation for a specified duration. Executes all "
             "registered timesteps for each model in sequence.")
        .def("get_models", &Simulation::GetModels,
             "Get the list of models in the simulation.")
        .def(
            "get_model",
            [](Simulation &self, size_t model_index) -> Model & {
                return self[model_index];
            },
            py::arg("model_index"), py::return_value_policy::reference_internal,
            "Get a model instance by its index in the simulation. Throws an "
            "exception if the index is out of bounds.")
        .def(
            "set_model",
            [](Simulation &self, size_t model_index,
               const Model &replacement_model) {
                self[model_index] = replacement_model;
            },
            py::arg("model_index"), py::arg("model"),
            "Replace a model instance by index with a cloned copy of the "
            "provided model. Throws an exception if the index is out of "
            "bounds.")
        .def(
            "__getitem__",
            [](Simulation &self, size_t model_index) -> Model & {
                return self[model_index];
            },
            py::arg("model_index"), py::return_value_policy::reference_internal,
            "Get a model using index access semantics.")
        .def(
            "__setitem__",
            [](Simulation &self, size_t model_index,
               const Model &replacement_model) {
                self[model_index] = replacement_model;
            },
            py::arg("model_index"), py::arg("model"),
            "Set a model using index access semantics.")
        .def("get_model_names", &Simulation::GetModelNames,
             "Get the list of model names in the simulation.")
        .def("get_model_index_name_map", &Simulation::GetModelIndexNameMap,
             "Get a mapping from model indices to model names.")
        .def(
            "get_model_history",
            py::overload_cast<size_t>(&Simulation::GetModelHistory, py::const_),
            py::arg("idx"),
            "Get the history of a model by its index in the simulation. Throws "
            "an exception if the index is out of bounds.")
        .def("get_model_history_names",
             py::overload_cast<size_t>(&Simulation::GetModelHistoryNames,
                                       py::const_),
             py::arg("idx"),
             "Get the list of history names for a model by its index in the "
             "simulation. Throws an exception if the index is out of bounds.")
        .def("set_duration", &Simulation::SetDuration, py::arg("duration"),
             "Set the duration for which the simulation should run.")
        .def("__repr__", [](const Simulation &m) {
            return "<respondpy.Simulation with " +
                   std::to_string(m.GetModelNames().size()) + " models>";
        });
}