#ifndef IMPORTS_H
#define IMPORTS_H

#include <3ds.h>
#include "../constants.h"

#define LINEAR_BUFFER 0x14000000
#define APPMEMTYPE_PTR 0x1FF80030
#define MAX_CODEBIN_SIZE 0x2D1000

static Handle* const fsHandle = (Handle*)FSUSER_HANDLE;
static Handle* const dspHandle = (Handle*)DSP_HANDLE;
static Handle* const gspHandle = (Handle*)GSPGPU_HANDLE;

static u32** const sharedGspCmdBuf = (u32**)(GSPGPU_INTERRUPT_RECEIVER_STRUCT + 0x58);

static Result (* const _GSPGPU_FlushDataCache)(Handle* handle, Handle kProcess, u32* addr, u32 size) = (void*)GSPGPU_FLUSHDATACACHE;
static Result (* const _GSPGPU_GxTryEnqueue)(u32** sharedGspCmdBuf, u32* cmdAddr) = (void*)GSPGPU_GXTRYENQUEUE;
static Result (* const _DSP_UnloadComponent)(Handle* handle) = (void*)DSP_UNLOADCOMPONENT;
static Result (* const _DSP_RegisterInterruptEvents)(Handle* handle, Handle event, u32 type, u32 port) = (void*)DSP_REGISTERINTERRUPTEVENTS;

#endif
