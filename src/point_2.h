/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

// ------------------------------------------------------------------
// Point_2 Class - A point in the plane
// ------------------------------------------------------------------

#ifndef POINT_2_H
#define POINT_2_H

#include <cmath>
#include <iostream>

#include "bbox.h"

namespace cbop {

class Point_2 {
 public:
  Point_2(double x = 0.0, double y = 0.0) : _x(x), _y(y) {}
  double x() const { return _x; }
  double y() const { return _y; }
  Bbox bbox() const { return Bbox(_x, _y, _x, _y); }
  /** Distance to other point */
  double dist(const Point_2& p) const {
    double dx = x() - p.x();
    double dy = y() - p.y();
    return sqrt(dx * dx + dy * dy);
  }

 private:
  /** coordinates */
  double _x, _y;
};

inline bool operator==(const Point_2& p1, const Point_2& p2) {
  return (p1.x() == p2.x()) && (p1.y() == p2.y());
}
inline bool operator!=(const Point_2& p1, const Point_2& p2) {
  return !(p1 == p2);
}

inline std::ostream& operator<<(std::ostream& o, const Point_2& p) {
  return o << "(" << p.x() << "," << p.y() << ")";
}

inline std::istream& operator>>(std::istream& i, Point_2& p) {
  double x, y;
  i >> x >> y;
  p = Point_2(x, y);
  return i;
}

}  // end of namespace cbop
#endif
