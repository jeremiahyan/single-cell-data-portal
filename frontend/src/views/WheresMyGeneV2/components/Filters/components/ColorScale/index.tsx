import { Tooltip } from "@czi-sds/components";
import { StyledDropdown, Wrapper } from "../common/style";
import { Label } from "src/views/WheresMyGeneV2/components/InfoPanel/common/style";
import { LabelWrapper } from "./style";
import {
  TooltipButton,
  StyledTooltip,
} from "src/views/WheresMyGeneV2/components/CellInfoSideBar/style";
import { COLOR_SCALE_TOOLTIP_TEXT } from "src/views/WheresMyGeneV2/common/constants";
import { COLOR_SCALE_OPTIONS } from "./constants";
import {
  ColorScaleOptionType,
  DEFAULT_INPUT_DROPDOWN_PROPS,
  Props,
} from "./types";
import { useConnect } from "./connect";
import { StyledQuestionMarkIcon } from "src/common/style";

export default function ColorScale({ setIsScaled }: Props): JSX.Element {
  const { colorScaleOnChange, colorScaledOption } = useConnect({ setIsScaled });

  return (
    <Wrapper>
      <LabelWrapper>
        <Label>Color Scale</Label>
        <Tooltip
          sdsStyle="dark"
          placement="right"
          width="default"
          arrow
          title={
            <StyledTooltip>
              <div>{COLOR_SCALE_TOOLTIP_TEXT}</div>
            </StyledTooltip>
          }
        >
          <TooltipButton
            data-testid="color-scale-tooltip-icon"
            sdsStyle="minimal"
            sdsType="secondary"
            isAllCaps={false}
          >
            <StyledQuestionMarkIcon />
          </TooltipButton>
        </Tooltip>
      </LabelWrapper>

      {/* Generic variables are
          <T: Dropdown's option type, Multiple, DisableClearable, FreeSolo>
      */}
      <StyledDropdown<ColorScaleOptionType, false, false, false>
        data-testid="color-scale-dropdown"
        onChange={colorScaleOnChange}
        label={colorScaledOption.name}
        options={COLOR_SCALE_OPTIONS}
        InputDropdownProps={DEFAULT_INPUT_DROPDOWN_PROPS}
        value={colorScaledOption}
      />
    </Wrapper>
  );
}
