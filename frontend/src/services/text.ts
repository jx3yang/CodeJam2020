import { serviceRequest } from '@/utils/request';

interface TextSearchData {
  query: string;
}

export async function textSearch(data: TextSearchData) {
  return serviceRequest('/text_search', {
    data,
    method: 'POST',
  });
}
