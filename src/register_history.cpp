////////////////////////////////////////////////////////////////////////////////
// File: register_history.cpp                                                 //
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

#include <string>

#include <respond/history.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_history(py::module &m) {
    py::enum_<HistoryMode>(m, "HistoryMode")
        .value("kSnapshot", HistoryMode::kSnapshot)
        .value("kAccumulated", HistoryMode::kAccumulated)
        .export_values();

    m.def("get_default_history_mode", &GetDefaultHistoryMode, py::arg("name"),
          "Return the default HistoryMode for a named history. Accumulated "
          "histories track intervention_admission, total_overdose, "
          "fatal_overdose, and background_death; all others are Snapshot.");

    py::class_<History>(m, "History")
        .def(py::init<>(), "Default constructor for a History with name "
                           "'state' and default mode.")
        .def(py::init<const std::string &>(), py::arg("name"),
             "Construct a History with a specified name and default mode.")
        .def(py::init<const std::string &, const HistoryMode &>(),
             py::arg("name"), py::arg("mode"),
             "Construct a History with a specified name and "
             "explicit recording mode.")
        .def(py::init<const std::string &, const HistoryMode &,
                      const std::string &>(),
             py::arg("name"), py::arg("mode"), py::arg("log_name"),
             "Construct a History with a specified name, mode, and logger.")
        .def(py::init<const std::string &, const std::string &>(),
             py::arg("name"), py::arg("log_name"),
             "Construct a History with a specified name "
             "and logger, using default mode.")
        .def(py::init<const std::string &, const std::string &,
                      const std::string &>(),
             py::arg("name"), py::arg("log_name"), py::arg("log_filepath"),
             "Construct a History with a specified name, logger, and log file "
             "path, using default mode.")
        .def(py::init<const std::string &, const HistoryMode &,
                      const std::string &, const std::string &>(),
             py::arg("name"), py::arg("mode"), py::arg("log_name"),
             py::arg("log_filepath"),
             "Construct a History with a specified name, mode, logger, and log "
             "file path.")
        .def("__copy__", [](const History &self) { return History(self); })
        .def(
            "__deepcopy__",
            [](const History &self, py::dict) { return History(self); }, "memo")
        .def("add_state", &History::AddState, py::arg("state"),
             py::arg("timestep") = -1,
             "Add a state vector at a given timestep (-1 for auto-increment).")
        .def("accumulate_state", &History::AccumulateState, py::arg("state"),
             "Add a per-step contribution to an accumulated history.")
        .def("flush_pending_state", &History::FlushPendingState,
             py::arg("timestep"), py::arg("state_size"),
             "Flush the pending accumulated state into a recorded timestep. "
             "Records a zero vector of state_size if nothing is pending.")
        .def("clear", &History::Clear, "Clear all stored state history.")
        .def("get_state_map", &History::GetStateMap,
             "Get the state map (timestep -> state vector).")
        .def("get_recorded_timesteps", &History::GetRecordedTimesteps,
             "Get the raw recorded timestep indices without gap-filling.")
        .def("get_recorded_states", &History::GetRecordedStates,
             "Get the raw recorded state vectors without gap-filling.")
        .def("get_history_mode", &History::GetHistoryMode,
             "Get the recording mode (Snapshot or Accumulated).")
        .def("get_pending_state", &History::GetPendingState,
             "Get the pending accumulated state vector, or an empty vector if "
             "none exists.")
        .def("get_latest_recorded_timestep",
             &History::GetLatestRecordedTimestep,
             "Get the largest recorded timestep, or -1 if history is empty.")
        .def("get_name", &History::GetName,
             "Get the name of the history object.")
        .def("get_state_as_vector", &History::GetStateAsVector,
             "Get the state as a dense vector, padding missing timesteps with "
             "zero vectors.")
        .def("__eq__", &History::operator==,
             "Check equality of History objects (name, log_name, mode, state, "
             "and pending state).")
        .def("__ne__", &History::operator!=,
             "Check inequality of History objects.")
        .def("__repr__", [](const History &self) {
            std::ostringstream ss;
            ss << self;
            return ss.str();
        });
}