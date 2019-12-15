/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

#include "polygon.h"

#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <set>
#include <sstream>

using namespace cbop;

static bool are_counterclockwise(const std::vector<Point_2>& points) {
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

Contour::Contour(const std::vector<cbop::Point_2>& points,
                 const std::vector<size_t>& holes, bool external)
    : _points(points),
      _holes(holes),
      _external(external),
      _CC(are_counterclockwise(points)) {}

void Contour::changeOrientation() {
  std::reverse(_points.begin(), _points.end());
  _CC = are_counterclockwise(_points);
}

Bbox_2 Contour::bbox() const {
  if (nvertices() == 0) return Bbox_2();
  Bbox_2 b = vertex(0).bbox();
  for (size_t i = 1; i < nvertices(); ++i) b = b + vertex(i).bbox();
  return b;
}

std::ostream& cbop::operator<<(std::ostream& o, Contour& c) {
  o << c.nvertices() << '\n';
  Contour::iterator i = c.begin();
  while (i != c.end()) {
    o << '\t' << i->x() << " " << i->y() << '\n';
    ++i;
  }
  return o;
}

bool Polygon::open(const std::string& filename) {
  clear();
  std::ifstream f(filename.c_str());
  if (!f) return false;
  f >> *this;
  if (!f.eof()) {
    clear();
    return false;
  }
  return true;
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

Bbox_2 Polygon::bbox() const {
  if (ncontours() == 0) return Bbox_2();
  Bbox_2 bb = _contours[0].bbox();
  for (size_t i = 1; i < ncontours(); i++) bb = bb + _contours[i].bbox();
  return bb;
}

std::ostream& cbop::operator<<(std::ostream& o, Polygon& p) {
  o << p.ncontours() << std::endl;
  for (size_t i = 0; i < p.ncontours(); i++)  // write the contours
    o << p.contour(i);
  for (size_t i = 0; i < p.ncontours();
       i++) {  // write the holes of every contour
    if (p.contour(i).nholes() > 0) {
      o << i << ": ";
      for (size_t j = 0; j < p.contour(i).nholes(); j++)
        o << p.contour(i).hole(j)
          << (j == p.contour(i).nholes() - 1 ? '\n' : ' ');
    }
  }
  return o;
}

std::istream& cbop::operator>>(std::istream& is, Polygon& p) {
  // read the contours
  int ncontours;
  double px, py;
  is >> ncontours;
  for (int i = 0; i < ncontours; i++) {
    int npoints;
    is >> npoints;
    p.push_back(Contour());
    Contour& contour = p.back();
    for (int j = 0; j < npoints; j++) {
      is >> px >> py;
      if (j > 0 && px == contour.back().x() && py == contour.back().y())
        continue;
      if (j == npoints - 1 && px == contour.vertex(0).x() &&
          py == contour.vertex(0).y())
        continue;
      contour.add(Point_2(px, py));
    }
    if (contour.nvertices() < 3) {
      p.pop_back();
      continue;
    }
  }
  // read holes information
  int contourId;
  char aux;
  std::string restOfLine;
  while (is >> contourId) {
    is >> aux;  // read the character :
    if (aux != ':') break;
    std::getline(is, restOfLine);
    std::istringstream iss(restOfLine);
    int hole;
    while (iss >> hole) {
      p[contourId].addHole(hole);
      p[hole].setExternal(false);
    }
    if (!iss.eof()) break;
  }
  return is;
}
