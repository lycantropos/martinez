/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

#ifndef POLYGON_H
#define POLYGON_H

#include <vector>

#include "bbox.h"
#include "utilities.h"

namespace cbop {

class Contour {
 public:
  typedef std::vector<Point>::iterator iterator;
  typedef std::vector<Point>::const_iterator const_iterator;

  Contour();
  Contour(const std::vector<Point>& points, const std::vector<size_t>& holes,
          bool external);

  /** Get the p-th vertex of the external contour */
  Point& vertex(size_t p) { return _points[p]; }
  Point vertex(size_t p) const { return _points[p]; }
  Segment segment(size_t p) const {
    return (p == nvertices() - 1) ? Segment(_points.back(), _points.front())
                                  : Segment(_points[p], _points[p + 1]);
  }
  /** Number of vertices and edges */
  size_t nvertices() const { return _points.size(); }
  /** Get the bounding box */
  Bbox bbox() const;
  /** Return if the contour is counterclockwise oriented */
  bool counterclockwise() const { return _CC; };
  /** Return if the contour is clockwise oriented */
  bool clockwise() const { return !counterclockwise(); }
  void changeOrientation();
  void setClockwise() {
    if (counterclockwise()) changeOrientation();
  }
  void setCounterClockwise() {
    if (clockwise()) changeOrientation();
  }

  void add(const Point& s) { _points.push_back(s); }
  void erase(iterator i) { _points.erase(i); }
  void clear() {
    _points.clear();
    _holes.clear();
  }
  void clearHoles() { _holes.clear(); }
  iterator begin() { return _points.begin(); }
  iterator end() { return _points.end(); }
  const_iterator begin() const { return _points.begin(); }
  const_iterator end() const { return _points.end(); }
  Point& back() { return _points.back(); }
  const Point& back() const { return _points.back(); }
  void addHole(size_t ind) { _holes.push_back(ind); }
  size_t nholes() const { return _holes.size(); }
  size_t hole(size_t p) const { return _holes[p]; }
  bool external() const { return _external; }
  void setExternal(bool e) { _external = e; }

 private:
  /** Set of points conforming the external contour */
  std::vector<Point> _points;
  /** Holes of the contour. They are stored as the indexes of the holes in a
   * polygon class */
  std::vector<size_t> _holes;
  bool _external;  // is the contour an external contour? (i.e., is it not a
                   // hole?)
  bool _CC;
};

class Polygon {
 public:
  typedef std::vector<Contour>::iterator iterator;
  typedef std::vector<Contour>::const_iterator const_iterator;

  Polygon() : _contours() {}
  Polygon(const std::vector<Contour>& contours) : _contours(contours) {}

  void join(const Polygon& pol);
  /** Get the p-th contour */
  Contour& contour(size_t p) { return _contours[p]; }
  const Contour& contour(size_t p) const { return _contours[p]; }
  Contour& operator[](size_t p) { return _contours[p]; }
  const Contour& operator[](size_t p) const { return _contours[p]; }
  /** Number of contours */
  size_t ncontours() const { return _contours.size(); }
  /** Number of vertices */
  size_t nvertices() const;
  /** Get the bounding box */
  Bbox bbox() const;
  void push_back(const Contour& c) { _contours.push_back(c); }
  Contour& back() { return _contours.back(); }
  const Contour& back() const { return _contours.back(); }
  void pop_back() { _contours.pop_back(); }
  void erase(iterator i) { _contours.erase(i); }
  void clear() { _contours.clear(); }

  iterator begin() { return _contours.begin(); }
  iterator end() { return _contours.end(); }
  const_iterator begin() const { return _contours.begin(); }
  const_iterator end() const { return _contours.end(); }

 private:
  /** Set of contours conforming the polygon */
  std::vector<Contour> _contours;
};
}  // end of namespace cbop
#endif
