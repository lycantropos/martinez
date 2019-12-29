/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

#include "booleanop.h"

#include <algorithm>

using namespace cbop;

SweepEvent::SweepEvent(bool _left, const Point& _point, SweepEvent* _otherEvent,
                       PolygonType _polygonType, EdgeType _edgeType,
                       bool _inOut, bool _otherInOut, bool _inResult,
                       bool _resultInOut, size_t position, size_t _contourId,
                       SweepEvent* prevInResult)
    : left(_left),
      point(_point),
      otherEvent(_otherEvent),
      pol(_polygonType),
      type(_edgeType),
      inOut(_inOut),
      otherInOut(_otherInOut),
      inResult(_inResult),
      resultInOut(_resultInOut),
      pos(position),
      contourId(_contourId),
      prevInResult(prevInResult) {}

// le1 and le2 are the left events of line segments (le1->point,
// le1->otherEvent->point) and (le2->point, le2->otherEvent->point)
bool SegmentComp::operator()(const SweepEvent* le1,
                             const SweepEvent* le2) const {
  if (le1 == le2) return false;
  if (signedArea(le1->point, le1->otherEvent->point, le2->point) != 0. ||
      signedArea(le1->point, le1->otherEvent->point, le2->otherEvent->point) !=
          0.) {
    // Segments are not collinear
    // If they share their left endpoint use the right endpoint to sort
    if (le1->point == le2->point) return le1->below(le2->otherEvent->point);
    // Different left endpoint: use the left endpoint to sort
    if (le1->point.x() == le2->point.x())
      return le1->point.y() < le2->point.y();
    SweepEventComp comp;
    if (comp(le1, le2))  // has the line segment associated to e1 been inserted
                         // into S after the line segment associated to e2 ?
      return le2->above(le1->point);
    // The line segment associated to e2 has been inserted into S after the line
    // segment associated to e1
    return le1->below(le2->point);
  }
  // Segments are collinear
  if (le1->pol != le2->pol) return le1->pol < le2->pol;
  SweepEventComp comp;
  return comp(le1, le2);
}

BooleanOpImp::BooleanOpImp(const Polygon& subject, const Polygon& clipping,
                           BooleanOpType operation)
    : _subject(subject),
      _clipping(clipping),
      _result(),
      _operation(operation),
      _subjectBB(subject.bbox()),
      _clippingBB(clipping.bbox()),
      _alreadyRun(false),
      eq(),
      sl(),
      eventHolder() {}

void BooleanOpImp::run() {
  if (_alreadyRun) return;
  // trivial cases can be quickly resolved without sweeping the plane
  if (trivial()) return;
  processSegments();
  connectEdges(sweep());
  _alreadyRun = true;
}

std::vector<SweepEvent*> BooleanOpImp::sweep() {
  const double MINMAXX =
      std::min(_subjectBB.xmax(), _clippingBB.xmax());  // for optimization 2
  std::set<SweepEvent*, SegmentComp>::iterator it, prev, next;
  std::vector<SweepEvent*> result;

  while (!eq.empty()) {
    SweepEvent* se = eq.top();
    // optimization 2
    if ((_operation == INTERSECTION && se->point.x() > MINMAXX) ||
        (_operation == DIFFERENCE && se->point.x() > _subjectBB.xmax())) {
      break;
    }
    result.push_back(se);
    eq.pop();
    if (se->left) {  // the line segment must be inserted into sl
      next = prev = it = sl.insert(se).first;
      (prev != sl.begin()) ? --prev : prev = sl.end();
      ++next;
      computeFields(se, prev);
      // Process a possible intersection between "se" and its next neighbor in
      // sl
      if (next != sl.end()) {
        if (possibleIntersection(se, *next) == 2) {
          computeFields(se, prev);
          computeFields(*next, it);
        }
      }
      // Process a possible intersection between "se" and its previous neighbor
      // in sl
      if (prev != sl.end()) {
        if (possibleIntersection(*prev, se) == 2) {
          std::set<SweepEvent*, SegmentComp>::iterator prevprev = prev;
          (prevprev != sl.begin()) ? --prevprev : prevprev = sl.end();
          computeFields(*prev, prevprev);
          computeFields(se, prev);
        }
      }
    } else {
      // the line segment must be removed from sl
      se = se->otherEvent;  // we work with the left event
      it = sl.find(se);
      if (it == sl.end()) continue;
      next = prev = it;
      (prev != sl.begin()) ? --prev : prev = sl.end();
      ++next;
      // delete line segment associated to "se" from sl and check for
      // intersection between the neighbors of "se" in sl
      sl.erase(it);
      if (next != sl.end() && prev != sl.end())
        possibleIntersection(*prev, *next);
    }
  }
  return result;
}

bool BooleanOpImp::trivial() {
  // Test 1 for trivial result case
  if (_subject.ncontours() * _clipping.ncontours() ==
      0) {  // At least one of the polygons is empty
    if (_operation == DIFFERENCE) _result = _subject;
    if (_operation == UNION || _operation == XOR)
      _result = (_subject.ncontours() == 0) ? _clipping : _subject;
    _alreadyRun = true;
    return true;
  }
  // Test 2 for trivial result case
  if (_subjectBB.xmin() > _clippingBB.xmax() ||
      _clippingBB.xmin() > _subjectBB.xmax() ||
      _subjectBB.ymin() > _clippingBB.ymax() ||
      _clippingBB.ymin() > _subjectBB.ymax()) {
    // the bounding boxes do not overlap
    if (_operation == DIFFERENCE)
      _result = _subject;
    else if (_operation == UNION || _operation == XOR) {
      _result = _subject;
      _result.join(_clipping);
    } else
      _result = Polygon();
    _alreadyRun = true;
    return true;
  }
  return false;
}

void BooleanOpImp::processSegments() {
  for (size_t i = 0; i < _subject.ncontours(); i++)
    for (size_t j = 0; j < _subject.contour(i).nvertices(); j++)
      processSegment(_subject.contour(i).segment(j), SUBJECT);
  for (size_t i = 0; i < _clipping.ncontours(); i++)
    for (size_t j = 0; j < _clipping.contour(i).nvertices(); j++)
      processSegment(_clipping.contour(i).segment(j), CLIPPING);
}

void BooleanOpImp::processSegment(const Segment& s, PolygonType pt) {
  /*	if (s.degenerate ()) // if the two edge endpoints are equal the segment
     is dicarded
              return;          // This can be done as preprocessing to avoid
     "polygons" with less than 3 edges */
  SweepEvent* e1 = storeSweepEvent(SweepEvent(true, s.source(), 0, pt));
  SweepEvent* e2 = storeSweepEvent(SweepEvent(true, s.target(), e1, pt));
  e1->otherEvent = e2;

  if (s.min() == s.source()) {
    e2->left = false;
  } else {
    e1->left = false;
  }
  eq.push(e1);
  eq.push(e2);
}

void BooleanOpImp::computeFields(
    SweepEvent* le, const std::set<SweepEvent*, SegmentComp>::iterator& prev) {
  // compute inOut and otherInOut fields
  if (prev == sl.end()) {
    le->inOut = false;
    le->otherInOut = true;
  } else if (le->pol ==
             (*prev)->pol) {  // previous line segment in sl belongs to the same
                              // polygon that "se" belongs to
    le->inOut = !(*prev)->inOut;
    le->otherInOut = (*prev)->otherInOut;
  } else {  // previous line segment in sl belongs to a different polygon that
            // "se" belongs to
    le->inOut = !(*prev)->otherInOut;
    le->otherInOut = (*prev)->vertical() ? !(*prev)->inOut : (*prev)->inOut;
  }
  // compute prevInResult field
  if (prev != sl.end())
    le->prevInResult = (!inResult(*prev) || (*prev)->vertical())
                           ? (*prev)->prevInResult
                           : *prev;
  // check if the line segment belongs to the Boolean operation
  le->inResult = inResult(le);
}

void BooleanOpImp::computeFields(SweepEvent* le, SweepEvent* prev) const {
  // compute inOut and otherInOut fields
  if (prev == nullptr) {
    le->inOut = false;
    le->otherInOut = true;
  } else if (le->pol == prev->pol) {  // previous line segment in sl belongs to
                                      // the same polygon that "se" belongs to
    le->inOut = !prev->inOut;
    le->otherInOut = prev->otherInOut;
  } else {  // previous line segment in sl belongs to a different polygon that
            // "se" belongs to
    le->inOut = !prev->otherInOut;
    le->otherInOut = prev->vertical() ? !prev->inOut : prev->inOut;
  }
  // compute prevInResult field
  if (prev != nullptr)
    le->prevInResult =
        (!inResult(prev) || prev->vertical()) ? prev->prevInResult : prev;
  // check if the line segment belongs to the Boolean operation
  le->inResult = inResult(le);
}

bool BooleanOpImp::inResult(SweepEvent* le) const {
  switch (le->type) {
    case NORMAL:
      switch (_operation) {
        case (INTERSECTION):
          return !le->otherInOut;
        case (UNION):
          return le->otherInOut;
        case (DIFFERENCE):
          return (le->pol == SUBJECT && le->otherInOut) ||
                 (le->pol == CLIPPING && !le->otherInOut);
        case (XOR):
          return true;
      }
    case SAME_TRANSITION:
      return _operation == INTERSECTION || _operation == UNION;
    case DIFFERENT_TRANSITION:
      return _operation == DIFFERENCE;
    case NON_CONTRIBUTING:
      return false;
  }
  return false;  // just to avoid the compiler warning
}

int BooleanOpImp::possibleIntersection(SweepEvent* le1, SweepEvent* le2) {
  // you can uncomment this line if self-intersecting polygons are not allowed
  //	if (e1->pol == e2->pol) return 0;

  Point ip1, ip2;  // intersection points
  int nintersections;

  if (!(nintersections =
            findIntersection(le1->segment(), le2->segment(), ip1, ip2)))
    return 0;  // no intersection

  if ((nintersections == 1) &&
      ((le1->point == le2->point) ||
       (le1->otherEvent->point == le2->otherEvent->point)))
    return 0;  // the line segments intersect at an endpoint of both line
               // segments

  if (nintersections == 2 && le1->pol == le2->pol)
    throw std::domain_error("Edges of the same polygon should not overlap.");

  // The line segments associated to le1 and le2 intersect
  if (nintersections == 1) {
    if (le1->point != ip1 &&
        le1->otherEvent->point != ip1)  // if the intersection point is not an
                                        // endpoint of le1->segment ()
      divideSegment(le1, ip1);
    if (le2->point != ip1 &&
        le2->otherEvent->point != ip1)  // if the intersection point is not an
                                        // endpoint of le2->segment ()
      divideSegment(le2, ip1);
    return 1;
  }
  // The line segments associated to le1 and le2 overlap
  std::vector<SweepEvent*> sortedEvents;
  if (le1->point == le2->point) {
    sortedEvents.push_back(0);
  } else if (sec(le1, le2)) {
    sortedEvents.push_back(le2);
    sortedEvents.push_back(le1);
  } else {
    sortedEvents.push_back(le1);
    sortedEvents.push_back(le2);
  }
  if (le1->otherEvent->point == le2->otherEvent->point) {
    sortedEvents.push_back(0);
  } else if (sec(le1->otherEvent, le2->otherEvent)) {
    sortedEvents.push_back(le2->otherEvent);
    sortedEvents.push_back(le1->otherEvent);
  } else {
    sortedEvents.push_back(le1->otherEvent);
    sortedEvents.push_back(le2->otherEvent);
  }

  if ((sortedEvents.size() == 2) ||
      (sortedEvents.size() == 3 && sortedEvents[2])) {
    // both line segments are equal or share the left endpoint
    le1->type = NON_CONTRIBUTING;
    le2->type =
        (le1->inOut == le2->inOut) ? SAME_TRANSITION : DIFFERENT_TRANSITION;
    if (sortedEvents.size() == 3)
      divideSegment(sortedEvents[2]->otherEvent, sortedEvents[1]->point);
    return 2;
  }
  if (sortedEvents.size() == 3) {  // the line segments share the right endpoint
    divideSegment(sortedEvents[0], sortedEvents[1]->point);
    return 3;
  }
  if (sortedEvents[0] !=
      sortedEvents[3]
          ->otherEvent) {  // no line segment includes totally the other one
    divideSegment(sortedEvents[0], sortedEvents[1]->point);
    divideSegment(sortedEvents[1], sortedEvents[2]->point);
    return 3;
  }
  // one line segment includes the other one
  divideSegment(sortedEvents[0], sortedEvents[1]->point);
  divideSegment(sortedEvents[3]->otherEvent, sortedEvents[2]->point);
  return 3;
}

void BooleanOpImp::divideSegment(SweepEvent* le, const Point& p) {
  //	std::cout << "YES. INTERSECTION" << std::endl;
  // "Right event" of the "left line segment" resulting from dividing
  // le->segment ()
  SweepEvent* r =
      storeSweepEvent(SweepEvent(false, p, le, le->pol /*, le->type*/));
  // "Left event" of the "right line segment" resulting from dividing
  // le->segment ()
  SweepEvent* l = storeSweepEvent(
      SweepEvent(true, p, le->otherEvent, le->pol /*, le->other->type*/));
  if (sec(l, le->otherEvent)) {  // avoid a rounding error. The left event would
                                 // be processed after the right event
    le->otherEvent->left = true;
    l->left = false;
  }
  le->otherEvent->otherEvent = l;
  le->otherEvent = r;
  eq.push(l);
  eq.push(r);
}

void BooleanOpImp::connectEdges(const std::vector<SweepEvent*>& events) {
  processEvents(collectEvents(events));
}

std::vector<SweepEvent*> BooleanOpImp::collectEvents(
    const std::vector<SweepEvent*>& events) {
  // copy the events in the result polygon to resultEvents array
  std::vector<SweepEvent*> result;
  result.reserve(events.size());
  for (auto it = events.begin(); it != events.end(); it++)
    if (((*it)->left && (*it)->inResult) ||
        (!(*it)->left && (*it)->otherEvent->inResult))
      result.push_back(*it);

  // Due to overlapping edges the result array can be not wholly sorted
  bool sorted = false;
  static const SweepEventComp cmp;  // to compare events
  while (!sorted) {
    sorted = true;
    for (size_t i = 0; i < result.size(); ++i) {
      if (i + 1 < result.size() && cmp(result[i], result[i + 1])) {
        std::swap(result[i], result[i + 1]);
        sorted = false;
      }
    }
  }

  for (size_t i = 0; i < result.size(); ++i) {
    result[i]->pos = i;
    if (!result[i]->left) std::swap(result[i]->pos, result[i]->otherEvent->pos);
  }
  return result;
}

void BooleanOpImp::processEvents(const std::vector<SweepEvent*>& events) {
  std::vector<bool> processed(events.size(), false);
  std::vector<int> depth;
  std::vector<int> holeOf;
  for (size_t i = 0; i < events.size(); i++) {
    if (processed[i]) continue;
    _result.push_back(Contour());
    Contour& contour = _result.back();
    size_t contourId = _result.ncontours() - 1;
    depth.push_back(0);
    holeOf.push_back(-1);
    if (events[i]->prevInResult) {
      size_t lowerContourId = events[i]->prevInResult->contourId;
      if (!events[i]->prevInResult->resultInOut) {
        _result[lowerContourId].addHole(contourId);
        holeOf[contourId] = lowerContourId;
        depth[contourId] = depth[lowerContourId] + 1;
        contour.setExternal(false);
      } else if (!_result[lowerContourId].external()) {
        _result[holeOf[lowerContourId]].addHole(contourId);
        holeOf[contourId] = holeOf[lowerContourId];
        depth[contourId] = depth[lowerContourId];
        contour.setExternal(false);
      }
    }
    size_t pos = i;
    Point initial = events[i]->point;
    contour.add(initial);
    while (events[pos]->otherEvent->point != initial) {
      processed[pos] = true;
      if (events[pos]->left) {
        events[pos]->resultInOut = false;
        events[pos]->contourId = contourId;
      } else {
        events[pos]->otherEvent->resultInOut = true;
        events[pos]->otherEvent->contourId = contourId;
      }
      processed[pos = events[pos]->pos] = true;
      contour.add(events[pos]->point);
      pos = nextPos(pos, events, processed);
    }
    processed[pos] = processed[events[pos]->pos] = true;
    events[pos]->otherEvent->resultInOut = true;
    events[pos]->otherEvent->contourId = contourId;
    if (depth[contourId] & 1) contour.changeOrientation();
  }
}

size_t BooleanOpImp::nextPos(size_t pos,
                             const std::vector<SweepEvent*>& resultEvents,
                             const std::vector<bool>& processed) {
  size_t newPos = pos + 1;
  while (newPos < resultEvents.size() &&
         resultEvents[newPos]->point == resultEvents[pos]->point) {
    if (!processed[newPos])
      return newPos;
    else
      ++newPos;
  }
  if (!pos) return 0;
  newPos = pos - 1;
  while (processed[newPos]) {
    if (!newPos) break;
    --newPos;
  }
  return newPos;
}
