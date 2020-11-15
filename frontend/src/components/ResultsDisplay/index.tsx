import { List, Card, Typography } from 'antd';
import React from 'react';

import styles from './style.less';

const { Paragraph } = Typography;

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
  loading: boolean;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = (props) => {
  const { results, loading } = props;

  const cardList = results && (
    <List<Result>
      rowKey='url'
      loading={loading}
      grid={{
        gutter: 16,
        xs: 1,
        sm: 2,
        md: 3,
        lg: 3,
        xl: 4,
        xxl: 4,
      }}
      dataSource={results}
      renderItem={(item) =>
        <List.Item>
          <Card
            className={styles.card}
            hoverable
            cover={<a href={item.url}><img alt={item.title} src={item.imageUrl} width={200} height={200}/></a>}
            style={{width: 240, height: 350}}
          >
            <Card.Meta
              title={<a href={item.url}>{item.title}</a>}
              description={
                <Paragraph className={styles.item} ellipsis={{ rows: 2 }}>
                  From {item.company} at ${item.price}
                </Paragraph>
              }
            />
          </Card>
        </List.Item>
      }
    />
  );

  return (
    <div className={styles.coverCardList}>
      {results && <h2>Search Results</h2>}
      <div className={styles.cardList}>{cardList}</div>
    </div>
  )
}

export default ResultsDisplay;
