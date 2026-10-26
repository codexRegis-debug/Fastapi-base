from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import json
import urllib.request
import urllib.errror
from my_app.data.my_base import get_db
from my_app.ai_models_checkpoint.models import AICheckPoint
from my_app.ai_models_checkpoint.schemas import CheckPointRegister, PredictRequest

router = APIRouter(prefix='/ai', tags=['ai_checkpoint'])

def _post_json(
    url: str,
    payload: dict,
    timeout=30,
):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout)s resp:
            body = resp.read().decode('utf-8')
            return json.loads(body)
        except urllib.error.URLError as e:
            raise e

def _get_json(url: str, timeout=2):
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode('utf-8')
        return json.loads(body), resp.status
