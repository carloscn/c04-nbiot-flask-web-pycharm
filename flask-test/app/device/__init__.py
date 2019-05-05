# coding: utf-8
from flask import Blueprint

device = Blueprint('device',__name__)

from . import views