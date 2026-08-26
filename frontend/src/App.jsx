import { useState } from 'react';

const initialForm = {
  location: 'Bengaluru',
  area: 1200,
  bedrooms: 2,
  bathrooms: 2,
  property_type: 'Apartment',
  floor: 5,
  parking: 1,
  age: 8,
};

const modelMetrics = [
  { name: 'Linear Regression', r2: 0.8718, mae: 65.2026, rmse: 88.5758 },
  { name: 'Random Forest', r2: 0.9526, mae: 38.3982, rmse: 53.8786 },
  { name: 'Gradient Boosting', r2: 0.9617, mae: 34.2649, rmse: 48.4187 },
];

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    const numericFields = ['area', 'floor', 'parking', 'age', 'bedrooms', 'bathrooms'];

    setForm((prev) => ({
      ...prev,
      [name]: numericFields.includes(name) ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error('Prediction failed. Please check the inputs.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI-Powered Real Estate Platform</p>
          <h1>Property Price Prediction</h1>
        </div>
      </header>

      <main className="dashboard">
        <section className="panel form-panel">
          <h2>Property Details</h2>
          <form onSubmit={handleSubmit} className="property-form">
            <div className="field-grid">
              <label>
                Location
                <select name="location" value={form.location} onChange={handleChange}>
                  <option>Bengaluru</option>
                  <option>Mysuru</option>
                  <option>Hyderabad</option>
                  <option>Chennai</option>
                  <option>Pune</option>
                  <option>Mumbai</option>
                  <option>Delhi</option>
                </select>
              </label>

              <label>
                Area (sq.ft)
                <input type="number" name="area" min="200" value={form.area} onChange={handleChange} />
              </label>

              <label>
                Bedrooms
                <input type="number" name="bedrooms" min="1" value={form.bedrooms} onChange={handleChange} />
              </label>

              <label>
                Bathrooms
                <input type="number" name="bathrooms" min="1" value={form.bathrooms} onChange={handleChange} />
              </label>

              <label>
                Property Type
                <select name="property_type" value={form.property_type} onChange={handleChange}>
                  <option>Apartment</option>
                  <option>Villa</option>
                  <option>Independent House</option>
                  <option>Plot</option>
                </select>
              </label>

              <label>
                Floor
                <input type="number" name="floor" min="0" value={form.floor} onChange={handleChange} />
              </label>

              <label>
                Parking
                <input type="number" name="parking" min="0" value={form.parking} onChange={handleChange} />
              </label>

              <label>
                Property Age (years)
                <input type="number" name="age" min="0" value={form.age} onChange={handleChange} />
              </label>
            </div>

            <button type="submit" disabled={loading}>
              {loading ? 'Predicting...' : 'Predict Price'}
            </button>
          </form>

          {error && <p className="error">{error}</p>}
        </section>

        <section className="panel result-panel">
          <h2>Estimated Property Price</h2>
          {result ? (
            <>
              <div className="price-box">
                <span className="label">Estimated Price</span>
                <strong>₹{result.estimated_price_lakhs.toFixed(2)} Lakhs</strong>
              </div>

              <div className="range-box">
                <span>Range</span>
                <p>
                  ₹{result.price_range_lakhs.min_lakhs.toFixed(2)}L - ₹{result.price_range_lakhs.max_lakhs.toFixed(2)}L
                </p>
              </div>

              <div className="range-box">
                <span>Market Pricing</span>
                <p>
                  Approx. ₹{(result.estimated_price_lakhs / form.area * 100000).toFixed(0)}/sqft based on {form.location} market trends
                </p>
              </div>

              <div className="stats-grid">
                <div>
                  <span>Model Used</span>
                  <strong>{result.model_used}</strong>
                </div>
                <div>
                  <span>R²</span>
                  <strong>{result.metrics.r2}</strong>
                </div>
                <div>
                  <span>MAE</span>
                  <strong>{result.metrics.mae}</strong>
                </div>
                <div>
                  <span>RMSE</span>
                  <strong>{result.metrics.rmse}</strong>
                </div>
              </div>
            </>
          ) : (
            <div className="placeholder">
              Fill in the form and predict the price for a property.
            </div>
          )}
        </section>
      </main>

      <section className="panel model-panel">
        <h2>Model Comparison</h2>
        <div className="comparison-table-wrap">
          <table>
            <thead>
              <tr>
                <th>Model</th>
                <th>R²</th>
                <th>MAE</th>
                <th>RMSE</th>
              </tr>
            </thead>
            <tbody>
              {modelMetrics.map((model) => (
                <tr key={model.name}>
                  <td>{model.name}</td>
                  <td>{model.r2}</td>
                  <td>{model.mae}</td>
                  <td>{model.rmse}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default App;
