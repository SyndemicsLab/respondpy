////////////////////////////////////////////////////////////////////////////////
// File: register_logging.cpp                                                 //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-07-16                                                  //
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
    py::enum_<respond::LogPattern>(m, "LogPattern")
        .value("kSimple", respond::LogPattern::kSimple)
        .value("kStandard", respond::LogPattern::kStandard)
        .value("kDetailed", respond::LogPattern::kDetailed)
        .value("kThreadSafe", respond::LogPattern::kThreadSafe)
        .export_values();

    m.def("create_file_logger", &respond::CreateFileLogger,
          py::arg("logger_name"), py::arg("filepath"),
          "Creates a File Logger for use with RESPOND.");
    m.def("create_shared_file_sink", &respond::CreateSharedFileSink,
          py::arg("filepath"),
          "Create a shared file sink for thread-safe concurrent logging from "
          "multiple models or threads to the same output file. Call before "
          "create_shared_logger().");
    m.def("create_shared_logger", &respond::CreateSharedLogger,
          py::arg("logger_name"),
          "Create a logger that writes to the shared file sink. Requires "
          "create_shared_file_sink() to be called first.");

    m.def("set_log_pattern", &respond::SetLogPattern, py::arg("pattern"),
          "Set the logging pattern template for all subsequent logger "
          "creations.");
    m.def("get_log_pattern", &respond::GetLogPattern,
          "Get the current logging pattern template.");
    m.def("set_flush_interval", &respond::SetFlushInterval, py::arg("seconds"),
          "Set the global flush interval in seconds (0 to disable "
          "auto-flush).");
    m.def("flush_all_loggers", &respond::FlushAllLoggers,
          "Flush all active loggers, ensuring buffered output is written.");

    m.def("check_logger_exists", &respond::CheckLoggerExists,
          py::arg("logger_name"),
          "Check if a logger with the given name exists. Returns "
          "CreationStatus.kExists or kNotCreated.");
    m.def("get_logger_info", &respond::GetLoggerInfo, py::arg("logger_name"),
          "Retrieve a string with details about a logger (name, file path, "
          "level, thread info).");
    m.def("set_logger_level", &respond::SetLoggerLevel, py::arg("logger_name"),
          py::arg("level"),
          "Set the logging level for a specific logger. level: 0=trace, "
          "1=debug, 2=info, 3=warn, 4=error, 5=critical.");

    m.def("log_info", &respond::LogInfo, py::arg("logger_name"),
          py::arg("message"), "Logs an info message to the log.");
    m.def("log_warning", &respond::LogWarning, py::arg("logger_name"),
          py::arg("message"), "Logs a warning message to the log.");
    m.def("log_error", &respond::LogError, py::arg("logger_name"),
          py::arg("message"), "Logs an error message to the log.");
    m.def("log_debug", &respond::LogDebug, py::arg("logger_name"),
          py::arg("message"), "Logs a debug message to the log.");
}
