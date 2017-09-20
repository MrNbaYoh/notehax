#ifndef UTILS_H
#define UTILS_H

#include <3ds.h>

void* memset(void * ptr, int value, size_t num);
void* memcpy(void *destination, const void *source, size_t num);
int memcmp(void *ptr1, void *ptr2, size_t num);

Result gspwn(void* dst, void* src, u32 size);
Result _GSPGPU_SetBufferSwap(Handle handle, u32 screenId, GSPGPU_FramebufferInfo framebufferInfo);
unsigned int _strlen(const char* str);

FS_Path _fsMakePath(FS_PathType type, const void* path);
#endif
