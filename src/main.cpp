#include <pybind11/pybind11.h>

#include <sstream>

#include "bbox_2.h"
#include "point_2.h"

namespace py = pybind11;

const std::string module_name = "_martinez";

PYBIND11_MODULE(_martinez, m) {
  m.doc() = R"pbdoc(
        Python binding of polygon clipping algorithm by F. Martínez et al.
    )pbdoc";

  py::class_<cbop::Point_2>(m, "Point")
      .def(py::init<double, double>(), py::arg("x") = 0., py::arg("y") = 0.)
      .def("__repr__",
           [&](const cbop::Point_2& self) {
             std::ostringstream stream;
             stream << module_name + ".Point(" << self.x() << ", " << self.y()
                    << ")";
             return std::string(stream.str());
           })
      .def("__eq__", [](const cbop::Point_2& self,
                        const cbop::Point_2& other) { return self == other; })
      .def("distance_to", &cbop::Point_2::dist)
      .def_property_readonly("x", &cbop::Point_2::x)
      .def_property_readonly("y", &cbop::Point_2::y)
      .def_property_readonly("bounding_box", &cbop::Point_2::bbox);

  py::class_<cbop::Bbox_2>(m, "BoundingBox")
      .def(py::init<double, double, double, double>(), py::arg("x_min") = 0.,
           py::arg("y_min") = 0., py::arg("x_max") = 0., py::arg("y_max") = 0.)
      .def("__repr__",
           [&](const cbop::Bbox_2& self) {
             std::ostringstream stream;
             stream << module_name + ".BoundingBox(" << self.xmin() << ", "
                    << self.ymin() << ", " << self.xmax() << ", " << self.ymax()
                    << ")";
             return std::string(stream.str());
           })
      .def("__eq__",
           [](const cbop::Bbox_2& self, const cbop::Bbox_2& other) {
             return self.xmin() == other.xmin() &&
                    self.ymin() == other.ymin() &&
                    self.xmax() == other.xmax() && self.ymax() == other.ymax();
           })
      .def_property_readonly("x_min", &cbop::Bbox_2::xmin)
      .def_property_readonly("y_min", &cbop::Bbox_2::ymin)
      .def_property_readonly("x_max", &cbop::Bbox_2::xmax)
      .def_property_readonly("y_max", &cbop::Bbox_2::ymax)
      .def("__add__", &cbop::Bbox_2::operator+);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
