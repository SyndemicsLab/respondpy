////////////////////////////////////////////////////////////////////////////////
// File: register_simulation.cpp                                              //
// Project: respondpy                                                         //
// Created Date: 2026-02-09                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-09-25                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/runtime_config.hpp>
#include <respond/simulation.hpp>

namespace py = pybind11;
using namespace respond;

namespace {

size_t normalize_model_index(const Simulation &simulation,
                                    py::ssize_t index) {
     const auto model_count = simulation.GetModelNames().size();
     if (index < 0) {
          index += static_cast<py::ssize_t>(model_count);
     }
     if (index < 0 || index >= static_cast<py::ssize_t>(model_count)) {
          throw py::index_error("Simulation model index out of range");
     }
     return static_cast<size_t>(index);
}

} // namespace

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_simulation(py::module &m) {
    py::class_<Simulation>(m, "Simulation")
        .def(py::init<>(),
             "Default constructor for a Simulation instance. Initializes the "
             "simulation with the default logger.")
        .def(py::init<const RuntimeConfig &>(), py::arg("runtime_config"),
             "Constructs a Simulation with shared runtime settings.")
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
                "Get independent model copies from the simulation.")
        .def(
            "get_model",
               [](const Simulation &self, py::ssize_t model_index) {
                    return self.GetModel(static_cast<int>(normalize_model_index(
                         self, model_index)));
            },
                   py::arg("model_index"),
               "Get an independent model copy by index. Negative indices count "
               "from the end.")
        .def(
            "set_model",
               [](Simulation &self, py::ssize_t model_index,
               const Model &replacement_model) {
                    self[normalize_model_index(self, model_index)] =
                         replacement_model;
            },
            py::arg("model_index"), py::arg("model"),
            "Replace a model instance by index with a cloned copy of the "
            "provided model. Throws an exception if the index is out of "
            "bounds.")
        .def(
            "__getitem__",
               [](const Simulation &self, py::ssize_t model_index) {
                    return self.GetModel(static_cast<int>(normalize_model_index(
                         self, model_index)));
            },
               py::arg("model_index"),
               "Get an independent model copy using index access semantics. "
               "Negative indices count from the end.")
        .def(
            "__setitem__",
               [](Simulation &self, py::ssize_t model_index,
               const Model &replacement_model) {
                    self[normalize_model_index(self, model_index)] =
                         replacement_model;
            },
            py::arg("model_index"), py::arg("model"),
            "Set a model using index access semantics.")
        .def("get_model_names", &Simulation::GetModelNames,
             "Get the list of model names in the simulation.")
        .def("get_model_index_name_map", &Simulation::GetModelIndexNameMap,
             "Get a mapping from model indices to model names.")
        .def(
            "get_model_history",
               [](const Simulation &self, py::ssize_t index) {
                    return self.GetModelHistory(
                         normalize_model_index(self, index));
               },
            py::arg("idx"),
               "Get copied histories for a model by index. Negative indices "
               "count from the end.")
        .def("get_model_history_names",
                [](const Simulation &self, py::ssize_t index) {
                     return self.GetModelHistoryNames(
                          normalize_model_index(self, index));
                },
             py::arg("idx"),
                "Get history names for a model by index. Negative indices count "
                "from the end.")
        .def("set_duration", &Simulation::SetDuration, py::arg("duration"),
             "Set the duration for which the simulation should run.")
        .def("get_execution_config", &Simulation::GetExecutionConfig,
             "Get the current execution configuration.")
        .def("set_execution_config", &Simulation::SetExecutionConfig,
             py::arg("execution_config"), "Set the execution configuration.")
        .def("get_runtime_config", &Simulation::GetRuntimeConfig,
             "Get the current runtime configuration.")
        .def("set_runtime_config", &Simulation::SetRuntimeConfig,
             py::arg("runtime_config"), "Set the runtime configuration.")
        .def("__repr__", [](const Simulation &m) {
            return "<respondpy.Simulation with " +
                   std::to_string(m.GetModelNames().size()) + " models>";
        });
}