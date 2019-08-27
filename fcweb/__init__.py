__version__ = '0.2.4'

from .fcweb import (
    fcIndex, get, post, put, delete
)

from .right import (
    isLogin, getTokenFromHeader, getDB, decode, updateToken, authRight, getBodyAsJson, getBodyAsStr, encodeToken, 
)

from .response import ResponseEntity

from .utils import responseFormat, pathMatch, createId