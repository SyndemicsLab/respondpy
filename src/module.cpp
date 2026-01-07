////////////////////////////////////////////////////////////////////////////////
// File: module.cpp                                                           //
// Project: respondpy                                                         //
// Created Date: 2025-08-01                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-01-07                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2025-2026 Syndemics Lab at Boston Medical Center             //
////////////////////////////////////////////////////////////////////////////////

#include <respond/respond.hpp>

#include <memory>
#include <string>

#include <pybind11/eigen.h>
#include <pybind11/eigen/tensor.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace respond;

PYBIND11_MODULE(respondpy, m) {
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

    // cost_effectiveness.hpp
    m.def("discount", &Discount,
          "Calculates the Discount for the provided Vector given the discount "
          "rate, week, and flag to indicate if it is discrete or not.");
    m.def("discount_cost_stamp", &DiscountCostStamp,
          "Apply a discount to the given cost stamp.");
    m.def("stamp_costs", &StampCosts, "Build a Cost Stamp.");
    m.def("stamp_utilities", &StampUtilities, "Build a Utility Stamp.");
    m.def("stamp_costs_over_time", &StampCostsOverTime,
          "Stamp costs over a history time period.");
    m.def("stamp_utilities_over_time", &StampUtilitiesOverTime,
          "Stamp utilities over a history time period.");
    m.def("calculate_perspectives", &CalculatePerspectives,
          "Calculate the Cost Stamps for the given perspectives.");
    m.def("calculate_life_years", &CalculateLifeYears,
          "Calculate the life years.");
    m.def("calculate_total_costs", &CalculateTotalCosts,
          "Calculate the total costs.");

    // markov.hpp
    py::class_<Markov>(m, "Markov")
        .def(py::init(&Markov::Create), pybind11::arg("log_name") = "console")
        .def("set_state", &Markov::SetState)
        .def("get_state", &Markov::GetState)
        .def("set_transitions", &Markov::SetTransitions)
        .def("get_transitions", &Markov::GetTransitions)
        .def("add_transition", &Markov::AddTransition)
        .def("run", &Markov::Run)
        .def("get_run_results", &Markov::GetRunResults);

    // respond.hpp
    m.def("migration", &Migration, "Applies the Migrating Cohort.");
    m.def("behavior", &Behavior, "Applies the Behavior Transition.");
    m.def("intervention", &Intervention,
          "Applies the Intervention Transition.");
    m.def("overdose", &Overdose, "Applies the Overdose Transition.");
    m.def("mortality", &Mortality, "Applies the Mortality Transition.");

    // logging.hpp
    py::enum_<LogType>(m, "LogType")
        .value("kInfo", LogType::kInfo)
        .value("kWarn", LogType::kWarn)
        .value("kError", LogType::kError)
        .value("kDebug", LogType::kDebug)
        .export_values();
    py::enum_<CreationStatus>(m, "CreationStatus")
        .value("kError", CreationStatus::kError)
        .value("kSuccess", CreationStatus::kSuccess)
        .value("kExists", CreationStatus::kExists)
        .value("kNotCreated", CreationStatus::kNotCreated)
        .export_values();

    m.def("create_file_logger", &CreateFileLogger,
          "Creates a File Logger for use with RESPOND.");

    m.def("log_info", &LogInfo, "Logs an info message to the log.");
    m.def("log_warning", &LogWarning, "Logs a warning message to the log.");
    m.def("log_error", &LogError, "Logs an error message to the log.");
    m.def("log_debug", &LogDebug, "Logs a debug message to the log.");
}