#ifndef BLACKSMITH_H
#define BLACKSMITH_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

// null if control flow should continue as normal, non-null if it should return early with the provided value (pointer is dereferenced)
typedef void* ControlFlowResult;

// add a hook to be called at the specified hook location. Can only be called during mod initalization; if called after mod initialization, will fail
// and crash/deload the mod.
extern void blacksmith_hook(uint32_t hook, ControlFlowResult (*callback)(...));

#include "generated_hook_constants.h"

// PROFILE_VERSION_CURRENT version - 14 maps to PROFILE_VERSION_12 which says Java 1.6.4
#define SUPPORTED_GAME_VERSION 14

#define BLACKSMITH_VERSION 0

#ifdef __cplusplus
}
#endif

#endif