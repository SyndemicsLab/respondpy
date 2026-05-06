////////////////////////////////////////////////////////////////////////////////
// File: register_transition.cpp                                              //
// Project: respondpy                                                         //
// Created Date: 2026-02-02                                                   //
// Author: Matthew Carroll                                                    //
// -----                                                                      //
// Last Modified: 2026-05-06                                                  //
// Modified By: Matthew Carroll                                               //
// -----                                                                      //
// Copyright (c) 2026 Syndemics Lab at Boston Medical Center                  //
////////////////////////////////////////////////////////////////////////////////

#include <respondpy/pybind11.hpp>

#include <map>
#include <string>

#include <respond/history.hpp>
#include <respond/logging.hpp>
#include <respond/transition.hpp>
#include <respond/transition_factory.hpp>

namespace py = pybind11;
using namespace respond;

// NOLINTNEXTLINE(misc-use-internal-linkage)
void register_transition(py::module &m) {
    py::class_<Transition, py::smart_holder> t(m, "Transition");
    t.def(py::init(&TransitionFactory::CreateTransition), py::arg("type"),
          py::arg("log_name") = "console")
        .def("execute",
             [](const Transition &self, const Eigen::VectorXd &state,
                py::object hist_obj) {
                 std::map<std::string, History> h;
                 if (hist_obj.is_none()) {
                     LogWarning(self.GetLogName(),
                                "execute() called without a history map. "
                                "History will not be recorded. Pass the "
                                "model's history map for expected behavior.");
                 } else {
                     h = hist_obj.cast<std::map<std::string, History>>();
                 }
                 auto result = self.Execute(state, h);
                 return py::make_tuple(result, h);
             },
             py::arg("state"), py::arg("history") = py::none(),
             "Execute the transition on the given state. Returns "
             "(state_result, history_map). Pass the model's history map for "
             "expected behavior; omitting it will issue a warning and the "
             "returned history map will be empty.")
        .def("add_transition_matrix", &Transition::AddTransitionMatrix)
        .def("get_transition_name", &Transition::GetTransitionName)
        .def("clear_transition_matrices", &Transition::ClearTransitionMatrices)
        .def("get_log_name", &Transition::GetLogName)
        .def("__repr__",
             [](const Transition &m) {
                 return "<respondpy.Transition named " + m.GetTransitionName() +
                        " >";
             })
        .def("__copy__", [](const Transition &self) { return self.clone(); })
        .def(
            "__deepcopy__",
            [](const Transition &self, py::dict) { return self.clone(); },
            "memo");
}