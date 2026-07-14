import unittest
from tde_runtime.query import QueryEngine

class QueryTests(unittest.TestCase):
    def test_filter_aggregation_and_projection(self):
        evidence={"repository":{"id":"repo"},"measurements":[{"metricKey":"a","value":1},{"metricKey":"b","value":2}],"capabilityResults":[],"findings":[],"policyEvidence":{}}
        result=QueryEngine().execute(evidence,{"resource":"metrics","filter":{"metricKey":"a"},"projection":["metricKey"]})
        self.assertEqual([{"metricKey":"a"}],result["results"])
        self.assertEqual(1,result["queryEvidence"]["resultCount"])
