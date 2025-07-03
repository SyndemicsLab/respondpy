////////////////////////////////////////////////////////////////////////////////
// File: respondpy.cpp                                                        //
// Project: respondpy                                                         //
// Created Date: 2025-05-21                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2025-07-03                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2025 Syndemics Lab at Boston Medical Center                  //
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
using namespace respond::data_ops;
using namespace respond::model;
using namespace respond::utils;

PYBIND11_MODULE(respondpy, m) {
    auto data_ops = m.def_submodule(
        "data_ops",
        "A submodule containing the data operations necessary for RESPOND.");

    // base_loader.hpp
    py::class_<BaseLoader>(data_ops, "BaseLoader")
        .def("load_data_table", &BaseLoader::LoadDataTable,
             pybind11::arg("path"), pybind11::arg("headers") = true)
        .def("set_config", &BaseLoader::SetConfig, pybind11::arg("config_file"))
        .def("get_config", &BaseLoader::GetConfig);

    // cost_loader.hpp
    py::class_<CostLoader, BaseLoader>(data_ops, "CostLoader")
        .def(py::init(&CostLoader::Create),
             pybind11::arg("log_name") = "console")
        .def("load_healthcare_utilization_cost",
             &CostLoader::LoadHealthcareUtilizationCost)
        .def("load_overdose_cost", &CostLoader::LoadOverdoseCost)
        .def("load_pharmaceutical_cost", &CostLoader::LoadPharmaceuticalCost)
        .def("load_treatment_utilization_cost",
             &CostLoader::LoadTreatmentUtilizationCost)
        .def("get_healthcare_utilization_cost",
             &CostLoader::GetHealthcareUtilizationCost)
        .def("get_pharmaceutical_cost", &CostLoader::GetPharmaceuticalCost)
        .def("get_treatment_utilization_cost",
             &CostLoader::GetTreatmentUtilizationCost)
        .def("get_non_fatal_overdose_cost",
             &CostLoader::GetNonFatalOverdoseCost)
        .def("get_fatal_overdose_cost", &CostLoader::GetFatalOverdoseCost);

    // data_formatter.hpp
    py::class_<DataFormatter>(data_ops, "DataFormatter")
        .def(py::init(&DataFormatter::Create))
        .def("extract_timesteps", &DataFormatter::ExtractTimesteps);

    // data_loader.hpp
    py::class_<DataLoader, BaseLoader>(data_ops, "DataLoader")
        .def(py::init(&DataLoader::Create),
             pybind11::arg("log_name") = "console")
        .def("get_initial_sample", &DataLoader::GetInitialSample)
        .def("get_entering_samples", &DataLoader::GetEnteringSamples)
        .def("get_oud_transition_rates", &DataLoader::GetOUDTransitionRates)
        .def("get_intervention_transition_rates",
             &DataLoader::GetInterventionTransitionRates)
        .def("get_overdose_rates", &DataLoader::GetOverdoseRates)
        .def("get_fatal_overdose_rates", &DataLoader::GetFatalOverdoseRates)
        .def("get_mortality_rates", &DataLoader::GetMortalityRates)
        .def("get_intervention_init_rates",
             &DataLoader::GetInterventionInitRates)
        .def("set_initial_sample", &DataLoader::SetInitialSample)
        .def("set_entering_samples", &DataLoader::SetEnteringSamples)
        .def("set_oud_transition_rates", &DataLoader::SetOUDTransitionRates)
        .def("set_intervention_transition_rates",
             &DataLoader::SetInterventionTransitionRates)
        .def("set_overdose_rates", &DataLoader::SetOverdoseRates)
        .def("set_fatal_overdose_rates", &DataLoader::SetFatalOverdoseRates)
        .def("set_mortality_rates", &DataLoader::SetMortalityRates)
        .def("set_intervention_init_rates",
             &DataLoader::SetInterventionInitRates)
        .def("load_initial_sample", &DataLoader::LoadInitialSample)
        .def("load_entering_samples",
             py::overload_cast<const std::string &, const std::string &,
                               const std::string &>(
                 &DataLoader::LoadEnteringSamples))
        .def("load_entering_samples", py::overload_cast<const std::string &>(
                                          &DataLoader::LoadEnteringSamples))
        .def("load_oud_transition_rates", &DataLoader::LoadOUDTransitionRates)
        .def("load_intervention_init_rates",
             &DataLoader::LoadInterventionInitRates)
        .def("load_intervention_transition_rates",
             &DataLoader::LoadInterventionTransitionRates)
        .def("load_overdose_rates", &DataLoader::LoadOverdoseRates)
        .def("load_fatal_overdose_rates", &DataLoader::LoadFatalOverdoseRates)
        .def("load_mortality_rates", &DataLoader::LoadMortalityRates);

    // data_types.hpp
    py::enum_<Dimension>(data_ops, "Dimension")
        .value("kIntervention", Dimension::kIntervention)
        .value("kOud", Dimension::kOud)
        .value("kDemographicCombo", Dimension::kDemographicCombo)
        .export_values();

    py::class_<History>(data_ops, "History")
        .def(py::init())
        .def_readwrite("state_history", &History::state_history)
        .def_readwrite("overdose_history", &History::overdose_history)
        .def_readwrite("fatal_overdose_history",
                       &History::fatal_overdose_history)
        .def_readwrite("mortality_history", &History::mortality_history)
        .def_readwrite("intervention_admission_history",
                       &History::intervention_admission_history);

    py::class_<Cost>(data_ops, "Cost")
        .def(py::init())
        .def_readwrite("perspective", &Cost::perspective)
        .def_readwrite("healthcare_cost", &Cost::healthcare_cost)
        .def_readwrite("non_fatal_overdose_cost",
                       &Cost::non_fatal_overdose_cost)
        .def_readwrite("fatal_overdose_cost", &Cost::fatal_overdose_cost)
        .def_readwrite("pharma_cost", &Cost::pharma_cost)
        .def_readwrite("treatment_cost", &Cost::treatment_cost);

    py::enum_<UtilityType>(data_ops, "UtilityType")
        .value("kMin", UtilityType::kMin)
        .value("kMult", UtilityType::kMult)
        .export_values();

    py::class_<Totals>(data_ops, "Totals")
        .def(py::init())
        .def_readwrite("base_costs", &Totals::base_costs)
        .def_readwrite("disc_costs", &Totals::disc_costs)
        .def_readwrite("base_life_years", &Totals::base_life_years)
        .def_readwrite("disc_life_years", &Totals::disc_life_years)
        .def_readwrite("base_utility", &Totals::base_utility)
        .def_readwrite("disc_utility", &Totals::disc_utility);

    // matrices.hpp
    data_ops.def("create_matrix3d", &CreateMatrix3d,
                 "A Factory Function to generate a new Eigen Matrix3d.");
    data_ops.def("print_matrix3d", &PrintMatrix3d,
                 "Prints an Eigen Matrix3d to the provided stream.");
    data_ops.def("print_timed_matrix3d", &PrintTimedMatrix3d,
                 "Prints a TimedMatrix3d to the provided stream.");
    data_ops.def("vec_min_matrix3d", &Matrix3dVectorMinimum,
                 "Returns the minimum of a vector of Eigen Matrix3d.");
    data_ops.def("vec_mult_matrix3d", &Matrix3dVectorMultiplied,
                 "Returns the product of a vector of Eigen Matrix3d.");
    data_ops.def("sum_timed_matrix3d", &TimedMatrix3dSummed,
                 "Returns the sum of a TimedMatrix3d.");
    data_ops.def("sum_timed_matrix3d_over_dimensions",
                 &TimedMatrix3dSummedOverDimensions,
                 "Returns the sum of all elements in a TimedMatrix3d.");
    data_ops.def("mult_timed_matrix3d_by_double",
                 &MultiplyTimedMatrix3dByDouble,
                 "Multiply a TimedMatrix3d by a double.");
    data_ops.def("mult_timed_matrix3d_by_matrix",
                 &MultiplyTimedMatrix3dByMatrix,
                 "Multiply a TimedMatrix3d by another Matrix3d.");

    // utility_loader.hpp
    py::class_<UtilityLoader, BaseLoader>(data_ops, "UtilityLoader")
        .def(py::init(&UtilityLoader::Create),
             pybind11::arg("log_name") = "console")
        .def("load_background_utility", &UtilityLoader::LoadBackgroundUtility)
        .def("load_oud_utility", &UtilityLoader::LoadOUDUtility)
        .def("load_setting_utility", &UtilityLoader::LoadSettingUtility)
        .def("get_background_utility", &UtilityLoader::GetBackgroundUtility)
        .def("get_oud_utility", &UtilityLoader::GetOUDUtility)
        .def("get_setting_utility", &UtilityLoader::GetSettingUtility);

    // writer.hpp
    py::enum_<WriterType>(data_ops, "WriterType")
        .value("kInput", WriterType::kInput)
        .value("kOutput", WriterType::kOutput)
        .value("kHistory", WriterType::kHistory)
        .value("kCost", WriterType::kCost)
        .value("kUtilities", WriterType::kUtilities)
        .value("kTotals", WriterType::kTotals)
        .export_values();

    py::enum_<OutputType>(data_ops, "OutputType")
        .value("kString", OutputType::kString)
        .value("kFile", OutputType::kFile)
        .export_values();

    py::class_<Writer>(data_ops, "Writer")
        .def(py::init(&Writer::Create), pybind11::arg("directory") = "",
             pybind11::arg("log_name") = "console")
        .def("write_input_data", &Writer::WriteInputData)
        .def("write_history_data", &Writer::WriteHistoryData)
        .def("write_cost_data", &Writer::WriteCostData)
        .def("write_utility_data", &Writer::WriteUtilityData)
        .def("write_totals_data", &Writer::WriteTotalsData);

    auto model = m.def_submodule(
        "model", "A submodule containing the model components for RESPOND.");

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

    auto utils = m.def_submodule(
        "utils", "A submodule containing the utility functions for RESPOND.");

    // logging.hpp
    py::enum_<CreationStatus>(utils, "CreationStatus")
        .value("kError", CreationStatus::kError)
        .value("kSuccess", CreationStatus::kSuccess)
        .value("kExists", CreationStatus::kExists)
        .value("kNotCreated", CreationStatus::kNotCreated)
        .export_values();

    utils.def("create_file_logger", &CreateFileLogger,
              "Creates a File Logger for use with RESPOND.");
}