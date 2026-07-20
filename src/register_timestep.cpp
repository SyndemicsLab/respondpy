////////////////////////////////////////////////////////////////////////////////
// File: register_timestep.cpp                                                //
// Project: respondpy                                                         //
// Created Date: 2026-07-16                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-07-16                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <respond/timestep.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_timestep(py::module &m) {
    py::class_<Timestep>(m, "Timestep")
        .def(py::init<>(), "Default constructor for a Timestep instance.")
        .def(py::init<const std::string &>(), py::arg("log_name"),
             "Constructs a Timestep with a specified log_name.")
        .def(
            py::init<const std::string &, const std::string &>(),
            py::arg("log_name"), py::arg("log_filepath"),
            "Constructs a Timestep with a specified log_name and log_filepath.")
        .def("__copy__", [](const Timestep &self) { return Timestep(self); })
        .def(
            "__deepcopy__",
            [](const Timestep &self, py::dict) { return Timestep(self); },
            "memo")
        .def(
            "create_transition",
            [](Timestep &self,
               const std::string &transition_name) -> const Transition * {
                return self.CreateTransition(transition_name).get();
            },
            py::arg("transition_name"),
            py::return_value_policy::reference_internal,
            "Create a new transition instance and add it to the timestep. "
            "Returns a reference to the created transition.")
        .def("remove_transition", &Timestep::RemoveTransition, py::arg("idx"),
             "Remove a transition from the timestep by its idx. Throws an "
             "exception if the idx is out of bounds.")
        .def(
            "add_matrix_to_transition",
            py::overload_cast<const size_t &,
                              const Eigen::Ref<const Eigen::MatrixXd> &>(
                &Timestep::AddMatrixToTransition),
            py::arg("idx"), py::arg("matrix"),
            "Add a matrix to a transition in the timestep by its index. Throws "
            "an exception if the index is out of bounds.")
        .def("add_matrix_to_transition",
             py::overload_cast<const std::string &,
                               const Eigen::Ref<const Eigen::MatrixXd> &>(
                 &Timestep::AddMatrixToTransition),
             py::arg("transition_name"), py::arg("matrix"),
             "Add a matrix to a transition in the timestep by its name. Throws "
             "an exception if the transition name is not found.")
        .def(
            "get_transition",
            [](const Timestep &self, const size_t &idx) -> const Transition * {
                return self.GetTransition(idx).get();
            },
            py::arg("idx"), py::return_value_policy::reference_internal,
            "Get a transition from the timestep by its index. Throws an "
            "exception if the index is out of bounds.")
        .def(
            "get_transition",
            [](const Timestep &self,
               const std::string &transition_name) -> const Transition * {
                return self.GetTransition(transition_name).get();
            },
            py::arg("transition_name"),
            py::return_value_policy::reference_internal,
            "Get a transition from the timestep by its name. Throws an "
            "exception if the transition name is not found.")
        .def("get_transitions", &Timestep::GetTransitions,
             "Get the list of transitions in the timestep.")
        .def("get_transition_names", &Timestep::GetTransitionNames,
             "Get the list of transition names in the timestep.")
        .def("__repr__",
             [](const Timestep &t) {
                 std::stringstream ss;
                 ss << t;
                 return ss.str();
             })
        .def("__eq__", &Timestep::operator==,
             "Check if two Timestep instances are equal.")
        .def("__ne__", &Timestep::operator!=,
             "Check if two Timestep instances are not equal.");
}