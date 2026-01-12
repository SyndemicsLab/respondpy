////////////////////////////////////////////////////////////////////////////////
// File: register_cost_effectiveness.cpp                                      //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-01-08                                                  //
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
    m.def("discount_cost_stamp", &respond::DiscountCostStamp,
          "Apply a discount to the given cost stamp.");
    m.def("stamp_costs", &respond::StampCosts, "Build a Cost Stamp.");
    m.def("stamp_utilities", &respond::StampUtilities,
          "Build a Utility Stamp.");
    m.def("stamp_costs_over_time", &respond::StampCostsOverTime,
          "Stamp costs over a history time period.");
    m.def("stamp_utilities_over_time", &respond::StampUtilitiesOverTime,
          "Stamp utilities over a history time period.");
    m.def("calculate_perspectives", &respond::CalculatePerspectives,
          "Calculate the Cost Stamps for the given perspectives.");
    m.def("calculate_life_years", &respond::CalculateLifeYears,
          "Calculate the life years.");
    m.def("calculate_total_costs", &respond::CalculateTotalCosts,
          "Calculate the total costs.");
}
