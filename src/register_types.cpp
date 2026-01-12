////////////////////////////////////////////////////////////////////////////////
// File: register_types.cpp                                                   //
// Project: respondpy                                                         //
// Created Date: 2026-01-08                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-01-08                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/types.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_types(py::module &m) {
    // types.hpp
    py::class_<HistoryStamp>(m, "HistoryStamp")
        .def(py::init())
        .def_readwrite("state", &HistoryStamp::state)
        .def_readwrite("overdoses", &HistoryStamp::overdoses)
        .def_readwrite("intervention_admissions",
                       &HistoryStamp::intervention_admissions);

    py::class_<CostStamp>(m, "CostStamp")
        .def(py::init())
        .def_readwrite("healthcare", &CostStamp::healthcare)
        .def_readwrite("non_fatal_overdoses", &CostStamp::non_fatal_overdoses)
        .def_readwrite("fatal_overdoses", &CostStamp::fatal_overdoses)
        .def_readwrite("pharmaceuticals", &CostStamp::pharmaceuticals)
        .def_readwrite("treatments", &CostStamp::treatments);

    py::enum_<UtilityType>(m, "UtilityType")
        .value("kMin", UtilityType::kMin)
        .value("kMult", UtilityType::kMult)
        .export_values();

    py::class_<ResultSets>(m, "ResultSets")
        .def(py::init())
        .def_readwrite("summed_costs", &ResultSets::summed_costs)
        .def_readwrite("summed_life_years", &ResultSets::summed_life_years)
        .def_readwrite("summed_utility", &ResultSets::summed_utility);

    py::class_<Totals>(m, "Totals")
        .def(py::init())
        .def_readwrite("base", &Totals::base)
        .def_readwrite("discounted", &Totals::discounted);
}
