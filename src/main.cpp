#include <pybind11/pybind11.h>

#include <iomanip>
#include <limits>
#include <sstream>

#include "bbox_2.h"
#include "point_2.h"
#include "segment_2.h"

namespace py = pybind11;

#define MODULE_NAME _martinez
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define BOUNDING_BOX_NAME "BoundingBox"
#define POINT_NAME "Point"
#define SEGMENT_NAME "Segment"

std::ostringstream make_stream() {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  return stream;
}

std::string point_repr(const cbop::Point_2& self) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << self.x() << ", "
         << self.y() << ")";
  return stream.str();
}

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of polygon clipping algorithm by F. Martínez et al.
    )pbdoc";

  py::class_<cbop::Bbox_2>(m, BOUNDING_BOX_NAME)
      .def(py::init<double, double, double, double>(), py::arg("x_min") = 0.,
           py::arg("y_min") = 0., py::arg("x_max") = 0., py::arg("y_max") = 0.)
      .def("__repr__",
           [](const cbop::Bbox_2& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." BOUNDING_BOX_NAME "("
                    << self.xmin() << ", " << self.ymin() << ", " << self.xmax()
                    << ", " << self.ymax() << ")";
             return stream.str();
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

  py::class_<cbop::Point_2>(m, POINT_NAME)
      .def(py::init<double, double>(), py::arg("x") = 0., py::arg("y") = 0.)
      .def("__repr__", point_repr)
      .def("__eq__", [](const cbop::Point_2& self,
                        const cbop::Point_2& other) { return self == other; })
      .def("distance_to", &cbop::Point_2::dist)
      .def_property_readonly("x", &cbop::Point_2::x)
      .def_property_readonly("y", &cbop::Point_2::y)
      .def_property_readonly("bounding_box", &cbop::Point_2::bbox);

  py::class_<cbop::Segment_2>(m, SEGMENT_NAME)
      .def(py::init<cbop::Point_2, cbop::Point_2>(),
           py::arg("source") = cbop::Point_2(),
           py::arg("target") = cbop::Point_2())
      .def("__repr__",
           [](const cbop::Segment_2& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." SEGMENT_NAME "("
                    << point_repr(self.source()) << ", "
                    << point_repr(self.target()) << ")";
             return stream.str();
           })
      .def("__eq__",
           [](const cbop::Segment_2& self, const cbop::Segment_2& other) {
             return self.source() == other.source() &&
                    self.target() == other.target();
           })
      .def_property("source", &cbop::Segment_2::source,
                    &cbop::Segment_2::setSource)
      .def_property("target", &cbop::Segment_2::target,
                    &cbop::Segment_2::setTarget)
      .def_property_readonly("max", &cbop::Segment_2::max)
      .def_property_readonly("min", &cbop::Segment_2::min)
      .def_property_readonly("is_degenerate", &cbop::Segment_2::degenerate)
      .def_property_readonly("is_vertical", &cbop::Segment_2::is_vertical)
      .def_property_readonly("reversed", &cbop::Segment_2::changeOrientation);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
