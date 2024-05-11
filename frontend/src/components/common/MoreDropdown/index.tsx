import { PopoverProps, Popover } from "@blueprintjs/core";
import { ButtonIconProps } from "@czi-sds/components";
import { MoreButton } from "src/components/common/MoreDropdown/style";

interface Props {
  popoverProps?: PopoverProps;
  buttonProps?: Partial<ButtonIconProps>;
}

const MoreDropdown = ({
  popoverProps = {},
  buttonProps = {} as Props["buttonProps"],
}: Props): JSX.Element => {
  return (
    <Popover {...popoverProps}>
      <MoreButton
        {...buttonProps}
        data-testid="collection-more-button"
        icon="DotsHorizontal"
        sdsSize="small"
        sdsType="tertiary"
      />
    </Popover>
  );
};

export default MoreDropdown;
