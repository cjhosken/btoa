// Copyright 2022 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software in either electronic or hard copy form.

#include "ai_api.h"

/**
 * \file
 * API for the usage and configuration of customer error reporting (CER)
 */

/** \defgroup ai_error_reporting error reporting API
 *
 * Error report usage and configuration.
 *
 * \details
 * To aid in developer debugging, Arnold can process and display stack-traces
 * during the event of a crash. Arnold can also optionally send error reports to
 * Autodesk for bug collection and analysis through a subsystem called CER.
 *
 * This report generation by default utilizes an auxiliary application called
 * 'senddmp' which will display a dialog box with a list of information to be
 * sent to Autodesk for developers to analyze, as well as a request of a user
 * description of the circumstances of the crash and a contact email if they wish.
 *
 * The dialog box will appear by default during the event of a crash unless otherwise
 * configured and will remain open until a user explicitly sends or cancels the report.
 * If desired, the dialog can be disabled entirely via the API or through settings
 * in the rendering plugins or kick, or toggled via the 'ARNOLD_CER_ENABLED' environment
 * variable.
 *
 * Unless disabled, the error reporting subsystem can also be set to silently send
 * crash reports when provided a contact email address beforehand through an
 * API call or the 'ARNOLD_CER_AUTOSEND_EMAIL' environment variable, which can be
 * useful for reporting crashes from batch rendering processes and render farms.
 *
 * \{
 */

AI_API void AiErrorReportingSetEnabled(bool value);
AI_API bool AiErrorReportingGetEnabled();
AI_API void AiErrorReportingSetAutosendEmail(AtString email);
AI_API AtString AiErrorReportingGetAutosendEmail();

/*\}*/