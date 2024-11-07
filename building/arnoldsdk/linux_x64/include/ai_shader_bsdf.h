// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Various BSDF functions available to shader writers
 */

#pragma once
#include "ai_color.h"
#include "ai_ray.h"
#include "ai_vector.h"
#include "ai_shaderglobals.h"

/** \defgroup ai_shader_bsdf BSDF API
 *
 *  Various BSDF functions available to shader writers.
 *
 * \{
 */

/** BSDF: bidirectional scattering distribution function */
struct AtBSDF;

/** BSDF Lobe flags */
enum AtBSDFLobeFlags {
   AI_BSDF_LOBE_SINGULAR          = 0x01,  /**< Sampling the BSDF always returns the same direction */
   AI_BSDF_LOBE_WAVELENGTH_SAMPLE = 0x02,  /**< Sampling the BSDF lobe requires a wavelength        */
   AI_BSDF_LOBE_EXIT_BACKGROUND   = 0x04,  /**< If ray depth exceeded, use background color         */
   AI_BSDF_LOBE_EXIT_WHITE        = 0x08   /**< If ray depth exceeded, use white color              */
};


/** BSDF lobe information */
struct AtBSDFLobeInfo {
   uint8_t ray_type;
   uint8_t flags;
   AtString label;
};


/** BSDF lobe bitmask */
typedef uint32_t AtBSDFLobeMask;
static const AtBSDFLobeMask AI_BSDF_LOBE_MASK_NONE = 0x0;


/** BSDF lobe sample */
struct AtBSDFLobeSample {
   AI_DEVICE AtBSDFLobeSample(AtRGB weight, float reverse_pdf, float pdf)
   : weight(weight), reverse_pdf(reverse_pdf), pdf(pdf) { }

   AI_DEVICE AtBSDFLobeSample(AtRGB eval)
   : weight(eval), reverse_pdf(1.0f), pdf(1.0f) { }

   AtBSDFLobeSample() = default;

   AtRGB weight;
   float reverse_pdf;
   float pdf;
};


/**
 * BSDF function table
 *
 * This structure is used to report the function pointers that the
 * renderer needs to call at runtime. The version field is used for runtime
 * compatibility checking.
 */
#ifdef AI_CPU_COMPILER
struct AtBSDFMethods
{
   int            version;
   void           (*Init)(const AtShaderGlobals* sg,
                          AtBSDF* bsdf);
   AtBSDFLobeMask (*Eval)(const AtBSDF* bsdf,
                          const AtVector& wi,
                          const AtBSDFLobeMask lobe_mask,
                          const bool need_pdf,
                          AtBSDFLobeSample out_lobes[]);
   AtBSDFLobeMask (*Sample)(const AtBSDF* bsdf,
                            const AtVector rnd,
                            const float wavelength,
                            const AtBSDFLobeMask lobe_mask,
                            const bool need_pdf,
                            AtVectorDv& out_wi,
                            int& out_lobe_index,
                            AtBSDFLobeSample out_lobes[]);
   AtRGB          (*Albedo)(const AtBSDF* bsdf,
                            const AtShaderGlobals* sg,
                            const AtBSDFLobeMask lobe_mask);
   bool           (*Merge)(AtBSDF* bsdf,
                           const AtBSDF* other_bsdf);
   AtClosureList  (*Interior)(const AtShaderGlobals* sg,
                              AtBSDF* bsdf);
};
#endif // AI_CPU_COMPILER

/** BSDF methods exporter */
#define AI_BSDF_EXPORT_METHODS(tag)      \
bsdf_init;                               \
bsdf_eval;                               \
bsdf_sample;                             \
static AtBSDFMethods ai_bsdf_methods = { \
   0,                                    \
   Init,                                 \
   Eval,                                 \
   Sample,                               \
   NULL,                                 \
   NULL,                                 \
   NULL,                                 \
};                                       \
AtBSDFMethods* tag = &ai_bsdf_methods;

/**
 * Initialize BSDF when before it is used for the first time.
 *
 * This method must set the BSDF lobes with \c AiBSDFInitLobes(), and may
 * optionally call \c AiBSDFInitBounds(). Other typical initializations performed
 * in this method would be ensuring the parameters are withing a valid range,
 * store local geometry data for later evaluation and sampling (geometric normal,
 * outgoing view direction, ..), and precomputing data.
 */
#define bsdf_init                           \
static void Init(const AtShaderGlobals* sg, \
                 AtBSDF* bsdf)

/**
 * Evaluate BSDF for the given incoming light direction.
 *
 * If the BSDF consists of multiple lobes, lobe_mask describes which lobes must
 * be evaluated. The result of this evaluation for each lobe is:
 * - RGB \c weight, defined as <tt>BSDF * cos(N.wi) / pdf</tt>. The cosine between
 *   the surface normal and the incoming light direction must be included, and
 *   the weight must be divided by the probability density. For a BSDF that does
 *   perfect importance sampling, this weight would be 1.
 * - pdf, the probability density for sampling the the incoming light direction with
 *   \c bsdf_sample.
 */
#define bsdf_eval                                          \
static AtBSDFLobeMask Eval(const AtBSDF* bsdf,             \
                           const AtVector& wi,             \
                           const AtBSDFLobeMask lobe_mask, \
                           const bool need_pdf,            \
                           AtBSDFLobeSample out_lobes[])

/**
 * Sample BSDF for an incoming light direction, and evaluate BSDF.
 *
 * This function returns:
 * - Sampled incoming light direction \c wi.
 * - Index of the lobe that was sampled.
 * - RGB \c weight and \c pdf, matching \c bsdf_eval for the same incoming light
 *   direction.
 */
#define bsdf_sample                                          \
static AtBSDFLobeMask Sample(const AtBSDF* bsdf,             \
                             const AtVector rnd,             \
                             const float wavelength,         \
                             const AtBSDFLobeMask lobe_mask, \
                             const bool need_pdf,            \
                             AtVectorDv& out_wi,             \
                             int& out_lobe_index,            \
                             AtBSDFLobeSample out_lobes[])

/**
 * Compute BSDF albedo for AOVs and importance sampling (optional method)
 */
#define bsdf_albedo                                                                                 \
static AtRGB Albedo(const AtBSDF* bsdf, const AtShaderGlobals* sg, const AtBSDFLobeMask lobe_mask); \
AI_OPTIONAL_METHOD_INSTALL(ai_bsdf_methods, Albedo)                                                 \
static AtRGB Albedo(const AtBSDF* bsdf, const AtShaderGlobals* sg, const AtBSDFLobeMask lobe_mask)

/**
 * Merge BSDF with another BSDF of the same type (optional method)
 *
 * Before initialization, evaluation and sampling, BSDFs of the same type can
 * be merged if their parameters are equal or close enough that they can be
 * mixed. This can improve rendering performance when mixing shaders.
 *
 * If this method returns true to indicate the BSDFs can be merged, the weight
 * of the other BSDF is added to this BSDF, and the other BSDF is discarded.
 */
#define bsdf_merge                                         \
static bool Merge(AtBSDF* bsdf, const AtBSDF* other_bsdf); \
AI_OPTIONAL_METHOD_INSTALL(ai_bsdf_methods, Merge)         \
static bool Merge(AtBSDF* bsdf, const AtBSDF* other_bsdf)

/**
 * Return volume closures describing the interior of the object.
 *
 * These closures control the volume interior shading after refraction rays
 * enter the object, typically for absorption inside glass.
 */
#define bsdf_interior                                                   \
static AtClosureList Interior(const AtShaderGlobals* sg, AtBSDF* bsdf); \
AI_OPTIONAL_METHOD_INSTALL(ai_bsdf_methods, Interior)                   \
static AtClosureList Interior(const AtShaderGlobals* sg, AtBSDF* bsdf)


/** \name Functions for implementing custom BSDFs
 * \{
 */
#ifdef AI_CPU_COMPILER
AI_API AtBSDF* AiBSDF(const AtShaderGlobals* sg, const AtRGB& weight, const AtBSDFMethods* methods, size_t data_size);

AI_API const AtBSDFMethods*  AiBSDFGetMethods (const AtBSDF* bsdf);
#endif // AI_CPU_COMPILER
AI_API AI_DEVICE void*       AiBSDFGetData    (const AtBSDF* bsdf);
AI_API const AtBSDFLobeInfo* AiBSDFGetLobes   (const AtBSDF* bsdf);
AI_API int                   AiBSDFGetNumLobes(const AtBSDF* bsdf);
AI_API AI_DEVICE AtRGB       AiBSDFGetWeight  (const AtBSDF* bsdf);

AI_API AI_DEVICE void AiBSDFSetDirectIndirect(AtBSDF* bsdf, float weight_direct, float weight_indirect);
AI_API AI_DEVICE void AiBSDFGetDirectIndirect(const AtBSDF* bsdf, float& weight_direct, float& weight_indirect);

AI_API AI_DEVICE void AiBSDFInitLobes (AtBSDF* bsdf, const AtBSDFLobeInfo* lobes, int num_lobes);
AI_API AI_DEVICE void AiBSDFInitNormal(AtBSDF* bsdf, const AtVector& N, bool bounding);

AI_API AI_DEVICE float AiBSDFBumpShadow  (const AtVector& Ns, const AtVector& N, const AtVector& Ld);
AI_API AI_DEVICE float AiBSDFMinRoughness(const AtShaderGlobals* sg);
/*\}*/


/** \name Built-in BSDFs
 * \{
 */


////////////////////////////////////////////////////////////////////////////////
/** \name Diffuse BRDF
 *
 * \{
 */

/**
 * Oren-Nayar mode
 */
enum AtOrenNayarModel : unsigned char
{
   QUALITATIVE,       // classic "qualitative" Oren-Nayar model (QON)
   ENERGY_PRESERVING  // energy preserving Oren-Nayar model (EON)
};

AI_API AI_DEPRECATED AI_DEVICE
AtBSDF* AiOrenNayarBSDF(const AtShaderGlobals* sg, const AtRGB& weight, const AtVector& N,
                        float r = 0.0f, bool transmission = false,
                        const AtString label = AtString());

AI_API AI_DEVICE
AtBSDF* AiOrenNayarBSDF_private(const AtShaderGlobals* sg, const AtRGB& weight, const AtVector& N,
                                AtOrenNayarModel model = AtOrenNayarModel::ENERGY_PRESERVING,
                                float r = 0.0f, bool transmission = false,
                                const AtString label = AtString());

inline AI_DEVICE
AtBSDF* AiOrenNayarBSDF(const AtShaderGlobals* sg, const AtRGB& weight, const AtVector& N,
                        AtOrenNayarModel model = AtOrenNayarModel::ENERGY_PRESERVING,
                        float r = 0.0f, bool transmission = false,
                        const AtString label = AtString())
{
   return AiOrenNayarBSDF_private(sg, weight, N, model, r, transmission, label);
}
/* \}*/ // Diffuse BRDF


////////////////////////////////////////////////////////////////////////////////
/** \name Microfacet BSDFs
 * \{
 */
AI_API AI_DEVICE
AtBSDF* AiMicrofacetBSDF(const AtShaderGlobals* sg, const AtRGB& weight,
                         int distribution, const AtVector& N, const AtVector *U,
                         float ior, float rx, float ry,
                         uint8_t exit_type = 0,
                         int32_t dielectric_priority = 0,
                         float thin_walled_transmission = 0,
                         const AtString label = AtString());

AI_API AI_DEVICE AtBSDF*
AiMicrofacetRefractionBSDF(const AtShaderGlobals* sg, const AtRGB& weight,
                           int distribution, const AtVector& N, const AtVector *U,
                           float ior, float rx, float ry, float dispersion,
                           bool use_fresnel = true, AtClosureList interior = AtClosureList(),
                           uint8_t exit_type = 0,
                           int32_t dielectric_priority = 0,
                           const AtString label = AtString());

AI_API AI_DEVICE AtBSDF*
AiMicrofacetThinWallRefractionBSDF(const AtShaderGlobals* sg, const AtRGB& weight,
                                   int distribution, const AtVector& N, const AtVector *U,
                                   float eta, float rx, float ry,
                                   uint8_t exit_type = 0, AtString label = AtString());

/** \name Microfacet distributions
 * \{
 */
#define AI_MICROFACET_BECKMANN   0x00  /**< Beckmann distribution */
#define AI_MICROFACET_GGX        0x01  /**< GGX distribution */
/*\}*/

/* \}*/ // Microfacet BSDFs


////////////////////////////////////////////////////////////////////////////////
/** \name Thin-film modifier
 * \{
 */
AI_API AI_DEPRECATED AI_DEVICE
void AiMicrofacetSetThinFilm(AtBSDF* bsdf, float thickness, float ior);

AI_API AI_DEVICE
void AiMicrofacetSetThinFilm_private(AtBSDF* bsdf, float weight, float thickness, float ior);

inline AI_DEVICE
void AiMicrofacetSetThinFilm(AtBSDF* bsdf, float weight, float thickness, float ior)
{
   AiMicrofacetSetThinFilm_private(bsdf, weight, thickness, ior);
}
/* \}*/ // Thin-film modifier


////////////////////////////////////////////////////////////////////////////////
/** \name Metal BRDF
 * \{
 */

/**
 * Metal Fresnel mode
 */
enum AtMetalFresnelMode
{
   GULBRANDSEN, // based on "Artist Friendly Metallic Fresnel", Gulbrandsen, JCGT (2014)
   F82_TINT     // based on the F82-tint model, from "Novel aspects of the Adobe Standard Material", Kutz et. al (2021)
};

AI_API AI_DEVICE AtBSDF* AiMetalBSDF(const AtShaderGlobals* sg, const AtRGB& weight,
                                     int distribution, const AtVector& N, const AtVector *U,
                                     AtMetalFresnelMode fresnel_mode,
                                     const AtRGB& fresnel1, const AtRGB& fresnel2, float rx, float ry,
                                     const AtString label = AtString());

/* \}*/ // Metal BRDF


////////////////////////////////////////////////////////////////////////////////
/** \name Hair BSDFs
 * \{
 */
AI_API AI_DEVICE AtBSDF* AidEonBSDF(const AtShaderGlobals* sg, const AtRGB& absorption, const AtRGB weights[3],
                                    const AtVector& tangent,
                                    const float roughness_longitudinal, const float roughness_azimuthal,
                                    const float eta, const float tilt, const AtString label = AtString());

AI_API AI_DEVICE AtBSDF* AiZinkeBSDF(const AtShaderGlobals* sg, const AtRGB &weight, const AtVector& tangent,
                                     const AtString label = AtString());

/* \}*/ // Hair BSDFs


////////////////////////////////////////////////////////////////////////////////
/** \name Sheen/Fuzz BRDFs
 * \{
 */
AI_API AI_DEVICE AtBSDF* AiSheenBSDF(const AtShaderGlobals* sg, const AtRGB &weight, const AtVector& N,
                                     const float r, const AtString label = AtString());

AI_API AI_DEVICE AtBSDF* AiFuzzBSDF(const AtShaderGlobals* sg, const AtRGB &weight, const AtVector& N,
                                    const float r, const AtString label = AtString());


/* \}*/ // Sheen/Fuzz BRDF

/* \}*/ // Built-in BSDFs



/** \name BSDF integration
 * \{
 */
AI_API void AiBSDFIntegrate(AtShaderGlobals* sg, AtRGB* direct, AtRGB* indirect, AtBSDF* bsdf);

AI_API AI_DEVICE AtRGB AiBSDFAlbedo(const AtShaderGlobals* sg, AtBSDF* bsdf);
/* \}*/

/*\}*/
