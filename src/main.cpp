#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <functional>
#include <iomanip>
#include <limits>
#include <memory>
#include <numeric>
#include <sstream>
#include <unordered_map>
#include <unordered_set>

#include "bbox.h"
#include "booleanop.h"
#include "point.h"
#include "polygon.h"
#include "segment.h"
#include "utilities.h"

namespace py = pybind11;

#define MODULE_NAME _martinez
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define BOUNDING_BOX_NAME "BoundingBox"
#define CONTOUR_NAME "Contour"
#define EDGE_TYPE_NAME "EdgeType"
#define EVENTS_QUEUE_KEY_NAME "EventsQueueKey"
#define OPERATION_NAME "Operation"
#define OPERATION_TYPE_NAME "OperationType"
#define POINT_NAME "Point"
#define POLYGON_NAME "Polygon"
#define POLYGON_TYPE_NAME "PolygonType"
#define SEGMENT_NAME "Segment"
#define SWEEP_EVENT_NAME "SweepEvent"
#define SWEEP_LINE_KEY_NAME "SweepLineKey"

static std::string join(const std::vector<std::string>& elements,
                        const std::string& separator) {
  if (elements.empty()) return std::string();
  return std::accumulate(
      std::next(std::begin(elements)), std::end(elements), elements[0],
      [&separator](const std::string& result, const std::string& value) {
        return result + separator + value;
      });
};

template <class Value>
static std::vector<const Value*> traverse(
    const Value* value, std::unordered_map<size_t, size_t>& left_links,
    std::unordered_map<size_t, size_t>& right_links,
    std::function<const Value*(const Value*)> to_left,
    std::function<const Value*(const Value*)> to_right) {
  std::vector<const Value*> result;
  std::unordered_map<const Value*, size_t> registry;
  std::vector<const Value*> queue{value};
  while (!queue.empty()) {
    const auto* cursor = queue.back();
    queue.pop_back();
    registry[cursor] = result.size();
    result.push_back(cursor);
    const auto* left = to_left(cursor);
    if (left != nullptr && registry.find(left) == registry.end())
      queue.push_back(left);
    const auto* right = to_right(cursor);
    if (right != nullptr && registry.find(right) == registry.end())
      queue.push_back(right);
  }
  queue.push_back(value);
  std::unordered_set<const Value*> visited{value};
  while (!queue.empty()) {
    const auto* cursor = queue.back();
    queue.pop_back();
    const auto index = registry[cursor];
    const auto* left = to_left(cursor);
    if (left != nullptr) {
      left_links[index] = registry[left];
      if (visited.find(left) == visited.end()) {
        visited.insert(left);
        queue.push_back(left);
      }
    }
    const auto* right = to_right(cursor);
    if (right != nullptr) {
      right_links[index] = registry[right];
      if (visited.find(right) == visited.end()) {
        visited.insert(right);
        queue.push_back(right);
      }
    }
  }
  return result;
}

static std::ostringstream make_stream() {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  return stream;
}

static std::vector<cbop::Point> contour_to_points(const cbop::Contour& self) {
  return std::vector<cbop::Point>(self.begin(), self.end());
}

static std::vector<size_t> contour_to_holes(const cbop::Contour& self) {
  std::vector<size_t> result;
  for (size_t index = 0; index < self.nholes(); ++index)
    result.push_back(self.hole(index));
  return result;
}

static std::vector<cbop::Contour> polygon_to_contours(
    const cbop::Polygon& self) {
  return std::vector<cbop::Contour>(self.begin(), self.end());
}

static std::string point_repr(const cbop::Point& self) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << self.x() << ", "
         << self.y() << ")";
  return stream.str();
}

static std::string edge_type_repr(const cbop::EdgeType& type) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." EDGE_TYPE_NAME;
  switch (type) {
    case cbop::EdgeType::DIFFERENT_TRANSITION:
      stream << ".DIFFERENT_TRANSITION";
      break;
    case cbop::EdgeType::NON_CONTRIBUTING:
      stream << ".NON_CONTRIBUTING";
      break;
    case cbop::EdgeType::NORMAL:
      stream << ".NORMAL";
      break;
    case cbop::EdgeType::SAME_TRANSITION:
      stream << ".SAME_TRANSITION";
      break;
  }
  return stream.str();
}

static std::string operation_type_repr(const cbop::BooleanOpType& type) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." OPERATION_TYPE_NAME;
  switch (type) {
    case cbop::BooleanOpType::INTERSECTION:
      stream << ".INTERSECTION";
      break;
    case cbop::BooleanOpType::UNION:
      stream << ".UNION";
      break;
    case cbop::BooleanOpType::DIFFERENCE:
      stream << ".DIFFERENCE";
      break;
    case cbop::BooleanOpType::XOR:
      stream << ".XOR";
      break;
  }
  return stream.str();
}

static std::string polygon_type_repr(const cbop::PolygonType& type) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." POLYGON_TYPE_NAME;
  switch (type) {
    case cbop::PolygonType::CLIPPING:
      stream << ".CLIPPING";
      break;
    case cbop::PolygonType::SUBJECT:
      stream << ".SUBJECT";
      break;
  }
  return stream.str();
}

static std::string bool_repr(bool value) { return py::str(py::bool_(value)); }

static void sweep_event_repr_impl(
    std::ostringstream& stream, const cbop::SweepEvent* sweep_event,
    std::unordered_set<const cbop::SweepEvent*> visited) {
  visited.insert(sweep_event);
  stream << C_STR(MODULE_NAME) "." SWEEP_EVENT_NAME "("
         << bool_repr(sweep_event->left) << ", "
         << point_repr(sweep_event->point) << ", ";
  const auto* left = sweep_event->otherEvent;
  if (left == nullptr)
    stream << std::string(py::str(py::none()));
  else if (visited.find(left) != visited.end())
    stream << "...";
  else
    sweep_event_repr_impl(stream, left, visited);
  stream << ", " << polygon_type_repr(sweep_event->pol) << ", "
         << edge_type_repr(sweep_event->type) << ", "
         << bool_repr(sweep_event->inOut) << ", "
         << bool_repr(sweep_event->otherInOut) << ", "
         << bool_repr(sweep_event->inResult) << ", "
         << bool_repr(sweep_event->resultInOut) << ", " << sweep_event->pos
         << ", " << sweep_event->contourId << ", ";
  const auto* right = sweep_event->prevInResult;
  if (right == nullptr)
    stream << std::string(py::str(py::none()));
  else if (visited.find(right) != visited.end())
    stream << "...";
  else
    sweep_event_repr_impl(stream, right, visited);
  stream << ")";
}

static std::string sweep_event_repr(const cbop::SweepEvent& self) {
  auto stream = make_stream();
  sweep_event_repr_impl(stream, std::addressof(self), {});
  return stream.str();
}

static std::string contour_repr(const cbop::Contour& self) {
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
         << ", " << bool_repr(self.external()) << ")";
  return stream.str();
}

static std::string polygon_repr(const cbop::Polygon& self) {
  auto stream = make_stream();
  std::vector<std::string> contours_reprs;
  for (auto& contour : self) contours_reprs.push_back(contour_repr(contour));
  stream << C_STR(MODULE_NAME) "." POLYGON_NAME "("
         << "[" << join(contours_reprs, ", ") << "]"
         << ")";
  return stream.str();
}

static bool are_contours_equal(const cbop::Contour& self,
                               const cbop::Contour& other) {
  return contour_to_points(self) == contour_to_points(other) &&
         contour_to_holes(self) == contour_to_holes(other) &&
         self.external() == other.external();
}

static bool are_sweep_events_equal_flat(const cbop::SweepEvent& self,
                                        const cbop::SweepEvent& other) {
  return self.left == other.left && self.point == other.point &&
         self.pol == other.pol && self.type == other.type &&
         self.inOut == other.inOut && self.otherInOut == other.otherInOut &&
         self.inResult == other.inResult &&
         self.resultInOut == other.resultInOut && self.pos == other.pos &&
         self.contourId == other.contourId;
}

static bool are_sweep_events_equal(const cbop::SweepEvent& self,
                                   const cbop::SweepEvent& other) {
  const auto* ptr = std::addressof(self);
  const auto* other_ptr = std::addressof(other);
  if (ptr == other_ptr) return true;
  std::unordered_map<size_t, size_t> left_links, other_left_links;
  std::unordered_map<size_t, size_t> right_links, other_right_links;
  const auto events = traverse<cbop::SweepEvent>(
      ptr, left_links, right_links, &cbop::SweepEvent::otherEvent,
      &cbop::SweepEvent::prevInResult);
  const auto other_events = traverse<cbop::SweepEvent>(
      other_ptr, other_left_links, other_right_links,
      &cbop::SweepEvent::otherEvent, &cbop::SweepEvent::prevInResult);
  if (!(left_links == other_left_links && right_links == other_right_links))
    return false;
  if (events.size() != other_events.size()) return false;
  for (size_t index = 0; index < events.size(); ++index)
    if (!are_sweep_events_equal_flat(*events[index], *other_events[index]))
      return false;
  return true;
}

static bool are_polygons_equal(const cbop::Polygon& self,
                               const cbop::Polygon& other) {
  if (self.ncontours() != other.ncontours()) return false;
  for (size_t index = 0; index < self.ncontours(); ++index)
    if (!are_contours_equal(self[index], other[index])) return false;
  return true;
}

static py::tuple to_sweep_event_state(const cbop::SweepEvent& self) {
  const auto* ptr = std::addressof(self);
  std::unordered_map<size_t, size_t> left_links, right_links;
  const auto events = traverse<cbop::SweepEvent>(
      ptr, left_links, right_links, &cbop::SweepEvent::otherEvent,
      &cbop::SweepEvent::prevInResult);
  py::list plain_states;
  for (const auto* event : events) {
    plain_states.append(
        py::make_tuple(event->left, event->point, event->pol, event->type,
                       event->inOut, event->otherInOut, event->inResult,
                       event->resultInOut, event->pos, event->contourId));
  }
  return py::make_tuple(plain_states, left_links, right_links);
};

static cbop::SweepEvent* from_plain_sweep_event_state(const py::tuple& state) {
  if (state.size() != 10) throw std::runtime_error("Invalid state!");
  return new cbop::SweepEvent(
      state[0].cast<bool>(), state[1].cast<cbop::Point>(), nullptr,
      state[2].cast<cbop::PolygonType>(), state[3].cast<cbop::EdgeType>(),
      state[4].cast<bool>(), state[5].cast<bool>(), state[6].cast<bool>(),
      state[7].cast<bool>(), state[8].cast<size_t>(), state[9].cast<size_t>(),
      nullptr);
}

static cbop::SweepEvent* from_sweep_event_state(py::tuple state) {
  std::vector<cbop::SweepEvent*> events;
  for (const auto& event_state : state[0].cast<py::list>())
    events.push_back(
        from_plain_sweep_event_state(event_state.cast<py::tuple>()));
  std::unordered_map<size_t, size_t> left_links, right_links;
  left_links = state[1].cast<std::unordered_map<size_t, size_t>>();
  for (const auto item : left_links)
    events[item.first]->otherEvent = events[item.second];
  right_links = state[2].cast<std::unordered_map<size_t, size_t>>();
  for (const auto item : right_links)
    events[item.first]->prevInResult = events[item.second];
  return events[0];
}

class EventsQueueKey {
 public:
  const cbop::SweepEvent* event() const { return _event; };

  EventsQueueKey(const cbop::SweepEvent* event) : _event(event){};

  bool operator<(const EventsQueueKey& other) const {
    static const cbop::SweepEventComp cmp;
    return cmp(_event, other._event);
  };

  bool operator==(const EventsQueueKey& other) const {
    return are_sweep_events_equal(*_event, *other._event);
  };

 private:
  const cbop::SweepEvent* _event;
};

class SweepLineKey {
 public:
  const cbop::SweepEvent* event() const { return _event; };

  SweepLineKey(const cbop::SweepEvent* event) : _event(event){};

  bool operator<(const SweepLineKey& other) const {
    static const cbop::SegmentComp cmp;
    return cmp(_event, other._event);
  };

  bool operator==(const SweepLineKey& other) const {
    return are_sweep_events_equal(*_event, *other._event);
  };

 private:
  const cbop::SweepEvent* _event;
};

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of polygon clipping algorithm by F. Martínez et al.
    )pbdoc";

  m.def("compute", &cbop::compute, pybind11::arg("left"),
        pybind11::arg("right"), pybind11::arg("operation_type"));

  m.def(
      "find_intersections",
      [](const cbop::Segment& first_segment,
         const cbop::Segment& second_segment) -> py::tuple {
        cbop::Point first_intersection_point, second_intersection_point;
        int intersections_count = cbop::findIntersection(
            first_segment, second_segment, first_intersection_point,
            second_intersection_point);
        switch (intersections_count) {
          case 0:
            return py::make_tuple(intersections_count, py::none(), py::none());
          case 1:
            return py::make_tuple(intersections_count, first_intersection_point,
                                  py::none());
          default:
            return py::make_tuple(intersections_count, first_intersection_point,
                                  second_intersection_point);
        }
      });
  m.def("sign", &cbop::sign, pybind11::arg("first_point"),
        pybind11::arg("second_point"), pybind11::arg("third_point"));

  py::enum_<cbop::EdgeType>(m, EDGE_TYPE_NAME)
      .value("NORMAL", cbop::EdgeType::NORMAL)
      .value("NON_CONTRIBUTING", cbop::EdgeType::NON_CONTRIBUTING)
      .value("SAME_TRANSITION", cbop::EdgeType::SAME_TRANSITION)
      .value("DIFFERENT_TRANSITION", cbop::EdgeType::DIFFERENT_TRANSITION)
      .export_values();

  py::enum_<cbop::BooleanOpType>(m, OPERATION_TYPE_NAME)
      .value("INTERSECTION", cbop::BooleanOpType::INTERSECTION)
      .value("UNION", cbop::BooleanOpType::UNION)
      .value("DIFFERENCE", cbop::BooleanOpType::DIFFERENCE)
      .value("XOR", cbop::BooleanOpType::XOR)
      .export_values();

  py::enum_<cbop::PolygonType>(m, POLYGON_TYPE_NAME)
      .value("SUBJECT", cbop::PolygonType::SUBJECT)
      .value("CLIPPING", cbop::PolygonType::CLIPPING)
      .export_values();

  py::class_<cbop::Bbox>(m, BOUNDING_BOX_NAME)
      .def(py::init<double, double, double, double>(), py::arg("x_min") = 0.,
           py::arg("y_min") = 0., py::arg("x_max") = 0., py::arg("y_max") = 0.)
      .def(py::pickle(
          [](const cbop::Bbox& self) {  // __getstate__
            return py::make_tuple(self.xmin(), self.ymin(), self.xmax(),
                                  self.ymax());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 4) throw std::runtime_error("Invalid state!");
            return cbop::Bbox(tuple[0].cast<double>(), tuple[1].cast<double>(),
                              tuple[2].cast<double>(), tuple[3].cast<double>());
          }))
      .def(py::self + py::self)
      .def("__eq__",
           [](const cbop::Bbox& self, const cbop::Bbox& other) {
             return self.xmin() == other.xmin() &&
                    self.ymin() == other.ymin() &&
                    self.xmax() == other.xmax() && self.ymax() == other.ymax();
           })
      .def("__repr__",
           [](const cbop::Bbox& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." BOUNDING_BOX_NAME "("
                    << self.xmin() << ", " << self.ymin() << ", " << self.xmax()
                    << ", " << self.ymax() << ")";
             return stream.str();
           })
      .def_property_readonly("x_min", &cbop::Bbox::xmin)
      .def_property_readonly("y_min", &cbop::Bbox::ymin)
      .def_property_readonly("x_max", &cbop::Bbox::xmax)
      .def_property_readonly("y_max", &cbop::Bbox::ymax);

  py::class_<cbop::Contour>(m, CONTOUR_NAME)
      .def(py::init<const std::vector<cbop::Point>&, const std::vector<size_t>&,
                    bool>(),
           py::arg("points"), py::arg("holes"), py::arg("is_external"))
      .def(py::pickle(
          [](const cbop::Contour& self) {  // __getstate__
            return py::make_tuple(contour_to_points(self),
                                  contour_to_holes(self), self.external());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return cbop::Contour(tuple[0].cast<std::vector<cbop::Point>>(),
                                 tuple[1].cast<std::vector<size_t>>(),
                                 tuple[2].cast<bool>());
          }))
      .def("__eq__", are_contours_equal)
      .def(
          "__iter__",
          [](const cbop::Contour& self) {
            return py::make_iterator(self.begin(), self.end());
          },
          py::keep_alive<0, 1>())
      .def("__repr__", contour_repr)
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
      .def("reverse", &cbop::Contour::changeOrientation)
      .def("set_clockwise", &cbop::Contour::setClockwise)
      .def("set_counterclockwise", &cbop::Contour::setCounterClockwise);

  py::class_<cbop::BooleanOpImp>(m, OPERATION_NAME)
      .def(py::init<const cbop::Polygon&, const cbop::Polygon&,
                    cbop::BooleanOpType>(),
           py::arg("left"), py::arg("right"), py::arg("type"))
      .def(py::pickle(
          [](const cbop::BooleanOpImp& self) {  // __getstate__
            return py::make_tuple(self.subject(), self.clipping(),
                                  self.operation());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return cbop::BooleanOpImp(tuple[0].cast<cbop::Polygon>(),
                                      tuple[1].cast<cbop::Polygon>(),
                                      tuple[2].cast<cbop::BooleanOpType>());
          }))
      .def("__eq__",
           [](const cbop::BooleanOpImp& self, const cbop::BooleanOpImp& other) {
             return are_polygons_equal(self.subject(), other.subject()) &&
                    are_polygons_equal(self.clipping(), other.clipping()) &&
                    self.operation() == other.operation();
           })
      .def("__repr__",
           [](const cbop::BooleanOpImp& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." OPERATION_NAME "("
                    << polygon_repr(self.subject()) << ", "
                    << polygon_repr(self.clipping()) << ", "
                    << operation_type_repr(self.operation()) << ")";
             return stream.str();
           })
      .def_property_readonly("left", &cbop::BooleanOpImp::subject)
      .def_property_readonly("right", &cbop::BooleanOpImp::clipping)
      .def_property_readonly("resultant", &cbop::BooleanOpImp::result)
      .def_property_readonly("type", &cbop::BooleanOpImp::operation)
      .def_property_readonly("events",
                             [](const cbop::BooleanOpImp& self) {
                               std::vector<cbop::SweepEvent*> result;
                               auto queue = self.eventsQueue();
                               while (!queue.empty()) {
                                 result.push_back(queue.top());
                                 queue.pop();
                               }
                               return result;
                             })
      .def_property_readonly("is_trivial", &cbop::BooleanOpImp::trivial)
      .def_static("collect_events", &cbop::BooleanOpImp::collectEvents,
                  py::arg("events"))
      .def(
          "compute_fields",
          [](const cbop::BooleanOpImp& self, cbop::SweepEvent* event,
             cbop::SweepEvent* previous_event) {
            return self.computeFields(event, previous_event);
          },
          py::arg("event"), py::arg("previous_event"))
      .def("connect_edges", &cbop::BooleanOpImp::connectEdges,
           py::arg("events"))
      .def("divide_segment", &cbop::BooleanOpImp::divideSegment,
           py::arg("event"), py::arg("point"))
      .def("in_result", &cbop::BooleanOpImp::inResult, py::arg("event"))
      .def("possible_intersection", &cbop::BooleanOpImp::possibleIntersection,
           py::arg("first_event"), py::arg("second_event"))
      .def("process_events", &cbop::BooleanOpImp::processEvents,
           py::arg("events"))
      .def("process_segments", &cbop::BooleanOpImp::processSegments)
      .def("run", &cbop::BooleanOpImp::run)
      .def("sweep", &cbop::BooleanOpImp::sweep)
      .def_static("to_next_position", &cbop::BooleanOpImp::nextPos,
                  py::arg("position"), py::arg("events"), py::arg("processed"));

  py::class_<cbop::Point>(m, POINT_NAME)
      .def(py::init<double, double>(), py::arg("x") = 0., py::arg("y") = 0.)
      .def(py::pickle(
          [](const cbop::Point& self) {  // __getstate__
            return py::make_tuple(self.x(), self.y());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return cbop::Point(tuple[0].cast<double>(),
                               tuple[1].cast<double>());
          }))
      .def(py::self == py::self)
      .def("__repr__", point_repr)
      .def("distance_to", &cbop::Point::dist, py::arg("other"))
      .def_property_readonly("x", &cbop::Point::x)
      .def_property_readonly("y", &cbop::Point::y)
      .def_property_readonly("bounding_box", &cbop::Point::bbox);

  py::class_<cbop::Polygon>(m, POLYGON_NAME)
      .def(py::init<const std::vector<cbop::Contour>&>(), py::arg("contours"))
      .def(py::pickle(
          [](const cbop::Polygon& self) {  // __getstate__
            return polygon_to_contours(self);
          },
          [](const std::vector<cbop::Contour>& contours) {  // __setstate__
            return cbop::Polygon(contours);
          }))
      .def("__eq__", are_polygons_equal)
      .def(
          "__iter__",
          [](const cbop::Polygon& self) {
            return py::make_iterator(self.begin(), self.end());
          },
          py::keep_alive<0, 1>())
      .def("__repr__", polygon_repr)
      .def_property_readonly("bounding_box", &cbop::Polygon::bbox)
      .def_property_readonly("contours", polygon_to_contours)
      .def("join", &cbop::Polygon::join);

  py::class_<cbop::Segment>(m, SEGMENT_NAME)
      .def(py::init<cbop::Point, cbop::Point>(),
           py::arg("source") = cbop::Point(),
           py::arg("target") = cbop::Point())
      .def(py::pickle(
          [](const cbop::Segment& self) {  // __getstate__
            return py::make_tuple(self.source(), self.target());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return cbop::Segment(tuple[0].cast<cbop::Point>(),
                                 tuple[1].cast<cbop::Point>());
          }))
      .def("__eq__",
           [](const cbop::Segment& self, const cbop::Segment& other) {
             return self.source() == other.source() &&
                    self.target() == other.target();
           })
      .def("__repr__",
           [](const cbop::Segment& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." SEGMENT_NAME "("
                    << point_repr(self.source()) << ", "
                    << point_repr(self.target()) << ")";
             return stream.str();
           })
      .def_property_readonly("source", &cbop::Segment::source)
      .def_property_readonly("target", &cbop::Segment::target)
      .def_property_readonly("max", &cbop::Segment::max)
      .def_property_readonly("min", &cbop::Segment::min)
      .def_property_readonly("is_degenerate", &cbop::Segment::degenerate)
      .def_property_readonly("is_vertical", &cbop::Segment::is_vertical)
      .def_property_readonly("reversed", &cbop::Segment::changeOrientation);

  py::class_<cbop::SweepEvent, std::unique_ptr<cbop::SweepEvent, py::nodelete>>(
      m, SWEEP_EVENT_NAME)
      .def(py::init<bool, const cbop::Point&, cbop::SweepEvent*,
                    cbop::PolygonType, cbop::EdgeType, bool, bool, bool, bool,
                    size_t, size_t, cbop::SweepEvent*>(),
           py::arg("left"), py::arg("point"), py::arg("other_event").none(true),
           py::arg("polygon_type"), py::arg("edge_type"),
           py::arg("in_out") = false, py::arg("other_in_out") = false,
           py::arg("in_result") = false, py::arg("result_in_out") = false,
           py::arg("position") = 0, py::arg("contour_id") = 0,
           py::arg("prev_in_result_event").none(true) = nullptr,
           py::return_value_policy::reference)
      .def(py::pickle(
          static_cast<std::function<py::tuple(const cbop::SweepEvent& self)>>(
              to_sweep_event_state),
          static_cast<std::function<cbop::SweepEvent*(py::tuple)>>(
              from_sweep_event_state)))
      .def("__eq__", are_sweep_events_equal)
      .def("__repr__", sweep_event_repr)
      .def_readwrite("is_left", &cbop::SweepEvent::left)
      .def_readwrite("point", &cbop::SweepEvent::point)
      .def_readwrite("other_event", &cbop::SweepEvent::otherEvent)
      .def_readwrite("polygon_type", &cbop::SweepEvent::pol)
      .def_readwrite("edge_type", &cbop::SweepEvent::type)
      .def_readwrite("in_out", &cbop::SweepEvent::inOut)
      .def_readwrite("other_in_out", &cbop::SweepEvent::otherInOut)
      .def_readwrite("in_result", &cbop::SweepEvent::inResult)
      .def_readwrite("result_in_out", &cbop::SweepEvent::resultInOut)
      .def_readwrite("position", &cbop::SweepEvent::pos)
      .def_readwrite("contour_id", &cbop::SweepEvent::contourId)
      .def_readwrite("prev_in_result_event", &cbop::SweepEvent::prevInResult)
      .def_property_readonly("is_vertical", &cbop::SweepEvent::vertical)
      .def_property_readonly("segment", &cbop::SweepEvent::segment)
      .def("is_above", &cbop::SweepEvent::above)
      .def("is_below", &cbop::SweepEvent::below);

  py::class_<EventsQueueKey>(m, EVENTS_QUEUE_KEY_NAME)
      .def(py::init<const cbop::SweepEvent*>(), py::arg("event"))
      .def(py::pickle(
          [](const EventsQueueKey& key) {
            return to_sweep_event_state(*key.event());
          },
          [](py::tuple state) {
            return EventsQueueKey(from_sweep_event_state(state));
          }))
      .def(py::self < py::self)
      .def(py::self == py::self)
      .def("__repr__",
           [](const EventsQueueKey& self) {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." EVENTS_QUEUE_KEY_NAME "("
                    << sweep_event_repr(*self.event()) << ")";
             return stream.str();
           })
      .def_property_readonly("event", &EventsQueueKey::event);

  py::class_<SweepLineKey>(m, SWEEP_LINE_KEY_NAME)
      .def(py::init<const cbop::SweepEvent*>(), py::arg("event"))
      .def(py::pickle(
          [](const SweepLineKey& key) {
            return to_sweep_event_state(*key.event());
          },
          [](py::tuple state) {
            return SweepLineKey(from_sweep_event_state(state));
          }))
      .def(py::self < py::self)
      .def(py::self == py::self)
      .def("__repr__",
           [](const SweepLineKey& self) {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." SWEEP_LINE_KEY_NAME "("
                    << sweep_event_repr(*self.event()) << ")";
             return stream.str();
           })
      .def_property_readonly("event", &SweepLineKey::event);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
