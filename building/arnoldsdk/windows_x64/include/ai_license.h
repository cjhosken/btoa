// Copyright 2021 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 * Utility functions for the configuration of the licensing system
 */

#pragma once
#include "ai_api.h"

/** \defgroup ai_license Licensing API
 * 
 * Arnold license system information.
 * 
 * \{
 */

AI_API void AiSetLicenseString(const char* lic);

/** License info structure. This is designed for RLM, so non-RLM licenses might
 * leave most fields uninitialized
 */
struct AtLicenseInfo {
   bool used;               /**< true if this is the license used by the current Arnold installation         */
   char name[64];           /**< product name                                                                */
   char ver[64];            /**< product version                                                             */
   char exp[64];            /**< expiration date                                                             */
   char options[64];        /**< product options                                                             */
   int  count;              /**< license count                                                               */
   int  current_inuse;      /**< license count in use                                                        */
   int  current_resuse;     /**< number of reservations in use                                               */
   int  hbased;             /**< HOST-BASED count                                                            */
   int  hold;               /**< license hold time                                                           */
   int  max_roam;           /**< maximum roam time                                                           */
   int  max_share;          /**< maximum number of processes that can share this license                     */
   int  min_remove;         /**< minimum rlmremove time                                                      */
   int  min_checkout;       /**< license minimum checkout time                                               */
   int  min_timeout;        /**< minimum timeout time                                                        */
   int  nres;               /**< number of license reservations                                              */
   int  num_roam_allowed;   /**< number of roaming licenses allowed                                          */
   int  roaming;            /**< number of licenses currently roaming (for roaming licenses)                 */
   int  share;              /**< license share flags (share flags RLM_LA_SHARE_xxx are defined in license.h) */
   int  soft_limit;         /**< license soft limit                                                          */
   int  thisroam;           /**< 1 if this license is a roaming license                                      */
   int  timeout;            /**< current license timeout                                                     */
   int  tz;                 /**< license timezone specification.                                             */
   int  tokens;             /**< if 0, this is a normal license. If non-zero, this is a token-based license  */
   int  type;               /**< license type (license type flags RLM_LA__xxx_TYPE are defined in license.h) */
   int  ubased;             /**< USER_BASED count                                                            */
};

/** \name Error Codes
 * \{
 */
#define AI_LIC_SUCCESS                  0   /**< no error                                  */
#define AI_LIC_ERROR_CANTCONNECT        1   /**< can't connect to any RLM server           */
#define AI_LIC_ERROR_INIT               2   /**< error on initialization                   */
#define AI_LIC_ERROR_NOTFOUND           3   /**< no licenses found (expired or not loaded) */
#define AI_LIC_ERROR_NOTAVAILABLE       4   /**< no licenses available (all in use)        */
#define AI_LIC_ERROR                   -1   /**< generic license error                     */
/*\}*/

AI_API int AiLicenseGetInfo(AtLicenseInfo*& licenses, unsigned int& n);

AI_API bool AiLicenseIsAvailable();
/*\}*/
