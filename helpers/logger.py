import json
import logging

import allure
from allure_commons.types import AttachmentType
from requests import Response


def response_logging(response: Response):
    """Log response and request data to the console or log file."""
    logging.info(f"Request URL: {response.request.method} {response.request.url}")

    if response.request.body:
        try:
            body = (
                json.dumps(json.loads(response.request.body), indent=2)
                if isinstance(response.request.body, (str, bytes))
                else str(response.request.body)
            )
        except Exception:
            body = str(response.request.body)
        logging.info("Request body:\n" + body)

    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Response code: " + str(response.status_code))
    logging.info("Response body:\n" + response.text)


def response_attaching(response: Response):
    """Attach request/response info to Allure report."""
    allure.attach(
        name="Request URL",
        body=f"{response.request.method} {response.request.url}",
        attachment_type=AttachmentType.TEXT,
    )

    if response.request.body:
        try:
            body_json = json.loads(response.request.body)
            allure.attach(
                name="Request Body",
                body=json.dumps(body_json, indent=4, ensure_ascii=False),
                attachment_type=AttachmentType.JSON,
            )
        except Exception:
            allure.attach(
                name="Request Body (raw)",
                body=str(response.request.body),
                attachment_type=AttachmentType.TEXT,
            )

    allure.attach(
        name="Response Code",
        body=str(response.status_code),
        attachment_type=AttachmentType.TEXT,
    )

    try:
        response_json = response.json()
        allure.attach(
            name="Response Body",
            body=json.dumps(response_json, indent=4, ensure_ascii=False),
            attachment_type=AttachmentType.JSON,
        )
    except Exception:
        allure.attach(
            name="Response Body (raw)",
            body=response.text,
            attachment_type=AttachmentType.TEXT,
        )