import styled from "@emotion/styled";
import { ReactElement } from "react";

const ResponsiveContainer = styled.div`
  position: relative;
  overflow: hidden;
  width: 100%;
  padding-top: 56.25%;
`;

const ResponsiveIFrame = styled.iframe`
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  width: 100%;
  height: 100%;
`;

const EmbeddedGoogleSlides = ({ src }: { src: string }): ReactElement => {
  return (
    <ResponsiveContainer>
      <ResponsiveIFrame
        sandbox="allow-scripts"
        src={src}
        frameBorder="0"
        allowFullScreen={true}
      ></ResponsiveIFrame>
    </ResponsiveContainer>
  );
};

export default EmbeddedGoogleSlides;