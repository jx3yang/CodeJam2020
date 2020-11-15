import { imageSearch, IMAGE_SEGMENTATION_URL } from '@/services/image';
import { UploadOutlined } from '@ant-design/icons';
import { Button, Image, Radio, Space, Upload } from 'antd';
import { UploadChangeParam, UploadFile } from 'antd/lib/upload/interface';
import React, { useState } from 'react';
import ResultsDisplay, { Result } from '../ResultsDisplay';

interface Segment {
  imageUrl: string;
  name: string;
}

interface SegmentationProps {
  currentImageUrl?: string;
  onChange: (imageUrl: string) => void;
}

const Segmentation: React.FC<SegmentationProps> = (props) => {
  const { currentImageUrl, onChange } = props;
  const [segments, setSegments] = useState<Segment[]>([]);
  const [segmentResults, setSegmentResults] = useState<Map<string, Result[]>>(new Map());

  const onUpload = (info: UploadChangeParam<UploadFile<any>>) => {
    const fileInfo = info.fileList[0];
    if (fileInfo.status === 'done') {
      console.log(fileInfo)
      const newSegments = fileInfo.response.segments as Segment[];
      onChange(fileInfo.response.imagePath);
      setSegments(newSegments);

      newSegments.forEach(segment => {
        imageSearch({ imagePath: segment.imageUrl }).then(res => {
          if (res.success === true) {
            const newSegmentResults = new Map<string, Result[]>(segmentResults);
            newSegmentResults.set(segment.imageUrl, res.data);
            setSegmentResults(newSegmentResults);
          }
        })
      });
    }
  }

  return (
    <>
      <div style={{textAlign: 'center'}}>
        {currentImageUrl
          ? <><Image src={currentImageUrl} width={200} /> <br /></>
          : <h3>Upload Image to Segment</h3>
        }
          <Upload
            action={IMAGE_SEGMENTATION_URL}
            name='file'
            fileList={[]}
            onChange={onUpload}
          >
            <Button icon={<UploadOutlined />}>Click to Upload</Button>
          </Upload>
      </div>
      {segments && segments.length > 0 &&
        <>
          <h2>Segments</h2>
          {segments.map((segment, index) =>
            <>
              <Space key={index}>
                <Image src={segment.imageUrl} width={200}/>
                <ResultsDisplay results={segmentResults.get(segment.imageUrl) || []} loading={false} />
              </Space>
              <br/>
            </>
          )}
        </>
      }
    </>
  );
}

export default Segmentation;
