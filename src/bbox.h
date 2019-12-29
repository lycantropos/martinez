/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

// ------------------------------------------------------------------
// Bbox Class : A bounding box
// ------------------------------------------------------------------

#ifndef BBOX_H
#define BBOX_H

#include <algorithm>

namespace cbop {

class Bbox {
 public:
  Bbox(double x_min = 0, double y_min = 0, double x_max = 0, double y_max = 0)
      : _xmin(x_min), _ymin(y_min), _xmax(x_max), _ymax(y_max) {}
  double xmin() const { return _xmin; }
  double xmax() const { return _xmax; }
  double ymin() const { return _ymin; }
  double ymax() const { return _ymax; }
  Bbox operator+(const Bbox& b) const {
    return Bbox(std::min(_xmin, b.xmin()), std::min(_ymin, b.ymin()),
                std::max(_xmax, b.xmax()), std::max(_ymax, b.ymax()));
  }

 private:
  double _xmin, _ymin, _xmax, _ymax;
};

}  // end of namespace cbop
#endif
