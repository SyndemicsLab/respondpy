////////////////////////////////////////////////////////////////////////////////
// File: pybind11.hpp                                                         //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-02-05                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////
#ifndef RESPONDPY_PYBIND_HPP_
#define RESPONDPY_PYBIND_HPP_

#include <pybind11/eigen.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <sstream>
#include <stdexcept>
#include <string>

namespace py = pybind11;

namespace respond {}

inline Eigen::VectorXd vector_from_python(const py::handle &value) {
    using Array = py::array_t<double, py::array::c_style | py::array::forcecast>;
    const auto array = Array::ensure(value);
    if (!array) {
        throw py::type_error("Expected a numeric one- or two-dimensional array.");
    }

    const auto info = array.request();
    if (info.ndim == 1) {
        return Eigen::Map<const Eigen::VectorXd>(
            static_cast<const double *>(info.ptr), info.shape[0]);
    }
    if (info.ndim == 2 && (info.shape[0] == 1 || info.shape[1] == 1)) {
        return Eigen::Map<const Eigen::VectorXd>(
            static_cast<const double *>(info.ptr), info.shape[0] * info.shape[1]);
    }
    throw py::value_error("Expected a vector with shape (N,), (N, 1), or (1, N).");
}

template <class T> std::string to_string(const T &x) {
    std::ostringstream oss;
    oss << x;
    return oss.str();
}

#endif // RESPONDPY_PYBIND_HPP_