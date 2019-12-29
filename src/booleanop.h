/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

#ifndef BOOLEANOP_H
#define BOOLEANOP_H

#include <functional>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

#include "polygon.h"

namespace cbop {

enum BooleanOpType { INTERSECTION, UNION, DIFFERENCE, XOR };
enum EdgeType {
  NORMAL,
  NON_CONTRIBUTING,
  SAME_TRANSITION,
  DIFFERENT_TRANSITION
};
enum PolygonType { SUBJECT, CLIPPING };

struct SweepEvent;  // forward declaration
struct SegmentComp {
  bool operator()(const SweepEvent* le1, const SweepEvent* le2) const;
};

struct SweepEvent {
  SweepEvent(bool left = false, const Point& point = Point(),
             SweepEvent* otherEvent = nullptr,
             PolygonType polygonType = SUBJECT, EdgeType edgeType = NORMAL,
             bool inOut = false, bool otherInOut = false, bool inResult = false,
             bool resultInOut = false, size_t position = 0,
             size_t contourId = 0, SweepEvent* prevInResult = nullptr);
  bool left;               // is point the left endpoint of the edge (point,
                           // otherEvent->point)?
  Point point;             // point associated with the event
  SweepEvent* otherEvent;  // event associated to the other endpoint of the edge
  PolygonType pol;         // Polygon to which the associated segment belongs to
  EdgeType type;
  // The following fields are only used in "left" events
  /**  Does segment (point, otherEvent->p) represent an inside-outside
   * transition in the polygon for a vertical ray from (p.x, -infinite)? */
  bool inOut;
  bool otherInOut;  // inOut transition for the segment from the other polygon
                    // preceding this segment in sl
  SweepEvent* prevInResult;  // previous segment in sl belonging to the result
                             // of the boolean operation
  bool inResult;
  size_t pos;
  bool resultInOut;
  size_t contourId;
  // member functions
  /** Is the line segment (point, otherEvent->point) below point p */
  bool below(const Point& p) const {
    validate();
    return (left) ? signedArea(point, otherEvent->point, p) > 0.
                  : signedArea(otherEvent->point, point, p) > 0.;
  }
  /** Is the line segment (point, otherEvent->point) above point p */
  bool above(const Point& p) const { return !below(p); }
  /** Is the line segment (point, otherEvent->point) a vertical line segment */
  bool vertical() const {
    validate();
    return point.x() == otherEvent->point.x();
  }
  /** Return the line segment associated to the SweepEvent */
  Segment segment() const {
    validate();
    return Segment(point, otherEvent->point);
  }
  void validate() const {
    if (!otherEvent) throw std::domain_error("No `otherEvent` found.");
  }
};

struct SweepEventComp
    : public std::binary_function<SweepEvent, SweepEvent,
                                  bool> {  // for sorting sweep events
  /* Compares two sweep events.
     Checks if e1 is placed at the event queue after e2,
     i.e e1 should be processed by the algorithm after e2 */
  bool operator()(const SweepEvent* e1, const SweepEvent* e2) const {
    if (e1->point.x() > e2->point.x())  // Different x-coordinate
      return true;
    if (e2->point.x() > e1->point.x())  // Different x-coordinate
      return false;
    if (e1->point.y() !=
        e2->point.y())  // Different points, but same x-coordinate. The event
                        // with lower y-coordinate is processed first
      return e1->point.y() > e2->point.y();
    if (e1->left !=
        e2->left)  // Same point, but one is a left endpoint and the other a
                   // right endpoint. The right endpoint is processed first
      return e1->left;
    // Same point, both events are left endpoints or both are right endpoints.
    if (signedArea(e1->point, e1->otherEvent->point, e2->otherEvent->point) !=
        0.)  // not collinear
      return e1->above(
          e2->otherEvent->point);  // the event associate to the bottom segment
                                   // is processed first
    return e1->pol > e2->pol;
  }
};

class BooleanOpImp {
 public:
  BooleanOpImp(const Polygon& subj, const Polygon& clip, BooleanOpType op);

  const Polygon& subject() const { return _subject; }

  const Polygon& clipping() const { return _clipping; }

  const Polygon& result() const { return _result; }

  BooleanOpType operation() const { return _operation; }

  std::priority_queue<SweepEvent*, std::vector<SweepEvent*>, SweepEventComp>
  eventsQueue() const {
    return eq;
  }

  static std::vector<SweepEvent*> collectEvents(
      const std::vector<SweepEvent*>& events);
  // connect the solution edges to build the result polygon
  void computeFields(SweepEvent* le, SweepEvent* prev) const;
  void connectEdges(const std::vector<SweepEvent*>& events);
  /** @brief return if the left event le belongs to the result of the Boolean
   * operation */
  bool inResult(SweepEvent* le) const;
  static size_t nextPos(size_t pos,
                        const std::vector<SweepEvent*>& resultEvents,
                        const std::vector<bool>& processed);
  /** @brief Process a posible intersection between the edges associated to the
   * left events le1 and le2 */
  int possibleIntersection(SweepEvent* le1, SweepEvent* le2);
  void processEvents(const std::vector<SweepEvent*>& events);
  void processSegments();
  void run();
  std::vector<SweepEvent*> sweep();
  bool trivial();

  /** @brief Divide the segment associated to left event le,
   *  updating pq and (implicitly) the status line */
  void divideSegment(SweepEvent* le, const Point& p);

 private:
  const Polygon _subject;
  const Polygon _clipping;
  Polygon _result;
  BooleanOpType _operation;
  Bbox _subjectBB;   // for optimizations 1 and 2
  Bbox _clippingBB;  // for optimizations 1 and 2
  bool _alreadyRun;
  std::priority_queue<SweepEvent*, std::vector<SweepEvent*>, SweepEventComp>
      eq;  // event queue (sorted events to be processed)
  std::set<SweepEvent*, SegmentComp>
      sl;  // segments intersecting the sweep line
  std::deque<SweepEvent>
      eventHolder;  // It holds the events generated during the computation of
                    // the boolean operation
  SweepEventComp sec;  // to compare events
  /** @brief Compute the events associated to segment s, and insert them into pq
   * and eq */
  void processSegment(const Segment& s, PolygonType pt);
  /** @brief Store the SweepEvent e into the event holder, returning the address
   * of e */
  SweepEvent* storeSweepEvent(const SweepEvent& e) {
    eventHolder.push_back(e);
    return &eventHolder.back();
  }
  /** @brief compute several fields of left event le */
  void computeFields(SweepEvent* le,
                     const std::set<SweepEvent*, SegmentComp>::iterator& prev);
};

inline Polygon compute(const Polygon& subj, const Polygon& clip,
                       BooleanOpType op) {
  BooleanOpImp boi(subj, clip, op);
  boi.run();
  return boi.result();
}

}  // end of namespace cbop
#endif
