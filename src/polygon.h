/***************************************************************************
 *   Developer: Francisco Martínez del Río (2012)                          *
 *   fmartin@ujaen.es                                                      *
 *   Version: 1.0                                                          *
 *                                                                         *
 *   This is a public domain program                                       *
 ***************************************************************************/

#ifndef POLYGON_H
#define POLYGON_H

#include <algorithm>
#include <vector>

#include "bbox_2.h"
#include "utilities.h"

namespace cbop {

class Contour {
 public:
  typedef std::vector<Point_2>::iterator iterator;
  typedef std::vector<Point_2>::const_iterator const_iterator;

  Contour();
  Contour(const std::vector<Point_2>& points,
          const std::vector<unsigned int>& holes, bool external);

  /** Get the p-th vertex of the external contour */
  Point_2& vertex(unsigned int p) { return _points[p]; }
  Point_2 vertex(unsigned int p) const { return _points[p]; }
  Segment_2 segment(unsigned int p) const {
    return (p == nvertices() - 1) ? Segment_2(_points.back(), _points.front())
                                  : Segment_2(_points[p], _points[p + 1]);
  }
  /** Number of vertices and edges */
  unsigned nvertices() const { return _points.size(); }
  unsigned nedges() const { return _points.size(); }
  /** Get the bounding box */
  Bbox_2 bbox() const;
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

  void move(double x, double y);
  void add(const Point_2& s) { _points.push_back(s); }
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
  Point_2& back() { return _points.back(); }
  const Point_2& back() const { return _points.back(); }
  void addHole(unsigned int ind) { _holes.push_back(ind); }
  unsigned int nholes() const { return _holes.size(); }
  unsigned int hole(unsigned int p) const { return _holes[p]; }
  bool external() const { return _external; }
  void setExternal(bool e) { _external = e; }

 private:
  /** Set of points conforming the external contour */
  std::vector<Point_2> _points;
  /** Holes of the contour. They are stored as the indexes of the holes in a
   * polygon class */
  std::vector<unsigned int> _holes;
  bool _external;  // is the contour an external contour? (i.e., is it not a
                   // hole?)
  bool _CC;
};

std::ostream& operator<<(std::ostream& o, Contour& c);

class Polygon {
 public:
  typedef std::vector<Contour>::iterator iterator;
  typedef std::vector<Contour>::const_iterator const_iterator;

  Polygon() : _contours() {}
  Polygon(const std::vector<Contour>& contours) : _contours(contours) {}

  // Get the polygon from a text file */
  bool open(const std::string& filename);
  void join(const Polygon& pol);
  /** Get the p-th contour */
  Contour& contour(unsigned int p) { return _contours[p]; }
  const Contour& contour(unsigned int p) const { return _contours[p]; }
  Contour& operator[](unsigned int p) { return _contours[p]; }
  const Contour& operator[](unsigned int p) const { return _contours[p]; }
  /** Number of contours */
  unsigned int ncontours() const { return _contours.size(); }
  /** Number of vertices */
  unsigned int nvertices() const;
  /** Get the bounding box */
  Bbox_2 bbox() const;

  void move(double x, double y);

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
  void computeHoles();

 private:
  /** Set of contours conforming the polygon */
  std::vector<Contour> _contours;
};

std::ostream& operator<<(std::ostream& o, Polygon& p);
std::istream& operator>>(std::istream& i, Polygon& p);

}  // end of namespace cbop
#endif
