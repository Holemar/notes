
#### dtype 参数支持的值，首字母如下:

首字母 | 含义
--- | ----
'?' | boolean
'b' | (signed) byte
'B' | unsigned byte
'i' | (signed) integer
'u' | unsigned integer
'f' | floating-point
'c' | complex-floating point
'm' | timedelta
'M' | datetime
'O' | (Python) objects
'S', 'a' | zero-terminated bytes (not recommended)
'U' | Unicode string
'V' | raw data (void)


#### dtype 参数支持的值，具体值如下:

type | type code | 含义
--- |-----------| ---
int8,uint8 | i1,u1     | 8-bit signed/unsigned integer
int16,uint16 | i2,u2     | 16-bit signed/unsigned integer
int32,uint32 | i4,u4     | 32-bit signed/unsigned integer
int64,uint64 | i8,u8     | 64-bit signed/unsigned integer
float16 | f2        | 16-bit floating-point number
float32 | f4 or f   | 32-bit floating-point number
float64 | f8 or d   | 64-bit floating-point number
float128 | f16 or g  | 128-bit floating-point number
complex64 | c8        | 64-bit complex-floating point number
complex128 | c16       | 128-bit complex floating-point number
complex256 | c32       | 256-bit complex floating-point number


dtype 值范例
```Python
import numpy as np
dt = np.dtype('u1')   # 8-bit unsigned integer
dt = np.dtype('i4')   # 32-bit signed integer
dt = np.dtype('f8')   # 64-bit floating-point number
dt = np.dtype('c16')  # 128-bit complex floating-point number
dt = np.dtype('a25')  # 25-length zero-terminated bytes
dt = np.dtype('U25')  # 25-character string
```
