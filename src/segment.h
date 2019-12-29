/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

// ------------------------------------------------------------------
// Segment Class - A line segment in the plane
// ------------------------------------------------------------------

#ifndef SEGMENT_H
#define SEGMENT_H

#include "point.h"

namespace cbop {

class Segment {
 public:
  /** Default constructor */
  Segment() {}

  /** Constructor from two points **/
  Segment(const Point& source, const Point& target)
      : _source(source), _target(target) {}

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
  Segment changeOrientation() { return Segment(_target, _source); }

 private:
  /** Segment endpoints */
  Point _source, _target;
};
}  // end of namespace cbop
#endif
