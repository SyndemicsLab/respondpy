////////////////////////////////////////////////////////////////////////////////
// File: register_logging.cpp                                                 //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-01-08                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/logging.hpp>

namespace py = pybind11;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_logging(py::module &m) {
    py::enum_<respond::LogType>(m, "LogType")
        .value("kInfo", respond::LogType::kInfo)
        .value("kWarn", respond::LogType::kWarn)
        .value("kError", respond::LogType::kError)
        .value("kDebug", respond::LogType::kDebug)
        .export_values();
    py::enum_<respond::CreationStatus>(m, "CreationStatus")
        .value("kError", respond::CreationStatus::kError)
        .value("kSuccess", respond::CreationStatus::kSuccess)
        .value("kExists", respond::CreationStatus::kExists)
        .value("kNotCreated", respond::CreationStatus::kNotCreated)
        .export_values();

    m.def("create_file_logger", &respond::CreateFileLogger,
          "Creates a File Logger for use with RESPOND.");

    m.def("log_info", &respond::LogInfo, "Logs an info message to the log.");
    m.def("log_warning", &respond::LogWarning,
          "Logs a warning message to the log.");
    m.def("log_error", &respond::LogError, "Logs an error message to the log.");
    m.def("log_debug", &respond::LogDebug, "Logs a debug message to the log.");
}
