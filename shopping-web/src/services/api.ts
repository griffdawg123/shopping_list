import {Product} from '../types';

const API_URL = 'http://localhost:3000/api';

export async function compareProducts(query: string): Promise<Product[]> {
  const response = await fetch(`${API_URL}/compare?q=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error('Failed to fetch results');
  }
  const data = await response.json();
  return data.products || [];
}
