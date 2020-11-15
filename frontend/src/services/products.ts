import { serviceRequest } from '@/utils/request';

interface GetProductsParams {
  page: number;
}

export async function getProducts(params: GetProductsParams) {
  return serviceRequest('/products', {
    params,
  });
}
