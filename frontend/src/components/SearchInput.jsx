import React, { useState } from 'react';

const SearchInput = ({ onSearch, isLoading }) => {
  const [keywordInput, setKeywordInput] = useState('');
  const [selectedMarkets, setSelectedMarkets] = useState({
    KRX: true,
    US: true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (keywordInput.trim()) {
      // Split by comma and clean up
      const keywords = keywordInput.split(',').map(k => k.trim()).filter(k => k);

      // Get selected markets
      const markets = Object.keys(selectedMarkets).filter(key => selectedMarkets[key]);

      if (markets.length === 0) {
        alert("최소 하나의 시장을 선택해주세요.");
        return;
      }

      onSearch(keywords, markets);
    }
  };

  const handleMarketChange = (market) => {
    setSelectedMarkets(prev => ({
      ...prev,
      [market]: !prev[market]
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="search-form-container">
      <div className="search-input-group">
        <input
          type="text"
          value={keywordInput}
          onChange={(e) => setKeywordInput(e.target.value)}
          placeholder="키워드 입력 (예: 반도체, 2차전지, HBM)"
          disabled={isLoading}
          className="search-input"
        />
        <button type="submit" disabled={isLoading} className="search-button">
          {isLoading ? '분석 중...' : '검색'}
        </button>
      </div>

      <div className="market-selector">
        <label className="market-checkbox">
          <input
            type="checkbox"
            checked={selectedMarkets.KRX}
            onChange={() => handleMarketChange('KRX')}
            disabled={isLoading}
          />
          국내 주식 (KRX)
        </label>
        <label className="market-checkbox">
          <input
            type="checkbox"
            checked={selectedMarkets.US}
            onChange={() => handleMarketChange('US')}
            disabled={isLoading}
          />
          미국 주식 (US)
        </label>
      </div>
    </form>
  );
};

export default SearchInput;
