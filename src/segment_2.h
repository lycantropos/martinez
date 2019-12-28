/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

// ------------------------------------------------------------------
// Segment_2 Class - A line segment in the plane
// ------------------------------------------------------------------

#ifndef SEGMENT_2_H
#define SEGMENT_2_H

#include <algorithm>

#include "point.h"

namespace cbop {

class Segment_2 {
 public:
  /** Default constructor */
  Segment_2() {}

  /** Constructor from two points **/
  Segment_2(const Point& source, const Point& target)
      : _source(source), _target(target) {}

  /** Set the source point */
  void setSource(const Point& source) { _source = source; }
  /** Set the target point */
  void setTarget(const Point& target) { _target = target; }

  /** Get the source point */
  const Point& source() const { return _source; }
  /** Get the target point */
  const Point& target() const { return _target; }

  /** Return the point of the segment with lexicographically smallest coordinate
   */
  const Point& min() const {
    return (_source.x() < _target.x()) ||
                   (_source.x() == _target.x() && _source.y() < _target.y())
               ? _source
               : _target;
  }
  /** Return the point of the segment with lexicographically largest coordinate
   */
  const Point& max() const {
    return (_source.x() > _target.x()) ||
                   (_source.x() == _target.x() && _source.y() > _target.y())
               ? _source
               : _target;
  }
  bool degenerate() const { return _source == _target; }
  bool is_vertical() const { return _source.x() == _target.x(); }
  /** Change the segment orientation */
  Segment_2 changeOrientation() { return Segment_2(_target, _source); }

 private:
  /** Segment endpoints */
  Point _source, _target;
};

inline std::ostream& operator<<(std::ostream& o, const Segment_2& p) {
  return o << p.source() << "-" << p.target();
}

}  // end of namespace cbop
#endif
