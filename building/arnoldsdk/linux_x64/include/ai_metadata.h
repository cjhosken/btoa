// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for writing and reading node metadata
 */

#pragma once
#include "ai_node_entry.h"
#include "ai_vector.h"
#include "ai_color.h"
#include "ai_api.h"
#include "ai_string.h"
#ifdef AI_CPU_COMPILER

/** \defgroup ai_metadata Metadata API
 *
 * Reading and writing of metadata.
 *
 * \details
 * Arnold provides a container for generic metadata called \ref AtMetadataStore.
 * An \ref AtMetadataStore object can contain any number of metadata items, each
 * consisting on a name, type and value.
 *
 * Every Arnold \ref AtNodeEntry object contains its own \ref AtMetadataStore,
 * with metadata specific to that node entry and its parameters. All this metadata
 * is shared among all nodes of that type. This metadata can be helpful to maintain
 * extra annotations about parameters for GUI tools for example.
 *
 * Finally, metadata can also be loaded from a metadata file, or embedded in .ass
 * files.
 *
 * The following metadata items are recognized by Arnold, and could be used to
 * modify the way nodes and parameters are processed.
 *
 *  <table>
 *  <tr><th>Name<th>Type<th>Applies to<th>Description
 *  <tr><td>animatable<td> *BOOLEAN*<td>Array parameters<td>Indicate if keyframe data in array parameter is used in animation (ie motion blur)
 *  <tr><td>aov_shader<td> *BOOLEAN*<td>Node entry<td>Indicate if a shader may usefully be assigned as a global AOV shader in the "aov_shaders" render option
 *  <tr><td>aov.type<td> *INTEGER*<td>STRING parameters<td>For string parameters describing custom AOV outputs of a shader, describes the AOV's type (AI_TYPE_INT, AI_TYPE_FLOAT, AI_TYPE_RGB, etc)
 *  <tr><td>category<td> *STRING*<td>Node entry<td>Category under which to display a shader node in UIs (built-in categories are: "AOV","Atmosphere","Color","Convert","Light Filter","Math","Matrix","Noise","Shading","State","Texture","User Data","Utility","Vector","Volume")
 *  <tr><td>default<td> *<Parameter's type>*<td>Parameters<td>Default value to present in user interfaces
 *  <tr><td>deprecated<td> *BOOLEAN*<td>Node entry<td>If a node entry has this metadata set to true, creating a node of that type will emit a warning about it being deprecated
 *  <tr><td>extensions<td> *STRING*<td>Parameters<td>Used to tag a file path parameter with supported extensions
 *  <tr><td>gpu_support<td> *BOOLEAN*<td>Node entry / Parameters<td>Used to flag node types or parameters that are not yet supported by GPU rendering
 *  <tr><td>help<td> *STRING*<td>Node entry / Parameters<td>Descriptive text used to help indicate the design and purpose of a node or one of its parameters
 *  <tr><td>is_perspective<td> *BOOLEAN*<td>Node entry<td>Should be set in a custom camera if it is a perspective camera
 *  <tr><td>linkable<td> *BOOLEAN*<td>Parameters<td>Can be use to flag if parameters can be linked (true if metadata is not set)
 *  <tr><td>max<td> *<Parameter type>*<td>Numeric parameters<td>Maximum value above which a parameter loses functionality
 *  <tr><td>min<td> *<Parameter type>*<td>Numeric parameters<td>Minimum value below which a parameter loses functionality
 *  <tr><td>opacity_term<td> *INTEGER*<td>Node entry / Parameters<td>Set to a shader node entry if it is always opaque, or set to a parameter that is opaque when equal to 1 (1, 1, 1)
 *  <tr><td>parallel_driver_needs_bucket<td> *BOOLEAN*<td>Node entry<td>Set on a driver to enable the driver_needs_bucket API to be executed in parallel
 *  <tr><td>parallel_driver_prepare_bucket<td> *BOOLEAN*<td>Node entry<td>Set on a driver to enable the driver_prepare_bucket API to be executed in parallel
 *  <tr><td>parallel_driver_write_bucket<td> *BOOLEAN*<td>Node entry<td>Set on a driver to enable the driver_write_bucket API to be executed in parallel
 *  <tr><td>parallel_init<td> *BOOLEAN*<td>Node Entry<td>Set in custom procedurals to allow parallel initialization
 *  <tr><td>path<td> *STRING*<td>String Parameters<td>Set to a string parameter to select specific semantics for the value (valid values: *file*, *folder*, *folderlist*)
 *  <tr><td>softmax<td> *<Parameter type>*<td>Numeric parameters<td>Recommended maximum value to present in user interfaces
 *  <tr><td>softmin<td> *<Parameter type>*<td>Numeric parameters<td>Recommended minimum value to present in user interfaces
 *  <tr><td>_synonym<td> *STRING*<td>Node entry / Parameters<td>Provides alternative name to node entries or parameters
 *  <tr><td>transparency_term<td> *INTEGER*<td>Node entry / Parameters<td>Set to a shader node entry if it is always transparent, or set to a parameter that is opaque when equal to 0 (0, 0, 0)
 *  <tr><td>_triggers_reinitialize<td> *BOOLEAN*<td>Parameters<td>Set on shape node parameters that will trigger a node deinit & reinitialization when modified
 *  <tr><td>_triggers_reload<td> *BOOLEAN*<td>Parameters<td> (Deprecated) Synonym for _triggers_reinitialize
 *  <tr><td>ui.groups<td> *STRING*<td>Node entry<td>String describing the recommended paramter grouping for UIs. Formatting is: "Group1:param1 param2,Group2:param3 param4"

 *  </table>
 *
 * \{
 */

/**
 * \struct AtMetadataStore
 *
 * This structure holds a generic list of metadata items, each of which could
 * optionally be associated to a specific parameter (for node metadata). The actual
 * contents of this struct are private.
 */
struct AtMetadataStore;

/**
 * \name Node metadata writing
 *
 * \details
 * These functions allow attaching auxiliary information about specific parameters or
 * the node itself. This information is stored within the \ref AtNodeEntry. These
 * methods may only be called within the \ref node_parameters function where the parameters
 * are declared.
 *
 * Here is an example:
 * \code
 * node_parameters
 * {
 *    AiParameterFlt("Kd", 0.7f);
 *
 *    // create a lower-case synonym for parameter Kd
 *    AiMetaDataSetStr(nentry, "Kd", "_synonym", "kd");
 *
 *    // describe the parameter
 *    AiMetaDataSetStr(nentry, "Kd", "description",
 *       "Diffuse coefficient");
 *    // describe the node itself
 *    AiMetaDataSetStr(nentry, NULL, "description",
 *       "This is a simple lambert shader for illustration purposes");
 * }
 * \endcode
 *
 * Note that you should never pass allocated strings, as they will not be freed.
 *
 * \param nentry this is the \ref AtNodeEntry (note that \e nentry is an argument to \ref node_parameters)
 * \param param  the name of the node parameter to which the metadata will be attached (or a
 *               null/empty string if you want to attach information to the node itself)
 * \param name   the name of the metadata you want to attach
 * \param value  the value of the metadata
 *
 * \{
 */
#define AiCreateFuncs(_name, _type)                                                                              \
AI_API void AiMetaDataSet##_name (AtNodeEntry* nentry, const AtString param, const AtString name, _type value);  \
inline void AiMetaDataSet##_name (AtNodeEntry* nentry, const char* param,    const char* name,    _type value)   \
{                                                                                                                \
   AiMetaDataSet##_name(nentry, AtString(param), AtString(name), value);                                         \
}                                                                                                                \

AiCreateFuncs(Bool, bool)
AiCreateFuncs(Int,  int)
AiCreateFuncs(Flt,  float)
AiCreateFuncs(RGB,  AtRGB)
AiCreateFuncs(RGBA, AtRGBA)
AiCreateFuncs(Vec,  AtVector)
AiCreateFuncs(Vec2, AtVector2)
AiCreateFuncs(Str,  AtString)
#undef AiCreateFuncs

inline void AiMetaDataSetStr(AtNodeEntry* nentry, const char* param, const char* name, const char* value)
{
   AiMetaDataSetStr(nentry, param, name, AtString(value));
}

/* \} */

/**
 * \name Node Metadata Retrieval
 *
 * \details
 * These functions allow client code to examine metadata attached to specific
 * parameters or to a node.
 *
 * Following on the example above:
 * \code
 * const AtNodeEntry* entry = AiNodeEntryLookUp("my_simple_lambert");
 * char* desc;
 * bool success = AiMetaDataGetStr(entry, "Kd", "description", &desc)
 * if (success)
 *    printf("\nDescription for parameter Kd: %s", desc);
 * \endcode
 *
 * \param entry       the \ref AtNodeEntry of the node you want to get metadata from
 * \param param       the name of the node parameter you want to get metadata from
 *                    (or null/empty string if you are looking for metadata on the node itself)
 * \param name        the name of the metadata you want to get
 * \param[out] value  if the read succeeds, the variable pointed to by \e value
 *                    will be overwritten with the metadata
 * \return            true when the lookup is succesful
 *
 * \{
 */
#define AiCreateFuncs(_name, _type)                                                                                                \
AI_API               bool AiMetaDataGet##_name(const AtNodeEntry* nentry, const AtString param, const AtString name, _type* value);\
inline AI_DEPRECATED bool AiMetaDataGet##_name(const AtNodeEntry* nentry, const char* param,    const char* name,    _type* value) \
{                                                                                                                                  \
   return AiMetaDataGet##_name(nentry, AtString(param), AtString(name), value);                                                    \
}

AiCreateFuncs(Bool, bool)
AiCreateFuncs(Int,  int)
AiCreateFuncs(Flt,  float)
AiCreateFuncs(RGB,  AtRGB)
AiCreateFuncs(RGBA,  AtRGBA)
AiCreateFuncs(Vec,  AtVector)
AiCreateFuncs(Vec2, AtVector2)
AiCreateFuncs(Str,  AtString)
#undef AiCreateFuncs

/* \} */

/**
 * \name AtMetadataStore Writing
 *
 * \details
 * These functions allow attaching auxiliary information to a specific metadata store.
 *
 * Here is an example:
 * \code
 * AiMetadataStoreSetStr(mds, AtString("author"), "William Shakespeare");
 * AiMetadataStoreSetStr(mds, AtString("bbox"), "-1 -1 -1 1 1 1");
 * AiMetadataStoreSetFlt(mds, AtString("temperature"), 21.0f);
 * \endcode
 *
 * Note that you should never pass allocated strings, as they will not be freed.
 *
 * \param mds    the metadata store to operate with
 * \param name   the name of the metadata you want to attach
 * \param value  the value of the metadata
 *
 * \{
 */
#define AiCreateFuncs(_name, _type) \
AI_API void AiMetadataStoreSet##_name(AtMetadataStore* mds, const AtString name, _type value); \
AI_API void AiMetadataStoreParamSet##_name(AtMetadataStore* mds, const AtString param, const AtString name, _type value);

AiCreateFuncs(Bool, bool)
AiCreateFuncs(Int,  int)
AiCreateFuncs(Flt,  float)
AiCreateFuncs(RGB,  AtRGB)
AiCreateFuncs(Vec,  AtVector)
AiCreateFuncs(Vec2, AtVector2)
AiCreateFuncs(Str,  AtString)
#undef AiCreateFuncs

inline void AiMetadataStoreSetStr(AtMetadataStore* mds, const AtString name, const char* value)
{
   AiMetadataStoreSetStr(mds, name, AtString(value));
}

inline void AiMetadataStoreParamSetStr(AtMetadataStore* mds, const AtString param, const AtString name, const char* value)
{
   AiMetadataStoreParamSetStr(mds, param, name, AtString(value));
}

/* \} */

/**
 * \name AtMetadataStore Retrieval
 *
 * \details
 * These functions allow client code to get metadata entries within a specific metadata store.
 *
 * Following on the example above:
 * \code
 * char* author;
 * bool success = AiMetadataStoreGetStr(mds, "author", &author)
 * if (success)
 *    printf("\nAuthor: %s", author);
 * \endcode
 *
 * \param mds         the metadata store to read from
 * \param name        the name of the metadata you want to get
 * \param[out] value  if the read succeeds, the variable pointed to by \e value
 *                    will be overwritten with the metadata
 * \return            true when the lookup is succesful
 *
 * \{
 */
#define AiCreateFuncs(_name, _type) \
AI_API bool AiMetadataStoreGet##_name(const AtMetadataStore* mds, const AtString name, _type* value); \
AI_API bool AiMetadataStoreParamGet##_name(const AtMetadataStore* mds, const AtString param, const AtString name, _type* value);

AiCreateFuncs(Bool, bool)
AiCreateFuncs(Int,  int)
AiCreateFuncs(Flt,  float)
AiCreateFuncs(RGB,  AtRGB)
AiCreateFuncs(Vec,  AtVector)
AiCreateFuncs(Vec2, AtVector2)
AiCreateFuncs(Str,  AtString)
#undef AiCreateFuncs

/* \} */

/**
 * Creates a new metadata store.
 *
 * \return  new metadata store object
 */
AI_API AtMetadataStore* AiMetadataStore();

/**
 * Destroys a metadata store object.
 *
 * \param mds     metadata store object to be destroyed
 */
AI_API void AiMetadataStoreDestroy(AtMetadataStore* mds);

/**
 * Load embedded metadata from an .ass file into a metadata store.
 *
 * \param mds     metadata store object where embedded metadata will be loaded
 * \param file    filename of the .ass file with the embedded metadata to load
 */
AI_API bool AiMetadataStoreLoadFromASS(AtMetadataStore* mds, const char* file);

/**
 * Creates a new metadata iterator that traverses all global metadata.
 *
 * \param mds     metadata store object to get an iterator for
 * \return        an iterator over all global metadata in a metadata store
 */
AI_API AtMetaDataIterator* AiMetadataStoreGetIterator(const AtMetadataStore* mds);

/**
 * Creates a new metadata iterator pointing at the first matching entry.
 *
 * \param mds        metadata store object to get an iterator for
 * \param param      request metadata for a specific param (or global metadata if param is NULL)
 * \param recursive  if true and param is NULL, it will traverse both global metadata and param metadata for all params
 * \return           an iterator over all metadata in a metadata store
 */
AI_API AtMetaDataIterator* AiMetadataStoreGetIteratorRecursive(const AtMetadataStore* mds, const char* param, bool recursive);

/**
 * Load a metadata file.
 *
 * Metadata items loaded from this file will be attached to existing
 * node entries and their parameters, as especified by the
 * <a href="https://docs.arnoldrenderer.com/x/kQNEB">.mtd file format</a>
 *
 * Usage:
 * \code
 * const char* metadata_file = "my_metadata_file.mtd";
 * bool success = AiMetaDataLoadFile(metadata_file)
 * if (!success)
 *    printf("\nError loading metadata file %s", metadata_file);
 * \endcode
 *
 * \param filename    the full path of the metadata file to load
 * \return            true when the file could be read succesfully
 */
AI_API bool AiMetaDataLoadFile(const char* filename);

/* \} */

#endif // AI_CPU_COMPILER
