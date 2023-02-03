import json
import logging
import os

import requests

from backend.common.corpora_config import CorporaConfig

logger = logging.getLogger(__name__)


def notify_slack(data: dict):
    """
    This will only create a slack notification if called in the production env
    In all other envs (and in prod) it will simply log alert data
    """
    msg = json.dumps(data, indent=2)
    logger.info(f"Slack notification function called with message: {msg}")
    if os.getenv("DEPLOYMENT_STAGE") == "prod":
        slack_webhook = CorporaConfig().slack_webhook
        requests.post(slack_webhook, headers={"Content-type": "application/json"}, data=msg)


def format_failed_batch_issue_slack_alert(data: dict) -> dict:
    aws_region = os.getenv("AWS_DEFAULT_REGION")
    job_id = os.getenv("AWS_BATCH_JOB_ID")
    job_url = f"https://{aws_region}.console.aws.amazon.com/batch/v2/home?region={aws_region}#jobs/detail/{job_id}"
    batch_data = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Batch processing job failed! @sc-oncall-eng\n" f"*Batch Job ID*:<{job_url}|{job_id}>\n",
        },
    }
    data["blocks"].append(batch_data)

    return data


def gen_wmg_pipeline_failure_message(failure_info: str) -> dict:
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"WMG Snapshot Generation Pipeline FAILED:fire: @sc-oncall-eng \n{failure_info}",
                    "emoji": True,
                },
            }
        ]
    }


def gen_wmg_pipeline_success_message(snapshot_path: str, dataset_count: int, cell_count: int, gene_count: int) -> dict:
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"WMG Snapshot Generation Pipeline Succeeded:tada: "
                    f"\n* WMG snapshot stored in {snapshot_path}"
                    f"\n* The cube contains {cell_count} cells from {dataset_count} "
                    f"\n  datasets, with expression scores across {gene_count} genes.",
                    "emoji": True,
                },
            }
        ]
    }
