#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iomanip>
#include <limits>
#include <numeric>
#include <sstream>

#include "bbox_2.h"
#include "point_2.h"
#include "polygon.h"
#include "segment_2.h"

namespace py = pybind11;

#define MODULE_NAME _martinez
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define BOUNDING_BOX_NAME "BoundingBox"
#define CONTOUR_NAME "Contour"
#define POINT_NAME "Point"
#define SEGMENT_NAME "Segment"

std::string join(const std::vector<std::string>& elements,
                 const std::string& separator) {
  if (elements.empty()) return std::string();
  return std::accumulate(
      std::next(std::begin(elements)), std::end(elements), elements[0],
      [&separator](const std::string& result, const std::string& value) {
        return result + separator + value;
      });
};

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

std::vector<cbop::Point_2> contour_to_points(const cbop::Contour& self) {
  return std::vector<cbop::Point_2>(self.begin(), self.end());
}

std::vector<unsigned int> contour_to_holes(const cbop::Contour& self) {
  std::vector<unsigned int> result;
  for (unsigned int index = 0; index < self.nholes(); ++index)
    result.push_back(self.hole(index));
  return result;
}

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of polygon clipping algorithm by F. Martínez et al.
    )pbdoc";

  py::class_<cbop::Bbox_2>(m, BOUNDING_BOX_NAME)
      .def(py::init<double, double, double, double>(), py::arg("x_min") = 0.,
           py::arg("y_min") = 0., py::arg("x_max") = 0., py::arg("y_max") = 0.)
      .def(py::pickle(
          [](const cbop::Bbox_2& self) {  // __getstate__
            return py::make_tuple(self.xmin(), self.ymin(), self.xmax(),
                                  self.ymax());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 4) throw std::runtime_error("Invalid state!");
            return cbop::Bbox_2(
                tuple[0].cast<double>(), tuple[1].cast<double>(),
                tuple[2].cast<double>(), tuple[3].cast<double>());
          }))
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

  py::class_<cbop::Contour>(m, CONTOUR_NAME)
      .def(py::init<const std::vector<cbop::Point_2>&,
                    const std::vector<unsigned int>&, bool>(),
           py::arg("points"), py::arg("holes"), py::arg("is_external"))
      .def(py::pickle(
          [](const cbop::Contour& self) {  // __getstate__
            return py::make_tuple(contour_to_points(self),
                                  contour_to_holes(self), self.external());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return cbop::Contour(tuple[0].cast<std::vector<cbop::Point_2>>(),
                                 tuple[1].cast<std::vector<unsigned int>>(),
                                 tuple[2].cast<bool>());
          }))
      .def("__repr__",
           [](const cbop::Contour& self) -> std::string {
             std::vector<std::string> points_reprs;
             for (auto& point : contour_to_points(self))
               points_reprs.push_back(point_repr(point));
             std::vector<std::string> holes_reprs;
             for (auto hole : contour_to_holes(self))
               holes_reprs.push_back(std::to_string(hole));
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." CONTOUR_NAME "("
                    << "[" << join(points_reprs, ", ") << "]"
                    << ", "
                    << "[" << join(holes_reprs, ", ") << "]"
                    << ", " << py::bool_(self.external()) << ")";
             return stream.str();
           })
      .def("__eq__",
           [](const cbop::Contour& self, const cbop::Contour& other) {
             return contour_to_points(self) == contour_to_points(other) &&
                    contour_to_holes(self) == contour_to_holes(other) &&
                    self.external() == other.external();
           })
      .def(
          "__iter__",
          [](const cbop::Contour& self) {
            return py::make_iterator(self.begin(), self.end());
          },
          py::keep_alive<0, 1>())
      .def_property_readonly("points", contour_to_points)
      .def_property_readonly("holes", contour_to_holes)
      .def_property("is_external", &cbop::Contour::external,
                    &cbop::Contour::setExternal)
      .def_property_readonly("is_clockwise", &cbop::Contour::clockwise)
      .def_property_readonly("is_counterclockwise",
                             &cbop::Contour::counterclockwise)
      .def_property_readonly("bounding_box", &cbop::Contour::bbox)
      .def("add", &cbop::Contour::add, py::arg("add"))
      .def("add_hole", &cbop::Contour::addHole, py::arg("hole"))
      .def("clear_holes", &cbop::Contour::clearHoles)
      .def("move", &cbop::Contour::move, py::arg("x"), py::arg("y"))
      .def("reverse", &cbop::Contour::changeOrientation)
      .def("set_clockwise", &cbop::Contour::setClockwise)
      .def("set_counterclockwise", &cbop::Contour::setCounterClockwise);

  py::class_<cbop::Point_2>(m, POINT_NAME)
      .def(py::init<double, double>(), py::arg("x") = 0., py::arg("y") = 0.)
      .def(py::pickle(
          [](const cbop::Point_2& self) {  // __getstate__
            return py::make_tuple(self.x(), self.y());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return cbop::Point_2(tuple[0].cast<double>(),
                                 tuple[1].cast<double>());
          }))
      .def("__repr__", point_repr)
      .def("__eq__", [](const cbop::Point_2& self,
                        const cbop::Point_2& other) { return self == other; })
      .def("distance_to", &cbop::Point_2::dist, py::arg("other"))
      .def_property_readonly("x", &cbop::Point_2::x)
      .def_property_readonly("y", &cbop::Point_2::y)
      .def_property_readonly("bounding_box", &cbop::Point_2::bbox);

  py::class_<cbop::Segment_2>(m, SEGMENT_NAME)
      .def(py::init<cbop::Point_2, cbop::Point_2>(),
           py::arg("source") = cbop::Point_2(),
           py::arg("target") = cbop::Point_2())
      .def(py::pickle(
          [](const cbop::Segment_2& self) {  // __getstate__
            return py::make_tuple(self.source(), self.target());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return cbop::Segment_2(tuple[0].cast<cbop::Point_2>(),
                                   tuple[1].cast<cbop::Point_2>());
          }))
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
