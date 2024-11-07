// Copyright 2023 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

/**
 * \file
 */

#pragma once
#include "ai_api.h"
#include "ai_map.h"
#include "ai_string.h"
/**
 * \defgroup ai_adp Autodesk Analytics Program
 * \{
 */

/**
 * We can add product metadata to provide further information to e.g. track which plugin
 * and host application is authoring the render session (see \ref AiADPAddProductMetadata)
 * 
 * The following metadata names are automatically handled as part of the data analytics.
 */
#define AI_ADP_HOSTNAME       AtString("ADDIN_PARENT_NAME")
#define AI_ADP_HOSTVERSION    AtString("ADDIN_PARENT_VERSION")
#define AI_ADP_PLUGINNAME     AtString("ADDIN_NAME")
#define AI_ADP_PLUGINVERSION  AtString("ADDIN_VERSION")

enum class AtADPDialogMode { ONLY_FIRST_TIME = 1, ALWAYS = 2 };
/**
 * Display a modal window that lets the user opt-in/out of various
 * analytics.
 *
 * @param mode Set to ALWAYS to force the window to display so the user can
 * change the opt-in settings. ONLY_FIRST_TIME will only show the window if
 * there is no prior record on the user's computer nor online that they have
 * previously seen this dialog window. The default of ALWAYS is normally what
 * should be chosen as Arnold is already internally calling the ONLY_FIRST_TIME
 * variant.
 */
AI_API void AiADPDisplayDialogWindow(AtADPDialogMode mode = AtADPDialogMode::ALWAYS);

/**
 * Prevent the dialog window from opening. This is useful when running Arnold
 * on a headless computer, such as on a render farm, where a window popping up
 * cannot be easily serviced. If the opt-in dialog window is not raised, this
 * means there is no way to change the opt-in setting.
 */ 
AI_API void AiADPDisableDialogWindow();

/**
 * Set to true if user agreed to optin and false if opted out.
 */
AI_API void AiADPSetOptedIn(bool wants_optin);

/**
 * \return true if user agreed to opt in and false if opted out.
 */
AI_API bool AiADPIsOptedIn();

/**
* Provide additional data to the product analytics, such as information about the
* client that created the Arnold render session. This has to be called before
* data is collected, for instance, before \ref AiRenderBegin.
*
* This example code sets a plugin name:
* \code
* AiADPAddProductMetadata(AI_ADP_PLUGINNAME, AtString("HtoA"));
* \endcode
*
* @param name   Name for the additional product analytics data entry
* @param value  Value for the additional product analytics data entry
*/
AI_API void AiADPAddProductMetadata(AtString name, AtString value);

/*\}*/
