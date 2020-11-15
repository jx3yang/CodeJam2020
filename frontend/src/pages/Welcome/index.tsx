import ResultsDisplay, { Result } from '@/components/ResultsDisplay';
import { getProducts } from '@/services/products';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Pagination } from 'antd';
import React, { useEffect, useState } from 'react';

const Welcome: React.FC<{}> = () => {
  const [results, setResults] = useState<Result[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [pageSize, setPageSize] = useState<number>(0);

  useEffect(() => {
    getProducts({ page: 1 }).then(res => {
      if (res.success === true) {
        setResults(res.data);
        setTotal(res.total);
        setPageSize(res.size);
      }
    })
  }, []);

  const onChange = (page: number) => {
    getProducts({ page }).then(res => {
      if (res.success === true) {
        setResults(res.data);
      }
    });
  }

  return (
    <PageContainer>
      <Card>
        <ResultsDisplay results={results} loading={false} title='Recommendations'/>
        <Pagination total={total} onChange={onChange} pageSize={pageSize} />
      </Card>
    </PageContainer>
  )
}

export default Welcome;
