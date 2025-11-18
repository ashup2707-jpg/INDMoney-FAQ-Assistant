import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [funds, setFunds] = useState([])
  const [selectedTab, setSelectedTab] = useState('chat')
  const [apiInfo, setApiInfo] = useState(null)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  // Fetch initial data
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Fetch API info
        const response = await fetch('/api');
        const data = await response.json();
        
        setApiInfo(data);
        
        // Fetch funds
        const fundsResponse = await fetch('/api/funds?limit=100');
        const fundsData = await fundsResponse.json();
        setFunds(fundsData);
      } catch (err) {
        console.error('Initialization error:', err);
        setError('Failed to initialize the application. Please refresh the page.');
      }
    };

    initializeApp();
  }, []);

  useEffect(() => {
    setMessages([
      {
        type: 'bot',
        content: 'Hello! 👋 I\'m your INDMoney FAQ Assistant. Ask me anything about HDFC mutual funds!',
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
      // Check if AI is available
      const aiAvailable = apiInfo?.ai_available;
      
      if (aiAvailable) {
        // Use AI endpoint
        const response = await axios.post('/api/ai/ask', {
          question: input,
          use_context: true
        })

        const botMessage = {
          type: 'bot',
          content: response.data.answer,
          source: response.data.source,
          timestamp: new Date()
        }

        setMessages(prev => [...prev, botMessage])
      } else {
        // Fallback to simple FAQ search
        const response = await fetch(`/api/faq?q=${encodeURIComponent(input)}&limit=3`);
        
        if (!response.ok) {
          throw new Error(`Failed to search FAQs: ${response.status}`);
        }
        
        const data = await response.json();
        
        let botMessage;
        if (data.length > 0) {
          // Format the FAQ responses
          const answer = data.map(faq => `Q: ${faq.question}\nA: ${faq.answer}`).join('\n\n');
          botMessage = {
            type: 'bot',
            content: answer,
            timestamp: new Date()
          };
        } else {
          botMessage = {
            type: 'bot',
            content: "I couldn't find any relevant information for your question. Please try rephrasing or ask something else.",
            timestamp: new Date()
          };
        }

        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: `Sorry, I encountered an error: ${error.message || 'Unknown error'}. Please try again.`,
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
                    {message.source && message.source !== 'none' && (
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
                <button onClick={() => askQuickQuestion('What is expense ratio?')}>
                  ❓ Expense Ratio
                </button>
                <button onClick={() => askQuickQuestion('Tell me about HDFC Mid Cap Fund')}>
                  📈 Mid Cap Fund
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
                      <span className="value">{fund.fund_manager || 'N/A'}</span>
                    </div>
                    <div className="fund-detail">
                      <span className="label">Expense Ratio:</span>
                      <span className="value">{fund.expense_ratio || 'N/A'}</span>
                    </div>
                    <div className="fund-detail">
                      <span className="label">Risk:</span>
                      <span className="value risk">{fund.riskometer || 'N/A'}</span>
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