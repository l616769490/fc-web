__version__ = '0.6.0'

from .connect import (
    getDB, getRedis, userCode2Session, guideCode2Session
)

from .constant import (
    getConfByName, initConfCenter
)

from .fcweb import (
    fcIndex, get, post, put, delete
)

from .right import (
    isLogin, getTokenFromHeader, getPayloadFromHeader, getDB, decode, updateToken, authRight, getBodyAsJson, getBodyAsStr, encodeToken
)

from .response import ResponseEntity

from .utils import pathMatch, createId

from .sign import (
    Sign
)