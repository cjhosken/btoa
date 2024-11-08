// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * AtNodeEntry type and methods
 */

#pragma once
#include "ai_params.h"
#include "ai_string.h"

// forward declarations
class  AtRenderSession;
struct AtNode;
struct AtList;
struct AtParamIterator;
struct AtMetaDataIterator;

/** \defgroup ai_node_entry AtNodeEntry API
 *  
 *  \ref AtNodeEntry methods.
 * 
 *  \details
 *  Arnold \ref AtNodeEntry class provides information about the structure of a given node type.
 *  For a discussion of Arnold's object-oriented system of pluggable nodes, please
 *  refer to \ref ai_nodes.
 * \{
 */ 

/** \name Node Types
 * \{
 */
#define AI_NODE_UNDEFINED     0x0000  /**< Undefined type */
#define AI_NODE_OPTIONS       0x0001  /**< Options node (following the "singleton" pattern, there is only one options node) */
#define AI_NODE_CAMERA        0x0002  /**< Camera nodes (\c persp_camera, \c fisheye_camera, etc) */
#define AI_NODE_LIGHT         0x0004  /**< Light source nodes (\c spot_light, etc) */
#define AI_NODE_SHAPE         0x0008  /**< Geometry nodes (\c sphere, \c polymesh, etc) */
#define AI_NODE_SHADER        0x0010  /**< Shader nodes (\c lambert, etc) */
#define AI_NODE_OVERRIDE      0x0020  /**< EXPERIMENTAL: override nodes support "delayed parameter overrides" for \c procedural nodes */
#define AI_NODE_DRIVER        0x0040  /**< Output driver nodes (\c driver_tiff, etc) */
#define AI_NODE_FILTER        0x0080  /**< Pixel sample filter nodes (\c box_filter, etc */
#define AI_NODE_COLOR_MANAGER 0x0800  /**< Color manager nodes (\c Syncolor, OCIO, etc) */
#define AI_NODE_OPERATOR      0x1000  /**< Operator plug-in nodes */
#define AI_NODE_IMAGER        0x2000  /**< Imager nodes (\c imager_tonemap, etc */
#define AI_NODE_ALL           0xFFFF  /**< Bitmask including all node types, used by AiASSWrite() */
/* \}*/

/** \name Derived Node Types
 * \{
 */
#define AI_NODE_SHAPE_PROCEDURAL 0x0100  /**< Procedural shape node */
#define AI_NODE_SHAPE_VOLUME     0x0200  /**< Volume shape node */
#define AI_NODE_SHAPE_IMPLICIT   0x0400  /**< Implicit shape node */
/* \}*/

/**
 * \struct AtNodeEntry
 * 
 * This represents a node type in Arnold. There is a node entry for each
 * installed node, whether built-in or plug-in. The actual contents of this
 * struct are private. 
 */
struct AtNodeEntry;

/**
 * Methods common to all nodes
 */
struct AtCommonMethods
{
   bool (*PluginInitialize)(void**);
   void (*PluginCleanup   )(void*);
   void (*Parameters      )(AtList*, AtNodeEntry*);
   void (*Initialize      )(AtRenderSession*, AtNode*);
   void (*Update          )(AtRenderSession*, AtNode*);
   void (*Finish          )(AtNode*);
};

/**
 * Node methods
 */
struct AtNodeMethods
{
   const AtCommonMethods* cmethods;    /**< common methods    */
   const void*            dmethods;    /**< derived methods   */
};

struct AtMetaDataEntry
{
   AtString     name;
   AtString     param;
   uint8_t      type;
   AtParamValue value;
};

/**
 * \name AtNodeEntry Methods
 * \{
 */
AI_API AI_PURE const AtNodeEntry*  AiNodeEntryLookUp            (const AtString name);
AI_API AI_PURE const char*         AiNodeEntryGetName           (const AtNodeEntry* nentry);
AI_API AI_PURE AtString            AiNodeEntryGetNameAtString   (const AtNodeEntry* nentry);
AI_API AI_PURE int                 AiNodeEntryGetType           (const AtNodeEntry* nentry);
AI_API AI_PURE const char*         AiNodeEntryGetTypeName       (const AtNodeEntry* nentry);
AI_API AI_PURE int                 AiNodeEntryGetDerivedType    (const AtNodeEntry* nentry);
AI_API AI_PURE const char*         AiNodeEntryGetDerivedTypeName(const AtNodeEntry* nentry);
AI_API AI_PURE int                 AiNodeEntryGetOutputType     (const AtNodeEntry* nentry);
AI_API AI_PURE const char*         AiNodeEntryGetFilename       (const AtNodeEntry* nentry);
AI_API AI_PURE const char*         AiNodeEntryGetVersion        (const AtNodeEntry* nentry);
AI_API AI_PURE int                 AiNodeEntryGetCount          (const AtNodeEntry* nentry);
AI_API AI_PURE int                 AiNodeEntryGetNumParams      (const AtNodeEntry* nentry);
AI_API AI_PURE const AtParamEntry* AiNodeEntryGetParameter      (const AtNodeEntry* nentry, int i);
AI_API AI_PURE const AtParamEntry* AiNodeEntryLookUpParameter   (const AtNodeEntry* nentry, const AtString param);
AI_API AI_PURE int                 AiNodeEntryGetNumOutputs     (const AtNodeEntry* nentry);
AI_API AI_PURE const AtParamEntry* AiNodeEntryGetOutput         (const AtNodeEntry* nentry, int i);
AI_API AI_PURE const AtParamEntry* AiNodeEntryLookUpOutput      (const AtNodeEntry* nentry, const AtString param);

#ifdef AI_CPU_COMPILER
// these are slower than the AtString versions
inline AI_DEPRECATED const AtNodeEntry*  AiNodeEntryLookUp(const char* name) { return AiNodeEntryLookUp(AtString(name)); }
inline AI_DEPRECATED const AtParamEntry* AiNodeEntryLookUpParameter(const AtNodeEntry* nentry, const char* param) { return AiNodeEntryLookUpParameter(nentry, AtString(param)); }
#endif

AI_API AtParamIterator*    AiNodeEntryGetParamIterator   (const AtNodeEntry* nentry);
AI_API AtMetaDataIterator* AiNodeEntryGetMetaDataIterator(const AtNodeEntry* nentry, const char* param = NULL);
AI_API void                AiNodeEntryInstall            (int type, uint8_t output_type, const char* name, const char* filename, const AtNodeMethods* methods, const char* version);
AI_API void                AiNodeEntryUninstall          (const char* name);
/* \}*/

/**
 * \name AtParamIterator Methods
 * \{
 */
AI_API void                AiParamIteratorDestroy(AtParamIterator* iter);
AI_API const AtParamEntry* AiParamIteratorGetNext(AtParamIterator* iter);
AI_API bool                AiParamIteratorFinished(const AtParamIterator* iter);
/* \}*/

/**
 * \name AtMetaDataIterator Methods
 * \{
 */
AI_API void                   AiMetaDataIteratorDestroy(AtMetaDataIterator* iter);
AI_API const AtMetaDataEntry* AiMetaDataIteratorGetNext(AtMetaDataIterator* iter);
AI_API bool                   AiMetaDataIteratorFinished(const AtMetaDataIterator* iter);
/* \}*/

/*\}*/
