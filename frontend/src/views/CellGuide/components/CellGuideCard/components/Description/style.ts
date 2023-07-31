import styled from "@emotion/styled";
import { fontBodyS, fontCapsXxs } from "@czi-sds/components";
import { gray100, gray500 } from "src/common/theme";

export const CellGuideCardDescription = styled.div`
  ${fontBodyS}
  font-weight: 400;
  white-space: pre-wrap;
  background-color: ${gray100};
  padding: 12px 16px 12px 16px;
  border-radius: 8px;
`;

export const Wrapper = styled.div`
  margin-top: 8px;
`;

export const Source = styled.div`
  ${fontBodyS}
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 40px;
  color: ${gray500};
`;

export const SourceLink = styled.div`
  white-space: nowrap;
`;

export const DescriptionHeader = styled.div`
  ${fontCapsXxs}
  font-weight: 600;
  color: ${gray500};
  margin-bottom: 8px;
`;
