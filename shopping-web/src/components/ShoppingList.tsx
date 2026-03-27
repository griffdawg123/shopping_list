import {useState} from 'react';
import {ShoppingListItem} from '../types';
import './ShoppingList.css';

interface Props {
  items: ShoppingListItem[];
  onAddItem: (name: string) => void;
  onRemoveItem: (id: string) => void;
  onToggleItem: (id: string) => void;
}

export function ShoppingList({items, onAddItem, onRemoveItem, onToggleItem}: Props) {
  const [newItem, setNewItem] = useState('');

  const handleAdd = () => {
    if (newItem.trim()) {
      onAddItem(newItem.trim());
      setNewItem('');
    }
  };

  return (
    <div className="shopping-list">
      <div className="list-input">
        <input
          type="text"
          placeholder="Add item..."
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
        />
        <button onClick={handleAdd}>Add</button>
      </div>
      <ul className="list-items">
        {items.map((item) => (
          <li key={item.id} className={item.checked ? 'checked' : ''}>
            <input
              type="checkbox"
              checked={item.checked}
              onChange={() => onToggleItem(item.id)}
            />
            <span>{item.name}</span>
            <button className="remove" onClick={() => onRemoveItem(item.id)}>×</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
