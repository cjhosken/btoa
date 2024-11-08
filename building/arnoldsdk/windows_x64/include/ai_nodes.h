// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * AtNode struct and methods
 */

#pragma once
#include "ai_node_entry.h"
#include "ai_params.h"
#include "ai_api.h"
#include "ai_string.h"

// forward declarations
class  AtUniverse;
class  AtRenderSession;
struct AtList;
struct AtNodeEntry;
struct AtUserParamEntry;
struct AtUserParamIterator;

/** \defgroup ai_nodes AtNode API
 *
 *  Creation, manipulation and operation with Arnold nodes.
 * 
 *  \details
 *  Arnold has a pluggable node-management system for the standard primitives
 *  such as lights, cameras, geometry, shaders, filters, drivers, etc.  Each
 *  node type has a set of associated methods (member functions) and
 *  parameters.   Like C++'s objects, Arnold's node system allows new nodes to
 *  inherit both parameters and methods from the "parent" node.  For example,
 *  all nodes have a "name" parameter and a "node_initialize{}" method (among
 *  others) because they are declared in the base node from which all nodes
 *  inherit.
 *
 *  In addition to these standard methods and parameters, derived nodes may
 *  have their own type-specific parameters and methods.  For example, all
 *  shaders have a "shader_evaluate{}" method and all driver nodes have a
 *  "driver_write_bucket{}" method (among others).  User-derived nodes may have their
 *  own new parameters but are not permitted to add new methods.
 *
 *  Optional "node_plugin_initialize{}" and "node_plugin_cleanup{}" methods
 *  can be used for initializing a plugin, if there is some initialization
 *  or data to be shared between nodes of the same type. These methods are only
 *  called if a node of this type is created. \ref AiNodeGetPluginData() can
 *  be used to retrieve the plugin data.
 *
 *  Two of the important data-structures in this object-oriented-like system are:
 *  \li  AtNodeEntry -- this contains the "description" of a particular node type
 *                      ("polymesh", "persp_camera", etc.)
 *  \li  AtNode -- this contains the "instantiation" of a particular node type
 * \{
 */

/**
 * \struct AtNode
 * 
 * This represents a node in Arnold.
 */
struct AtNode;

/**
 * \name Node Method Declarations
 * \{
 */

/** Parameter declaration method */
#define node_parameters \
static void Parameters(AtList* params, AtNodeEntry* nentry)

/** Node plugin initialize method (optional) */
#define node_plugin_initialize                               \
static bool PluginInitialize(void** plugin_data);            \
AI_OPTIONAL_METHOD_INSTALL(ai_common_mtds, PluginInitialize) \
static bool PluginInitialize(void** plugin_data)

/** Node plugin cleanup method (optional) */
#define node_plugin_cleanup                               \
static void PluginCleanup(void* plugin_data);             \
AI_OPTIONAL_METHOD_INSTALL(ai_common_mtds, PluginCleanup) \
static void PluginCleanup(void* plugin_data)

/** Node initialization method
 * 
 * This function can be used to allocate and/or initialize any data required
 * by the node during rendering. Those allocations should be released in
 * \ref node_finish.
 * 
 * This function is called once when the scene is initialized, and will only be
 * called again if the node is interactively reloaded.
 * 
 * An example could be allocating space for matrices, lookup tables or any
 * kind of cached values that only needs to happen once.
 * 
 * \param render_session  render session where this node will be used for rendering
 * \param node            pointer to the node
 */
#define node_initialize \
static void Initialize(AtRenderSession* render_session, AtNode* node)

/** Node update method
 * 
 * Unlike the \ref node_initialize function, which usually is called just once,
 * this will be called every time a render pass is executed. This is where data
 * derived from modifiable node parameters should be precomputed for later use
 * during rendering. Computation that only needs to happen once should be moved
 * to \ref node_initialization so that there is less overhead during IPR.
 * 
 * \param render_session  render session where this node will be used for rendering
 * \param node            pointer to the node
 */
#define node_update \
static void Update(AtRenderSession* render_session, AtNode* node)

/** Node de-initialization method
 * 
 * This function is used to revert the actions performed in \ref node_initialize,
 * such as releasing memory allocated by node_init and bringing the node back to its
 * initial state.
 * 
 * This is called when a node is destroyed, and when it is reverted to its
 * initial value, which could happen when interactively modifying a value for
 * a parameter that has the `_triggers_reinitialize` metadata set.
 * 
 * \param node  pointer to the node
 */
#define node_finish \
static void Finish(AtNode* node)

/** Node loading method (for plugin nodes in dynamic libraries) */
#define node_loader \
AI_EXPORT_LIB bool NodeLoader(int i, AtNodeLib* node)
/* \}*/

/** Exporter for common methods */
#define AI_INSTANCE_COMMON_METHODS         \
node_parameters;                           \
node_initialize;                           \
node_update;                               \
node_finish;                               \
static AtCommonMethods ai_common_mtds = {  \
   NULL,                                   \
   NULL,                                   \
   Parameters,                             \
   Initialize,                             \
   Update,                                 \
   Finish                                  \
};

/** Exporter for common shape methods */
#define AI_INSTANCE_COMMON_SHAPE_METHODS   \
node_parameters;                           \
static AtCommonMethods ai_common_mtds = {  \
   NULL,                                   \
   NULL,                                   \
   Parameters,                             \
   NULL,                                   \
   NULL,                                   \
   NULL                                    \
};

/**
 * \name AtNode Methods
 * \{
 */
AI_API               AtNode*                 AiNode                    (AtUniverse* universe, const AtString nentry_name, const AtString name = AtString(), const AtNode* parent = NULL);
AI_API AI_PURE       AtNode*                 AiNodeLookUpByName        (const AtUniverse* universe, const AtString name, const AtNode* parent = NULL);
AI_API               bool                    AiNodeDeclare             (AtNode* node, const AtString param, const char* declaration);
AI_API AI_PURE       const AtUserParamEntry* AiNodeLookUpUserParameter (const AtNode* node, const AtString param);
AI_API AI_PURE       bool                    AiNodeIs                  (const AtNode* node, AtString str);
AI_API               void                    AiNodeReset               (AtNode* node);
AI_API               void                    AiNodeResetParameter      (AtNode* node, const char* param);
AI_API               AtNode*                 AiNodeClone               (const AtNode* node, const AtString new_name = AtString(), const AtNode* parent = NULL);
AI_API               bool                    AiNodeDestroy             (AtNode* node);
AI_API               void                    AiNodeReplace             (AtNode* old_node, AtNode* new_node, bool remove);
AI_API               bool                    AiNodeLink                (AtNode* src,  const char* input, AtNode* target);
AI_API               bool                    AiNodeLinkOutput          (AtNode* src,  const char* output, AtNode* target, const char* input);
AI_API               bool                    AiNodeUnlink              (AtNode* node, const char* input);
AI_API AI_PURE       bool                    AiNodeIsLinked            (const AtNode* node, const char* input);
AI_API               AtNode*                 AiNodeGetLink             (const AtNode* node, const char* input, int* comp = NULL);
AI_API               AtNode*                 AiNodeGetLinkOutput       (const AtNode* node, const char* input, int& output_param, int& output_comp);
AI_API AI_PURE       const char*             AiNodeGetName             (const AtNode* node);
AI_API AI_PURE       const AtNodeEntry*      AiNodeGetNodeEntry        (const AtNode* node);
AI_API AI_PURE       void*                   AiNodeGetLocalData        (const AtNode* node);
AI_API               void                    AiNodeSetLocalData        (AtNode* node, void* data);
AI_API AI_PURE       void*                   AiNodeGetPluginData       (const AtNode* node);
AI_API               void                    AiNodeSetDisabled         (AtNode* node, bool disabled);
AI_API AI_PURE       bool                    AiNodeIsDisabled          (const AtNode* node);
AI_API AI_PURE       AtNode*                 AiNodeGetParent           (const AtNode* node);
AI_API AI_PURE       AtUniverse*             AiNodeGetUniverse         (const AtNode* node);
AI_API               AtUserParamIterator*    AiNodeGetUserParamIterator(const AtNode* node);
AI_API               AtNode*                 AiNodeGetProcessedGeometry(AtNode* source_node, AtUniverse* dest_universe);
AI_API               void                    AiNodeAddDependencyParam  (AtNode* consumer, const AtNode* producer, const AtString param);
AI_API AI_DEPRECATED void                    AiNodeAddDependency       (AtNode* consumer, const AtNode* producer);
AI_API               void                    AiNodeClearDependency     (AtNode* consumer, const AtNode* producer);

inline void AiNodeAddDependency(AtNode* consumer, const AtNode* producer, const AtString param)
{
   AiNodeAddDependencyParam(consumer, producer, param);
}

#ifdef AI_CPU_COMPILER

// these are slower than the AtString versions
inline AI_DEPRECATED AtNode*                 AiNode                    (AtUniverse* universe, const char* nentry_name, const char* name = "", const AtNode* parent = NULL) { return AiNode(universe, AtString(nentry_name), AtString(name), parent); }
inline AI_DEPRECATED AtNode*                 AiNodeLookUpByName        (const AtUniverse* universe, const char* name, const AtNode* parent = NULL) { return AiNodeLookUpByName(universe, AtString(name), parent); }
inline AI_DEPRECATED bool                    AiNodeDeclare             (AtNode* node, const char* param, const char* declaration) { return AiNodeDeclare(node, AtString(param), declaration); }
inline AI_DEPRECATED const AtUserParamEntry* AiNodeLookUpUserParameter (const AtNode* node, const char* param) { return AiNodeLookUpUserParameter(node, AtString(param)); }
#endif
/* \}*/

/**
 * \name AtUserParamIterator Methods
 * \{
 */
AI_API void                    AiUserParamIteratorDestroy(AtUserParamIterator* iter);
AI_API const AtUserParamEntry* AiUserParamIteratorGetNext(AtUserParamIterator* iter);
AI_API bool                    AiUserParamIteratorFinished(const AtUserParamIterator* iter);
/* \}*/

/**
 * \name Parameter Writers
 * \{
 */
AI_API               void AiNodeSetByte  (AtNode* node, const AtString param, uint8_t val); 
AI_API               void AiNodeSetInt   (AtNode* node, const AtString param, int val); 
AI_API               void AiNodeSetUInt  (AtNode* node, const AtString param, unsigned int val); 
AI_API               void AiNodeSetBool  (AtNode* node, const AtString param, bool val); 
AI_API               void AiNodeSetFlt   (AtNode* node, const AtString param, float val); 
AI_API               void AiNodeSetPtr   (AtNode* node, const AtString param, void* val); 
AI_API               void AiNodeSetArray (AtNode* node, const AtString param, AtArray* val); 
AI_API               void AiNodeSetMatrix(AtNode* node, const AtString param, AtMatrix val); 
AI_API               void AiNodeSetStr   (AtNode* node, const AtString param, const AtString str);
AI_API               void AiNodeSetRGB   (AtNode* node, const AtString param, float r, float g, float b);
AI_API               void AiNodeSetRGBA  (AtNode* node, const AtString param, float r, float g, float b, float a);
AI_API               void AiNodeSetVec   (AtNode* node, const AtString param, float x, float y, float z);
AI_API               void AiNodeSetVec2  (AtNode* node, const AtString param, float x, float y);

#ifdef AI_CPU_COMPILER
// these are slower than the AtString versions
inline AI_DEPRECATED void AiNodeSetByte  (AtNode* node, const char* param, uint8_t val)                        { AiNodeSetByte  (node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetInt   (AtNode* node, const char* param, int val)                            { AiNodeSetInt   (node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetUInt  (AtNode* node, const char* param, unsigned int val)                   { AiNodeSetUInt  (node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetBool  (AtNode* node, const char* param, bool val)                           { AiNodeSetBool  (node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetFlt   (AtNode* node, const char* param, float val)                          { AiNodeSetFlt   (node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetPtr   (AtNode* node, const char* param, void* val)                          { AiNodeSetPtr   (node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetArray (AtNode* node, const char* param, AtArray* val)                       { AiNodeSetArray (node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetMatrix(AtNode* node, const char* param, AtMatrix val)                       { AiNodeSetMatrix(node, AtString(param), val); }
inline AI_DEPRECATED void AiNodeSetStr   (AtNode* node, const char* param, const char* str)                    { AiNodeSetStr   (node, AtString(param), AtString(str)); }
inline AI_DEPRECATED void AiNodeSetRGB   (AtNode* node, const char* param, float r, float g, float b)          { AiNodeSetRGB   (node, AtString(param), r, g, b); }
inline AI_DEPRECATED void AiNodeSetRGBA  (AtNode* node, const char* param, float r, float g, float b, float a) { AiNodeSetRGBA  (node, AtString(param), r, g, b, a); }
inline AI_DEPRECATED void AiNodeSetVec   (AtNode* node, const char* param, float x, float y, float z)          { AiNodeSetVec   (node, AtString(param), x, y, z); }
inline AI_DEPRECATED void AiNodeSetVec2  (AtNode* node, const char* param, float x, float y)                   { AiNodeSetVec2  (node, AtString(param), x, y); }
#endif

AI_API void AiNodeSetAttributes(AtNode *node, const char* attributes);

/* \}*/

/**
 * \name Parameter Readers
 * \{
 */
AI_API               uint8_t      AiNodeGetByte  (const AtNode* node, const AtString param);
AI_API               int          AiNodeGetInt   (const AtNode* node, const AtString param);
AI_API               unsigned int AiNodeGetUInt  (const AtNode* node, const AtString param);
AI_API               bool         AiNodeGetBool  (const AtNode* node, const AtString param);
AI_API               float        AiNodeGetFlt   (const AtNode* node, const AtString param);
AI_API               AtRGB        AiNodeGetRGB   (const AtNode* node, const AtString param);
AI_API               AtRGBA       AiNodeGetRGBA  (const AtNode* node, const AtString param);
AI_API               AtVector     AiNodeGetVec   (const AtNode* node, const AtString param);
AI_API               AtVector2    AiNodeGetVec2  (const AtNode* node, const AtString param);
AI_API               AtString     AiNodeGetStr   (const AtNode* node, const AtString param);
AI_API               void*        AiNodeGetPtr   (const AtNode* node, const AtString param);
AI_API               AtArray*     AiNodeGetArray (const AtNode* node, const AtString param);
AI_API               AtMatrix     AiNodeGetMatrix(const AtNode* node, const AtString param);

#ifdef AI_CPU_COMPILER
// these are slower than the AtString versions
inline AI_DEPRECATED uint8_t      AiNodeGetByte  (const AtNode* node, const char* param) { return AiNodeGetByte  (node, AtString(param)); }
inline AI_DEPRECATED int          AiNodeGetInt   (const AtNode* node, const char* param) { return AiNodeGetInt   (node, AtString(param)); }
inline AI_DEPRECATED unsigned int AiNodeGetUInt  (const AtNode* node, const char* param) { return AiNodeGetUInt  (node, AtString(param)); }
inline AI_DEPRECATED bool         AiNodeGetBool  (const AtNode* node, const char* param) { return AiNodeGetBool  (node, AtString(param)); }
inline AI_DEPRECATED float        AiNodeGetFlt   (const AtNode* node, const char* param) { return AiNodeGetFlt   (node, AtString(param)); }
inline AI_DEPRECATED AtRGB        AiNodeGetRGB   (const AtNode* node, const char* param) { return AiNodeGetRGB   (node, AtString(param)); }
inline AI_DEPRECATED AtRGBA       AiNodeGetRGBA  (const AtNode* node, const char* param) { return AiNodeGetRGBA  (node, AtString(param)); }
inline AI_DEPRECATED AtVector     AiNodeGetVec   (const AtNode* node, const char* param) { return AiNodeGetVec   (node, AtString(param)); }
inline AI_DEPRECATED AtVector2    AiNodeGetVec2  (const AtNode* node, const char* param) { return AiNodeGetVec2  (node, AtString(param)); }
inline AI_DEPRECATED AtString     AiNodeGetStr   (const AtNode* node, const char* param) { return AiNodeGetStr   (node, AtString(param)); }
inline AI_DEPRECATED void*        AiNodeGetPtr   (const AtNode* node, const char* param) { return AiNodeGetPtr   (node, AtString(param)); }
inline AI_DEPRECATED AtArray*     AiNodeGetArray (const AtNode* node, const char* param) { return AiNodeGetArray (node, AtString(param)); }
inline AI_DEPRECATED AtMatrix     AiNodeGetMatrix(const AtNode* node, const char* param) { return AiNodeGetMatrix(node, AtString(param)); }

/* \}*/

/*\}*/

#define AiNodeDeclareGPULocalData(type) namespace {}
#endif
