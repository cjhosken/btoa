// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Uber-include file, convenient way of making the entire Arnold API available
 * 
 * Note that the order of includes is _not_ random. For more information about
 * correct include ordering conventions:
 *    http://www.topology.org/linux/include.html
 */

#pragma once

#ifdef _ARNOLDDLL
#error "Users can directly include ai.h, but arnold core code must not."
#endif

// dso's
#include "ai_procedural.h"
#include "ai_volume.h"
#include "ai_plugins.h"
#include "ai_operator.h"

// node types
#include "ai_color_managers.h"
#include "ai_drivers.h"
#include "ai_driver_utils.h"
#include "ai_imagers.h"
#include "ai_filters.h"
#include "ai_cameras.h"
#include "ai_shaders.h"
#include "ai_nodes.h"
#include "ai_params.h"
#include "ai_metadata.h"

// scene loading/saving
#include "ai_dotass.h"
#include "ai_scene.h"

// error/warning messages
#include "ai_msg.h"

// error reporting
#include "ai_error_reporting.h"

// profiler / stats
#include "ai_stats.h"

// ADP optin
#include "ai_adp.h"

// shader functions
#include "ai_sampler.h"
#include "ai_shader_aovs.h"
#include "ai_shader_bsdf.h"
#include "ai_shader_closure.h"
#include "ai_shaderglobals.h"
#include "ai_shader_lights.h"
#include "ai_shader_message.h"
#include "ai_shader_radiance.h"
#include "ai_shader_sample.h"
#include "ai_shader_sss.h"
#include "ai_shader_userdef.h"
#include "ai_shader_parameval.h"
#include "ai_shader_util.h"
#include "ai_shader_volume.h"
#include "ai_noise.h"
#include "ai_texture.h"

// ray tracing
#include "ai_ray.h"
#include "ai_render.h"

// core
#include "ai_unit_test.h"
#include "ai_universe.h"

// system
#include "ai_critsec.h"
#include "ai_threads.h"

// simple data types
#include "ai_array.h"
#include "ai_bbox.h"
#include "ai_matrix.h"
#include "ai_vector.h"
#include "ai_color.h"
#include "ai_enum.h"
#include "ai_map.h"

// misc math
#include "ai_math.h"
#include "ai_constants.h"

// version info
#include "ai_version.h"

// licensing
#include "ai_license.h"

// memory allocation
#include "ai_allocate.h"

// render device APIs
#include "ai_device.h"

// materialx
#include "ai_materialx.h"

// file utils
#include "ai_file_utils.h"

// font utils
#include "ai_font.h"

