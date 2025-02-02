import gzip
import json
import os
from collections import defaultdict

from backend.cellguide.common.config import CellGuideConfig
from backend.cellguide.common.constants import COMPUTATIONAL_MARKER_GENES_FOLDERNAME, MARKER_GENE_PRESENCE_FILENAME
from backend.cellguide.common.providers.s3_provider import S3Provider
from backend.cellguide.common.utils import get_object_key

_marker_gene_data_cache = None


def _defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        # Convert the defaultdict to a dict and recursively apply this function
        return {key: _defaultdict_to_dict(value) for key, value in d.items()}
    else:
        return d


def _initialize_cellguide_marker_gene_dict():
    bucket = CellGuideConfig().bucket
    s3_provider = S3Provider()

    latest_snapshot_identifier = (
        s3_provider.download_file(bucket_name=bucket, object_key=get_object_key(object="latest_snapshot_identifier"))
        .decode("utf-8")
        .strip()
    )
    compressed_data = s3_provider.download_file(
        bucket_name=bucket,
        object_key=get_object_key(
            object=f"{latest_snapshot_identifier}/{COMPUTATIONAL_MARKER_GENES_FOLDERNAME}/{MARKER_GENE_PRESENCE_FILENAME}"
        ),
    )
    marker_gene_data = json.loads(gzip.decompress(compressed_data).decode("utf-8"))

    return format_marker_gene_data(marker_gene_data)


def format_marker_gene_data(marker_gene_data):
    """
    Reformat the raw marker gene data into a structured dictionary.

    The function transforms the raw marker gene data into a nested dictionary format organized by organism, tissue,
    and cell type, where each cell type contains a list of marker genes with their respective scores and properties.

    Parameters:
        marker_gene_data (dict): The raw marker gene data loaded from JSON, expected to have a structure where each
                                 gene is mapped to organisms, which in turn map to tissues, and then to a list of
                                 marker details.

    Returns:
        dict: A nested dictionary with the structure {organism: {tissue: {cell_type_id: [marker details]}}}.
              Each marker detail is a dictionary containing the gene, marker score, and other properties.
    """

    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for gene in marker_gene_data:
        for organism in marker_gene_data[gene]:
            for tissue in marker_gene_data[gene][organism]:
                for marker in marker_gene_data[gene][organism][tissue]:
                    data[organism][tissue][marker["cell_type_id"]].append(
                        {"marker_score": marker["marker_score"], "me": marker["me"], "pc": marker["pc"], "gene": gene}
                    )

    data = _defaultdict_to_dict(data)

    for organism in data:
        for tissue in data[organism]:
            for cell_type in data[organism][tissue]:
                data[organism][tissue][cell_type].sort(key=lambda x: -x["marker_score"])

    return data


def get_marker_gene_data():
    global _marker_gene_data_cache
    if _marker_gene_data_cache is None:
        if os.getenv("DEPLOYMENT_STAGE") != "test":
            # Initialize the marker gene data from the latest snapshot only if not in test mode
            _marker_gene_data_cache = _initialize_cellguide_marker_gene_dict()
        else:
            # Initialize an empty structure if in test mode
            _marker_gene_data_cache = {}
    return _marker_gene_data_cache
