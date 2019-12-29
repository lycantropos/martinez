/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

#include "polygon.h"

#include <algorithm>

using namespace cbop;

static bool are_counterclockwise(const std::vector<Point>& points) {
  if (points.size() <= 1) return true;
  double area = 0.0;
  for (size_t index = 0; index < points.size() - 1; ++index)
    area += points[index].x() * points[index + 1].y() -
            points[index + 1].x() * points[index].y();
  area += points[points.size() - 1].x() * points[0].y() -
          points[0].x() * points[points.size() - 1].y();
  return area >= 0.0;
}

Contour::Contour() : _points(), _holes(), _external(true), _CC(true) {}

Contour::Contour(const std::vector<cbop::Point>& points,
                 const std::vector<size_t>& holes, bool external)
    : _points(points),
      _holes(holes),
      _external(external),
      _CC(are_counterclockwise(points)) {}

void Contour::changeOrientation() {
  std::reverse(_points.begin(), _points.end());
  _CC = are_counterclockwise(_points);
}

Bbox Contour::bbox() const {
  if (nvertices() == 0) return Bbox();
  Bbox b = vertex(0).bbox();
  for (size_t i = 1; i < nvertices(); ++i) b = b + vertex(i).bbox();
  return b;
}

void Polygon::join(const Polygon& pol) {
  size_t size = ncontours();
  for (size_t i = 0; i < pol.ncontours(); ++i) {
    push_back(pol.contour(i));
    back().clearHoles();
    for (size_t j = 0; j < pol.contour(i).nholes(); ++j)
      back().addHole(pol.contour(i).hole(j) + size);
  }
}

size_t Polygon::nvertices() const {
  size_t nv = 0;
  for (size_t i = 0; i < ncontours(); i++) nv += _contours[i].nvertices();
  return nv;
}

Bbox Polygon::bbox() const {
  if (ncontours() == 0) return Bbox();
  Bbox bb = _contours[0].bbox();
  for (size_t i = 1; i < ncontours(); i++) bb = bb + _contours[i].bbox();
  return bb;
}
