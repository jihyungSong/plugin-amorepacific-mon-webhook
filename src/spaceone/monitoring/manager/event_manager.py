import re
import logging
import hashlib
from spaceone.core import utils
from spaceone.core.manager import BaseManager
from datetime import datetime
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *

_LOGGER = logging.getLogger(__name__)

TITLE_PARSING_META = [' - ']

class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, raw_data):

        results = []
        # resource_name ip or id or name
        try:
            summary = self._remove_blank(raw_data.get('summary', ''))
            metric_name = self._remove_blank(raw_data.get('metric_name', ''))
            host_ip = self._remove_blank(raw_data.get('host_ip', ''))
            severity = self._get_severity(self, raw_data.get('severity', ''))
            event_key = self._get_event_key(summary, metric_name, host_ip)
            event_type = self._get_event_type(severity)
            description = raw_data.get('conditionlog', '')
            resource = self._get_resource(raw_data)
            occured_at = self._get_occurred_at(raw_data.get('event_time', datetime.now()))
            additional_info = self._get_additional_info(self, raw_data)

            event_dict = {
                'event_key': event_key,
                'event_type': event_type,
                'severity': severity,
                'resource': resource,
                'description': description,
                'title': summary,
                'rule': metric_name,
                'occurred_at': occured_at,
                'additional_info': additional_info
            }
            event_vo = self._validate_parsed_event(event_dict)
            results.append(event_vo)
            _LOGGER.debug(f'[EventManager] parse Event : {event_dict}')
            return results

        except Exception as e:
            '''
            generated = utils.generate_id('amore-pacific', 4)
            hash_object = hashlib.md5(generated.encode())
            md5_hash = hash_object.hexdigest()
            error_message = repr(e)

            event_dict = {
                'event_key': md5_hash,
                'event_type': 'ERROR',
                'severity': 'CRITICAL',
                'resource': {},
                'description': error_message,
                'title': 'AmorePacific Parsing ERROR',
                'rule': '',
                'occurred_at': datetime.now(),
                'additional_info': {}
            }
            event_vo = self._validate_parsed_event(event_dict)
            results.append(event_vo)
            _LOGGER.debug(f'[EventManager] parse Event(parsingError) : {event_dict}')
            return results
            '''

    @staticmethod
    def _get_occurred_at(event_time):
        occurred_at = event_time

        try:
            if not isinstance(occurred_at, datetime):
                timestamp_str = occurred_at.split(' ')
                if len(timestamp_str) != 2:
                    occurred_at = datetime.now()
                else:
                    date_object = datetime.strptime(f'{timestamp_str[0]}T{timestamp_str[1]}', '%Y-%m-%dT%H:%M:%S')
                    occurred_at = date_object

            _LOGGER.debug(f'[EventManager] _occurred_at : {occurred_at}')
            print(type(occurred_at))
            return occurred_at

        except Exception as e:
            parsed_occurred_at = datetime.now()
            _LOGGER.error(f'[EventManager] _occurred_at : {parsed_occurred_at} due to {e}')


    @staticmethod
    def _get_event_key(summary, metric_name, host_ip):
        event_key_base = f'{summary}' + f'{metric_name}' + f'{host_ip}'
        hash_object = hashlib.md5(event_key_base.encode())
        md5_hash = hash_object.hexdigest()

        return md5_hash

    @staticmethod
    def _get_severity(self, severity):  # TODO: NOT AVAILABLE..?
        """
               심각 : CRITICAL
               경고 : ERROR
               주의 : WARNING
               해제: INFO
               CRITICAL | ERROR | WARNING | INFO | NOT_AVAILABLE | NONE(default)
               ------
               """
        severity = self._remove_blank(severity)

        severity_flag = 'NONE'

        if severity == '심각':
            severity_flag = 'CRITICAL'
        elif severity == '경고':
            severity_flag = 'ERROR'
        elif severity == '주의':
            severity_flag = 'WARNING'
        elif severity == '해제':
            severity_flag = 'INFO'

        return severity_flag

    @staticmethod
    def _get_resource(raw_data):
        resource_info = {}
        if 'host_ip' in raw_data:
            resource_info.update({'name': raw_data.get('host_ip')})

        elif 'resource_name' in raw_data:
            resource_info.update({'name': raw_data.get('resource_name')})

        return resource_info

    @staticmethod
    def _get_event_type(severity):
        event_type = 'ALERT'
        if severity in ['심각', '경고', '주의']:
            event_type = 'ALERT'
        elif severity == '해제':
            event_type = 'RECOVERY'

        return event_type

    @staticmethod
    def _validate_parsed_event(event_dict):
        try:
            event_result_model = EventModel(event_dict, strict=False)
            event_result_model.validate()
            event_result_model_primitive = event_result_model.to_native()
            return event_result_model_primitive

        except Exception as e:
            raise ERROR_CHECK_VALIDITY(field=e)

    @staticmethod
    def _get_additional_info(self, raw_data):
        raw_data_key_set = ['event_id', 'status', 'threshold', 'urgency', 'metric_value', 'metric_name']
        additional_info = {}
        for raw_data_key in raw_data_key_set:
            if raw_data_key in raw_data and isinstance(raw_data.get(raw_data_key), str):
                additional_trimmed_data = self._remove_blank(raw_data.get(raw_data_key))
                additional_info.update({raw_data_key: additional_trimmed_data})

        return additional_info

    @staticmethod
    def _remove_blank(data):
        return data.replace(" ", "")