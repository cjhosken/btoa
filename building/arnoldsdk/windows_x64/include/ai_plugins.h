// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * Runtime loading of plugin nodes
 */

#pragma once
#include "ai_api.h"
#include "ai_version.h"
#include <stdint.h> // uint32_t etc

#ifdef _WIN32
#define AI_DLL_EXPORT __declspec(dllexport)
#else
#define AI_DLL_EXPORT __attribute__ ((visibility("default")))
#endif

/** \defgroup ai_plugins Plug-in Loading API 
 * 
 * Loading of external dynamically linked plugins into Arnold.
 * 
 * \{                                                                              
 */       

/**
 * Used by dynamically-linked nodes to export the entry-point function
 */
#define AI_EXPORT_LIB AI_EXTERN_C AI_DLL_EXPORT

/**
 * Used by dynamically-linked nodes to return node info
 */
struct AtNodeLib {
   int         node_type;                    /**< type of node (\c AI_NODE_SHADER, \c AI_NODE_CAMERA, etc) */
   uint8_t     output_type;                  /**< output type for shader nodes (\c AI_TYPE_RGB, etc)       */
   const char* name;                         /**< name of this plug-in node ("lambert", etc)               */
   const void* methods;                      /**< pointer to this node's methods                           */
   char        version[AI_MAXSIZE_VERSION];  /**< Arnold version that this node was compiled against       */
};

AI_API void AiLoadPlugins(const char* directory);

/*\}*/
