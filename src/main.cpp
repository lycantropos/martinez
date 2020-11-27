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

using BoundingBox = cbop::Bbox;
using Contour = cbop::Contour;
using EdgeType = cbop::EdgeType;
using Operation = cbop::BooleanOpImp;
using OperationType = cbop::BooleanOpType;
using Point = cbop::Point;
using Polygon = cbop::Polygon;
using PolygonType = cbop::PolygonType;
using Segment = cbop::Segment;
using SweepEvent = cbop::SweepEvent;

static std::string join(const std::vector<std::string>& elements,
                        const std::string& separator) {
  if (elements.empty()) return std::string();
  return std::accumulate(
      std::next(std::begin(elements)), std::end(elements), elements[0],
      [&separator](const std::string& result, const std::string& value) {
        return result + separator + value;
      });
};

template <class Type>
static std::vector<const Type*> traverse(
    const Type* value, std::unordered_map<size_t, size_t>& left_links,
    std::unordered_map<size_t, size_t>& right_links,
    std::function<const Type*(const Type*)> to_left,
    std::function<const Type*(const Type*)> to_right) {
  std::vector<const Type*> result;
  std::unordered_map<const Type*, size_t> registry;
  std::vector<const Type*> queue{value};
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
  std::unordered_set<const Type*> visited{value};
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

static std::vector<Point> contour_to_points(const Contour& self) {
  return std::vector<Point>(self.begin(), self.end());
}

static std::vector<size_t> contour_to_holes(const Contour& self) {
  std::vector<size_t> result;
  for (size_t index = 0; index < self.nholes(); ++index)
    result.push_back(self.hole(index));
  return result;
}

static std::vector<Contour> polygon_to_contours(const Polygon& self) {
  return std::vector<Contour>(self.begin(), self.end());
}

static std::string point_repr(const Point& self) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << self.x() << ", "
         << self.y() << ")";
  return stream.str();
}

static std::string edge_type_repr(const EdgeType& type) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." EDGE_TYPE_NAME;
  switch (type) {
    case EdgeType::DIFFERENT_TRANSITION:
      stream << ".DIFFERENT_TRANSITION";
      break;
    case EdgeType::NON_CONTRIBUTING:
      stream << ".NON_CONTRIBUTING";
      break;
    case EdgeType::NORMAL:
      stream << ".NORMAL";
      break;
    case EdgeType::SAME_TRANSITION:
      stream << ".SAME_TRANSITION";
      break;
  }
  return stream.str();
}

static std::string operation_type_repr(const OperationType& type) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." OPERATION_TYPE_NAME;
  switch (type) {
    case OperationType::INTERSECTION:
      stream << ".INTERSECTION";
      break;
    case OperationType::UNION:
      stream << ".UNION";
      break;
    case OperationType::DIFFERENCE:
      stream << ".DIFFERENCE";
      break;
    case OperationType::XOR:
      stream << ".XOR";
      break;
  }
  return stream.str();
}

static std::string polygon_type_repr(const PolygonType& type) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." POLYGON_TYPE_NAME;
  switch (type) {
    case PolygonType::CLIPPING:
      stream << ".CLIPPING";
      break;
    case PolygonType::SUBJECT:
      stream << ".SUBJECT";
      break;
  }
  return stream.str();
}

static std::string bool_repr(bool value) { return py::str(py::bool_(value)); }

static void sweep_event_repr_impl(
    std::ostringstream& stream, const SweepEvent* sweep_event,
    std::unordered_set<const SweepEvent*> visited) {
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

static std::string sweep_event_repr(const SweepEvent& self) {
  auto stream = make_stream();
  sweep_event_repr_impl(stream, std::addressof(self), {});
  return stream.str();
}

static std::string contour_repr(const Contour& self) {
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

static std::string polygon_repr(const Polygon& self) {
  auto stream = make_stream();
  std::vector<std::string> contours_reprs;
  for (auto& contour : self) contours_reprs.push_back(contour_repr(contour));
  stream << C_STR(MODULE_NAME) "." POLYGON_NAME "("
         << "[" << join(contours_reprs, ", ") << "]"
         << ")";
  return stream.str();
}

static bool are_contours_equal(const Contour& self, const Contour& other) {
  return contour_to_points(self) == contour_to_points(other) &&
         contour_to_holes(self) == contour_to_holes(other) &&
         self.external() == other.external();
}

static bool are_sweep_events_equal_flat(const SweepEvent& self,
                                        const SweepEvent& other) {
  return self.left == other.left && self.point == other.point &&
         self.pol == other.pol && self.type == other.type &&
         self.inOut == other.inOut && self.otherInOut == other.otherInOut &&
         self.inResult == other.inResult &&
         self.resultInOut == other.resultInOut && self.pos == other.pos &&
         self.contourId == other.contourId;
}

static bool are_sweep_events_equal(const SweepEvent& self,
                                   const SweepEvent& other) {
  const auto* ptr = std::addressof(self);
  const auto* other_ptr = std::addressof(other);
  if (ptr == other_ptr) return true;
  std::unordered_map<size_t, size_t> left_links, other_left_links;
  std::unordered_map<size_t, size_t> right_links, other_right_links;
  const auto events =
      traverse<SweepEvent>(ptr, left_links, right_links,
                           &SweepEvent::otherEvent, &SweepEvent::prevInResult);
  const auto other_events =
      traverse<SweepEvent>(other_ptr, other_left_links, other_right_links,
                           &SweepEvent::otherEvent, &SweepEvent::prevInResult);
  if (!(left_links == other_left_links && right_links == other_right_links))
    return false;
  if (events.size() != other_events.size()) return false;
  for (size_t index = 0; index < events.size(); ++index)
    if (!are_sweep_events_equal_flat(*events[index], *other_events[index]))
      return false;
  return true;
}

static bool are_polygons_equal(const Polygon& self, const Polygon& other) {
  if (self.ncontours() != other.ncontours()) return false;
  for (size_t index = 0; index < self.ncontours(); ++index)
    if (!are_contours_equal(self[index], other[index])) return false;
  return true;
}

static py::tuple to_sweep_event_state(const SweepEvent& self) {
  const auto* ptr = std::addressof(self);
  std::unordered_map<size_t, size_t> left_links, right_links;
  const auto events =
      traverse<SweepEvent>(ptr, left_links, right_links,
                           &SweepEvent::otherEvent, &SweepEvent::prevInResult);
  py::list plain_states;
  for (const auto* event : events) {
    plain_states.append(
        py::make_tuple(event->left, event->point, event->pol, event->type,
                       event->inOut, event->otherInOut, event->inResult,
                       event->resultInOut, event->pos, event->contourId));
  }
  return py::make_tuple(plain_states, left_links, right_links);
};

static SweepEvent* from_plain_sweep_event_state(const py::tuple& state) {
  if (state.size() != 10) throw std::runtime_error("Invalid state!");
  return new SweepEvent(state[0].cast<bool>(), state[1].cast<Point>(), nullptr,
                        state[2].cast<PolygonType>(), state[3].cast<EdgeType>(),
                        state[4].cast<bool>(), state[5].cast<bool>(),
                        state[6].cast<bool>(), state[7].cast<bool>(),
                        state[8].cast<size_t>(), state[9].cast<size_t>(),
                        nullptr);
}

static SweepEvent* from_sweep_event_state(py::tuple state) {
  std::vector<SweepEvent*> events;
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
  const SweepEvent* event() const { return _event; };

  EventsQueueKey(const SweepEvent* event) : _event(event){};

  bool operator<(const EventsQueueKey& other) const {
    static const cbop::SweepEventComp cmp;
    return cmp(_event, other._event);
  };

  bool operator==(const EventsQueueKey& other) const {
    return are_sweep_events_equal(*_event, *other._event);
  };

 private:
  const SweepEvent* _event;
};

class SweepLineKey {
 public:
  const SweepEvent* event() const { return _event; };

  SweepLineKey(const SweepEvent* event) : _event(event){};

  bool operator<(const SweepLineKey& other) const {
    static const cbop::SegmentComp cmp;
    return cmp(_event, other._event);
  };

  bool operator==(const SweepLineKey& other) const {
    return are_sweep_events_equal(*_event, *other._event);
  };

 private:
  const SweepEvent* _event;
};

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of polygon clipping algorithm by F. Martínez et al.
    )pbdoc";

  m.attr("__version__") = C_STR(VERSION_INFO);

  m.def("compute", &cbop::compute, pybind11::arg("left"),
        pybind11::arg("right"), pybind11::arg("operation_type"));

  m.def(
      "find_intersections",
      [](const Segment& first_segment,
         const Segment& second_segment) -> py::tuple {
        Point first_intersection_point, second_intersection_point;
        int intersections_count = findIntersection(
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

  py::enum_<EdgeType>(m, EDGE_TYPE_NAME)
      .value("NORMAL", EdgeType::NORMAL)
      .value("NON_CONTRIBUTING", EdgeType::NON_CONTRIBUTING)
      .value("SAME_TRANSITION", EdgeType::SAME_TRANSITION)
      .value("DIFFERENT_TRANSITION", EdgeType::DIFFERENT_TRANSITION)
      .export_values();

  py::enum_<OperationType>(m, OPERATION_TYPE_NAME)
      .value("INTERSECTION", OperationType::INTERSECTION)
      .value("UNION", OperationType::UNION)
      .value("DIFFERENCE", OperationType::DIFFERENCE)
      .value("XOR", OperationType::XOR)
      .export_values();

  py::enum_<PolygonType>(m, POLYGON_TYPE_NAME)
      .value("SUBJECT", PolygonType::SUBJECT)
      .value("CLIPPING", PolygonType::CLIPPING)
      .export_values();

  py::class_<BoundingBox>(m, BOUNDING_BOX_NAME)
      .def(py::init<double, double, double, double>(), py::arg("x_min") = 0.,
           py::arg("y_min") = 0., py::arg("x_max") = 0., py::arg("y_max") = 0.)
      .def(py::pickle(
          [](const BoundingBox& self) {  // __getstate__
            return py::make_tuple(self.xmin(), self.ymin(), self.xmax(),
                                  self.ymax());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 4) throw std::runtime_error("Invalid state!");
            return BoundingBox(tuple[0].cast<double>(), tuple[1].cast<double>(),
                               tuple[2].cast<double>(),
                               tuple[3].cast<double>());
          }))
      .def(py::self + py::self)
      .def("__eq__",
           [](const BoundingBox& self, const BoundingBox& other) {
             return self.xmin() == other.xmin() &&
                    self.ymin() == other.ymin() &&
                    self.xmax() == other.xmax() && self.ymax() == other.ymax();
           })
      .def("__repr__",
           [](const BoundingBox& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." BOUNDING_BOX_NAME "("
                    << self.xmin() << ", " << self.ymin() << ", " << self.xmax()
                    << ", " << self.ymax() << ")";
             return stream.str();
           })
      .def_property_readonly("x_min", &BoundingBox::xmin)
      .def_property_readonly("y_min", &BoundingBox::ymin)
      .def_property_readonly("x_max", &BoundingBox::xmax)
      .def_property_readonly("y_max", &BoundingBox::ymax);

  py::class_<Contour>(m, CONTOUR_NAME)
      .def(py::init<const std::vector<Point>&, const std::vector<size_t>&,
                    bool>(),
           py::arg("points"), py::arg("holes"), py::arg("is_external"))
      .def(py::pickle(
          [](const Contour& self) {  // __getstate__
            return py::make_tuple(contour_to_points(self),
                                  contour_to_holes(self), self.external());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return Contour(tuple[0].cast<std::vector<Point>>(),
                           tuple[1].cast<std::vector<size_t>>(),
                           tuple[2].cast<bool>());
          }))
      .def("__eq__", are_contours_equal)
      .def(
          "__iter__",
          [](const Contour& self) {
            return py::make_iterator(self.begin(), self.end());
          },
          py::keep_alive<0, 1>())
      .def("__repr__", contour_repr)
      .def_property_readonly("points", contour_to_points)
      .def_property_readonly("holes", contour_to_holes)
      .def_property("is_external", &Contour::external, &Contour::setExternal)
      .def_property_readonly("is_clockwise", &Contour::clockwise)
      .def_property_readonly("is_counterclockwise", &Contour::counterclockwise)
      .def_property_readonly("bounding_box", &Contour::bbox)
      .def("add", &Contour::add, py::arg("add"))
      .def("add_hole", &Contour::addHole, py::arg("hole"))
      .def("clear_holes", &Contour::clearHoles)
      .def("reverse", &Contour::changeOrientation)
      .def("set_clockwise", &Contour::setClockwise)
      .def("set_counterclockwise", &Contour::setCounterClockwise);

  py::class_<Operation>(m, OPERATION_NAME)
      .def(py::init<const Polygon&, const Polygon&, OperationType>(),
           py::arg("left"), py::arg("right"), py::arg("type"))
      .def(py::pickle(
          [](const Operation& self) {  // __getstate__
            return py::make_tuple(self.subject(), self.clipping(),
                                  self.operation());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return Operation(tuple[0].cast<Polygon>(), tuple[1].cast<Polygon>(),
                             tuple[2].cast<OperationType>());
          }))
      .def("__eq__",
           [](const Operation& self, const Operation& other) {
             return are_polygons_equal(self.subject(), other.subject()) &&
                    are_polygons_equal(self.clipping(), other.clipping()) &&
                    self.operation() == other.operation();
           })
      .def("__repr__",
           [](const Operation& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." OPERATION_NAME "("
                    << polygon_repr(self.subject()) << ", "
                    << polygon_repr(self.clipping()) << ", "
                    << operation_type_repr(self.operation()) << ")";
             return stream.str();
           })
      .def_property_readonly("left", &Operation::subject)
      .def_property_readonly("right", &Operation::clipping)
      .def_property_readonly("resultant", &Operation::result)
      .def_property_readonly("type", &Operation::operation)
      .def_property_readonly("events",
                             [](const Operation& self) {
                               std::vector<SweepEvent*> result;
                               auto queue = self.eventsQueue();
                               while (!queue.empty()) {
                                 result.push_back(queue.top());
                                 queue.pop();
                               }
                               return result;
                             })
      .def_property_readonly("is_trivial", &Operation::trivial)
      .def_static("collect_events", &Operation::collectEvents,
                  py::arg("events"))
      .def(
          "compute_fields",
          [](const Operation& self, SweepEvent* event,
             SweepEvent* previous_event) {
            return self.computeFields(event, previous_event);
          },
          py::arg("event"), py::arg("previous_event"))
      .def("connect_edges", &Operation::connectEdges, py::arg("events"))
      .def("divide_segment", &Operation::divideSegment, py::arg("event"),
           py::arg("point"))
      .def("in_result", &Operation::inResult, py::arg("event"))
      .def("possible_intersection", &Operation::possibleIntersection,
           py::arg("first_event"), py::arg("second_event"))
      .def("process_events", &Operation::processEvents, py::arg("events"))
      .def("process_segments", &Operation::processSegments)
      .def("run", &Operation::run)
      .def("sweep", &Operation::sweep)
      .def_static("to_next_position", &Operation::nextPos, py::arg("position"),
                  py::arg("events"), py::arg("processed"));

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<double, double>(), py::arg("x") = 0., py::arg("y") = 0.)
      .def(py::pickle(
          [](const Point& self) {  // __getstate__
            return py::make_tuple(self.x(), self.y());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return Point(tuple[0].cast<double>(), tuple[1].cast<double>());
          }))
      .def(py::self == py::self)
      .def("__repr__", point_repr)
      .def("distance_to", &Point::dist, py::arg("other"))
      .def_property_readonly("x", &Point::x)
      .def_property_readonly("y", &Point::y)
      .def_property_readonly("bounding_box", &Point::bbox);

  py::class_<Polygon>(m, POLYGON_NAME)
      .def(py::init<const std::vector<Contour>&>(), py::arg("contours"))
      .def(py::pickle(
          [](const Polygon& self) {  // __getstate__
            return polygon_to_contours(self);
          },
          [](const std::vector<Contour>& contours) {  // __setstate__
            return Polygon(contours);
          }))
      .def("__eq__", are_polygons_equal)
      .def(
          "__iter__",
          [](const Polygon& self) {
            return py::make_iterator(self.begin(), self.end());
          },
          py::keep_alive<0, 1>())
      .def("__repr__", polygon_repr)
      .def_property_readonly("bounding_box", &Polygon::bbox)
      .def_property_readonly("contours", polygon_to_contours)
      .def("join", &Polygon::join);

  py::class_<Segment>(m, SEGMENT_NAME)
      .def(py::init<Point, Point>(), py::arg("source") = Point(),
           py::arg("target") = Point())
      .def(py::pickle(
          [](const Segment& self) {  // __getstate__
            return py::make_tuple(self.source(), self.target());
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return Segment(tuple[0].cast<Point>(), tuple[1].cast<Point>());
          }))
      .def("__eq__",
           [](const Segment& self, const Segment& other) {
             return self.source() == other.source() &&
                    self.target() == other.target();
           })
      .def("__repr__",
           [](const Segment& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." SEGMENT_NAME "("
                    << point_repr(self.source()) << ", "
                    << point_repr(self.target()) << ")";
             return stream.str();
           })
      .def_property_readonly("source", &Segment::source)
      .def_property_readonly("target", &Segment::target)
      .def_property_readonly("max", &Segment::max)
      .def_property_readonly("min", &Segment::min)
      .def_property_readonly("is_degenerate", &Segment::degenerate)
      .def_property_readonly("is_vertical", &Segment::is_vertical)
      .def_property_readonly("reversed", &Segment::changeOrientation);

  py::class_<SweepEvent, std::unique_ptr<SweepEvent, py::nodelete>>(
      m, SWEEP_EVENT_NAME)
      .def(py::init<bool, const Point&, SweepEvent*, PolygonType, EdgeType,
                    bool, bool, bool, bool, size_t, size_t, SweepEvent*>(),
           py::arg("left"), py::arg("point"), py::arg("other_event").none(true),
           py::arg("polygon_type"), py::arg("edge_type"),
           py::arg("in_out") = false, py::arg("other_in_out") = false,
           py::arg("in_result") = false, py::arg("result_in_out") = false,
           py::arg("position") = 0, py::arg("contour_id") = 0,
           py::arg("prev_in_result_event").none(true) = nullptr,
           py::return_value_policy::reference)
      .def(py::pickle(
          static_cast<std::function<py::tuple(const SweepEvent& self)>>(
              to_sweep_event_state),
          static_cast<std::function<SweepEvent*(py::tuple)>>(
              from_sweep_event_state)))
      .def("__eq__", are_sweep_events_equal)
      .def("__repr__", sweep_event_repr)
      .def_readwrite("is_left", &SweepEvent::left)
      .def_readwrite("point", &SweepEvent::point)
      .def_readwrite("other_event", &SweepEvent::otherEvent)
      .def_readwrite("polygon_type", &SweepEvent::pol)
      .def_readwrite("edge_type", &SweepEvent::type)
      .def_readwrite("in_out", &SweepEvent::inOut)
      .def_readwrite("other_in_out", &SweepEvent::otherInOut)
      .def_readwrite("in_result", &SweepEvent::inResult)
      .def_readwrite("result_in_out", &SweepEvent::resultInOut)
      .def_readwrite("position", &SweepEvent::pos)
      .def_readwrite("contour_id", &SweepEvent::contourId)
      .def_readwrite("prev_in_result_event", &SweepEvent::prevInResult)
      .def_property_readonly("is_vertical", &SweepEvent::vertical)
      .def_property_readonly("segment", &SweepEvent::segment)
      .def("is_above", &SweepEvent::above)
      .def("is_below", &SweepEvent::below);

  py::class_<EventsQueueKey>(m, EVENTS_QUEUE_KEY_NAME)
      .def(py::init<const SweepEvent*>(), py::arg("event"))
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
      .def(py::init<const SweepEvent*>(), py::arg("event"))
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
}
