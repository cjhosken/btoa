// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for writing custom scene formats
 */

#pragma once

#include <ai_map.h>
#include <ai_scene.h>
#include <ai_version.h>

/** \defgroup ai_scene_format Scene Format Plugin API
 * 
 * Implementation of custom scene formats.
 * 
 *  \details
 * This API is used to implement support for loading and/or writing custom scene
 * formats.
 * 
 * Implementing support for a new scene format requires exposing the plugin entry
 * point symbol, which in this case is called \c SceneFormatLoader(). This can 
 * be done through the convenience macro \c scene_format_loader. For example, this
 * is how a plugin could be implemented to support the fictional ".xxx" scene format:
 * 
 * \code
 * AI_SCENE_FORMAT_EXPORT_METHODS(XXXSceneFormatMtd);
 * 
 * scene_load
 * {
 *    . . .
 * }
 * 
 * scene_write
 * {
 *    . . .
 * }
 * 
 * scene_format_loader
 * {
 *    static const char* extensions[] = { ".xxx", NULL };
 * 
 *    format->methods     = XXXSceneFormatMtd;
 *    format->extensions  = extensions;
 *    format->name        = "XXX";
 *    format->description = "Support for loading XXX files in Arnold";
 *    strcpy(format->version, AI_VERSION);
 *    return true;
 * }
 * \endcode
 * 
 * Both load and write methods are optional, so any of them can be implemented, or
 * both could be implemented.
 * 
 * \{
 */

/**
 * Used by dynamically-linked scene format plugins
 */
struct AtSceneFormatLib {
   const char**           extensions;                   /**< null-terminated list of extensions used by this format   */
   const char*            name;                         /**< name of this scene format ("ASS", "USD", etc)            */
   const char*            description;                  /**< description for this scene format                        */
   const void*            methods;                      /**< pointer to load/write methods for this format            */
   char                   version[AI_MAXSIZE_VERSION];  /**< Arnold version that this plugin was compiled against     */
   const AtParamValueMap* params;                       /**< optional params that will be passed on to the methods    */
};

/**
 * Scene format load method.
 * 
 * \param universe  universe where the loaded scene nodes will be created (NULL for default universe)
 * \param filename  name of the scene file to load
 * \param params    list of arbitrary params which will be interpreted by the specific scene format
 * \return          true upon success
 */
typedef bool (*AtSceneLoad)(AtUniverse* universe, const char* filename, const AtParamValueMap* params);

/**
 * Scene format write method.
 * 
 * \param universe  universe with the nodes to be written to the scene file (NULL for default universe)
 * \param filename  name of the scene file to write to
 * \param params    list of arbitrary params which will be interpreted by the specific scene format
 * \param mds       metadata store that might be stored in the output scene file (if supported)
 * \return          true upon success
 */
typedef bool (*AtSceneWrite)(AtUniverse* universe, const char* filename, const AtParamValueMap* params, const AtMetadataStore* mds);

/**
 * Scene format methods
 */
struct AtSceneFormatMethods
{
   AtSceneLoad   SceneLoad;
   AtSceneWrite  SceneWrite;
};

/** Exporter for common methods */
#define AI_SCENE_FORMAT_EXPORT_METHODS(tag)    \
static AtSceneFormatMethods ai_scene_mtds = {  \
   NULL,                                       \
   NULL                                        \
};                                             \
const AtSceneFormatMethods* tag = &ai_scene_mtds;

/** Entry point for the scene format plugin */
#define scene_format_loader \
AI_EXPORT_LIB bool SceneFormatLoader(AtSceneFormatLib* format)

/** Scene format loading method */
#define scene_load \
static bool SceneLoad(AtUniverse* universe, const char* filename, const AtParamValueMap* params); \
AI_OPTIONAL_METHOD_INSTALL(ai_scene_mtds, SceneLoad) \
static bool SceneLoad(AtUniverse* universe, const char* filename, const AtParamValueMap* params)

/** Scene format writing method */
#define scene_write \
static bool SceneWrite(AtUniverse* universe, const char* filename, const AtParamValueMap* params, const AtMetadataStore* mds); \
AI_OPTIONAL_METHOD_INSTALL(ai_scene_mtds, SceneWrite) \
static bool SceneWrite(AtUniverse* universe, const char* filename, const AtParamValueMap* params, const AtMetadataStore* mds)
