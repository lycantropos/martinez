#include <pybind11/pybind11.h>

#include "point_2.h"

namespace py = pybind11;

PYBIND11_MODULE(_martinez, m) {
  m.doc() = R"pbdoc(
        Python binding of polygon clipping algorithm by F. Martínez et al.
        ------------------------------------------------------------------
        .. currentmodule: martinez
        .. autosummary::
           :toctree: _generate

    )pbdoc";

  py::class_<cbop::Point_2>(m, "Point_2")
      .def(py::init<double, double>(), py::arg("x")=0., py::arg("y")=0.)
      .def_property_readonly("x", &cbop::Point_2::x)
      .def_property_readonly("y", &cbop::Point_2::y);

#ifdef VERSION_INFO
          m.attr("__version__") = VERSION_INFO;
#else
          m.attr("__version__") = "dev";
#endif
}
