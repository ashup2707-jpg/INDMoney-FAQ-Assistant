import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [funds, setFunds] = useState([])
  const [selectedTab, setSelectedTab] = useState('chat')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetchFunds()
    setMessages([
      {
        type: 'bot',
        content: 'Hello! 👋 I\'m your INDMoney FAQ Assistant. Ask me anything about HDFC mutual funds, investment advice, or fund comparisons!',
        timestamp: new Date()
      }
    ])
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const fetchFunds = async () => {
    try {
      const response = await axios.get('/api/funds')
      setFunds(response.data)
    } catch (error) {
      console.error('Error fetching funds:', error)
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/ai/ask', {
        question: input,
        use_context: true
      })

      const botMessage = {
        type: 'bot',
        content: response.data.answer,
        source: response.data.source,
        fund_sources: response.data.fund_sources || [],
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error. Please make sure the backend API is running and Gemini API key is configured.',
        timestamp: new Date(),
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const askQuickQuestion = async (question) => {
    setInput(question)
    setTimeout(() => {
      document.querySelector('form').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }))
    }, 100)
  }

  return (
    <div className="app-container">
      <div className="chat-card">
        <div className="header">
          <div className="header-content">
            <div className="logo">
              <div className="logo-icon">💰</div>
              <div>
                <h1>INDMoney</h1>
                <p>FAQ Assistant</p>
              </div>
            </div>
            <div className="tabs">
              <button 
                className={selectedTab === 'chat' ? 'active' : ''}
                onClick={() => setSelectedTab('chat')}
              >
                💬 Chat
              </button>
              <button 
                className={selectedTab === 'funds' ? 'active' : ''}
                onClick={() => setSelectedTab('funds')}
              >
                📊 Funds
              </button>
            </div>
          </div>
        </div>

        {selectedTab === 'chat' ? (
          <>
            <div className="messages-container">
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.type}`}>
                  <div className="message-bubble">
                    <div className="message-content">{message.content}</div>
                    {message.fund_sources && message.fund_sources.length > 0 && (
                      <div className="message-sources">
                        <div className="sources-title">📚 Sources:</div>
                        {message.fund_sources.map((source, idx) => (
                          <a 
                            key={idx}
                            href={source.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="source-link"
                          >
                            {source.fund_name}
                          </a>
                        ))}
                      </div>
                    )}
                    {message.source && (
                      <div className="message-source">
                        Powered by {message.source}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message bot">
                  <div className="message-bubble typing">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="quick-questions">
              <div className="quick-questions-label">Quick questions:</div>
              <div className="quick-buttons">
                <button onClick={() => askQuickQuestion('What is the minimum SIP amount?')}>
                  💵 Minimum SIP
                </button>
                <button onClick={() => askQuickQuestion('Compare HDFC mid cap and small cap funds')}>
                  📈 Compare Funds
                </button>
                <button onClick={() => askQuickQuestion('What is expense ratio?')}>
                  ❓ Expense Ratio
                </button>
                <button onClick={() => askQuickQuestion('Suggest a fund for 5 year investment')}>
                  🎯 Investment Advice
                </button>
              </div>
            </div>

            <form className="input-container" onSubmit={sendMessage}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask anything about mutual funds..."
                disabled={loading}
              />
              <button type="submit" disabled={loading || !input.trim()}>
                <span>Send</span>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                </svg>
              </button>
            </form>
          </>
        ) : (
          <div className="funds-container">
            <div className="funds-header">
              <h2>Available HDFC Funds</h2>
              <p>{funds.length} funds in database</p>
            </div>
            <div className="funds-grid">
              {funds.map((fund, index) => (
                <div key={index} className="fund-card">
                  <div className="fund-name">{fund.fund_name}</div>
                  <div className="fund-details">
                    <div className="fund-detail">
                      <span className="label">Manager:</span>
                      <span className="value">{fund.fund_manager}</span>
                    </div>
                    <div className="fund-detail">
                      <span className="label">Expense Ratio:</span>
                      <span className="value">{fund.expense_ratio}</span>
                    </div>
                    <div className="fund-detail">
                      <span className="label">Risk:</span>
                      <span className="value risk">{fund.riskometer}</span>
                    </div>
                  </div>
                  <div className="returns">
                    <div className="returns-title">Returns</div>
                    <div className="returns-grid">
                      {Object.entries(fund.returns || {}).map(([period, value]) => (
                        <div key={period} className="return-item">
                          <span className="period">{period}</span>
                          <span className="return-value">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <button 
                    className="ask-about-fund"
                    onClick={() => {
                      setSelectedTab('chat')
                      askQuickQuestion(`Tell me about ${fund.fund_name}`)
                    }}
                  >
                    Ask about this fund
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
