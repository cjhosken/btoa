// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Closure type and utilities
 */

#pragma once
#include "ai_api.h"
#include "ai_color.h"

#include <stdint.h>

/** \defgroup ai_closure AtClosure API
 * 
 * \ref AtClosure type and related utilities.
 * 
 * \{
 */

struct AtBSDF;
struct AtClosureBase;

/**
 * Shader closure types
 */
enum AtClosureType {
   AI_CLOSURE_NONE = 0,
   AI_CLOSURE_BSDF,
   AI_CLOSURE_BSSRDF,
   AI_CLOSURE_EMISSION,
   AI_CLOSURE_DEBUG,
   AI_CLOSURE_TRANSPARENT,
   AI_CLOSURE_MATTE,
   AI_CLOSURE_BACKGROUND,
   AI_CLOSURE_VOLUME_ABSORPTION,
   AI_CLOSURE_VOLUME_SCATTERING,
   AI_CLOSURE_VOLUME_EMISSION,
   AI_CLOSURE_VOLUME_MATTE,
   AI_CLOSURE_VOLUME_ATMOSPHERE,
   AI_CLOSURE_DIELECTRIC
};

AI_API AI_DEVICE AtClosureType  AiClosureType(AtClosureBase* closure);
AI_API AI_DEVICE AtRGB          AiClosureWeight(AtClosureBase* closure);
AI_API AI_DEVICE void           AiClosureSetWeight(AtClosureBase* closure, const AtRGB& weight);
AI_API           AtString       AiClosureLabel(AtClosureBase* closure);
AI_API           void           AiClosureSetLabel(AtClosureBase* closure, const AtString label);
AI_API AI_DEVICE AtClosureBase* AiClosureNext(AtClosureBase* closure);
AI_API AI_DEVICE void           AiClosureSetExtraDepth(AtClosureBase* closure, uint8_t extra_depth);
AI_API AI_DEVICE void           AiClosureSetExtraSamples(AtClosureBase* closure, uint8_t extra_samples);

/*
 * Closure
 */
struct AtClosure
{
   /** Get closure type */
   AI_DEVICE AtClosureType type() { return AiClosureType(data); }

   /** Get closure weight */
   AI_DEVICE AtRGB weight() { return AiClosureWeight(data); }

   /** Get next closure, if part of an \c AtClosureList */
   AI_DEVICE AtClosure next() { return AiClosureNext(data); };

   AI_DEVICE AtClosure(AtClosureBase* data_) : data(data_) {}
   AI_DEVICE operator AtClosureBase*() const { return data; }

private:
   AtClosureBase* data;
};

/*
 * Closure List
 */
AI_API AI_DEVICE AtClosureBase* AiClosureListAdd(AtClosureBase* listA, AtClosureBase* listB);
AI_API AI_DEVICE AtClosureBase* AiClosureListWeight(AtClosureBase* list, const AtRGB& weight);

struct AtClosureList
{
   /** Create empty closure list */
   AI_DEVICE AtClosureList()
   : data(NULL)
   {
   }

   /** Create closure list from single closure */
   AI_DEVICE AtClosureList(AtClosure data_)
   : data(data_)
   {
   }

   /** Create closure list from single BSDF */
   AI_DEVICE AtClosureList(AtBSDF* data_)
   : data((AtClosureBase*)data_)
   {
   }

   /** First element in the list */
   AI_DEVICE AtClosure front() const
   {
      return data;
   }

   /** Add closure to closure list */
   AI_DEVICE inline void add(AtClosure closure)
   {
      data = AiClosureListAdd(data, (AtClosureBase*)closure);
   }

   /** Add BSDF to closure list */
   AI_DEVICE inline void add(AtBSDF* bsdf)
   {
      data = AiClosureListAdd(data, (AtClosureBase*)bsdf);
   }

   /** Add closure list to closure list */
   AI_DEVICE inline void add(AtClosureList list)
   {
      data = AiClosureListAdd(data, list.data);
   }

   /** Multiply weight of all closures in the list */
   AI_DEVICE inline void operator*=(const AtRGB& weight)
   {
      data = AiClosureListWeight(data, weight);
   }

   /** Multiply weight of all closures in the list */
   AI_DEVICE inline void operator*=(float weight)
   {
      data = AiClosureListWeight(data, AtRGB(weight));
   }

   /** Test if list is empty */
   AI_DEVICE inline bool empty() const
   {
      return data == NULL;
   }

private:
   AtClosureBase* data;
};

/*\}*/
