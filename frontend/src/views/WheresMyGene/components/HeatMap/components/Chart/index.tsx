import { Tooltip } from "czifui";
import { init } from "echarts";
import cloneDeep from "lodash/cloneDeep";
import debounce from "lodash/debounce";
import throttle from "lodash/throttle";
import {
  Dispatch,
  memo,
  SetStateAction,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { EMPTY_ARRAY, EMPTY_OBJECT, noop } from "src/common/constants/utils";
import {
  CellTypeGeneExpressionSummaryData,
  CellTypeSummary,
  GeneExpressionSummary,
  Tissue,
} from "src/views/WheresMyGene/common/types";
import { ChartProps } from "../../hooks/common/types";
import { useUpdateChart } from "../../hooks/useUpdateChart";
import {
  dataToChartFormat,
  getAllSerializedCellTypeMetadata,
  getGeneNames,
  getHeatmapHeight,
  getHeatmapWidth,
} from "../../utils";
import {
  ChartContainer,
  StyledTooltipTable,
  tooltipCss,
  Wrapper,
} from "./style";

interface Props {
  cellTypes: CellTypeSummary[];
  selectedGeneData: (GeneExpressionSummary | undefined)[];
  setIsLoading: Dispatch<
    SetStateAction<{
      [tissue: Tissue]: boolean;
    }>
  >;
  tissue: Tissue;
}

const BASE_DEBOUNCE_MS = 200;

const MAX_DEBOUNCE_MS = 2 * 1000;

const TOOLTIP_THROTTLE_MS = 100;

export default memo(function Chart({
  cellTypes,
  selectedGeneData,
  setIsLoading,
  tissue,
}: Props): JSX.Element {
  const [currentIndices, setCurrentIndices] = useState([-1, -1]);
  const [cursorOffset, setCursorOffset] = useState([-1, -1]);

  const [isChartInitialized, setIsChartInitialized] = useState(false);

  const [chart, setChart] = useState<echarts.ECharts | null>(null);
  const ref = useRef(null);

  const [heatmapWidth, setHeatmapWidth] = useState(
    getHeatmapWidth(selectedGeneData)
  );
  const [heatmapHeight, setHeatmapHeight] = useState(
    getHeatmapHeight(cellTypes)
  );

  const [chartProps, setChartProps] = useState<ChartProps | null>(null);

  useEffect(() => {
    setIsLoading((isLoading) => ({ ...isLoading, [tissue]: true }));
  }, [cellTypes, selectedGeneData, setIsLoading, tissue]);

  const throttledSetCurrentIndices = useMemo(() => {
    return throttle((params, chart) => {
      const { offsetX, offsetY, event } = params;
      const { pageX, pageY } = event;

      const pointInGrid = chart.convertFromPixel("grid", [offsetX, offsetY]);

      setCursorOffset([pageX, pageY]);
      setCurrentIndices(pointInGrid);
    }, TOOLTIP_THROTTLE_MS);
  }, []);

  // Initialize charts
  useEffect(() => {
    const { current } = ref;

    if (!current || isChartInitialized) {
      return;
    }

    setIsChartInitialized(true);

    const chart = init(current, EMPTY_OBJECT, { useDirtyRect: true });

    chart.getZr().on("mousemove", function (params) {
      throttledSetCurrentIndices(params, chart);
    });

    setChart(chart);
  }, [ref, isChartInitialized, throttledSetCurrentIndices]);

  // Update heatmap size
  useEffect(() => {
    setHeatmapWidth(getHeatmapWidth(selectedGeneData));
    setHeatmapHeight(getHeatmapHeight(cellTypes));
  }, [cellTypes, selectedGeneData]);

  useUpdateChart({ chart, chartProps });

  // Calculate cellTypeSummaries
  /**
   * This is the formatted data that we use to render the heatmap.
   */
  const [cellTypeSummaries, setCellTypeSummaries] =
    useState<CellTypeSummary[]>(EMPTY_ARRAY);

  const debouncedIntegrateCellTypesAndGenes = useMemo(() => {
    return debounce(
      (cellTypes: CellTypeSummary[], geneData: Props["selectedGeneData"]) => {
        setCellTypeSummaries(integrateCelTypesAndGenes(cellTypes, geneData));
      },
      getDebounceMs(selectedGeneData.length),
      { leading: false }
    );
  }, [selectedGeneData]);

  // Cancel debounce when unmounting
  useEffect(() => {
    return () => debouncedIntegrateCellTypesAndGenes.cancel();
  }, [debouncedIntegrateCellTypesAndGenes]);

  /**
   * Performance optimization:
   * We only format and `setCellTypeSummaries()` after the watch list has stopped changing for
   * `getDebounceMs()`
   */
  useEffect(() => {
    debouncedIntegrateCellTypesAndGenes(cellTypes, selectedGeneData);
  }, [selectedGeneData, cellTypes, debouncedIntegrateCellTypesAndGenes]);

  // Generate chartProps
  const debouncedDataToChartFormat = useMemo(() => {
    return debounce(
      (
        cellTypeSummaries: CellTypeSummary[],
        selectedGeneData: Props["selectedGeneData"]
      ) => {
        const result = {
          cellTypeMetadata: getAllSerializedCellTypeMetadata(cellTypeSummaries),
          chartData: dataToChartFormat(cellTypeSummaries, selectedGeneData),
          geneNames: getGeneNames(selectedGeneData),
        };

        setChartProps(result);

        setIsLoading((isLoading) => ({ ...isLoading, [tissue]: false }));
      },
      getDebounceMs(selectedGeneData.length),
      { leading: false }
    );
  }, [selectedGeneData, setIsLoading, tissue]);

  useEffect(() => {
    debouncedDataToChartFormat(cellTypeSummaries, selectedGeneData);
  }, [cellTypeSummaries, selectedGeneData, debouncedDataToChartFormat]);

  // Cancel debounce when unmounting
  useEffect(() => {
    return () => debouncedDataToChartFormat.cancel();
  }, [debouncedDataToChartFormat]);

  const [hoveredGeneIndex, hoveredCellTypeIndex] = currentIndices;

  const tooltipContent = useMemo(() => {
    if (!chartProps) return null;

    const { chartData } = chartProps;

    const dataPoint = chartData.find(
      ({ geneIndex, cellTypeIndex }) =>
        geneIndex === hoveredGeneIndex && cellTypeIndex === hoveredCellTypeIndex
    );

    const cellType = cellTypes[hoveredCellTypeIndex];
    const gene = selectedGeneData[hoveredGeneIndex];

    if (!dataPoint || !cellType || !gene) return null;

    const data = [
      {
        dataRows: [
          {
            label: "Expressing Cells",
            value: ((dataPoint?.percentage || 0) * 100).toFixed(2) + "%",
          },
          {
            label: "Relative Expressions",
            value: (dataPoint?.meanExpression || 0).toFixed(2),
          },
          {
            label: "Scaled Relative Expressions",
            value: (dataPoint?.scaledMeanExpression || 0).toFixed(2),
          },
        ],
      },
      {
        dataRows: [
          { label: "Cell Type", value: cellType.name },
          { label: "Tissue Composition", value: "" },
        ],
      },
      {
        dataRows: [
          { label: "Gene Name", value: "" },
          { label: "Gene Symbol", value: gene?.name || "" },
        ],
      },
    ];

    return <StyledTooltipTable data={data || undefined} />;
  }, [
    chartProps,
    cellTypes,
    hoveredGeneIndex,
    hoveredCellTypeIndex,
    selectedGeneData,
  ]);

  const tooltipClasses = useMemo(() => ({ tooltip: tooltipCss }), []);

  return (
    <Wrapper height={heatmapHeight} width={heatmapWidth}>
      <Tooltip
        placement="right-start"
        classes={tooltipClasses}
        title={tooltipContent || <>No data</>}
        PopperProps={{
          anchorEl: {
            clientHeight: 0,
            clientWidth: 0,
            getBoundingClientRect: () => ({
              bottom: cursorOffset[1],
              height: 0,
              left: cursorOffset[0],
              right: cursorOffset[0],
              toJSON: noop,
              top: cursorOffset[1],
              width: 0,
              x: cursorOffset[0],
              y: cursorOffset[1],
            }),
          },
          modifiers: {
            offset: { offset: "0,20" },
          },
        }}
      >
        <ChartContainer height={heatmapHeight} width={heatmapWidth} ref={ref} />
      </Tooltip>
    </Wrapper>
  );
});

/**
 * Adds gene expressions to the cell types.
 */
function integrateCelTypesAndGenes(
  cellTypeSummaries: CellTypeSummary[],
  geneExpressionSummaries: Props["selectedGeneData"]
): CellTypeSummary[] {
  const geneMaps = geneExpressionSummaries.map((geneExpressionSummary) =>
    rawGeneDataToMap(geneExpressionSummary)
  );

  const newCellTypeSummaries = cloneDeep(cellTypeSummaries);

  return newCellTypeSummaries.map((cellTypeSummary) => {
    const { id } = cellTypeSummary;

    for (const [name, geneMap] of geneMaps) {
      const columnData = geneMap.get(id);

      if (columnData !== undefined) {
        cellTypeSummary.geneExpressions = {
          ...(cellTypeSummary.geneExpressions || {}),
          [name]: columnData,
        };
      }
    }

    return cellTypeSummary;
  });
}

function rawGeneDataToMap(
  gene?: GeneExpressionSummary
): [string, Map<string, CellTypeGeneExpressionSummaryData>] {
  if (!gene) return ["", new Map()];

  const { cellTypeGeneExpressionSummaries, name } = gene;

  return [
    name,
    new Map(cellTypeGeneExpressionSummaries?.map((row) => [row.id, row])),
  ];
}

const BROWSER_PARALLEL_CALL_LIMIT = 10;

function getDebounceMs(geneCount: number): number {
  if (geneCount <= BROWSER_PARALLEL_CALL_LIMIT) return 0;
  if (geneCount >= 100) return MAX_DEBOUNCE_MS;

  return Math.floor(geneCount / BROWSER_PARALLEL_CALL_LIMIT) * BASE_DEBOUNCE_MS;
}