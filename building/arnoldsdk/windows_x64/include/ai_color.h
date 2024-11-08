// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Color types and utilities
 */

#pragma once
#include "ai_comparison.h"
#include "ai_math.h"
#include "ai_string.h"
#include "ai_constants.h"
#include "ai_api.h"

struct AtRGBA;

/** \defgroup ai_color AtRGB API
 * 
 * Creation and operation with Arnold color types.
 * 
 * \{
 */

/**
 * RGB color
 */
struct AtRGB
{
   float r, g, b;

   AtRGB() = default;
   AI_DEVICE constexpr explicit AtRGB(float c)                   : r(c), g(c), b(c) { }
   AI_DEVICE constexpr          AtRGB(float r, float g, float b) : r(r), g(g), b(b) { }
   AI_DEVICE constexpr explicit AtRGB(const AtRGBA& rgba);

   AI_DEVICE constexpr AtRGB operator+(const AtRGB& rgb) const
   {
      return AtRGB(r + rgb.r,
                   g + rgb.g,
                   b + rgb.b);
   }

   AI_DEVICE AtRGB& operator+=(const AtRGB& rgb)
   {
      r += rgb.r;
      g += rgb.g;
      b += rgb.b;
      return *this;
   }

   AI_DEVICE constexpr AtRGB operator+(float f) const
   {
      return AtRGB(r + f,
                   g + f,
                   b + f);
   }

   AI_DEVICE AtRGB& operator+=(float f)
   {
      r += f;
      g += f;
      b += f;
      return *this;
   }

   AI_DEVICE constexpr AtRGB operator-(const AtRGB& rgb) const
   {
      return AtRGB(r - rgb.r,
                   g - rgb.g,
                   b - rgb.b);
   }

   AI_DEVICE AtRGB& operator-=(const AtRGB& rgb)
   {
      r -= rgb.r;
      g -= rgb.g;
      b -= rgb.b;
      return *this;
   }

   AI_DEVICE constexpr AtRGB operator-(float f) const
   {
      return AtRGB(r - f,
                   g - f,
                   b - f);
   }

   AI_DEVICE AtRGB& operator-=(float f)
   {
      r -= f;
      g -= f;
      b -= f;
      return *this;
   }

   AI_DEVICE constexpr AtRGB operator-() const
   {
      return AtRGB(-r, -g, -b);
   }

   AI_DEVICE constexpr AtRGB operator*(const AtRGB& rgb) const
   {
      return AtRGB(r * rgb.r,
                   g * rgb.g,
                   b * rgb.b);
   }

   AI_DEVICE AtRGB operator*=(const AtRGB& rgb)
   {
      r *= rgb.r;
      g *= rgb.g;
      b *= rgb.b;
      return *this;
   }

   AI_DEVICE constexpr AtRGB operator*(float f) const
   {
      return AtRGB(r * f,
                   g * f,
                   b * f);
   }

   AI_DEVICE AtRGB operator*=(float f)
   {
      r *= f;
      g *= f;
      b *= f;
      return *this;
   }

   AI_DEVICE constexpr AtRGB operator/(const AtRGB& rgb) const
   {
      return AtRGB(r / rgb.r,
                   g / rgb.g,
                   b / rgb.b);
   }

   AI_DEVICE AtRGB operator/=(const AtRGB& rgb)
   {
      r /= rgb.r;
      g /= rgb.g;
      b /= rgb.b;
      return *this;
   }

   AI_DEVICE AtRGB operator/(float f) const
   {
      return AtRGB(r / f,
                   g / f,
                   b / f);
   }

   AI_DEVICE AtRGB operator/=(float f)
   {
      r /= f;
      g /= f;
      b /= f;
      return *this;
   }

   AI_DEVICE constexpr bool operator==(const AtRGB& rgb) const
   {
      return (r == rgb.r && g == rgb.g && b == rgb.b);
   }

   AI_DEVICE constexpr bool operator!=(const AtRGB& rgb) const
   {
      return !(*this == rgb);
   }

   AI_DEVICE AtRGB& operator=(float f)
   {
      r = f;
      g = f;
      b = f;
      return *this;
   }

   AI_DEVICE float& operator[](unsigned int i)
   {
      return *(&r + i);  // warning: no bounds checking!
   }

   AI_DEVICE constexpr const float& operator[](unsigned int i) const
   {
      return *(&r + i);  // warning: no bounds checking!
   }

   AI_DEVICE friend constexpr AtRGB operator*(float f, const AtRGB& rgb);
   AI_DEVICE friend constexpr AtRGB operator+(float f, const AtRGB& rgb);
   AI_DEVICE friend constexpr AtRGB operator-(float f, const AtRGB& rgb);
};

AI_DEVICE inline constexpr AtRGB operator*(float f, const AtRGB& rgb)
{
   return rgb * f;
}

AI_DEVICE inline constexpr AtRGB operator+(float f, const AtRGB& rgb)
{
   return rgb + f;
}

AI_DEVICE inline constexpr AtRGB operator-(float f, const AtRGB& rgb)
{
   return AtRGB(f - rgb.r,
                f - rgb.g,
                f - rgb.b);
}

AI_DEVICE inline constexpr AtRGB operator/(float f, const AtRGB& rgb)
{
   return AtRGB(f / rgb.r,
                f / rgb.g,
                f / rgb.b);
}

AI_DEVICE inline AtBooleanMask<3> operator<(const AtRGB& lhs, const AtRGB& rhs)
{
  return AtBooleanMask<3>::lt(&(lhs[0]), &(rhs[0]));
}

AI_DEVICE inline AtBooleanMask<3> operator<=(const AtRGB& lhs, const AtRGB& rhs)
{
  return AtBooleanMask<3>::le(&(lhs[0]), &(rhs[0]));
}

AI_DEVICE inline AtBooleanMask<3> operator>(const AtRGB& lhs, const AtRGB& rhs)
{
  return AtBooleanMask<3>::gt(&(lhs[0]), &(rhs[0]));
}

AI_DEVICE inline AtBooleanMask<3> operator>=(const AtRGB& lhs, const AtRGB& rhs)
{
  return AtBooleanMask<3>::ge(&(lhs[0]), &(rhs[0]));
}

AI_DEVICE inline AtBooleanMask<3> operator<(const AtRGB& lhs, float rhs)
{
  return AtBooleanMask<3>::lt(&(lhs[0]), rhs);
}

AI_DEVICE inline AtBooleanMask<3> operator<=(const AtRGB& lhs, float rhs)
{
  return AtBooleanMask<3>::le(&(lhs[0]), rhs);
}

AI_DEVICE inline AtBooleanMask<3> operator>(const AtRGB& lhs, float rhs)
{
  return AtBooleanMask<3>::gt(&(lhs[0]), rhs);
}

AI_DEVICE inline AtBooleanMask<3> operator>=(const AtRGB& lhs, float rhs)
{
  return AtBooleanMask<3>::ge(&(lhs[0]), rhs);
}


/**
 * RGB color + alpha
 */
struct AtRGBA
{
   float r, g, b, a;

   AtRGBA() = default;
   AI_DEVICE constexpr AtRGBA(float r, float g, float b, float a) : r(r), g(g), b(b), a(a) { }
   AI_DEVICE constexpr AtRGBA(const AtRGB& rgb, float a=1) : r(rgb.r), g(rgb.g), b(rgb.b), a(a) { }

   AI_DEVICE AtRGB& rgb()
   {
      return *static_cast<AtRGB*>(static_cast<void*>(this));
   }

   AI_DEVICE const AtRGB& rgb() const
   {
      return *static_cast<const AtRGB*>(static_cast<const void*>(this));
   }

   AI_DEVICE constexpr AtRGBA operator+(const AtRGBA& rgba) const
   {
      return AtRGBA(r + rgba.r,
                    g + rgba.g,
                    b + rgba.b,
                    a + rgba.a);
   }

   AI_DEVICE AtRGBA& operator+=(const AtRGBA& rgba)
   {
      r += rgba.r;
      g += rgba.g;
      b += rgba.b;
      a += rgba.a;
      return *this;
   }

   AI_DEVICE constexpr AtRGBA operator+(float f) const
   {
      return AtRGBA(r + f,
                    g + f,
                    b + f,
                    a + f);
   }

   AI_DEVICE AtRGBA& operator+=(float f)
   {
      r += f;
      g += f;
      b += f;
      a += f;
      return *this;
   }

   AI_DEVICE constexpr AtRGBA operator-(const AtRGBA& rgba) const
   {
      return AtRGBA(r - rgba.r,
                    g - rgba.g,
                    b - rgba.b,
                    a - rgba.a);
   }

   AI_DEVICE AtRGBA& operator-=(const AtRGBA& rgba)
   {
      r -= rgba.r;
      g -= rgba.g;
      b -= rgba.b;
      a -= rgba.a;
      return *this;
   }

   AI_DEVICE constexpr AtRGBA operator-(float f) const
   {
      return AtRGBA(r - f,
                    g - f,
                    b - f,
                    a - f);
   }

   AI_DEVICE AtRGBA& operator-=(float f)
   {
      r -= f;
      g -= f;
      b -= f;
      a -= f;
      return *this;
   }

   AI_DEVICE constexpr AtRGBA operator-() const
   {
      return AtRGBA(-r, -g, -b, -a);
   }

   AI_DEVICE constexpr AtRGBA operator*(const AtRGBA& rgba) const
   {
      return AtRGBA(r * rgba.r,
                    g * rgba.g,
                    b * rgba.b,
                    a * rgba.a);
   }

   AI_DEVICE AtRGBA operator*=(const AtRGBA& rgba)
   {
      r *= rgba.r;
      g *= rgba.g;
      b *= rgba.b;
      a *= rgba.a;
      return *this;
   }

   AI_DEVICE constexpr AtRGBA operator*(float f) const
   {
      return AtRGBA(r * f,
                    g * f,
                    b * f,
                    a * f);
   }

   AI_DEVICE AtRGBA operator*=(float f)
   {
      r *= f;
      g *= f;
      b *= f;
      a *= f;
      return *this;
   }

   AI_DEVICE constexpr AtRGBA operator/(const AtRGBA& rgba) const
   {
      return AtRGBA(r / rgba.r,
                    g / rgba.g,
                    b / rgba.b,
                    a / rgba.a);
   }

   AI_DEVICE AtRGBA operator/=(const AtRGBA& rgba)
   {
      r /= rgba.r;
      g /= rgba.g;
      b /= rgba.b;
      a /= rgba.a;
      return *this;
   }

   AI_DEVICE AtRGBA operator/(float f) const
   {
      return AtRGBA(r / f,
                    g / f,
                    b / f,
                    a / f);
   }

   AI_DEVICE AtRGBA operator/=(float f)
   {
      r /= f;
      g /= f;
      b /= f;
      a /= f;
      return *this;
   }

   AI_DEVICE constexpr bool operator==(const AtRGBA& rgba) const
   {
      return (r == rgba.r && g == rgba.g && b == rgba.b && a == rgba.a);
   }

   AI_DEVICE constexpr bool operator!=(const AtRGBA& rgba) const
   {
      return !(*this == rgba);
   }

   AI_DEVICE AtRGBA& operator=(float f)
   {
      r = f;
      g = f;
      b = f;
      a = f;
      return *this;
   }

   AI_DEVICE float& operator[](unsigned int i)
   {
      return *(&r + i);  // warning: no bounds checking!
   }

   AI_DEVICE constexpr const float& operator[](unsigned int i) const
   {
      return *(&r + i);  // warning: no bounds checking!
   }

   AI_DEVICE friend constexpr AtRGBA operator*(float f, const AtRGBA& rgba);
   AI_DEVICE friend constexpr AtRGBA operator+(float f, const AtRGBA& rgba);
   AI_DEVICE friend constexpr AtRGBA operator-(float f, const AtRGBA& rgba);
};

AI_DEVICE inline constexpr AtRGBA operator*(float f, const AtRGBA& rgba)
{
   return rgba * f;
}

AI_DEVICE inline constexpr AtRGBA operator+(float f, const AtRGBA& rgba)
{
   return rgba + f;
}

AI_DEVICE inline constexpr AtRGBA operator-(float f, const AtRGBA& rgba)
{
   return AtRGBA(f - rgba.r,
                 f - rgba.g,
                 f - rgba.b,
                 f - rgba.a);
}

inline AtBooleanMask<4> operator<(const AtRGBA& lhs, const AtRGBA& rhs)
{
  return AtBooleanMask<4>::lt(&(lhs[0]), &(rhs[0]));
}

inline AtBooleanMask<4> operator<=(const AtRGBA& lhs, const AtRGBA& rhs)
{
  return AtBooleanMask<4>::le(&(lhs[0]), &(rhs[0]));
}

inline AtBooleanMask<4> operator>(const AtRGBA& lhs, const AtRGBA& rhs)
{
  return AtBooleanMask<4>::gt(&(lhs[0]), &(rhs[0]));
}

inline AtBooleanMask<4> operator>=(const AtRGBA& lhs, const AtRGBA& rhs)
{
  return AtBooleanMask<4>::ge(&(lhs[0]), &(rhs[0]));
}

inline AtBooleanMask<4> operator<(const AtRGBA& lhs, float rhs)
{
  return AtBooleanMask<4>::lt(&(lhs[0]), rhs);
}

inline AtBooleanMask<4> operator<=(const AtRGBA& lhs, float rhs)
{
  return AtBooleanMask<4>::le(&(lhs[0]), rhs);
}

inline AtBooleanMask<4> operator>(const AtRGBA& lhs, float rhs)
{
  return AtBooleanMask<4>::gt(&(lhs[0]), rhs);
}

inline AtBooleanMask<4> operator>=(const AtRGBA& lhs, float rhs)
{
  return AtBooleanMask<4>::ge(&(lhs[0]), rhs);
}

AI_DEVICE inline constexpr AtRGB::AtRGB(const AtRGBA& rgba) : r(rgba.r), g(rgba.g), b(rgba.b) { }


/** \name Other Color Operations
 * \{
 */

/**
 * Clamp the RGB color vector to the specified range
 */
AI_DEVICE inline constexpr AtRGB AiRGBClamp(const AtRGB& c, float lo, float hi)
{
   return AtRGB(AiClamp(c.r, lo, hi),
                AiClamp(c.g, lo, hi),
                AiClamp(c.b, lo, hi));
}

/**
 * Clamp the RGBA color vector to the specified range
 */
AI_DEVICE inline constexpr AtRGBA AiRGBAClamp(const AtRGBA& c, float lo, float hi)
{
   return AtRGBA(AiClamp(c.r, lo, hi),
                 AiClamp(c.g, lo, hi),
                 AiClamp(c.b, lo, hi),
                 AiClamp(c.a, lo, hi));
}

/**
 * Clip negative values
 */
AI_DEVICE inline void  AiColorClipToZero(AtRGB& c)
{
   c.r = AiMax(c.r, 0.0f);
   c.g = AiMax(c.g, 0.0f);
   c.b = AiMax(c.b, 0.0f);
}

/**
 * Check for almost black
 */
AI_DEVICE inline bool AiColorIsSmall(const AtRGB& c, float epsilon = AI_EPSILON)
{
   return std::abs(c.r) < epsilon && std::abs(c.g) < epsilon && std::abs(c.b) < epsilon;
}

/**
 * Absolute value of color
 */
AI_DEVICE inline AtRGB AiColorABS(const AtRGB& c)
{
   return AtRGB(std::abs(c.r),
                std::abs(c.g),
                std::abs(c.b));
}

/**
 * Absolute value of color, RGBA version
 */
AI_DEVICE inline AtRGBA AiColorABS(const AtRGBA& c)
{
   return AtRGBA(std::abs(c.r),
                 std::abs(c.g),
                 std::abs(c.b),
                 std::abs(c.a));
}

/**
 * Max RGB component of color
 */
AI_DEVICE inline constexpr float AiColorMaxRGB(const AtRGB& c)
{
   return AiMax(c.r, c.g, c.b);
}

/**
 * Max RGB component of color, RGBA version (ignores alpha)
 */
AI_DEVICE inline constexpr float AiColorMaxRGB(const AtRGBA& c)
{
   return AiMax(c.r, c.g, c.b);
}

/**
 * Check to see if two colors differ by more than a threhsold
 */
inline bool AiColorThreshold(const AtRGB& c1, const AtRGB& c2, float t)
{
   return std::abs(c1.r - c2.r) >= t || std::abs(c1.g - c2.g) >= t || std::abs(c1.b - c2.b) >= t;
}

/**
 * Convert a RGB color to grey scale (take average of R, G, B)
 */
AI_DEVICE inline constexpr float AiColorToGrey(const AtRGB& c)
{
   return (c.r + c.g + c.b) / 3;
}

/**
 * Convert a RGBA color to grey scale (take average of R, G, B - ignore alpha)
 */
AI_DEVICE inline constexpr float AiColorToGrey(const AtRGBA& rgba)
{
   return (rgba.r + rgba.g + rgba.b) / 3;
}

/**
 * Check to see if an RGB color has any corrupted components (nan or infinite).
 */
AI_API AI_PURE bool AiRGBIsFinite(const AtRGB& rgba);

/**
 * Check to see if an RGBA color has any corrupted components (nan or infinite).
 */
AI_API AI_PURE bool AiRGBAIsFinite(const AtRGBA& rgba);

/**
 * Barycentric interpolation of triangle vertex colors
 */
inline AtRGB AiBerpRGB(float a, float b, const AtRGB& c0, const AtRGB& c1, const AtRGB& c2)
{
   float c = 1 - (a+b);
   return c*c0 + a*c1 + b*c2;
}

AI_API AI_DEVICE AI_PURE AtRGB AiColorHeatMap(const AtRGB* map_colors, const float* map_values, unsigned int map_length, float lookup);

/*\}*/

/** \name Constants
 * \{
 */
#ifdef AI_CPU_COMPILER
static constexpr const AtRGB AI_RGB_BLACK (0.0f, 0.0f, 0.0f);
static constexpr const AtRGB AI_RGB_ZERO  (0.0f, 0.0f, 0.0f);
static constexpr const AtRGB AI_RGB_RED   (1.0f, 0.0f, 0.0f);
static constexpr const AtRGB AI_RGB_GREEN (0.0f, 1.0f, 0.0f);
static constexpr const AtRGB AI_RGB_BLUE  (0.0f, 0.0f, 1.0f);
static constexpr const AtRGB AI_RGB_50GREY(0.5f, 0.5f, 0.5f);
static constexpr const AtRGB AI_RGB_WHITE (1.0f, 1.0f, 1.0f);
#else
__device__ static const AtRGB AI_RGB_BLACK (0.0f, 0.0f, 0.0f);
__device__ static const AtRGB AI_RGB_ZERO  (0.0f, 0.0f, 0.0f);
__device__ static const AtRGB AI_RGB_RED   (1.0f, 0.0f, 0.0f);
__device__ static const AtRGB AI_RGB_GREEN (0.0f, 1.0f, 0.0f);
__device__ static const AtRGB AI_RGB_BLUE  (0.0f, 0.0f, 1.0f);
__device__ static const AtRGB AI_RGB_50GREY(0.5f, 0.5f, 0.5f);
__device__ static const AtRGB AI_RGB_WHITE (1.0f, 1.0f, 1.0f);
#endif

#ifdef AI_CPU_COMPILER
static constexpr const AtRGBA AI_RGBA_ZERO  (0.0f, 0.0f, 0.0f, 0.0f);
static constexpr const AtRGBA AI_RGBA_RED   (1.0f, 0.0f, 0.0f, 1.0f);
static constexpr const AtRGBA AI_RGBA_GREEN (0.0f, 1.0f, 0.0f, 1.0f);
static constexpr const AtRGBA AI_RGBA_BLUE  (0.0f, 0.0f, 1.0f, 1.0f);
static constexpr const AtRGBA AI_RGBA_50GREY(0.5f, 0.5f, 0.5f, 1.0f);
static constexpr const AtRGBA AI_RGBA_WHITE (1.0f, 1.0f, 1.0f, 1.0f);
#else
__device__ static const AtRGBA AI_RGBA_ZERO  (0.0f, 0.0f, 0.0f, 0.0f);
__device__ static const AtRGBA AI_RGBA_RED   (1.0f, 0.0f, 0.0f, 1.0f);
__device__ static const AtRGBA AI_RGBA_GREEN (0.0f, 1.0f, 0.0f, 1.0f);
__device__ static const AtRGBA AI_RGBA_BLUE  (0.0f, 0.0f, 1.0f, 1.0f);
__device__ static const AtRGBA AI_RGBA_50GREY(0.5f, 0.5f, 0.5f, 1.0f);
__device__ static const AtRGBA AI_RGBA_WHITE (1.0f, 1.0f, 1.0f, 1.0f);
#endif

/*\}*/

/*\}*/
