import React from 'react';

const StockCard = ({ stock }) => {
    const isPositive = stock.change >= 0;
    const changeColor = isPositive ? '#d32f2f' : '#1976d2'; // Red for up (KR style), Blue for down
    const changeSign = isPositive ? '+' : '';

    return (
        <div className="stock-card">
            <div className="stock-header">
                <h3>{stock.name} <span className="ticker">({stock.ticker})</span></h3>
                <span className="market-badge">{stock.market}</span>
            </div>

            <div className="stock-price" style={{ color: changeColor }}>
                <span className="price">{stock.price?.toLocaleString()}</span>
                <span className="change">
                    {changeSign}{stock.change}%
                </span>
            </div>

            <p className="stock-reason"><strong>추천 사유:</strong> {stock.reason}</p>

            {stock.chart_url && (
                <div className="stock-chart">
                    {/* Use full URL for local dev or proxy */}
                    <img src={`http://localhost:8000${stock.chart_url}`} alt={`${stock.name} Chart`} />
                </div>
            )}
        </div>
    );
};

export default StockCard;
