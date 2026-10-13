////////////////////////////////////////////////////////////////////////////////
// File: helpers.hpp                                                          //
// Project: respondpy                                                         //
// Created Date: 2026-10-13                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-10-13                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#ifndef RESPONDPY_INTERNAL_HELPERS_HPP_
#define RESPONDPY_INTERNAL_HELPERS_HPP_

#include <cstddef>

#include <respondpy/pybind11.hpp>

namespace respondpy::helpers {

/// @brief Normalize a potentially negative index to a non-negative index within
/// the bounds of a container. This allows Pythonic-like negative indexing.
/// @param count The number of elements in the container.
/// @param index The index to normalize. Can be negative to count from the end.
/// @return The normalized non-negative index.
/// @throws pybind11::index_error If the index is out of range.
inline size_t normalize_index(size_t count, pybind11::ssize_t index) {
    const auto normalized =
        index < 0 ? static_cast<pybind11::ssize_t>(count) + index : index;
    if (normalized < 0 || static_cast<size_t>(normalized) >= count) {
        throw pybind11::index_error("index out of range");
    }
    return static_cast<size_t>(normalized);
}

/// @brief Convert an Eigen vector to a JSON-compatible Python list.
/// @param value The Eigen vector to convert.
/// @return A Python list containing the elements of the Eigen vector.
inline pybind11::list vector_to_json(const Eigen::VectorXd &value) {
    pybind11::list result;
    for (Eigen::Index index = 0; index < value.size(); ++index) {
        result.append(value(index));
    }
    return result;
}

} // namespace respondpy::helpers

#endif // RESPONDPY_INTERNAL_HELPERS_HPP