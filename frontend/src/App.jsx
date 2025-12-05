import React, { useState } from 'react';
import axios from 'axios';
import SearchInput from './components/SearchInput';
import StockCard from './components/StockCard';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (keywords, markets) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        keywords,
        markets
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError('분석 정보를 가져오는데 실패했습니다. 다시 시도해주세요.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendTelegram = async () => {
    if (!result) return;
    try {
      await axios.post('http://localhost:8000/send-telegram', result);
      alert('텔레그램으로 전송되었습니다!');
    } catch (err) {
      alert('텔레그램 전송에 실패했습니다.');
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI 주식 뉴스 분석기</h1>
        <p>AI와 함께 시장 테마와 기회를 발견하세요</p>
      </header>

      <main>
        <SearchInput onSearch={handleSearch} isLoading={isLoading} />

        {error && <div className="error-message">{error}</div>}

        {result && (
          <div className="result-container">
            <section className="summary-section">
              <h2>뉴스 요약</h2>
              <div className="summary-box">
                <p>{result.news_summary}</p>
              </div>

              <div className="themes-box">
                <h3>관련 테마</h3>
                <div className="tags">
                  {result.themes.map((theme, index) => (
                    <span key={index} className="tag">{theme}</span>
                  ))}
                </div>
              </div>

              {result.news_items && result.news_items.length > 0 && (
                <div className="news-links-box">
                  <h3>참고 뉴스</h3>
                  <ul className="news-list">
                    {result.news_items.map((item, index) => (
                      <li key={index}>
                        <a href={item.link} target="_blank" rel="noopener noreferrer">
                          {item.title}
                        </a>
                        <span className="news-date">{item.date}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </section>

            <section className="recommendations-section">
              <h2>추천 종목</h2>
              <div className="stock-grid">
                {result.recommended_stocks.map((stock, index) => (
                  <StockCard key={index} stock={stock} />
                ))}
              </div>
            </section>

            <div className="action-bar">
              <button onClick={handleSendTelegram} className="telegram-button">
                텔레그램으로 전송
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
