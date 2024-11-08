// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file 
 * API for managing gpu rendering
 */

#pragma once
#include "ai_api.h"
#include <ai_string.h>
#include <ai_array.h>
#include <ai_render.h>

/** \defgroup ai_device Render device API
 * 
 * Render device querying and selection.
 * 
 * \{
 */

/**
 * Device types
 */
enum AtDeviceType
{
   AI_DEVICE_TYPE_CPU  = 0,   /**< Render using the CPU */
   AI_DEVICE_TYPE_GPU  = 1    /**< Render using the GPU */
};

/**
 * Queriable memory attributes
 */
enum AtDeviceMemory
{
   AI_DEVICE_MEMORY_TOTAL,   /**< Total memory on device               */
   AI_DEVICE_MEMORY_FREE,    /**< Total free memory available to device*/
   AI_DEVICE_MEMORY_USED     /**< Total used memory                    */
};

/**
 * Returns if a given device is supported on the current system
 */
AI_API bool AiDeviceTypeIsSupported(AtDeviceType device_type, AtString& reason);

/**
 * Select render device
 */
AI_API int AiDeviceSelect(AtRenderSession* render_session, AtDeviceType device_type, const AtArray* device_ids);

/**
 * Automatically select render device based on options
 */
AI_API int AiDeviceAutoSelect(AtRenderSession* render_session);

/**
 * Returns the currently selected render device type
 */
AI_API AtDeviceType AiDeviceGetSelectedType(const AtRenderSession* render_session);

/**
 * Returns the currently selected devices ids of a device type
 */
AI_API const AtArray* AiDeviceGetSelectedIds(const AtRenderSession* render_session, AtDeviceType device_type);

/**
 * Returns the number of available devices of a given type
 */
AI_API unsigned int AiDeviceGetCount(AtDeviceType device_type);

/**
 * Returns the ids of available devices of a given type
 */
AI_API const AtArray* AiDeviceGetIds(AtDeviceType device_type);

/**
 * Returns the name of a device
 */
AI_API AtString AiDeviceGetName(AtDeviceType device_type, unsigned int device_id);

/**
 * Returns memory information of a device
 */
AI_API unsigned int AiDeviceGetMemoryMB(AtDeviceType device_type, unsigned int device_id, AtDeviceMemory memory);

/**
 * GPU cache population report callback.
 *  This callback provides:
 *     - user_ptr:      the user data pointer passed to AiGPUCachePopulate
 *     - status:        status code as returned from AiGPUCachePopulateStatus (AI_RENDER_STATUS_FINISHED will occur only once, on completion)
 *     - fraction_done: the progress as a fraction in [0.0, 1.0]
 *     - msg:           a report string
 */
typedef void (*AtGPUCachePopulateCallback)(void* user_ptr, AtRenderStatus status, float fraction_done, const char* msg);

enum AtGPUCachePopulateMode
{
   AI_GPU_CACHE_POPULATE_BLOCKING,
   AI_GPU_CACHE_POPULATE_NON_BLOCKING
};

/**
 * Set the directory where the OptiX cache will be stored
 */
AI_API void AiGPUCacheSetDirectory(const char* dir_path);

/**
 * Get the directory specified via AiGPUCacheSetDirectory (or if not specified, the default)
 */
AI_API AtString AiGPUCacheGetDirectory();
/*\}*/
