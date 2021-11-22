
from flask import request, jsonify, Blueprint
import logging

from api.integrations.nalog_ru import NalogRuApi
from api.api import auth, jsonbody, query_params, features

logger = logging.getLogger(name="external_auth")

external_auth_api = Blueprint('external_auth', __name__)


@external_auth_api.route('/api/v1/nalog/otp/send', methods=['POST'])
@auth()
def send_otp():
    nalog_ru_api.send_otp_sms(user_id=getattr(request, "user_id"))
    return jsonify("Ok"), 200


@external_auth_api.route('/api/v1/nalog/otp/verify', methods=['POST'])
@auth()
@jsonbody(otp=features(type=str, required=True))
def verify_otp(otp: str):
    nalog_ru_api.verify_otp(user_id=getattr(request, "user_id"), otp=otp)
    return jsonify("Ok"), 200


nalog_ru_api = NalogRuApi()

