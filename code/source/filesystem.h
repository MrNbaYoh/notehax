#ifndef FS_H
#define FS_H

#include <3ds.h>

typedef struct
{
	u32 id;          ///< Archive ID.
	FS_Path lowPath; ///< FS path.
	u64 handle;      ///< Handle.
} FS_archive;

Result _FSUSER_OpenFileDirectly(Handle* handle, Handle* out, FS_archive archive, FS_Path fileLowPath, u32 openflags, u32 attributes);
Result _FSFILE_Close(Handle handle);
Result _FSFILE_Read(Handle handle, u32 *bytesRead, u64 offset, u32 *buffer, u32 size);
Result _FSFILE_GetSize(Handle handle, u64 *size);

#endif
