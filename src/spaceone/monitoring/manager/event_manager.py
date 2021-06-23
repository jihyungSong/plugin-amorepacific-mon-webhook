import re
import logging
import hashlib
from spaceone.core import utils
from spaceone.core.manager import BaseManager
from datetime import datetime
from spaceone.monitoring.model.event_response_model import EventModel
_LOGGER = logging.getLogger(__name__)

TITLE_PARSING_META = [' - ']
_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, raw_data):
        """
            {
                "resource_name": "aplprdebawas01",
                "urgency": "2",
                "status": "UP",
                "host_ip": "172.28.102.12",
                "threshold": "ecp-batch.log_delivery",
                "summary": "[경고]02. ECP(APMALL&ETUDE)>APNE2-DSPPRD-A-ECP-EBAWAS-01>monitor group>ecp-batch.log_delivery - [1회 발생] 이벤트 탐지 [심각도: ERROR, 내용: [2020-09-25 07:46:32,155] [ERROR] [schedulerForBatch_Worker-21] [B2CMON_LOG.logging:124] [MON||ERROR|M02|||delivery|||2020-09-25 07:46:32,155|MLEC_EORD056|/MON] 21042564 [OrderServiceImpl.deliveryInfoMonLogging:20779 < OrderServiceImpl$$FastClassBySpringCGLIB$$3c44f530.invoke:-1 < MethodProxy.invoke:204 < CglibAopProxy$CglibMethodInvocation.invokeJoinpoint:738 < ReflectiveMethodInvocation.proceed:157]]",
                "event_time": "2020-09-25 07:46:32",
                "metric_value": "이벤트 탐지 [심각도: ERROR , 개행 포함, 내용 패턴: .*delivery.*MLEC_.*] ",
                "event_id": "21296053",
                "metric_name": "배송_경고로그 "
            }

        """
        default_parsed_data_list = []

        event_key = raw_data.get('event_id')
        ip_address = raw_data.get('host_ip')
        resource_id = raw_data.get('resource_name')
        metric_value = raw_data.get('metric_value')
        summary = raw_data.get('summary')
        event_resource_vo = {}

        try:

            if ip_address is not None:
                event_resource_vo.update({'ip_address': ip_address})

            if resource_id is not None:
                event_resource_vo.update({'resource_id': resource_id})
                event_resource_vo.update({'name': f'{resource_id}'})

            parsed_summary = self._parse_summary(summary)

            event_vo = {
                'event_key': event_key,
                'event_type': 'ALERT',
                'severity': 'CRITICAL',
                'resource': event_resource_vo,
                'description': parsed_summary.get('body'),
                'title': parsed_summary.get('title'),
                'rule': metric_value,
                'occurred_at': self._occurred_at(raw_data),
                'additional_info': {}
            }

            _LOGGER.debug(f'[EventManager] parse Event : {event_vo}')

            event_result_model = EventModel(event_vo, strict=False)
            event_result_model.validate()
            event_result_model_native = event_result_model.to_native()
            default_parsed_data_list.append(event_result_model_native)

        except Exception as e:
            generated = utils.generate_id('amore-pacific', 4)
            hash_object = hashlib.md5(generated.encode())
            md5_hash = hash_object.hexdigest()
            error_message = repr(e)
            event_vo = {
                'event_key': md5_hash,
                'event_type': 'ALERT',
                'severity': 'CRITICAL',
                'resource': {},
                'description': error_message,
                'title': 'AmorePacific Parsing ERROR',
                'rule': '',
                'occurred_at': datetime.now(),
                'additional_info': {}
            }
            event_result_model = EventModel(event_vo, strict=False)
            event_result_model.validate()
            event_result_model_native = event_result_model.to_native()
            default_parsed_data_list.append(event_result_model_native)

        return default_parsed_data_list

    @staticmethod
    def _occurred_at(raw_data):
        current_time = datetime.now()
        occurred_at = raw_data.get('event_time', current_time)
        parsed_occurred_at = None
        try:
            if isinstance(occurred_at, datetime):
                parsed_occurred_at = occurred_at
            else:
                timestamp_str = occurred_at.split(' ')
                if len(timestamp_str) != 2:
                    parsed_occurred_at = current_time
                else:
                    date_object = datetime.strptime(f'{timestamp_str[0]}T{timestamp_str[1]}', _TIMESTAMP_FORMAT)
                    parsed_occurred_at = date_object
        except Exception as e:
            parsed_occurred_at = datetime.now()

        _LOGGER.debug(f'[EventManager] _occurred_at : {parsed_occurred_at}')
        return parsed_occurred_at

    @staticmethod
    def _parse_summary(raw_data_summary):
        parsed_summary = {}
        if raw_data_summary is not None:
            first_parsing_index = re.search(r"\d", raw_data_summary)
            if first_parsing_index is not None:
                title_first_idx = first_parsing_index.start()
                title_last_idx = None
                for meta in TITLE_PARSING_META:
                    parse_temp_meta = raw_data_summary.find(meta)
                    if parse_temp_meta > -1:
                        title_last_idx = parse_temp_meta
                        break

            title = raw_data_summary[title_first_idx:title_last_idx]
            parsed_summary.update({
                'title': title,
                'body': raw_data_summary[title_last_idx + 1:]
            })
        return parsed_summary
