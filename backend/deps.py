from fastapi import Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer

import typing
import jwt

from pydantic import ValidationError

from . import models
from . import security
from . import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")