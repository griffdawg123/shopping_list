export interface Product {
  name: string;
  price: string;
  unitPrice: string;
  supermarket: 'coles' | 'woolworths' | 'aldi';
  isOnSale?: boolean;
}

export interface ShoppingListItem {
  id: string;
  name: string;
  checked: boolean;
}
