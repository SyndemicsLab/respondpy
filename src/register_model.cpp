////////////////////////////////////////////////////////////////////////////////
// File: register_model.cpp                                                   //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-09-25                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <algorithm>
#include <stdexcept>
#include <sstream>

#include <respond/constants.hpp>
#include <respond/history.hpp>
#include <respond/model.hpp>
#include <respond/runtime_config.hpp>

namespace py = pybind11;
using namespace respond;

namespace {

py::list vector_to_json(const Eigen::VectorXd &value) {
     py::list result;
     for (Eigen::Index index = 0; index < value.size(); ++index) {
          result.append(value(index));
     }
     return result;
}

py::dict history_to_json(const History &history) {
     py::dict result;
     result["name"] = history.GetName();
     result["mode"] = history.GetHistoryMode() == HistoryMode::kAccumulated
                                ? "accumulated"
                                : "snapshot";

     py::list records;
     const auto &timesteps = history.GetRecordedTimesteps();
     const auto &states = history.GetRecordedStates();
     const auto record_count = std::min(timesteps.size(), states.size());
     for (size_t index = 0; index < record_count; ++index) {
          py::dict record;
          record["timestep"] = timesteps[index];
          record["state"] = vector_to_json(states[index]);
          records.append(record);
     }
     result["records"] = records;
     result["pending_state"] = vector_to_json(history.GetPendingState());
     return result;
}

std::string model_to_json(const Model &model) {
     py::dict snapshot;
     snapshot["format"] = "respondpy.model.snapshot";
     snapshot["schema_version"] = 1;
     snapshot["resumable"] = false;

     py::list limitations;
     limitations.append(
          "This snapshot cannot restore a model through the current RESPOND API.");
     limitations.append(
          "Runtime configuration and structured timestep data are not exposed by the current RESPOND API.");
     snapshot["limitations"] = limitations;

     py::dict model_data;
     model_data["name"] = model.GetName();
     model_data["state"] = vector_to_json(model.GetState());
     model_data["current_timestep"] = model.GetTimestep();
     model_data["history_capture_interval"] =
          model.GetHistoryCaptureInterval();
     model_data["final_timestep"] = model.GetFinalTimestep();
     model_data["initial_history_recorded"] =
          model.GetInitialHistoryRecorded();
     snapshot["model"] = model_data;

     py::dict histories;
     for (const auto &[name, history] : model.GetHistories()) {
          histories[name.c_str()] = history_to_json(history);
     }
     snapshot["histories"] = histories;

     std::ostringstream native_summary;
     native_summary << model;
     snapshot["native_summary"] = native_summary.str();

     py::module_ json = py::module_::import("json");
     return json.attr("dumps")(snapshot, py::arg("sort_keys") = true)
          .cast<std::string>();
}

size_t model_timestep_count(const Model &model) {
     size_t count = 0;
     while (true) {
          try {
               static_cast<void>(model.GetTimestepAtIndex(count));
               ++count;
          } catch (const std::out_of_range &) {
               return count;
          }
     }
}

size_t normalize_model_timestep_index(const Model &model, py::ssize_t index) {
     const auto count = model_timestep_count(model);
     const auto normalized = index < 0 ? static_cast<py::ssize_t>(count) + index
                                       : index;
     if (normalized < 0 || static_cast<size_t>(normalized) >= count) {
          throw py::index_error("Model timestep index out of range");
     }
     return static_cast<size_t>(normalized);
}

} // namespace

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_model(py::module &m) {
    py::class_<Model, py::smart_holder>(m, "Model")
        .def(py::init(
                 py::overload_cast<const std::string &, const RuntimeConfig &>(
                     &Model::Create)),
             py::arg("name"), py::arg("runtime_config"),
             "Factory method to create a Model instance with shared runtime "
             "configuration.")
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
        .def("run_timestep",
             [](Model &self, py::ssize_t idx) {
                  self.RunTimestep(normalize_model_timestep_index(self, idx));
             },
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
        .def("get_timestep_at_index",
             [](const Model &self, py::ssize_t idx) {
                  return self.GetTimestepAtIndex(
                      normalize_model_timestep_index(self, idx));
             },
             py::arg("idx"),
             "Get the timestep at the specified index in the model's sequence.")
        .def(
            "get_state",
            [](const Model &self) {
                // Return a concrete vector copy to avoid exposing Eigen::Ref
                // lifetimes across the Python boundary.
                return Eigen::VectorXd(self.GetState());
            },
            "Get the current state vector of the model.")
        .def("get_name", &Model::GetName, "Get the name of the model.")
        .def("get_histories", &Model::GetHistories,
             "Get the list of histories associated with the model.")
        .def("get_timestep", &Model::GetTimestep,
             "Get the current timestep index.")
        .def("get_timestep_count", &model_timestep_count,
             "Get the number of timesteps registered in the model.")
        .def(
            "get_history_capture_interval", &Model::GetHistoryCaptureInterval,
            "Get the active capture interval. A value of 1 means full capture.")
        .def("get_final_timestep", &Model::GetFinalTimestep,
             "Get the configured final simulation timestep, or -1 if unset.")
        .def("get_initial_history_recorded", &Model::GetInitialHistoryRecorded,
             "Check if the initial history has been recorded.")
        .def(
            "set_state",
               [](Model &self, const py::object &state) {
                    self.SetState(vector_from_python(state));
            },
            py::arg("state"), "Set the current state vector of the model.")
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
        .def("to_json", &model_to_json,
             "Return a versioned, non-resumable JSON inspection snapshot.")
        .def("__repr__", [](const Model &m) {
            std::stringstream ss;
            ss << m;
            return ss.str();
        });
}
