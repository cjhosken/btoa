// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for writing color managers
 */

#pragma once
#include "ai_api.h"
#include "ai_bbox.h"
#include "ai_nodes.h"

#include <stddef.h>

struct AtChannelLayout {
   AtChannelLayout(uint8_t ct, uint8_t t, size_t x, size_t y) : channel_type(ct), type(t), x_stride(x), y_stride(y) { }
   uint8_t channel_type;
   uint8_t type;
   size_t x_stride;
   size_t y_stride;
};

/** \defgroup ai_color_managers Color Manager Nodes
 *
 * Implementation of pluggable color manager nodes.
 *
 * \{
 */

/** Color Manager Node methods structure */
struct AtColorManagerNodeMethods {
   bool      (*ColorManagerTransform)(AtNode*, AtString, bool, bool, const AtBBox2*,
                                      void*, const AtChannelLayout*, void*, const AtChannelLayout*);
   void      (*ColorManagerGetDefaults)(AtNode*, AtString&, AtString&);
   bool      (*ColorManagerGetChromaticities)(AtNode*, AtString, float*);
   void      (*ColorManagerGetCustomAttributes)(AtNode*, AtString, int&, const char**);
   int       (*ColorManagerGetNumColorSpaces)(AtNode*, AtString);
   AtString  (*ColorManagerGetColorSpaceNameByIndex)(AtNode*, int i, AtString);
   int       (*ColorManagerGetNumFamilies)(AtNode*);
   AtString  (*ColorManagerGetFamilyNameByIndex)(AtNode*, int);
   bool      (*ColorManagerColorSpaceIsLinear)(AtNode*, AtString);
};

/** Color manager node methods exporter */
#define AI_COLOR_MANAGER_NODE_EXPORT_METHODS(tag)               \
AI_INSTANCE_COMMON_METHODS                                      \
color_manager_transform;                                        \
color_manager_get_defaults;                                     \
color_manager_get_chromaticities;                               \
color_manager_get_custom_attributes;                            \
color_manager_get_num_color_spaces;                             \
color_manager_get_color_space_name_by_index;                    \
static AtColorManagerNodeMethods ai_color_manager_mtds = {      \
   ColorManagerTransform,                                       \
   ColorManagerGetDefaults,                                     \
   ColorManagerGetChromaticities,                               \
   ColorManagerGetCustomAttributes,                             \
   ColorManagerGetNumColorSpaces,                               \
   ColorManagerGetColorSpaceNameByIndex,                        \
   NULL,                                                        \
   NULL,                                                        \
   NULL,                                                        \
};                                                              \
static AtNodeMethods ai_node_mtds = {                           \
   &ai_common_mtds,                                             \
   &ai_color_manager_mtds                                       \
};                                                              \
const AtNodeMethods *tag = &ai_node_mtds;

/**
 * \name Node Method Declarations
 * \{
 */

/** Color Manager's color_manager_transform method declaration
 *
 *  Convert the specified count of RGB colors using the named
 *  color space for output or input.
 *
 *  \return true if the color manager was able to perform the
 *          operation
 *
 */
#define color_manager_transform                                                    \
static bool ColorManagerTransform(AtNode* node, AtString color_space,              \
                                  bool is_output, bool dither,                     \
                                  const AtBBox2* roi,                              \
                                  void* src, const AtChannelLayout* src_layout,    \
                                  void* dst, const AtChannelLayout* dst_layout)

/** Color Manager's color_manager_get_defaults method declaration
 *
 *  Optionally specify color spaces for 8 bit images (typically sRGB)
 *  and for the default linear color space
 */
#define color_manager_get_defaults                                                 \
static void ColorManagerGetDefaults(AtNode* node, AtString &sRGB, AtString &linear)

/** Color Manager's color_manager_get_chromaticities method declaration
 *
 *  \return true if the color space is linear
 */
#define color_manager_get_chromaticities                                           \
static bool ColorManagerGetChromaticities(AtNode* node, AtString space, float *chromaticities)

/** Color Manager's color_manager_get_custom_attributes method declaration
 */
#define color_manager_get_custom_attributes                                        \
static void ColorManagerGetCustomAttributes(AtNode* node, AtString space, int &num, const char **attributes)

/** Color Manager's color_manager_get_num_color_spaces method declaration
 *
 *  \return number of color spaces available (for a given "family" if specified)
 */
#define color_manager_get_num_color_spaces                                         \
static int ColorManagerGetNumColorSpaces(AtNode *node, AtString family)

/** Color Manager's color_manager_get_color_space_name_by_index method declaration
 *
 *  \return name of color space at the given index (for a given "family" if specified)
 */
#define color_manager_get_color_space_name_by_index                                \
static AtString ColorManagerGetColorSpaceNameByIndex(AtNode *node, int i, AtString family)

/** Color Manager's color_manager_get_num_families method declaration
 *
 *  \return number of available color space families
 */
#define color_manager_get_num_families                                        \
static int ColorManagerGetNumFamilies(AtNode *node);                          \
AI_OPTIONAL_METHOD_INSTALL(ai_color_manager_mtds, ColorManagerGetNumFamilies) \
static int ColorManagerGetNumFamilies(AtNode *node)

/** Color Manager's color_manager_get_family_name_by_index method declaration
 *
 *  \return name of color space family at the given index
 */
#define color_manager_get_family_name_by_index                                      \
static AtString ColorManagerGetFamilyNameByIndex(AtNode *node, int i);              \
AI_OPTIONAL_METHOD_INSTALL(ai_color_manager_mtds, ColorManagerGetFamilyNameByIndex) \
static AtString ColorManagerGetFamilyNameByIndex(AtNode *node, int i)

/** Color Manager's color_manager_color_space_is_linear method declaration
 *
 *  \return true if the color space is linear
 */
#define color_manager_color_space_is_linear                                       \
static bool ColorManagerColorSpaceIsLinear(AtNode *node, AtString cs);            \
AI_OPTIONAL_METHOD_INSTALL(ai_color_manager_mtds, ColorManagerColorSpaceIsLinear) \
static bool ColorManagerColorSpaceIsLinear(AtNode *node, AtString cs)



AI_API bool AiColorManagerTransform(AtNode* node, AtString name,
                                    bool is_output = true, bool dither = false,
                                    const AtBBox2* roi = NULL,
                                    void* src = NULL, const AtChannelLayout* src_layout = NULL,
                                    void* dst = NULL, const AtChannelLayout* dst_layout = NULL);
AI_API void AiColorManagerGetDefaults(AtNode* node, AtString &sRGB, AtString &linear);
AI_API bool AiColorManagerGetChromaticities(AtNode* node, AtString space, float *chromaticities);
AI_API void AiColorManagerGetCustomAttributes(AtNode* node, AtString space, int &num, const char **attributes);
AI_API int AiColorManagerGetNumColorSpaces(AtNode *node, AtString family = AtString());
AI_API AtString AiColorManagerGetColorSpaceNameByIndex(AtNode *node, int i, AtString family = AtString());
AI_API int AiColorManagerGetNumFamilies(AtNode *node);
AI_API AtString AiColorManagerGetFamilyNameByIndex(AtNode *node, int i);
AI_API bool AiColorManagerColorSpaceIsLinear(AtNode *node, AtString cs);

