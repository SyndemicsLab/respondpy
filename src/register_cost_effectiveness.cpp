////////////////////////////////////////////////////////////////////////////////
// File: register_cost_effectiveness.cpp                                      //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-09                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <pybind11/pybind11.h>

#include <respond/cost_effectiveness.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_cost_effectiveness(py::module &m) {
    m.def("discount", &respond::Discount,
          "Calculates the Discount for the provided Vector given the discount "
          "rate, week, and flag to indicate if it is discrete or not.");
    m.def("cwise_product", &respond::CwiseProduct,
          "Calculate the element wise product of two matrices.");
    m.def("cwise_min", &respond::CwiseMin,
          "Calculate the element wise minimum of two matrices.");
    m.def("calculate_life_years", &respond::CalculateLifeYears,
          "Calculate the life years.");
}
