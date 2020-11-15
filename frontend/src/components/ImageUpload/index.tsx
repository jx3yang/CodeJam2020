import { IMAGE_UPLOAD_URL } from '@/services/image';
import { UploadOutlined } from '@ant-design/icons';
import { Button, Image, Upload } from 'antd';
import { UploadChangeParam, UploadFile } from 'antd/lib/upload/interface';
import React from 'react';

import styles from './style.less';

interface ImageUploadProps {
  currentImageUrl?: string;
  onChange: (imageUrl: string) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = (props) => {
  const { currentImageUrl, onChange } = props;

  const onUpload = (info: UploadChangeParam<UploadFile<any>>) => {
    const fileInfo = info.fileList[0];
    if (fileInfo.status === 'done') {
      onChange(fileInfo.response.imagePath);
    }
  }

  return (
    <div style={{textAlign: 'center'}}>
      {currentImageUrl
        ? <Image src={currentImageUrl} width={200} />
        : <h3>Upload Image To Search For Similar Products!</h3>
      }
        <Upload
          action={IMAGE_UPLOAD_URL}
          name='file'
          fileList={[]}
          className={styles.upload}
          onChange={onUpload}
        >
          <Button icon={<UploadOutlined />}>Click to Upload</Button>
        </Upload>
    </div>
  );
}

export default ImageUpload;
