////////////////////////////////////////////////////////////////////////////////
// File: register_cost_effectiveness.cpp                                      //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-09-25                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/cost_effectiveness.hpp>

namespace py = pybind11;
using namespace respond;

using DoubleArray =
    py::array_t<double, py::array::c_style | py::array::forcecast>;

Eigen::VectorXd to_vector(const DoubleArray &data) {
    if (data.ndim() != 1) {
        throw py::value_error("Expected a one-dimensional numeric array.");
    }
    return Eigen::Map<const Eigen::VectorXd>(
        data.data(), static_cast<Eigen::Index>(data.size()));
}

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_cost_effectiveness(py::module &m) {
    m.def(
        "discount",
        [](const DoubleArray &data, double discount_rate, int week,
           bool is_discrete, double total_weeks) {
            return respond::Discount(to_vector(data), discount_rate, week,
                                     is_discrete, total_weeks);
        },
        py::arg("data"), py::arg("discount_rate"), py::arg("week"),
        py::arg("is_discrete") = true, py::arg("total_weeks") = 52.0,
        "Calculates the Discount for the provided Vector given the discount "
        "rate, week, and flag to indicate if it is discrete or not.");
    m.def(
        "cwise_product",
        [](const DoubleArray &state, const DoubleArray &multiplier) {
            return respond::CwiseProduct(to_vector(state),
                                         to_vector(multiplier));
        },
        py::arg("state"), py::arg("multiplier"),
        "Calculate the element wise product of two matrices.");
    m.def(
        "cwise_min",
        [](const DoubleArray &state, const DoubleArray &multiplier) {
            return respond::CwiseMin(to_vector(state), to_vector(multiplier));
        },
        py::arg("state"), py::arg("multiplier"),
        "Calculate the element wise minimum of two matrices.");
    m.def("calculate_life_years", &respond::CalculateLifeYears,
          "Calculate the life years.");
}
