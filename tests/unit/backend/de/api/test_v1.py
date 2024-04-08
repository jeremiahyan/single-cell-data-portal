import json
import unittest
from math import log
from unittest.mock import patch

from backend.api_server.app import app
from tests.unit.backend.fixtures.environment_setup import EnvironmentSetup
from tests.unit.backend.wmg.fixtures.test_snapshot import (
    load_realistic_test_snapshot,
)

TEST_SNAPSHOT = "realistic-test-snapshot"


class DeAPIV1Tests(unittest.TestCase):
    def setUp(self):
        super().setUp()
        with EnvironmentSetup(dict(APP_NAME="corpora-api")):
            self.app = app.test_client(use_cookies=False)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.maxDiff = None

    @patch("backend.de.api.v1.load_snapshot")
    def test__differentialExpression_returns_expected_results(self, load_snapshot):
        test_cases = [
            {
                "queryGroup1Filters": {
                    "organism_ontology_term_id": "NCBITaxon:9606",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000066"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": [],
                },
                "queryGroup2Filters": {
                    "organism_ontology_term_id": "NCBITaxon:9606",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000084"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": [],
                },
            },
            {
                "queryGroup1Filters": {
                    "organism_ontology_term_id": "NCBITaxon:9606",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": [],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": ["HANCESTRO:0014"],
                    "sex_ontology_term_ids": [],
                },
                "queryGroup2Filters": {
                    "organism_ontology_term_id": "NCBITaxon:9606",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": [],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": ["HANCESTRO:0005"],
                    "sex_ontology_term_ids": [],
                },
            },
            {
                "queryGroup1Filters": {
                    "organism_ontology_term_id": "NCBITaxon:9606",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000066"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": ["HANCESTRO:0014"],
                    "sex_ontology_term_ids": [],
                },
                "queryGroup2Filters": {
                    "organism_ontology_term_id": "NCBITaxon:9606",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000084"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": ["HANCESTRO:0005"],
                    "sex_ontology_term_ids": [],
                },
            },
            {
                "queryGroup1Filters": {
                    "organism_ontology_term_id": "NCBITaxon:10090",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000115"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": [],
                },
                "queryGroup2Filters": {
                    "organism_ontology_term_id": "NCBITaxon:10090",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000169"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": [],
                },
            },
            {
                "queryGroup1Filters": {
                    "organism_ontology_term_id": "NCBITaxon:10090",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": [],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": ["PATO:0000383"],
                },
                "queryGroup2Filters": {
                    "organism_ontology_term_id": "NCBITaxon:10090",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": [],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": ["PATO:0000384"],
                },
            },
            {
                "queryGroup1Filters": {
                    "organism_ontology_term_id": "NCBITaxon:10090",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000115"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": ["PATO:0000383"],
                },
                "queryGroup2Filters": {
                    "organism_ontology_term_id": "NCBITaxon:10090",
                    "tissue_ontology_term_ids": [],
                    "cell_type_ontology_term_ids": ["CL:0000169"],
                    "publication_citations": [],
                    "disease_ontology_term_ids": [],
                    "self_reported_ethnicity_ontology_term_ids": [],
                    "sex_ontology_term_ids": ["PATO:0000384"],
                },
            },
        ]
        expected_effect_size_sums = [-425, 689, 24, 3211, 761, 3325]
        expected_t_score_sums = [-30185, 40208, -2615, -10351, 25281, -13515]
        expected_log_p_value_sums = [151838, 160395, 127387, 53251, 136980, 23265]
        with load_realistic_test_snapshot(TEST_SNAPSHOT) as snapshot:
            for i, test_case in enumerate(test_cases):
                with self.subTest(test_case=test_case):
                    load_snapshot.return_value = snapshot
                    response = self.app.post(
                        "/de/v1/differentialExpression",
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(test_case),
                    )
                    self.assertEqual(response.status_code, 200)
                    result = json.loads(response.data)
                    effect_size_sum = round(sum([i["effect_size"] for i in result["differentialExpressionResults"]]))
                    log_p_value_sum = round(
                        sum([-log(i["p_value"] + 1e-300) for i in result["differentialExpressionResults"]])
                    )
                    t_score_sum = round(sum([i["t_score"] for i in result["differentialExpressionResults"]]))
                    self.assertEqual(effect_size_sum, expected_effect_size_sums[i])
                    self.assertEqual(t_score_sum, expected_t_score_sums[i])
                    self.assertEqual(log_p_value_sum, expected_log_p_value_sums[i])
