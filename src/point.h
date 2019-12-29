/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

// ------------------------------------------------------------------
// Point Class - A point in the plane
// ------------------------------------------------------------------

#ifndef POINT_H
#define POINT_H

#include <cmath>

#include "bbox.h"

namespace cbop {

class Point {
 public:
  Point(double x = 0.0, double y = 0.0) : _x(x), _y(y) {}
  double x() const { return _x; }
  double y() const { return _y; }
  Bbox bbox() const { return Bbox(_x, _y, _x, _y); }
  /** Distance to other point */
  double dist(const Point& p) const {
    double dx = x() - p.x();
    double dy = y() - p.y();
    return sqrt(dx * dx + dy * dy);
  }

 private:
  /** coordinates */
  double _x, _y;
};

inline bool operator==(const Point& p1, const Point& p2) {
  return (p1.x() == p2.x()) && (p1.y() == p2.y());
}
inline bool operator!=(const Point& p1, const Point& p2) { return !(p1 == p2); }
}  // end of namespace cbop
#endif
