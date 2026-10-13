////////////////////////////////////////////////////////////////////////////////
// File: register_runtime_config.cpp                                          //
// Project: respondpy                                                         //
// Created Date: 2026-09-24                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-09-24                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/execution_config.hpp>
#include <respond/logging_config.hpp>
#include <respond/runtime_config.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_runtime_config(py::module &m) {
    py::class_<ExecutionConfig>(m, "ExecutionConfig")
        .def(py::init<>())
        .def_readwrite("total_threads", &ExecutionConfig::total_threads)
        .def_readwrite("eigen_threads", &ExecutionConfig::eigen_threads)
        .def_readwrite("run_models_concurrently",
                       &ExecutionConfig::run_models_concurrently);

    py::class_<LoggingConfig>(m, "LoggingConfig")
        .def(py::init<>())
        .def_readwrite("logger_name", &LoggingConfig::logger_name)
        .def_readwrite("file_path", &LoggingConfig::file_path)
        .def_readwrite("use_shared_sink", &LoggingConfig::use_shared_sink);

    py::class_<RuntimeConfig>(m, "RuntimeConfig")
        .def(py::init<>())
        .def_readwrite("execution", &RuntimeConfig::execution)
        .def_readwrite("logging", &RuntimeConfig::logging);
}