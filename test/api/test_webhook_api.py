import logging
import unittest
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)


class TestWebHook(TestCase):

    def test_init(self):
        v_info = self.monitoring.Webhook.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.monitoring.Webhook.verify({'options': options})


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)