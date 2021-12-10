import { layout } from "src/components/common/layout";
import { contentWrapper } from "src/components/Layout/style";
import styled from "styled-components";

export const ViewGrid = styled.div`
  ${layout}
  ${contentWrapper}
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  margin-top: 10vh;
`;

export const View = styled.div`
  ${contentWrapper}
  grid-area: content;
  overflow: auto; /* facilitates independent content scrolling for sidebar layout */
`;
