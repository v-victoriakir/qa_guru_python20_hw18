import json
import logging

import allure
from allure_commons.types import AttachmentType
from requests import Response


def response_logging(response: Response):
    logging.info("Request: " + response.request.url)
    if response.request.body:
        logging.info("INFO Request body: " + response.request.body)  # логирование тела запроса если оно есть
    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)


def response_attaching(response: Response):
    allure.attach(
        body=response.request.url,
        name="Request url",
        attachment_type=AttachmentType.TEXT,
    )

    if response.request.body:  # логирование тела запроса если оно есть
        allure.attach(
            body=json.dumps(response.request.body, indent=4, ensure_ascii=True),
            name="Request body",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )
        allure.attach(
            body=json.dumps(response.json(), indent=4, ensure_ascii=True),
            name="Response",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )
        allure.attach(
            body=f'Method: {response.request.method}\nURL: {response.request.url}',
            name='Request Info',
            attachment_type=AttachmentType.TEXT,
            extension='txt'
        )
        allure.attach(
            body=f'Status code: {response.status_code}',
            name='Response status code',
            attachment_type=AttachmentType.TEXT,
            extension='txt'
        )
