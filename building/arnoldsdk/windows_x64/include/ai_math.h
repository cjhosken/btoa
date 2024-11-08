// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Math operations
 */

#pragma once
#include "ai_api.h"
#include "ai_constants.h"
#include <cmath>
#include <cstdlib> // for int abs(int)
#include <cstring> // for memcpy

/** \defgroup ai_math Math Functions
 *
 * Math and comparison functions tuned for Arnold.
 *
 * \{
 */

/**
 * Minimum of 'a' and 'b' 
 */
template <typename T>
AI_DEVICE inline constexpr T AiMin(T a, T b)
{
#ifdef AI_CPU_COMPILER
   return (a < b) ? a : b;
#else
   return min(a,b);
#endif
}

/**
 * Maximum of 'a' and 'b'
 */
template <typename T>
AI_DEVICE inline constexpr T AiMax(T a, T b)
{
#ifdef AI_CPU_COMPILER
   return (a > b) ? a : b;
#else
   return max(a,b);
#endif
}

/**
 * Minimum of three values: a, b, c
 */
template <typename T>
AI_DEVICE inline constexpr T AiMin(T a, T b, T c)
{
   return AiMin(AiMin(a, b), c);
}

/**
 * Maximum of three values: a, b, c
 */
template <typename T>
AI_DEVICE inline constexpr T AiMax(T a, T b, T c)
{
   return AiMax(AiMax(a, b), c);
}

/**
 * Minimum of four values: a, b, c, d
 */
template <typename T>
AI_DEVICE inline constexpr T AiMin(T a, T b, T c, T d)
{
   return AiMin(AiMin(a, b), AiMin(c, d));
}

/**
 * Maximum of four values: a, b, c, d
 */
template <typename T>
AI_DEVICE inline constexpr T AiMax(T a, T b, T c, T d)
{
   return AiMax(AiMax(a, b), AiMax(c, d));
}

/**
 * Square of 'a'
 */
template <typename T>
AI_DEVICE inline constexpr T AiSqr(T a)
{
   return (a * a);
}

/**
 * Clamp the input to the specified range 
 */
template <typename T>
AI_DEVICE inline constexpr T AiClamp(T v, T lo, T hi)
{
   return AiMax(lo, AiMin(v, hi));
}

/**
 * Safe arc cosine of 'x' (acos() returns NaN if x<-1 or x>1)
 */
template <typename T>
AI_DEVICE inline constexpr T AiSafeAcos(T x)
{
   return (x >= 1) ? 0 : ((x <= -1) ? static_cast<T>(AI_PI) : std::acos(x));
}

/**
 * Linear interpolation between 'a' and 'b' using 't' (0<=t<=1)
 */
template <typename T1, typename T2>
AI_DEVICE inline constexpr T1 AiLerp(T2 t, T1 a, T1 b)
{
   return ((T2(1) - t) * a) + (b * t);
}

/**
 * Hermite interpolation between 0 and 1 using 't' (0<=t<=1)
 */
template <typename T>
AI_DEVICE inline constexpr T AiHerp01(T t)
{
   return t * t * ((T) 3 - (T) 2 * t);
}

/**
 * Hermite interpolation between 'a' and 'b' using 't' (0<=t<=1)
 */
template <typename T1, typename T2>
AI_DEVICE inline constexpr T1 AiHerp(T2 t, T1 a, T1 b)
{
   return AiLerp(AiHerp01(t), a, b);
}

/**
 * Bilinear interpolation between four float values using 's' and 't' (0<=st<=1)
 */
template <typename T1, typename T2>
AI_DEVICE inline T1 AiBiLerp(T2 s, T2 t, T1 c00, T1 c10, T1 c01, T1 c11)
{
   T1 c0x = AiLerp(t, c00, c01);
   T1 c1x = AiLerp(t, c10, c11);
   return AiLerp(s, c0x, c1x);
}

/**
 * Bias function
 */
template <typename T>
AI_DEVICE inline constexpr T AiBias(T a, T b)
{
   return (a > 0) ? ((b == (T) 0.5) ? a : std::pow(a, (std::log(b) * (T)-1.442695041))) : 0;
}

/**
 * Gain function
 */
template <typename T>
AI_DEVICE inline constexpr T AiGain(T a, T g)
{
   return (g == (T) 0.5) ? a : ((a < (T) 0.5) ? (AiBias(a + a, (T) 1 - g) * (T) 0.5) : ((T) 1 - AiBias((T) 2 - a - a, (T) 1 - g) * (T) 0.5));
}

/**
 * Step function
 */
template <typename T>
AI_DEVICE inline constexpr T AiStep(T x, T e)
{
   return (x < e) ? (T) 0 : (T) 1;
}

/**
 * Filtered-step function
 */
template <typename T>
AI_DEVICE inline constexpr T AiFilterStep(T x, T e, T w)
{
   return AiClamp((x + w * (T) 0.5 - e) / w, (T) 0, (T) 1);
}
#ifdef AI_GPU_COMPILER
AI_DEVICE inline float AiFilterStep(float x, float e, float w)
{
   return __saturatef((x + w * 0.5f - e) / w);
}
#endif


/**
 * Linearly interpolated step from 'lo' to 'hi'.
 * Returns x where (0 <= x <= 1). Similar to AiFilterStep()
 * but slightly different mode of calling
 */
template <typename T>
AI_DEVICE inline constexpr T AiLinearStep(T lo, T hi, T t)
{
   return AiClamp((t - lo) / (hi - lo), (T) 0, (T) 1);
}
#ifdef AI_GPU_COMPILER
AI_DEVICE inline float AiLinearStep(float lo, float hi, float t)
{
   return __saturatef((t - lo) / (hi - lo));
}
#endif

/**
 * RenderMan's smoothstep() function.
 * Returns 0 if (t < e0) or 1 if (t > e1) or
 * a hermitian interpolation for (e0 < t < e1)
 */
template <typename T>
AI_DEVICE inline constexpr T AiSmoothStep(T e0, T e1, T t)
{
   return AiHerp01(AiClamp((t - e0) / (e1 - e0), (T) 0, (T) 1));
}
#ifdef AI_GPU_COMPILER
AI_DEVICE inline float AiSmoothStep(float e0, float e1, float t)
{
   return AiHerp01(__saturatef((t - e0) / (e1 - e0)));
}
#endif

/**
 * This function can be used to go between different interpretations of the
 * same bits.  A common use case is to operate on the bits of a float as if
 * they were an int. This should be a safe way to re-interpret bits.  The
 * alternative method of casting the address causes pointer aliasing and the
 * results are undefined by the language. Some compilers, such as gcc, will
 * warn about this when using -Wall and the resulting code can result in hard
 * to debug bugs.
 */
template <typename OUT_T, typename IN_T>
AI_DEVICE inline OUT_T reinterpret_type(const IN_T in)
{
   OUT_T out;
   std::memcpy(&out, &in, sizeof(OUT_T));
   return out;
}

AI_API AI_DEVICE AI_CONST bool AiIsFinite(float x);
AI_API AI_CONST float AiFastExp(float x);
AI_API AI_DEVICE AI_CONST float AiFastPow(float x, float y);

/*\}*/
