import { PageContainer } from '@ant-design/pro-layout';
import { Card } from 'antd';
import React, { useState } from 'react';
import ImageUpload from '@/components/ImageUpload';
import ResultsDisplay, { Result } from '@/components/ResultsDisplay';
import { imageSearch } from '@/services/image';

const ImageSearch: React.FC<{}> = () => {
  const [imageUrl, setImageUrl] = useState<string>('');
  const [results, setResults] = useState<Result[]>([]);
  const [resultsLoading, setResultsLoading] = useState<boolean>(false);

  const onChange = (url: string) => {
    setImageUrl(url);
    setResults([]);
    setResultsLoading(true);
    imageSearch({ imagePath: url }).then(res => {
      if (res.success === true) {
        setResults(res.data);
        setResultsLoading(false);
      }
    });
  }

  return (
    <PageContainer>
      <Card bordered={false}>
        <ImageUpload
          currentImageUrl={imageUrl}
          onChange={onChange}
        />
      </Card>
      <Card bordered={false}>
        {results.length > 0 &&
          <ResultsDisplay results={results} loading={resultsLoading} />
        }
      </Card>
    </PageContainer>
  );
}

export default ImageSearch;
