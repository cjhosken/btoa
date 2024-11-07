// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Vector math types, operators and utilities
 */

#pragma once
#include "ai_comparison.h"
#include "ai_constants.h"
#include "ai_math.h"
#include "ai_api.h"
#include <cmath>

/** \defgroup ai_vector AtVector API
 *
 * Vector math types and their related utilities.
 *
 * \{
 */

/**
 * 3D point (single precision)
 */
struct AtVector
{
   float x, y, z;

   AtVector() = default;
   AI_DEVICE constexpr AtVector(float x, float y, float z) : x(x), y(y), z(z) { }

   AI_DEVICE constexpr AtVector operator+(const AtVector& p) const
   {
      return AtVector(x + p.x,
                      y + p.y,
                      z + p.z);
   }

   AI_DEVICE AtVector& operator+=(const AtVector& p)
   {
      x += p.x;
      y += p.y;
      z += p.z;
      return *this;
   }

   AI_DEVICE constexpr AtVector operator+(float f) const
   {
      return AtVector(x + f,
                      y + f,
                      z + f);
   }

   AI_DEVICE AtVector& operator+=(float f)
   {
      x += f;
      y += f;
      z += f;
      return *this;
   }

   AI_DEVICE constexpr AtVector operator-(const AtVector& p) const
   {
      return AtVector(x - p.x,
                      y - p.y,
                      z - p.z);
   }

   AI_DEVICE AtVector& operator-=(const AtVector& p)
   {
      x -= p.x;
      y -= p.y;
      z -= p.z;
      return *this;
   }

   AI_DEVICE constexpr AtVector operator-(float f) const
   {
      return AtVector(x - f,
                      y - f,
                      z - f);
   }

   AI_DEVICE AtVector& operator-=(float f)
   {
      x -= f;
      y -= f;
      z -= f;
      return *this;
   }

   AI_DEVICE constexpr AtVector operator-() const
   {
      return AtVector(-x, -y, -z);
   }

   AI_DEVICE constexpr AtVector operator*(const AtVector& p) const
   {
      return AtVector(x * p.x,
                      y * p.y,
                      z * p.z);
   }

   AI_DEVICE AtVector operator*=(const AtVector& p)
   {
      x *= p.x;
      y *= p.y;
      z *= p.z;
      return *this;
   }

   AI_DEVICE constexpr AtVector operator*(float f) const
   {
      return AtVector(x * f,
                      y * f,
                      z * f);
   }

   AI_DEVICE AtVector operator*=(float f)
   {
      x *= f;
      y *= f;
      z *= f;
      return *this;
   }

   AI_DEVICE constexpr AtVector operator/(const AtVector& p) const
   {
      return AtVector(x / p.x,
                      y / p.y,
                      z / p.z);
   }

   AI_DEVICE AtVector operator/=(const AtVector& p)
   {
      x /= p.x;
      y /= p.y;
      z /= p.z;
      return *this;
   }

   AI_DEVICE AtVector operator/(float f) const
   {
      return AtVector(x / f,
                      y / f,
                      z / f);
   }

   AI_DEVICE AtVector operator/=(float f)
   {
      x /= f;
      y /= f;
      z /= f;
      return *this;
   }

   AI_DEVICE constexpr bool operator==(const AtVector& p) const
   {
      return (x == p.x && y == p.y && z == p.z);
   }

   AI_DEVICE constexpr bool operator!=(const AtVector& p) const
   {
      return !(*this == p);
   }

   AI_DEVICE AtVector& operator=(float f)
   {
      x = f;
      y = f;
      z = f;
      return *this;
   }

   AI_DEVICE float& operator[](unsigned int i)
   {
      return *(&x + i);  // no bounds checking!
   }

   AI_DEVICE constexpr const float& operator[](unsigned int i) const
   {
      return *(&x + i);  // no bounds checking!
   }

   AI_DEVICE friend constexpr AtVector operator*(float f, const AtVector& p);
   AI_DEVICE friend constexpr AtVector operator+(float f, const AtVector& p);
   AI_DEVICE friend constexpr AtVector operator-(float f, const AtVector& p);
};

AI_DEVICE inline constexpr AtVector operator*(float f, const AtVector& p)
{
   return p * f;
}

AI_DEVICE inline constexpr AtVector operator+(float f, const AtVector& p)
{
   return p + f;
}

AI_DEVICE inline constexpr AtVector operator-(float f, const AtVector& p)
{
   return AtVector(f - p.x,
                   f - p.y,
                   f - p.z);
}

AI_DEVICE inline AtBooleanMask<3> operator<(const AtVector& lhs, float f)
{
  return AtBooleanMask<3>::lt(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<3> operator<=(const AtVector& lhs, float f)
{
  return AtBooleanMask<3>::le(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<3> operator>(const AtVector& lhs, float f)
{
  return AtBooleanMask<3>::gt(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<3> operator>=(const AtVector& lhs, float f)
{
  return AtBooleanMask<3>::ge(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<3> operator<(const AtVector& lhs, const AtVector& rhs)
{
  return AtBooleanMask<3>::lt(&lhs[0], &rhs[0]);
}

AI_DEVICE inline AtBooleanMask<3> operator<=(const AtVector& lhs, const AtVector& rhs)
{
  return AtBooleanMask<3>::le(&lhs[0], &rhs[0]);
}

AI_DEVICE inline AtBooleanMask<3> operator>(const AtVector& lhs, const AtVector& rhs)
{
  return AtBooleanMask<3>::gt(&lhs[0], &rhs[0]);
}

AI_DEVICE inline AtBooleanMask<3> operator>=(const AtVector& lhs, const AtVector& rhs)
{
  return AtBooleanMask<3>::ge(&lhs[0], &rhs[0]);
}

/**
 * 2D point
 */
struct AtVector2
{
   float x, y;

   AtVector2() = default;
   AI_DEVICE constexpr AtVector2(float x, float y) : x(x), y(y) { }

   AI_DEVICE constexpr AtVector2(const AtVector& v) : x(v.x), y(v.y) { }

   AI_DEVICE constexpr AtVector2 operator+(const AtVector2& p) const
   {
      return AtVector2(x + p.x,
                       y + p.y);
   }

   AI_DEVICE AtVector2& operator+=(const AtVector2& p)
   {
      x += p.x;
      y += p.y;
      return *this;
   }

   AI_DEVICE constexpr AtVector2 operator+(float f) const
   {
      return AtVector2(x + f,
                       y + f);
   }

   AI_DEVICE AtVector2& operator+=(float f)
   {
      x += f;
      y += f;
      return *this;
   }

   AI_DEVICE constexpr AtVector2 operator-(const AtVector2& p) const
   {
      return AtVector2(x - p.x,
                       y - p.y);
   }

   AI_DEVICE AtVector2& operator-=(const AtVector2& p)
   {
      x -= p.x;
      y -= p.y;
      return *this;
   }

   AI_DEVICE constexpr AtVector2 operator-(float f) const
   {
      return AtVector2(x - f,
                       y - f);
   }

   AI_DEVICE AtVector2& operator-=(float f)
   {
      x -= f;
      y -= f;
      return *this;
   }

   AI_DEVICE constexpr AtVector2 operator-() const
   {
      return AtVector2(-x, -y);
   }

   AI_DEVICE constexpr AtVector2 operator*(const AtVector2& p) const
   {
      return AtVector2(x * p.x,
                       y * p.y);
   }

   AI_DEVICE AtVector2 operator*=(const AtVector2& p)
   {
      x *= p.x;
      y *= p.y;
      return *this;
   }

   AI_DEVICE constexpr AtVector2 operator*(float f) const
   {
      return AtVector2(x * f,
                       y * f);
   }

   AI_DEVICE AtVector2 operator*=(float f)
   {
      x *= f;
      y *= f;
      return *this;
   }

   AI_DEVICE constexpr AtVector2 operator/(const AtVector2& p) const
   {
      return AtVector2(x / p.x,
                       y / p.y);
   }

   AI_DEVICE AtVector2 operator/=(const AtVector2& p)
   {
      x /= p.x;
      y /= p.y;
      return *this;
   }

   AI_DEVICE AtVector2 operator/(float f) const
   {
      return AtVector2(x / f,
                       y / f);
   }

   AI_DEVICE AtVector2 operator/=(float f)
   {
      x /= f;
      y /= f;
      return *this;
   }

   AI_DEVICE constexpr bool operator==(const AtVector2& p) const
   {
      return (x == p.x && y == p.y);
   }

   AI_DEVICE constexpr bool operator!=(const AtVector2& p) const
   {
      return !(*this == p);
   }

   AI_DEVICE AtVector2& operator=(float f)
   {
      x = f;
      y = f;
      return *this;
   }

   AI_DEVICE float& operator[](unsigned int i)
   {
      return *(&x + i);  // no bounds checking!
   }

   AI_DEVICE constexpr const float& operator[](unsigned int i) const
   {
      return *(&x + i);  // no bounds checking!
   }

   AI_DEVICE friend constexpr AtVector2 operator*(float f, const AtVector2& p);
   AI_DEVICE friend constexpr AtVector2 operator+(float f, const AtVector2& p);
   AI_DEVICE friend constexpr AtVector2 operator-(float f, const AtVector2& p);
};

AI_DEVICE inline constexpr AtVector2 operator*(float f, const AtVector2& p)
{
   return p * f;
}

AI_DEVICE inline constexpr AtVector2 operator+(float f, const AtVector2& p)
{
   return p + f;
}

AI_DEVICE inline constexpr AtVector2 operator-(float f, const AtVector2& p)
{
   return AtVector2(f - p.x,
                    f - p.y);
}

AI_DEVICE inline AtBooleanMask<2> operator<(const AtVector2& lhs, float f)
{
  return AtBooleanMask<2>::lt(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<2> operator<=(const AtVector2& lhs, float f)
{
  return AtBooleanMask<2>::le(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<2> operator>(const AtVector2& lhs, float f)
{
  return AtBooleanMask<2>::gt(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<2> operator>=(const AtVector2& lhs, float f)
{
  return AtBooleanMask<2>::ge(&lhs[0], f);
}

AI_DEVICE inline AtBooleanMask<2> operator<(const AtVector2& lhs, const AtVector2& rhs)
{
  return AtBooleanMask<2>::lt(&lhs[0], &rhs[0]);
}

AI_DEVICE inline AtBooleanMask<2> operator<=(const AtVector2& lhs, const AtVector2& rhs)
{
  return AtBooleanMask<2>::le(&lhs[0], &rhs[0]);
}

AI_DEVICE inline AtBooleanMask<2> operator>(const AtVector2& lhs, const AtVector2& rhs)
{
  return AtBooleanMask<2>::gt(&lhs[0], &rhs[0]);
}

AI_DEVICE inline AtBooleanMask<2> operator>=(const AtVector2& lhs, const AtVector2& rhs)
{
  return AtBooleanMask<2>::ge(&lhs[0], &rhs[0]);
}


/**
 * Homogeneous point
 */
struct AtHPoint
{
   float x, y, z, w;

   AtHPoint() = default;
   AI_DEVICE constexpr AtHPoint(float x, float y, float z, float w) : x(x),   y(y),   z(z),   w(w) { }
   AI_DEVICE constexpr AtHPoint(const AtVector& v,         float w) : x(v.x), y(v.y), z(v.z), w(w) { }

   AI_DEVICE constexpr AtHPoint operator+(const AtHPoint& p) const
   {
      return AtHPoint(x + p.x,
                      y + p.y,
                      z + p.z,
                      w + p.w);
   }

   AI_DEVICE constexpr AtHPoint operator-(const AtHPoint& p) const
   {
      return AtHPoint(x - p.x,
                      y - p.y,
                      z - p.z,
                      w - p.w);
   }

   AI_DEVICE constexpr AtHPoint operator*(float k) const
   {
      return AtHPoint(x * k,
                      y * k,
                      z * k,
                      w * k);
   }

   AI_DEVICE constexpr AtHPoint operator-() const
   {
      return AtHPoint(-x, -y, -z, -w);
   }

   /**
    * Project a homogeneous vector back into 3d: vout = vin.w != 0 ? vin * (1 / vin.w) : (0,0,0)
    */
   AI_DEVICE inline AtVector project() const
   {
      return w != 0 ?
         AtVector(x, y, z) / w :
         AtVector(0, 0, 0);
   }
};

/**
 * Vector with differentials
 */
struct AtVectorDv {
   AtVector val, dx, dy;

   AtVectorDv() = default;
   AI_DEVICE constexpr AtVectorDv(AtVector val, AtVector dx, AtVector dy) : val(val), dx(dx), dy(dy) { }
   AI_DEVICE constexpr explicit AtVectorDv(AtVector val) : val(val), dx(0, 0, 0), dy(0, 0, 0) { }

   AI_DEVICE constexpr AtVectorDv operator-() const
   {
      return AtVectorDv(-val, -dx, -dy);
   }
};

/** \name Vector Components
 * \{
 */
#define AI_X  0   /**< X component */
#define AI_Y  1   /**< Y component */
#define AI_Z  2   /**< Z component */
/*\}*/



/** \name 2D Vector Operations
 * \{
 */

/**
 * Dot product:   <v1, v2>
 */
AI_DEVICE inline constexpr float AiV2Dot(const AtVector2& v1, const AtVector2& v2)
{
   return v1.x * v2.x + v1.y * v2.y;
}

/**
 * Vector Length:   ||v1||
 */
AI_DEVICE inline float AiV2Length(const AtVector2& v1)
{
   return sqrtf(v1.x * v1.x + v1.y * v1.y);
}

/**
 * Distance between two points:   ||p1-p2||
 */
inline float AiV2Dist(const AtVector2& p1, const AtVector2& p2)
{
   return sqrtf(AiSqr(p1.x-p2.x) + AiSqr(p1.y - p2.y));
}

/**
 * 2D vector linear interpolation
 * (t=0 -> result=lo, t=1 -> result=hi)
 */
inline constexpr AtVector2 AiV2Lerp(float t, const AtVector2& lo, const AtVector2& hi)
{
   return AiLerp(t, lo, hi);
}

/**
 * Clamp each vector coordinate to the range [lo,hi]
 */
inline constexpr AtVector2 AiV2Clamp(const AtVector2& in, float lo, float hi)
{
   return AtVector2(AiClamp(in.x, lo, hi),
                    AiClamp(in.y, lo, hi));
}

/**
 * Absolute value of each component
 */
AI_DEVICE inline AtVector2 ABS(const AtVector2& a)
{
   return AtVector2( std::abs(a.x), std::abs(a.y) );
}

/**
 * Element-wise max
 */
AI_DEVICE inline float AiMaxElement(const AtVector2& a)
{
   return AiMax(a.x, a.y);
}

/**
 * Element-wise min
 */
inline float AiMinElement(const AtVector2& a)
{
   return AiMin(a.x, a.y);
}
/*\}*/



/** \name 3D Vector Operations
 * \{
 */

/**
 * Vector Length:   ||a||
 */
AI_DEVICE inline float AiV3Length(const AtVector& a)
{
   return sqrtf(a.x*a.x + a.y*a.y + a.z*a.z);
}

/**
 * Dot product:   <a, b>
 */
AI_DEVICE inline constexpr float AiV3Dot(const AtVector& a, const AtVector& b)
{
   return a.x*b.x + a.y*b.y + a.z*b.z;
} 

/**
 * Distance between two points:   ||a-b||
 */
AI_DEVICE inline float AiV3Dist(const AtVector& a, const AtVector& b)
{
   return sqrtf(AiSqr(a.x-b.x) + AiSqr(a.y-b.y) + AiSqr(a.z-b.z));
}

/**
 * Squared distance between two points:   ||a-b||^2
 */
AI_DEVICE inline constexpr float AiV3Dist2(const AtVector& a, const AtVector& b)
{
   return AiSqr(a.x-b.x) + AiSqr(a.y-b.y) + AiSqr(a.z-b.z); 
}

/**
 * Signed distance between point x and a plane defined by point p and normalized vector n
 */
AI_DEVICE inline constexpr float AiV3DistPlane(const AtVector& x, const AtVector& p, const AtVector& n)
{
   return AiV3Dot(x, n) - AiV3Dot(p, n);
}

/**
 * Cross product:   a x b
 */
AI_DEVICE inline constexpr AtVector AiV3Cross(const AtVector& a, const AtVector& b)
{
   return AtVector(a.y * b.z - a.z * b.y,
                   a.z * b.x - a.x * b.z,
                   a.x * b.y - a.y * b.x);
}

/**
 * Normalize a vector:   a / ||a||
 */
AI_DEVICE inline AtVector AiV3Normalize(const AtVector& a)
{
   float len = AiV3Length(a);
   return len == 0 ? a : a / len;
}

/**
 * 3D vector linear interpolation
 * (t=0 -> result=lo, t=1 -> result=hi)
 */
AI_DEVICE inline constexpr AtVector AiV3Lerp(float t, const AtVector& lo, const AtVector& hi)
{
   return AiLerp(t, lo, hi);
}

/**
 * Clamp each vector coordinate to the range [lo,hi]
 */
AI_DEVICE inline constexpr AtVector AiV3Clamp(const AtVector& in, float lo, float hi)
{
   return AtVector(AiClamp(in.x, lo, hi),
                   AiClamp(in.y, lo, hi),
                   AiClamp(in.z, lo, hi));
}

/**
 * Minimum of two vectors, component-wise
 */
AI_DEVICE inline constexpr AtVector AiV3Min(const AtVector& a, const AtVector& b)
{
   return AtVector(AiMin(a.x, b.x),
                   AiMin(a.y, b.y),
                   AiMin(a.z, b.z));
}

/**
 * Maximum of two vectors, component-wise
 */
AI_DEVICE inline constexpr AtVector AiV3Max(const AtVector& a, const AtVector& b)
{
   return AtVector(AiMax(a.x, b.x),
                   AiMax(a.y, b.y),
                   AiMax(a.z, b.z));
}

/**
 * Absolute value of each component
 */
AI_DEVICE inline AtVector ABS(const AtVector& a)
{
   return AtVector( std::abs(a.x), std::abs(a.y), std::abs(a.z) );
}

/**
 * Element-wise max
 */
AI_DEVICE inline float AiMaxElement(const AtVector& a)
{
   return AiMax(a.x, a.y, a.z);
}

/**
 * Element-wise min
 */
AI_DEVICE inline float AiMinElement(const AtVector& a)
{
   return AiMin(a.x, a.y, a.z);
}

/**
 * Barycentric interpolation of a point inside a triangle
 */
AI_DEVICE inline AtVector AiBerpXYZ(float a, float b, const AtVector& p0, const AtVector& p1, const AtVector& p2)
{
   float c = 1 - (a + b);
   return c*p0 + a*p1 + b*p2;
}

/**
 * Check whether a vector has all valid components (not NaN and not infinite)
 */
AI_API AI_DEVICE AI_PURE bool AiV3IsFinite(const AtVector& a);

/**
 * Check for a zero vector, within a small tolerance:   ||a|| < epsilon
 */
AI_DEVICE inline bool AiV3IsSmall(const AtVector& a, float epsilon = AI_EPSILON)
{
   return std::abs(a.x) < epsilon && std::abs(a.y) < epsilon && std::abs(a.z) < epsilon;
}

/**
 * Rotate vector a so that it aligns with frame {u,v,w}
 */
AI_DEVICE inline void AiV3RotateToFrame(AtVector& a, const AtVector& u, const AtVector& v, const AtVector& w)
{
   a = u * a.x + v * a.y + w * a.z;
}

/**
 * Barycentric interpolation of UV coordinates inside a 3D triangle
 */
AI_DEVICE inline void AiBerpUV(float a, float b, float u0, float v0, float u1, float v1, float u2, float v2, float* u, float* v)
{
   float c = 1.0f - (a + b);
   *u = c * u0 + a * u1 + b * u2;
   *v = c * v0 + a * v1 + b * v2;
}

/*\}*/

/** \name 4D Vector Operations
 * \{
 */

/**
 * Create a 4D point:   pout = (v.x, v.y, v.z, 1)
 */
AI_DEVICE inline AtHPoint AiV4CreatePoint(const AtVector& v)
{
   return AtHPoint(v, 1);
}

/**
 * Create a 4D vector:   vout = (v.x, v.y, v.z, 0)
 */
AI_DEVICE inline AtHPoint AiV4CreateVector(const AtVector& v)
{
   return AtHPoint(v, 0);
}

AI_DEVICE inline void AiV4CreatePoint(AtHPoint& pout, const AtVector& v)
{
   pout = AtHPoint(v, 1);
}

/**
 * Create a 4D vector:   vout = (v.x, v.y, v.z, 0)
 */
inline void AiV4CreateVector(AtHPoint& vout, const AtVector& v)
{
   vout = AtHPoint(v, 0);
}

/**
 * Add two vectors:   vout = v1 + v2
 */
inline void AiV4Add(AtHPoint& vout, const AtHPoint& v1, const AtHPoint& v2)
{
   vout = v1 + v2;
}

/**
 * Substract two vectors:   vout = v1 - v2
 */
inline void AiV4Sub(AtHPoint& vout, const AtHPoint& v1, const AtHPoint& v2)
{
   vout = v1 - v2;
}

/**
 * Scale a vector by a constant:   vout = vin * k
 */
inline void AiV4Scale(AtHPoint& vout, const AtHPoint& vin, float k)
{
   vout = vin * k;
}

/**
 * Negate a vector:   vout = -vin
 */
inline void AiV4Neg(AtHPoint& vout, const AtHPoint& vin)
{
   vout = -vin;
}

/**
 * Project a homogeneous vector back into 3d: vout = vin.w != 0 ? vin * (1 / vin.w) : (0,0,0)
 */
inline void AiV4Project(AtVector& vout, const AtHPoint& vin)
{
   vout = vin.project();
}


/**
 * Build an orthonormal basis aligned with vector N (Frisvad's method).
 */
AI_API AI_DEVICE void AiV3BuildLocalFrame(AtVector& u, AtVector& v, const AtVector& N);

/**
 * Build an orthonormal basis aligned with vector N (polar method).
 */
AI_API AI_DEVICE void AiV3BuildLocalFramePolar(AtVector& u, AtVector& v, const AtVector& N);

/*\}*/

/** \name Constants
 * \{
 */
#ifdef AI_CPU_COMPILER
static constexpr const AtVector AI_P3_ZERO( 0.0f,  0.0f,  0.0f);
static constexpr const AtVector AI_V3_ZERO( 0.0f,  0.0f,  0.0f);
static constexpr const AtVector AI_V3_HALF( 0.5f,  0.5f,  0.5f);
static constexpr const AtVector AI_V3_ONE ( 1.0f,  1.0f,  1.0f);
static constexpr const AtVector AI_V3_X   ( 1.0f,  0.0f,  0.0f);
static constexpr const AtVector AI_V3_Y   ( 0.0f,  1.0f,  0.0f);
static constexpr const AtVector AI_V3_Z   ( 0.0f,  0.0f,  1.0f);
static constexpr const AtVector AI_V3_NEGX(-1.0f,  0.0f,  0.0f);
static constexpr const AtVector AI_V3_NEGY( 0.0f, -1.0f,  0.0f);
static constexpr const AtVector AI_V3_NEGZ( 0.0f,  0.0f, -1.0f);
static constexpr const AtVector2 AI_P2_ZERO( 0.0f,  0.0f);
static constexpr const AtVector2 AI_P2_ONE ( 1.0f,  1.0f);
#else
static __device__ const AtVector AI_P3_ZERO( 0.0f,  0.0f,  0.0f);
static __device__ const AtVector AI_V3_ZERO( 0.0f,  0.0f,  0.0f);
static __device__ const AtVector AI_V3_HALF( 0.5f,  0.5f,  0.5f);
static __device__ const AtVector AI_V3_ONE ( 1.0f,  1.0f,  1.0f);
static __device__ const AtVector AI_V3_X   ( 1.0f,  0.0f,  0.0f);
static __device__ const AtVector AI_V3_Y   ( 0.0f,  1.0f,  0.0f);
static __device__ const AtVector AI_V3_Z   ( 0.0f,  0.0f,  1.0f);
static __device__ const AtVector AI_V3_NEGX(-1.0f,  0.0f,  0.0f);
static __device__ const AtVector AI_V3_NEGY( 0.0f, -1.0f,  0.0f);
static __device__ const AtVector AI_V3_NEGZ( 0.0f,  0.0f, -1.0f);
static __device__ const AtVector2 AI_P2_ZERO( 0.0f,  0.0f);
static __device__ const AtVector2 AI_P2_ONE ( 1.0f,  1.0f);
#endif
/*\}*/

/*\}*/
