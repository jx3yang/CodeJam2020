import { serviceRequest, SERVER_URL } from '@/utils/request';

export const IMAGE_UPLOAD_URL = `${SERVER_URL}/upload`;

interface ImageSearchData {
  imagePath: string;
}

export async function imageSearch(data: ImageSearchData) {
  return serviceRequest('/image_search', {
    data,
    method: 'POST',
  });
}
