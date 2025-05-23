////////////////////////////////////////////////////////////////////////////////
// File: register_model.cpp                                                   //
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

#include <respond/model/post_sim.hpp>
#include <respond/model/simulation.hpp>

namespace py = pybind11;
using namespace respond::model;

void register_model(py::module &model) {
    // post_sim.hpp
    model.def("calculate_discount", &CalculateDiscount,
              "Calculates the Discount for the provided Matrix3d.");
    model.def("calculate_costs", &CalculateCosts,
              "Calculates the Costs of the provided History.");
    model.def("calculate_utilities", &CalculateUtilities,
              "Calculate the Utilities of the provided History.");
    model.def("calculate_life_years", &CalculateLifeYears,
              "Calculate the Life Years of the provided History.");
    model.def("calculate_total_costs", &CalculateTotalCosts,
              "Calculate the Total Costs of the provided History.");

    // simulation.hpp
    py::class_<Respond>(model, "Respond")
        .def(py::init(&Respond::Create), pybind11::arg("log_name") = "console")
        .def("run", &Respond::Run)
        .def("get_history", &Respond::GetHistory);
}