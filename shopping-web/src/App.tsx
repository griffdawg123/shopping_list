import {useState, useCallback} from 'react';
import {CompareResults} from './components/CompareResults';
import {ShoppingList} from './components/ShoppingList';
import {compareProducts} from './services/api';
import {Product, ShoppingListItem} from './types';
import './App.css';

type Tab = 'search' | 'list';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('search');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [shoppingList, setShoppingList] = useState<ShoppingListItem[]>([]);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const products = await compareProducts(query);
      setResults(products);
    } catch {
      setError('Unable to connect to backend. Make sure the server is running:\n\nnode server.js');
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, [query]);

  const addToList = useCallback((name: string) => {
    setShoppingList(prev => [...prev, {id: Date.now().toString(), name, checked: false}]);
  }, []);

  const removeFromList = useCallback((id: string) => {
    setShoppingList(prev => prev.filter(item => item.id !== id));
  }, []);

  const toggleListItem = useCallback((id: string) => {
    setShoppingList(prev =>
      prev.map(item => item.id === id ? {...item, checked: !item.checked} : item)
    );
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>Shopping Compare</h1>
      </header>

      <nav className="tabs">
        <button
          className={activeTab === 'search' ? 'active' : ''}
          onClick={() => setActiveTab('search')}
        >
          Compare
        </button>
        <button
          className={activeTab === 'list' ? 'active' : ''}
          onClick={() => setActiveTab('list')}
        >
          List ({shoppingList.length})
        </button>
      </nav>

      <main className="content">
        {activeTab === 'search' ? (
          <>
            <div className="search-row">
              <input
                type="text"
                placeholder="Search for a product..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              />
              <button onClick={handleSearch} disabled={loading}>
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>

            {error ? (
              <div className="error">{error}</div>
            ) : (
              <CompareResults results={results} />
            )}
          </>
        ) : (
          <ShoppingList
            items={shoppingList}
            onAddItem={addToList}
            onRemoveItem={removeFromList}
            onToggleItem={toggleListItem}
          />
        )}
      </main>
    </div>
  );
}

export default App;
