from .helpers import ConstantsCustom
import json
import requests

class PushHelper:
    def sendPushNotifications(ids, subject, content):
        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = {"app_id": ConstantsCustom.oneSignalAppID}

        payload['include_player_ids'] = ids
        payload['headings'] = {
            "en": subject,
            "ru": subject
        }
        if content is not None:
            payload['contents'] = {
                "en": content,
                "ru": content
            }
        req = requests.post(ConstantsCustom.oneSignalSendPushAPI, headers=header, data=json.dumps(payload))

        return req
