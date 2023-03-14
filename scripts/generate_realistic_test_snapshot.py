import json
import os
import sys

import tiledb

from backend.wmg.data.snapshot import (
    DATASET_TO_GENE_IDS_FILENAME,
    FILTER_RELATIONSHIPS_FILENAME,
)
from backend.wmg.pipeline.summary_cubes.cell_count import create_filter_relationships_graph
from backend.wmg.pipeline.summary_cubes.marker_genes import create_marker_genes_cube

test_tissue = "UBERON:0002048"
test_organism = "NCBITaxon:9606"
test_genes = [
    "ENSG00000256480",
    "ENSG00000254037",
    "ENSG00000206862",
    "ENSG00000241853",
    "ENSG00000280809",
    "ENSG00000151012",
    "ENSG00000230184",
    "ENSG00000171067",
    "ENSG00000103942",
    "ENSG00000275025",
    "ENSG00000228784",
    "ENSG00000249425",
    "ENSG00000143412",
    "ENSG00000139266",
    "ENSG00000163421",
    "ENSG00000146809",
    "ENSG00000116473",
    "ENSG00000203729",
    "ENSG00000259863",
    "ENSG00000279500",
    "ENSG00000256658",
    "ENSG00000272334",
    "ENSG00000100122",
    "ENSG00000235548",
    "ENSG00000233894",
    "ENSG00000121075",
    "ENSG00000204792",
    "ENSG00000259410",
    "ENSG00000171311",
    "ENSG00000236564",
    "ENSG00000277617",
    "ENSG00000130479",
    "ENSG00000232383",
    "ENSG00000237389",
    "ENSG00000104341",
    "ENSG00000124143",
    "ENSG00000177706",
    "ENSG00000278819",
    "ENSG00000273415",
    "ENSG00000255992",
    "ENSG00000179476",
    "ENSG00000143473",
    "ENSG00000102271",
    "ENSG00000118729",
    "ENSG00000112319",
    "ENSG00000237292",
    "ENSG00000226854",
    "ENSG00000164896",
    "ENSG00000284197",
    "ENSG00000088836",
    "ENSG00000167065",
    "ENSG00000245060",
    "ENSG00000227002",
    "ENSG00000265429",
    "ENSG00000255395",
    "ENSG00000214243",
    "ENSG00000257195",
    "ENSG00000286369",
    "ENSG00000092929",
    "ENSG00000261429",
    "ENSG00000139220",
    "ENSG00000115459",
    "ENSG00000174807",
    "ENSG00000227825",
    "ENSG00000099958",
    "ENSG00000173702",
    "ENSG00000118976",
    "ENSG00000257509",
    "ENSG00000226686",
    "ENSG00000279637",
    "ENSG00000249084",
    "ENSG00000270702",
    "ENSG00000165078",
    "ENSG00000236411",
    "ENSG00000249275",
    "ENSG00000251090",
    "ENSG00000224289",
    "ENSG00000117133",
    "ENSG00000164742",
    "ENSG00000070526",
    "ENSG00000227070",
    "ENSG00000103227",
    "ENSG00000256314",
    "ENSG00000223046",
    "ENSG00000108242",
    "ENSG00000228067",
    "ENSG00000207784",
    "ENSG00000127526",
    "ENSG00000285835",
    "ENSG00000139155",
    "ENSG00000243960",
    "ENSG00000213079",
    "ENSG00000186818",
    "ENSG00000197272",
    "ENSG00000272420",
    "ENSG00000223387",
    "ENSG00000141979",
    "ENSG00000249148",
    "ENSG00000197461",
    "ENSG00000283503",
    "ENSG00000284708",
    "ENSG00000130368",
    "ENSG00000113734",
    "ENSG00000255648",
    "ENSG00000265544",
    "ENSG00000173992",
    "ENSG00000186197",
    "ENSG00000188372",
    "ENSG00000111450",
    "ENSG00000163029",
    "ENSG00000134970",
    "ENSG00000222267",
    "ENSG00000133135",
    "ENSG00000232486",
    "ENSG00000051108",
    "ENSG00000159516",
    "ENSG00000100445",
    "ENSG00000092054",
    "ENSG00000118363",
    "ENSG00000152952",
    "ENSG00000227838",
    "ENSG00000147459",
    "ENSG00000257135",
    "ENSG00000264176",
    "ENSG00000249006",
    "ENSG00000137225",
    "ENSG00000197617",
    "ENSG00000243297",
    "ENSG00000253964",
    "ENSG00000248227",
    "ENSG00000197312",
    "ENSG00000259881",
    "ENSG00000100744",
    "ENSG00000148690",
    "ENSG00000256288",
    "ENSG00000286246",
    "ENSG00000106554",
    "ENSG00000279903",
    "ENSG00000232286",
    "ENSG00000207308",
    "ENSG00000100473",
    "ENSG00000273312",
    "ENSG00000148824",
    "ENSG00000264236",
    "ENSG00000235549",
    "ENSG00000237676",
    "ENSG00000239511",
    "ENSG00000254272",
    "ENSG00000109790",
    "ENSG00000253295",
    "ENSG00000170476",
    "ENSG00000226519",
    "ENSG00000207245",
    "ENSG00000186940",
    "ENSG00000285043",
    "ENSG00000250365",
    "ENSG00000152061",
    "ENSG00000177535",
    "ENSG00000220267",
    "ENSG00000227155",
    "ENSG00000275291",
    "ENSG00000251555",
    "ENSG00000254261",
    "ENSG00000235904",
    "ENSG00000229155",
    "ENSG00000078403",
    "ENSG00000224137",
    "ENSG00000214145",
    "ENSG00000106367",
    "ENSG00000115109",
    "ENSG00000031698",
    "ENSG00000265450",
    "ENSG00000170296",
    "ENSG00000268288",
    "ENSG00000204253",
    "ENSG00000237781",
    "ENSG00000223350",
    "ENSG00000259437",
    "ENSG00000144119",
    "ENSG00000226131",
    "ENSG00000254914",
    "ENSG00000135940",
    "ENSG00000145781",
    "ENSG00000224812",
    "ENSG00000286212",
    "ENSG00000168746",
    "ENSG00000220842",
    "ENSG00000181097",
    "ENSG00000255071",
    "ENSG00000203993",
    "ENSG00000179270",
    "ENSG00000267641",
    "ENSG00000100219",
    "ENSG00000254166",
    "ENSG00000275005",
    "ENSG00000155034",
    "ENSG00000259754",
    "ENSG00000181355",
    "ENSG00000253114",
    "ENSG00000201184",
    "ENSG00000260914",
    "ENSG00000224957",
    "ENSG00000165113",
    "ENSG00000201342",
    "ENSG00000224080",
    "ENSG00000006788",
    "ENSG00000239641",
    "ENSG00000266885",
    "ENSG00000279174",
    "ENSG00000168028",
    "ENSG00000125740",
    "ENSG00000274986",
    "ENSG00000140534",
    "ENSG00000253953",
    "ENSG00000147036",
    "ENSG00000088179",
    "ENSG00000177257",
    "ENSG00000255537",
    "ENSG00000169618",
    "ENSG00000258044",
    "ENSG00000268751",
    "ENSG00000230869",
    "ENSG00000212455",
    "ENSG00000229921",
    "ENSG00000249025",
    "ENSG00000226098",
    "ENSG00000273262",
    "ENSG00000264840",
    "ENSG00000177324",
    "ENSG00000102158",
    "ENSG00000182162",
    "ENSG00000236404",
    "ENSG00000206737",
    "ENSG00000142065",
    "ENSG00000231084",
    "ENSG00000179676",
    "ENSG00000252581",
    "ENSG00000239494",
    "ENSG00000122483",
    "ENSG00000132004",
    "ENSG00000217746",
    "ENSG00000218336",
    "ENSG00000067840",
    "ENSG00000177803",
    "ENSG00000282916",
    "ENSG00000286000",
    "ENSG00000222667",
    "ENSG00000099203",
    "ENSG00000271151",
    "ENSG00000279294",
    "ENSG00000111846",
    "ENSG00000238042",
    "ENSG00000113580",
    "ENSG00000163623",
    "ENSG00000152818",
    "ENSG00000232341",
    "ENSG00000082512",
    "ENSG00000112874",
    "ENSG00000180879",
    "ENSG00000166073",
    "ENSG00000067646",
    "ENSG00000259847",
    "ENSG00000265810",
    "ENSG00000259570",
    "ENSG00000248592",
    "ENSG00000278576",
    "ENSG00000161547",
    "ENSG00000234915",
    "ENSG00000277423",
    "ENSG00000102007",
    "ENSG00000221040",
    "ENSG00000249378",
    "ENSG00000196544",
    "ENSG00000133460",
    "ENSG00000258169",
    "ENSG00000044459",
    "ENSG00000226978",
    "ENSG00000260430",
    "ENSG00000224189",
    "ENSG00000203883",
    "ENSG00000248791",
    "ENSG00000213791",
    "ENSG00000231689",
    "ENSG00000265366",
    "ENSG00000279811",
    "ENSG00000152380",
    "ENSG00000259773",
    "ENSG00000229447",
    "ENSG00000280040",
    "ENSG00000002330",
    "ENSG00000132254",
    "ENSG00000113318",
    "ENSG00000278768",
    "ENSG00000251445",
    "ENSG00000242107",
    "ENSG00000136932",
    "ENSG00000259843",
    "ENSG00000270296",
    "ENSG00000206104",
    "ENSG00000261529",
    "ENSG00000258794",
    "ENSG00000268521",
    "ENSG00000200885",
    "ENSG00000133454",
    "ENSG00000179031",
    "ENSG00000084072",
    "ENSG00000125337",
    "ENSG00000116128",
    "ENSG00000275995",
    "ENSG00000244187",
    "ENSG00000134285",
    "ENSG00000106302",
    "ENSG00000200840",
    "ENSG00000244462",
    "ENSG00000280650",
    "ENSG00000075415",
    "ENSG00000239023",
    "ENSG00000251792",
    "ENSG00000238829",
    "ENSG00000166897",
    "ENSG00000243926",
    "ENSG00000248394",
    "ENSG00000268650",
    "ENSG00000200389",
    "ENSG00000248491",
    "ENSG00000253448",
    "ENSG00000199552",
    "ENSG00000160785",
    "ENSG00000254109",
    "ENSG00000143442",
    "ENSG00000211592",
    "ENSG00000122025",
    "ENSG00000159128",
    "ENSG00000181894",
    "ENSG00000153820",
    "ENSG00000224481",
    "ENSG00000269950",
    "ENSG00000279720",
    "ENSG00000183690",
    "ENSG00000117152",
    "ENSG00000166562",
    "ENSG00000260619",
    "ENSG00000116690",
    "ENSG00000092820",
    "ENSG00000213033",
    "ENSG00000116127",
    "ENSG00000237361",
    "ENSG00000158636",
    "ENSG00000286796",
    "ENSG00000135097",
    "ENSG00000248489",
    "ENSG00000257520",
    "ENSG00000249169",
    "ENSG00000280339",
    "ENSG00000240043",
    "ENSG00000199764",
    "ENSG00000236252",
    "ENSG00000186918",
    "ENSG00000104901",
    "ENSG00000119326",
    "ENSG00000213296",
    "ENSG00000261049",
    "ENSG00000225264",
    "ENSG00000255871",
    "ENSG00000174776",
    "ENSG00000207864",
    "ENSG00000267299",
    "ENSG00000230686",
    "ENSG00000271849",
    "ENSG00000256660",
    "ENSG00000261419",
    "ENSG00000179409",
    "ENSG00000171612",
    "ENSG00000225358",
    "ENSG00000130270",
    "ENSG00000278952",
    "ENSG00000224592",
    "ENSG00000201003",
    "ENSG00000172732",
    "ENSG00000186184",
    "ENSG00000267589",
    "ENSG00000267179",
    "ENSG00000143952",
    "ENSG00000104435",
    "ENSG00000255075",
    "ENSG00000259070",
    "ENSG00000119865",
    "ENSG00000207638",
    "ENSG00000221604",
    "ENSG00000266941",
    "ENSG00000232113",
    "ENSG00000211721",
    "ENSG00000204930",
    "ENSG00000241884",
    "ENSG00000265995",
    "ENSG00000101189",
    "ENSG00000228981",
    "ENSG00000265206",
    "ENSG00000273407",
    "ENSG00000142197",
    "ENSG00000267646",
    "ENSG00000224282",
    "ENSG00000152454",
    "ENSG00000109171",
    "ENSG00000274209",
    "ENSG00000283828",
    "ENSG00000215467",
    "ENSG00000239880",
    "ENSG00000255780",
    "ENSG00000286707",
    "ENSG00000130653",
    "ENSG00000143622",
    "ENSG00000260231",
    "ENSG00000250447",
    "ENSG00000188021",
    "ENSG00000187242",
    "ENSG00000070831",
    "ENSG00000121879",
    "ENSG00000228360",
    "ENSG00000283376",
    "ENSG00000285900",
    "ENSG00000249846",
    "ENSG00000228739",
    "ENSG00000221148",
    "ENSG00000272829",
    "ENSG00000170542",
    "ENSG00000035115",
    "ENSG00000252553",
    "ENSG00000271841",
    "ENSG00000188512",
    "ENSG00000122417",
    "ENSG00000166224",
    "ENSG00000279422",
    "ENSG00000133424",
    "ENSG00000163568",
    "ENSG00000200327",
    "ENSG00000132465",
    "ENSG00000199886",
    "ENSG00000267686",
    "ENSG00000279149",
    "ENSG00000268794",
    "ENSG00000128683",
    "ENSG00000177679",
    "ENSG00000254118",
    "ENSG00000211873",
    "ENSG00000184661",
    "ENSG00000267881",
    "ENSG00000286234",
    "ENSG00000211861",
    "ENSG00000210154",
    "ENSG00000240342",
    "ENSG00000177990",
    "ENSG00000226049",
    "ENSG00000250887",
    "ENSG00000224349",
    "ENSG00000125498",
    "ENSG00000259075",
    "ENSG00000248790",
    "ENSG00000179388",
    "ENSG00000232118",
    "ENSG00000169203",
    "ENSG00000230897",
    "ENSG00000267119",
    "ENSG00000204709",
    "ENSG00000221932",
    "ENSG00000175728",
    "ENSG00000178078",
    "ENSG00000133112",
    "ENSG00000276436",
    "ENSG00000115137",
    "ENSG00000271947",
    "ENSG00000224331",
    "ENSG00000276043",
    "ENSG00000179256",
    "ENSG00000135778",
    "ENSG00000258386",
    "ENSG00000255422",
    "ENSG00000243199",
    "ENSG00000115687",
    "ENSG00000125844",
    "ENSG00000049167",
    "ENSG00000237328",
    "ENSG00000110169",
    "ENSG00000280016",
    "ENSG00000283509",
    "ENSG00000257754",
    "ENSG00000237377",
    "ENSG00000140553",
    "ENSG00000138769",
    "ENSG00000183908",
    "ENSG00000167612",
    "ENSG00000275613",
    "ENSG00000250376",
    "ENSG00000144290",
    "ENSG00000230859",
    "ENSG00000234360",
    "ENSG00000182568",
    "ENSG00000048545",
    "ENSG00000129204",
    "ENSG00000199291",
    "ENSG00000102802",
    "ENSG00000173110",
    "ENSG00000210107",
    "ENSG00000229275",
    "ENSG00000253792",
    "ENSG00000206785",
    "ENSG00000237580",
    "ENSG00000139438",
    "ENSG00000283999",
    "ENSG00000284430",
]

if __name__ == "__main__":
    snapshot = sys.argv[1]
    new_snapshot = sys.argv[2]

    if not os.path.isdir(new_snapshot):
        os.mkdir(new_snapshot)

    with tiledb.open(f"{snapshot}/expression_summary") as es_arr, tiledb.open(
        f"{snapshot}/expression_summary_fmg"
    ) as esfmg_arr, tiledb.open(f"{snapshot}/expression_summary_default") as es_def_arr, tiledb.open(
        f"{snapshot}/expression_summary_fmg"
    ) as esfmg_arr, tiledb.open(
        f"{snapshot}/cell_counts"
    ) as cc_arr, open(
        f"{snapshot}/dataset_to_gene_ids.json", "r"
    ) as dtg_file:
        print("Subsetting existing snapshot...")
        es = es_arr.df[(test_genes, test_tissue, [], test_organism)]
        esdef = es_def_arr.df[(test_genes, test_tissue, test_organism)]
        esfmg = esfmg_arr.query(attr_cond=tiledb.QueryCondition(f"gene_ontology_term_id in {test_genes}")).df[
            (test_tissue, test_organism, [])
        ]
        cc = cc_arr.df[(test_tissue, [], test_organism)]
        filter_relationships = create_filter_relationships_graph(cc)

        print("Creating new snapshot...")
        with open(f"{new_snapshot}/{FILTER_RELATIONSHIPS_FILENAME}", "w") as new_fr_file:
            json.dump(filter_relationships, new_fr_file)

        tiledb.Array.create(f"{new_snapshot}/expression_summary", es_arr.schema, overwrite=True)
        tiledb.Array.create(f"{new_snapshot}/expression_summary_fmg", esfmg_arr.schema, overwrite=True)
        tiledb.Array.create(f"{new_snapshot}/expression_summary_default", es_def_arr.schema, overwrite=True)
        tiledb.Array.create(f"{new_snapshot}/cell_counts", cc_arr.schema, overwrite=True)

        tiledb.from_pandas(f"{new_snapshot}/expression_summary", es, mode="append")
        tiledb.from_pandas(f"{new_snapshot}/expression_summary_fmg", esfmg, mode="append")
        tiledb.from_pandas(f"{new_snapshot}/expression_summary_default", esdef, mode="append")
        tiledb.from_pandas(f"{new_snapshot}/cell_counts", cc, mode="append")

        dtg = json.load(dtg_file)
        genes = set(es["gene_ontology_term_id"])
        for k in dtg:
            dtg[k] = list(genes.intersection(dtg[k]))
        with open(f"{new_snapshot}/{DATASET_TO_GENE_IDS_FILENAME}", "w") as fp:
            json.dump(dtg, fp)

    print("Creating marker genes cube...")
    create_marker_genes_cube(new_snapshot)
