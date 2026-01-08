////////////////////////////////////////////////////////////////////////////////
// File: pybind11.hpp                                                         //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-01-08                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////
#ifndef RESPONDPY_PYBIND_HPP_
#define RESPONDPY_PYBIND_HPP_

#include <pybind11/eigen.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <sstream>
#include <string>

namespace py = pybind11;

namespace respond {}

template <class T> std::string to_string(const T &x) {
    std::ostringstream oss;
    oss << x;
    return oss.str();
}

#endif // RESPONDPY_PYBIND_HPP_