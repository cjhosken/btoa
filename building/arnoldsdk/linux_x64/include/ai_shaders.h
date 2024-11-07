// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for writing shader nodes
 */

#pragma once
#include "ai_nodes.h"
#include "ai_api.h"

// forward declarations
struct AtNode;
struct AtShaderGlobals;


/** \defgroup ai_shaders  Shader Nodes
 * 
 * Implementation of custom shader nodes.
 * 
 * \{
 */

/** Shader Node methods structure */
struct  AtShaderNodeMethods {
   void  (*Evaluate)(AtNode*, AtShaderGlobals*);
};

/** Shader Node methods exporter */
#define AI_SHADER_NODE_EXPORT_METHODS(tag)      \
AI_INSTANCE_COMMON_METHODS                      \
shader_evaluate;                                \
static AtShaderNodeMethods ai_shader_mtds = {   \
   Evaluate                                     \
};                                              \
static AtNodeMethods ai_node_mtds = {           \
   &ai_common_mtds,                             \
   &ai_shader_mtds                              \
};                                              \
const AtNodeMethods* tag = &ai_node_mtds;

/**
 * \name Node Method Declarations
 * \{
 */

/** Evaluate Shader method declaration */
#define shader_evaluate \
static void Evaluate(AtNode* node, AtShaderGlobals* sg)

/**
 * \name Node Methods
 * \{
 */

AI_API void AiShaderEvaluate(AtNode* node, AtShaderGlobals* sg);

/* \}*/

/*\}*/
