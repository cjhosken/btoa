// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * API for reading and writing scene file formats
 */

#pragma once

#include <ai_map.h>

struct AtMetadataStore;
class AtUniverse;

/** \defgroup ai_scene Scene File API
 *
 *  Scene file loading and writing using multiple formats.
 * 
 *  \details
 *  The implementation of each specific scene format will determine how to load
 *  nodes into an Arnold universe or how to store the contents of an Arnold 
 *  universe into a scene file.
 *
 * \{
 */

/**
 *  Load all nodes from a scene file into a specific Arnold universe
 *
 *  If the filename is "-", it reads data from stdin (assuming ASS format)
 *
 *  This example code loads all node types from a scene file:
 *  \code
 *  AtParamValueMap* params = AiParamValueMap();
 *  AiParamValueMapSetInt(params, AtString("mask"), AI_NODE_ALL);
 *  AiSceneLoad(universe, "scene.ass", params); 
 *  AiParamValueMapDestroy(params);
 *  \endcode
 * 
 *  Supported format specific params:
 * 
 *  <table>
 *  <tr><th>Scene format<th colspan="3">Supported load parameters
 *  <tr><td>ASS<td> **mask**<td> *INTEGER*<td>Only node types matching this mask will be loaded
 *  <tr><td rowspan="2">USD<td> **mask**<td> *INTEGER*<td>Only node types matching this mask will be loaded
 *  <tr><td> **frame**<td> *FLOAT*<td>Load a given frame from the USD file
 *  </table>
 * 
 *  \param universe    universe where the nodes will be created (NULL for default universe)
 *  \param filename    input filename (extension will be used to determine scene format)
 *  \param params      list of arbitrary params which will be interpreted by the specific scene format
 *  \return            true if the file was loaded succesfully, false otherwise
 */
AI_API bool AiSceneLoad(AtUniverse* universe, const char* filename, const AtParamValueMap* params);

/**
 *  Write all nodes in the given universe to a scene file.
 *
 *  This function can selectively write all nodes in a given universe to a scene file,
 *  which format will be determined from the filename extension.
 *
 *  An arbitrary list of attributes can be passed, and these attributes can be used by
 *  specific file formats. For example, the .ass file format supports "mask", "binary"
 *  and "open_procs" attributes, which are equivalent to the parameters on \ref AiASSWrite.
 *  Note these attributes might not work on other file formats.
 * 
 *  For example, to write light nodes and camera nodes only, use:
 *  \code
 *  AtParamValueMap* params = AiParamValueMap();
 *  AiParamValueMapSetInt(params, AtString("mask"), AI_NODE_LIGHT + AI_NODE_CAMERA);
 *  AiSceneWrite(universe, "lightsncams.ass", params);
 *  AiParamValueMapDestroy(params);
 *  \endcode
 *
 *  To write all nodes of all types, use:
 *  \code
 *  AtParamValueMap* params = AiParamValueMap();
 *  AiParamValueMapSetInt(params, AtString("mask"), AI_NODE_ALL);
 *  AiSceneWrite(universe, "everything.ass", params); 
 *  AiParamValueMapDestroy(params);
 *  \endcode
 *
 *  Supported format specific params:
 * 
 *  <table>
 *  <tr><th>Scene format<th colspan="3">Supported write parameters
 *  <tr><td rowspan="3">ASS<td> **mask**<td> *INTEGER*<td>Only node types matching this mask will be written
 *  <tr><td> **binary**<td> *BOOLEAN*<td>Allow binary encoding in .ass files
 *  <tr><td> **open_procs**<td> *BOOLEAN*<td>Procedurals will be expanded before writing
 *  <tr><td>USD<td> **mask**<td> *INTEGER*<td>Only node types matching this mask will be written
 *  </table>
 * 
 *  \param universe    universe whose contents will be written to the scene file (NULL for default universe)
 *  \param filename    output filename (extension will be used to select scene format)
 *  \param params      list of arbitrary params which will be interpreted by the specific scene format
 *  \param mds         optional metadata store for writing metadata into the file
 *  \return            true if the file was written succesfully, false otherwise
 */
AI_API bool AiSceneWrite(AtUniverse* universe, const char* filename, const AtParamValueMap* params, const AtMetadataStore* mds = NULL);

/**
 *  Check if the scene format corresponding to a given filename extension is supported
 *
 *  \param extension   scene file extension to check for support (should start with ".")
 *  \return            true if the format is supported, false otherwise
 */
AI_API bool AiSceneFormatSupported(const char* extension);

/** \name Node Iterator API
 * \{
 */

/**
 * \struct AtSceneFormatIterator
 * 
 * Allows iterating over the list of supported scene formats.
 */
struct AtSceneFormatIterator;

/**
 * \struct AtSceneFormatExtensionIterator
 * 
 * Allows iterating over the list of supported extensions for a given scene format.
 */
struct AtSceneFormatExtensionIterator;

/**
 * \struct AtSceneFormatData
 * 
 * Provides access to information about the scene format.
 */
struct AtSceneFormatData;

/**
 * Get new scene format iterator
 * 
 * \return New scene format iterator
 */
AI_API AtSceneFormatIterator* AiSceneFormatIterator();

/**
 * Destroys scene format iterator and releases any allocated memory
 * 
 * \param iter  Scene format iterator to destroy
 */
AI_API void AiSceneFormatIteratorDestroy(AtSceneFormatIterator* iter);

/**
 * Gets the next supported scene format
 * 
 * \param iter Scene format iterator
 * \return     Information about the next supported scene format
 */
AI_API const AtSceneFormatData* AiSceneFormatIteratorGetNext(AtSceneFormatIterator* iter);

/**
 * Check if there are more scene formats to iterate over
 * 
 * \param iter Scene format iterator
 * \return     true if the iterator reached the last supported scene format
 */
AI_API AI_PURE bool AiSceneFormatIteratorFinished(const AtSceneFormatIterator* iter);

/**
 * Get an iterator over all supported extensions for this scene format
 * 
 * \param format_data Scene format data returned by \c AiSceneFormatIteratorGetNext
 * \return            Iterator
 */
AI_API AtSceneFormatExtensionIterator* AiSceneFormatGetExtensionIterator(const AtSceneFormatData* format_data);

/**
 * Destroys scene format extension iterator and releases any allocated memory
 * 
 * \param iter  Scene format extension iterator to destroy
 */
AI_API void AiSceneFormatExtensionIteratorDestroy(AtSceneFormatExtensionIterator* iter);

/**
 * Gets the next supported scene format extension
 * 
 * \param iter Scene format extension iterator
 * \return     Next supported extension
 */
AI_API const char* AiSceneFormatExtensionIteratorGetNext(AtSceneFormatExtensionIterator* iter);

/**
 * Check if there are more scene formats extensions to iterate over
 * 
 * \param iter Scene format extension iterator
 * \return     true if the iterator reached the last supported scene format extension
 */
AI_API AI_PURE bool AiSceneFormatExtensionIteratorFinished(const AtSceneFormatExtensionIterator* iter);

/**
 * Get the name of the scene format
 * 
 * \param format_data Scene format data returned by \c AiSceneFormatIteratorGetNext
 * \return            Name of the scene format
 */
AI_API AI_PURE const char* AiSceneFormatGetName(const AtSceneFormatData* format_data);

/**
 * Get a description of the scene format
 * 
 * \param format_data Scene format data returned by \c AiSceneFormatIteratorGetNext
 * \return            Description of the scene format
 */
AI_API AI_PURE const char* AiSceneFormatGetDescription(const AtSceneFormatData* format_data);

/**
 * True if the scene format supports reading from file
 * 
 * \param format_data Scene format data returned by \c AiSceneFormatIteratorGetNext
 * \return            true if it can be read from file, false otherwise
 */
AI_API AI_PURE bool AiSceneFormatSupportsReading(const AtSceneFormatData* format_data);

/**
 * True if the scene format supports writing to a file
 * 
 * \param format_data Scene format data returned by \c AiSceneFormatIteratorGetNext
 * \return            true if it can be written to a file, false otherwise
 */
AI_API AI_PURE bool AiSceneFormatSupportsWriting(const AtSceneFormatData* format_data);

/**
 * Get metadata for the scene format and its optional parameters
 * 
 * \param format_data Scene format data returned by \c AiSceneFormatIteratorGetNext
 * \return            Metadata store with all metadata for the scene format and its optional parameters
 */
AI_API const AtMetadataStore* AiSceneFormatGetMetadataStore(const AtSceneFormatData* format_data);

/*\}*/

/*\}*/
