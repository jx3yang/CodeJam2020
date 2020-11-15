import { Col, Image, Row } from 'antd';
import React from 'react';

export interface Result {
  url: string;
  title: string;
  imageUrl: string;
  price: string;
  company: string;
  distance?: number;
}

interface ResultsDisplayProps {
  results: Result[];
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = (props) => {
  const { results } = props;

  const numCols = 5;
  const numRows = Math.ceil(results.length / numCols);

  const makeRow = (index: number) => {
    const resultSlice = results.slice(index, index+5);
    return (
      <Row
        key={index}
      >
        {resultSlice.map((result, idx) =>
          <Col
            key={index * 10 + idx}
            span={24/numCols}
          >
            <Image src={result.imageUrl} />
          </Col>
        )}
      </Row>
    );
  }

  return (
    <>
      {new Array(numRows).fill(0).map((_, index) => makeRow(index))}
    </>
  );
}

export default ResultsDisplay;
