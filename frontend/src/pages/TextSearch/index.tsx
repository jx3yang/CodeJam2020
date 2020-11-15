import ResultsDisplay, { Result } from '@/components/ResultsDisplay';
import { textSearch } from '@/services/text';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Input, Form } from 'antd';
import React, { useState } from 'react';

const { Search } = Input;

const TextSearch: React.FC<{}> = () => {
  const [results, setResults] = useState<Result[]>([]);
  const [resultsLoading, setResultsLoading] = useState<boolean>(false);

  const onSearch = (value: string) => {
    setResultsLoading(true);
    textSearch({ query: value }).then(res => {
      if (res.success === true) {
        setResults(res.data);
        setResultsLoading(false);
      }
    })
  }

  return (
    <PageContainer>
      <Card
        bordered={false}
        style={{textAlign: 'center'}}
      >
        <div style={{ width: '50%', margin: '0 auto'}}>
          <Form.Item label='Search Product'>
            <Search
              placeholder="Product name, title, description"
              onSearch={onSearch}
              enterButton
            />
          </Form.Item>
        </div>
      </Card>
      <Card
        bordered={false}
      >
        {results.length > 0 &&
          <ResultsDisplay results={results} loading={resultsLoading} />
        }
      </Card>
    </PageContainer>
  );
}

export default TextSearch;
