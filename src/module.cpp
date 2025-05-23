////////////////////////////////////////////////////////////////////////////////
// File: module.cpp                                                           //
// Project: respondpy                                                         //
// Created Date: 2025-01-14                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2025-05-23                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2025 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <pybind11/pybind11.h>

namespace py = pybind11;

void register_data_ops(py::module &data_ops);
void register_model(py::module &model);
void register_utils(py::module &utils);

PYBIND11_MODULE(_core, m, py::mod_gil_not_used()) {
    py::module data_ops = m.def_submodule(
        "data_ops",
        "A submodule containing the data operations necessary for RESPOND.");
    register_data_ops(data_ops);

    py::module model = m.def_submodule(
        "model", "A submodule containing the model components for RESPOND.");
    register_model(model);

    py::module utils = m.def_submodule(
        "utils", "A submodule containing the utility functions for RESPOND.");
}