import {Product} from '../types';
import './CompareResults.css';

interface Props {
  results: Product[];
}

export function CompareResults({results}: Props) {
  if (results.length === 0) {
    return <div className="empty">Search for products to compare</div>;
  }

  return (
    <div className="results-container">
      <div className="results-header">
        <span>Store</span>
        <span>Product</span>
        <span>Price</span>
        <span>Unit Price</span>
      </div>
      {results.map((product, index) => (
        <div key={index} className="result-row">
          <span className={`store ${product.supermarket}`}>
            {product.supermarket === 'coles' ? 'Coles' : 'Woolies'}
          </span>
          <span className="name">
            {product.name}
            {product.isOnSale && <span className="sale-badge">*</span>}
          </span>
          <span className="price">${product.price}</span>
          <span className="unit">{product.unitPrice}</span>
        </div>
      ))}
    </div>
  );
}
