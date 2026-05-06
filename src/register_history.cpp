////////////////////////////////////////////////////////////////////////////////
// File: register_history.cpp                                                 //
// Project: respondpy                                                         //
// Created Date: 2026-02-09                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-05-06                                                  //
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
        .value("Snapshot", HistoryMode::Snapshot)
        .value("Accumulated", HistoryMode::Accumulated)
        .export_values();

    m.def("get_default_history_mode", &GetDefaultHistoryMode,
          py::arg("name"),
          "Return the default HistoryMode for a named history. Accumulated "
          "histories track intervention_admission, total_overdose, "
          "fatal_overdose, and background_death; all others are Snapshot.");

    py::class_<History>(m, "History")
        .def(py::init<std::string, std::string>(),
             py::arg("name") = "state",
             py::arg("log_name") = "console")
        .def(py::init<std::string, std::string, HistoryMode>(),
             py::arg("name"),
             py::arg("log_name"),
             py::arg("mode"),
             "Construct a History with an explicit recording mode.")
        .def("__copy__", [](const History &self) { return History(self); })
        .def("get_state_map", &History::GetStateMap,
             "Get the state map (timestep -> state vector).")
        .def("get_history_name", &History::GetHistoryName,
             "Get the name of the history object.")
        .def("get_log_name", &History::GetLogName,
             "Get the log name used for logging.")
        .def("get_history_mode", &History::GetHistoryMode,
             "Get the recording mode (Snapshot or Accumulated).")
        .def("get_state_as_vector", &History::GetStateAsVector,
             "Get the state as a dense vector, padding missing timesteps with "
             "zero vectors.")
        .def("get_recorded_timesteps", &History::GetRecordedTimesteps,
             "Get the raw recorded timestep indices without gap-filling.")
        .def("get_recorded_states", &History::GetRecordedStates,
             "Get the raw recorded state vectors without gap-filling.")
        .def("has_pending_state", &History::HasPendingState,
             "Return True when an accumulated history has a pending aggregate "
             "not yet flushed.")
        .def("get_pending_state", &History::GetPendingState,
             "Get the pending accumulated state vector, or an empty vector if "
             "none exists.")
        .def("get_latest_recorded_timestep", &History::GetLatestRecordedTimestep,
             "Get the largest recorded timestep, or -1 if history is empty.")
        .def("add_state", &History::AddState,
             py::arg("state"),
             py::arg("timestep") = -1,
             "Add a state vector at a given timestep (-1 for auto-increment).")
        .def("record_snapshot", &History::RecordSnapshot,
             py::arg("state"),
             py::arg("timestep"),
             "Record a snapshot state vector at a concrete timestep.")
        .def("accumulate_state", &History::AccumulateState,
             py::arg("state"),
             "Add a per-step contribution to an accumulated history.")
        .def("flush_pending_state", &History::FlushPendingState,
             py::arg("timestep"),
             py::arg("state_size") = 0,
             "Flush the pending accumulated state into a recorded timestep. "
             "Records a zero vector of state_size if nothing is pending.")
        .def("clear", &History::Clear, "Clear all stored state history.")
        .def("__eq__", &History::operator==,
             "Check equality of History objects (name, log_name, mode, state, "
             "and pending state).")
        .def("__ne__", &History::operator!=,
             "Check inequality of History objects.");
}