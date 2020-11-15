import { PageContainer } from '@ant-design/pro-layout';
import { Card } from 'antd';
import React, { useState } from 'react';
import Segmentation from '@/components/Segmentation';

const ClothesSegmentation: React.FC<{}> = () => {
  const [imageUrl, setImageUrl] = useState<string>('');
  const onChange = (url: string) => {
    setImageUrl(url);
  }

  return (
    <PageContainer>
      <Card bordered={false}>
        <Segmentation
          currentImageUrl={imageUrl}
          onChange={onChange}
        />
      </Card>
    </PageContainer>
  );
}

export default ClothesSegmentation;
