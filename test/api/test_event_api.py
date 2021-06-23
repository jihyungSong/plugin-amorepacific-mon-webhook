import logging
import unittest
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json
from pprint import pprint
_LOGGER = logging.getLogger(__name__)


class TestEvent(TestCase):

    def test_parse(self):

        options = {}
        raw_data = {
            "resource_name": "aplprdebawas01",
            "urgency": "2",
            "status": "UP ",
            "host_ip": "172.28.102.12",
            "threshold": "ecp-batch.log_delivery",
            "summary": "[경고]02. ECP(APMALL&ETUDE)>APNE2-DSPPRD-A-ECP-EBAWAS-01>monitor group>ecp-batch.log_delivery - [1회 발생] 이벤트 탐지 [심각도: ERROR, 내용: [2020-09-25 07:46:32,155] [ERROR] [schedulerForBatch_Worker-21] [B2CMON_LOG.logging:124] [MON||ERROR|M02|||delivery|||2020-09-25 07:46:32,155|MLEC_EORD056|/MON] 21042564 [OrderServiceImpl.deliveryInfoMonLogging:20779 < OrderServiceImpl$$FastClassBySpringCGLIB$$3c44f530.invoke:-1 < MethodProxy.invoke:204 < CglibAopProxy$CglibMethodInvocation.invokeJoinpoint:738 < ReflectiveMethodInvocation.proceed:157]]",
            "event_time": "2020-09-25 07:46:32",
            "metric_value": "이벤트 탐지 [심각도: ERROR , 개행 포함, 내용 패턴: .*delivery.*MLEC_.*] ",
            "event_id": "21296053",
            "metric_name": "배송_경고로그 "
        }
        raw_data2 = {}
        parsed_data = self.monitoring.Event.parse({'options': options, 'data': raw_data})
        print_json(parsed_data)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)