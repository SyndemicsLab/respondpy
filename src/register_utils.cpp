////////////////////////////////////////////////////////////////////////////////
// File: register_utils.cpp                                                   //
// Project: respondpy                                                         //
// Created Date: 2025-05-23                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2025-05-23                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2025 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <pybind11/pybind11.h>

#include <pybind11/eigen.h>
#include <pybind11/eigen/tensor.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <respond/utils/logging.hpp>

namespace py = pybind11;
using namespace respond::utils;

void register_utils(py::module &utils) {
    // logging.hpp
    py::enum_<CreationStatus>(utils, "CreationStatus")
        .value("kError", CreationStatus::kError)
        .value("kSuccess", CreationStatus::kSuccess)
        .value("kExists", CreationStatus::kExists)
        .value("kNotCreated", CreationStatus::kNotCreated)
        .export_values();

    utils.def("create_file_logger", &CreateFileLogger,
              "Creates a File Logger for use with RESPOND.");
}