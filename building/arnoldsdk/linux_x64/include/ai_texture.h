// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Texture mapping system
 */

#pragma once
#include "ai_allocate.h"
#include "ai_api.h"
#include "ai_color.h"
#include "ai_shaderglobals.h"

// forward declares
class AtUniverse;

/** \defgroup ai_texture Texture Mapping API
 * 
 * Texture mapping system.
 * 
 * \{
 */

/** \name Wrapping Modes
 *
 * Wrap mode describes what happens when texture coordinates describe a value
 * outside the usual [0,1] range in (s,t)-space where a texture is defined.
 * \{
 */
#define AI_WRAP_PERIODIC          0   /**< the texture repeats itself outside the [0,1] range */
#define AI_WRAP_BLACK             1   /**< return black outside the [0,1] range               */
#define AI_WRAP_CLAMP             2   /**< clamp to the closest texture edge                  */
#define AI_WRAP_MIRROR            3   /**< mirror the image across the boundaries             */
#define AI_WRAP_FILE              4   /**< use wrap mode found in the EXR file's metadata     */
/*\}*/

/**
 * \name Texture Look-Up/Interpolation Modes
 *
 * The look-up mode determines how we sample within a mimap level.
 * \{
 */
#define AI_TEXTURE_CLOSEST        0  /**< force the closest texel                           */
#define AI_TEXTURE_BILINEAR       1  /**< force bilinear look-up within a mip level         */
#define AI_TEXTURE_BICUBIC        2  /**< force bicubic look-up within a mip level          */
#define AI_TEXTURE_SMART_BICUBIC  3  /**< bicubic when maxifying, else use bilinear look-up */
/*\}*/

/**
* \name MIP modes
*
* The MIP mode determines how we sample between mipmap levels.
* \{
*/
#define AI_TEXTURE_MIPMODE_DEFAULT      0  /**< use the default mode (auto-selected)                  */
#define AI_TEXTURE_MIPMODE_NONE         1  /**< use highest-res mip level only                        */
#define AI_TEXTURE_MIPMODE_ONE          2  /**< just use one mip level (closest)                      */
#define AI_TEXTURE_MIPMODE_TRILINEAR    3  /**< trilinear blending of two closest mip levels          */
#define AI_TEXTURE_MIPMODE_ANISOTROPIC  4  /**< use two closest mip levels with anisotropic filtering */
/*\}*/

/** Structure that holds all of the available texture map look-up options */
struct AtTextureParams {
   float    fill;               /**< value for nonexistent channels (e.g. alpha)        */
   uint8_t  filter         : 2; /**< texture look-up mode                               */
   uint8_t  wrap_s         : 3; /**< wrap mode for S coordinate                         */
   uint8_t  wrap_t         : 3; /**< wrap mode for T coordinate                         */
   uint8_t  start_channel;      /**< starting channel index to read from                */
   int8_t   mipmap_bias;        /**< mipmap level bias                                  */
   uint8_t  mipmap_mode    : 3; /**< mode for mipmap blending and filtering             */
   bool     single_channel : 1; /**< treat image as single channel                      */
   bool     flip_s         : 1; /**< flip S coordinate                                  */
   bool     flip_t         : 1; /**< flip T coordinate                                  */
   bool     swap_st        : 1; /**< enable swapping of S and T coordinates             */
   float    scale_s;            /**< scale S coordinate                                 */
   float    scale_t;            /**< scale T coordinate                                 */
   float    width_s;            /**< multiplicative widening of look-ups on the S axis  */
   float    width_t;            /**< multiplicative widening of look-ups on the T axis  */
   float    blur_s;             /**< additive blur in look-ups along the S axis         */
   float    blur_t;             /**< additive blur in look-ups along the T axis         */
};

AI_API void AiTextureParamsSetDefaults(AtTextureParams& params);

/**
 * \struct AtTextureHandle
 *
 * \brief  Structure that holds a handle for a given texture
 *
 * Texture handles can be created through \ref AiTextureHandleCreate and destroyed
 * with \ref AiTextureHandleDestroy. Texture lookups can be done with \ref AiTextureHandleAccess,
 * which is faster than \ref AiTextureAccess.
 */
struct AtTextureHandle;

/**
 * \struct AtImage
 *
 * \brief  Structure that holds infromation for reading, writing and resizing images
 *
 */
struct AtImage
{
   void*   buffer      = nullptr; /**< pixel values        */
   int     width       = 0;       /**< width of the image in pixels        */
   int     height      = 0;       /**< height of the image in pixels        */
   int     full_width  = 0; /**< width of the full display window  in pixels        */
   int     full_height = 0; /**< height of the full display window in pixels        */
   int     x           = 0; /**< origin (upper left corner) of pixel data       */
   int     y           = 0; /**< origin (upper left corner) of pixel data        */
   int     channels    = 0; /**< number of channels per pixel        */
   uint8_t format = 0; /**< data type of pixels AI_TYPE_(BYTE, USHORT, HALF, UINT, FLOAT)*/
   AtArray* aov_names = nullptr; /**< AtArray of AtStrings of aov names        */
   ~AtImage()
   {
      AiFree(aov_names);
      AiFree(buffer);
   }
};

AI_API AtTextureHandle*    AiTextureHandleCreate(const char* filename, AtString texture_color_space = AtString());
AI_API AtRGBA              AiTextureHandleAccess(const AtShaderGlobals* sg, AtTextureHandle* handle, const AtTextureParams& params, bool* success = NULL);
AI_API void                AiTextureHandleDestroy(AtTextureHandle* handle);

AI_API         AtRGBA      AiTextureAccess(const AtShaderGlobals* sg, AtString filename, AtString texture_color_space, const AtTextureParams& params, bool* success = NULL);
AI_API         bool        AiTextureLoad(const AtString filename, const bool use_float, const unsigned int miplevel, void* image);
AI_API         bool        AiTextureGetResolution(const char* filename, unsigned int* width, unsigned int* height);
AI_API         bool        AiTextureGetNumChannels(const char* filename, unsigned int* num_channels);
AI_API AI_PURE const char* AiTextureGetChannelName(const char* filename, unsigned int channel_index);
AI_API         bool        AiTextureGetFormat(const char* filename, unsigned int* format);
AI_API         bool        AiTextureGetBitDepth(const char* filename, unsigned int* bit_depth);
AI_API         bool        AiTextureGetMatrices(const char* filename, AtMatrix& world_to_screen, AtMatrix& world_to_camera);
AI_API         void        AiTextureInvalidate(const char* filename);

AI_API         AtString    AiTextureGetTxFileName(const char* filename, AtString texture_color_space, AtString render_color_space, const AtUniverse* universe);
AI_API         AtString    AiTextureGetTxSourceFileName(const char* tx_filename);
AI_API         AtString    AiTextureAutoTxFlags(const char* texture_file, AtString texture_color_space, const AtUniverse* universe);
AI_API         bool        AiTextureTxFileNeedsUpdate(const char* texture_file, const char* tx_filename, const char* flags);

AI_API               bool AiReadImage(const char* filename, const uint8_t format, AtImage& image, AtParamValueMap* params = nullptr);
AI_API               bool AiWriteImage(const char* filename, const AtImage& image, AtParamValueMap* params = nullptr);
AI_API               bool AiResizeImage(const AtImage& inImage, AtImage& outImage, AtParamValueMap* params = nullptr);
inline AI_DEPRECATED bool AiLoadImage(const char* filename, const uint8_t format, AtImage& image)
{
   return AiReadImage(filename, format, image, nullptr);
}

/**
 * Status of AiMakeTx jobs.
 */
enum AtMakeTxStatus { AiTxPending, AiTxError, AiTxUpdated, AiTxUpdate_unneeded, AiTxAborted };
AI_API         void        AiMakeTx(const char* filename, const char* flags, const AtUniverse* universe = NULL);
AI_API         unsigned    AiMakeTxWaitJob(AtMakeTxStatus*& statuses, const char**& source_files, unsigned int& num_submitted_textures);
AI_API         void        AiMakeTxAbort(AtMakeTxStatus*& statuses, const char**& source_files, unsigned int& num_submitted_textures);
/*\}*/
