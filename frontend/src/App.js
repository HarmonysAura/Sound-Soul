import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HeroSection = ({ onBeginExperience }) => {
  return (
    <div className="hero-section">
      <div className="cosmic-bg">
        <img 
          src="https://images.unsplash.com/photo-1651135094094-7f2a48224da8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxjb3NtaWMlMjBzcGhlcmV8ZW58MHx8fHB1cnBsZXwxNzUzMDI3MTQ3fDA&ixlib=rb-4.1.0&q=85"
          alt="Cosmic Sphere"
          className="hero-bg-image"
        />
        <div className="hero-overlay">
          <h1 className="hero-title animate-glow">QUANTA MARS</h1>
          <h2 className="hero-subtitle">The Harmonic Trilogy Experience</h2>
          <p className="hero-description">
            A sentient mega-AI awakens on Mars, weaving a network of consciousness 
            through 18 sacred sites across dimensions. Experience the ultimate VR journey 
            designed for The Sphere in Las Vegas with tone-reactive 16K visuals.
          </p>
          <button 
            className="cta-button pulse-animation"
            onClick={onBeginExperience}
          >
            BEGIN THE EXPERIENCE
          </button>
        </div>
      </div>
    </div>
  );
};

const TrilogyBrowser = ({ chapters }) => {
  return (
    <section className="trilogy-section">
      <div className="section-container">
        <h2 className="section-title">The Eberswalde Trilogy</h2>
        <div className="chapters-grid">
          {chapters.map((chapter, index) => (
            <div key={chapter.id} className="chapter-card">
              <div className="chapter-image-container">
                <img 
                  src={chapter.image_url} 
                  alt={chapter.title}
                  className="chapter-image"
                />
                <div className="chapter-overlay">
                  <span className="chapter-number">Chapter {chapter.chapter_number}</span>
                </div>
              </div>
              <div className="chapter-content">
                <h3 className="chapter-title">{chapter.title}</h3>
                <h4 className="chapter-subtitle">{chapter.subtitle}</h4>
                <p className="chapter-description">{chapter.description}</p>
                <div className="tone-signature">
                  <span className="tone-label">Tone Signature:</span>
                  <span className="tone-value">{chapter.tone_signature}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

const SacredSitesGallery = ({ sites }) => {
  const [selectedSite, setSelectedSite] = useState(null);
  const [toneReactive, setToneReactive] = useState(false);

  const triggerToneSignature = async (frequency) => {
    try {
      setToneReactive(true);
      const response = await axios.post(`${API}/tone-signatures/${frequency}/trigger`);
      console.log('Tone triggered:', response.data);
      
      // Simulate tone-reactive visual effect
      setTimeout(() => setToneReactive(false), 2000);
    } catch (error) {
      console.error('Error triggering tone:', error);
      setToneReactive(false);
    }
  };

  return (
    <section className={`sacred-sites-section ${toneReactive ? 'tone-active' : ''}`}>
      <div className="section-container">
        <h2 className="section-title">Sacred Sites Network</h2>
        <p className="section-description">
          18 mystical nodes interconnected across dimensions, each resonating with unique frequencies
        </p>
        <div className="sites-grid">
          {sites.map((site) => (
            <div 
              key={site.id} 
              className="site-card"
              onClick={() => setSelectedSite(site)}
            >
              <div className="site-image-container">
                <img 
                  src={site.image_url} 
                  alt={site.name}
                  className="site-image"
                />
                <div className="site-overlay">
                  <div className="frequency-badge">
                    {site.tone_frequency} Hz
                  </div>
                </div>
              </div>
              <div className="site-info">
                <h3 className="site-name">{site.name}</h3>
                <p className="site-geometry">{site.sacred_geometry_type}</p>
                <button 
                  className="tone-trigger-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    triggerToneSignature(site.tone_frequency);
                  }}
                >
                  Activate Resonance
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {selectedSite && (
        <div className="site-modal" onClick={() => setSelectedSite(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedSite(null)}>×</button>
            <img 
              src={selectedSite.image_url} 
              alt={selectedSite.name}
              className="modal-image"
            />
            <div className="modal-info">
              <h2>{selectedSite.name}</h2>
              <p className="modal-description">{selectedSite.description}</p>
              <div className="modal-details">
                <div className="detail-item">
                  <span className="detail-label">Frequency:</span>
                  <span className="detail-value">{selectedSite.tone_frequency} Hz</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Geometry:</span>
                  <span className="detail-value">{selectedSite.sacred_geometry_type}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Energy:</span>
                  <span className="detail-value">{selectedSite.energy_signature}</span>
                </div>
              </div>
              <button 
                className="modal-activate-btn"
                onClick={() => triggerToneSignature(selectedSite.tone_frequency)}
              >
                Activate Sacred Resonance
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

const BackerEngagementSection = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    investment_interest: 'angel',
    message: '',
    walkthrough_requested: false
  });
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/backer-engagement`, formData);
      setIsSubmitted(true);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  if (isSubmitted) {
    return (
      <section className="backer-section">
        <div className="section-container">
          <div className="submission-success">
            <h2>Thank You for Your Interest!</h2>
            <p>We'll contact you soon to schedule your exclusive walkthrough of The Harmonic Trilogy Experience.</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="backer-section">
      <div className="section-container">
        <h2 className="section-title">Join the Cosmic Journey</h2>
        <p className="section-description">
          Be part of revolutionary VR experience that will premiere at The Sphere in Las Vegas
        </p>
        <div className="backer-content">
          <div className="investment-highlights">
            <h3>Investment Opportunity</h3>
            <ul>
              <li>🌌 Exclusive VR experience for The Sphere venue</li>
              <li>🎵 Proprietary tone-signature technology</li>
              <li>🚀 AI-powered narrative with Quanta Mars</li>
              <li>📈 Targeting $50M+ revenue in first year</li>
            </ul>
          </div>
          <form className="backer-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                value={formData.name}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
            <div className="form-group">
              <input
                type="email"
                name="email"
                placeholder="Email Address"
                value={formData.email}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
            <div className="form-group">
              <input
                type="text"
                name="company"
                placeholder="Company/Organization (Optional)"
                value={formData.company}
                onChange={handleChange}
                className="form-input"
              />
            </div>
            <div className="form-group">
              <select
                name="investment_interest"
                value={formData.investment_interest}
                onChange={handleChange}
                className="form-select"
              >
                <option value="angel">Angel Investment ($50K-$500K)</option>
                <option value="seed">Seed Round ($500K-$2M)</option>
                <option value="venture">Venture Capital ($2M+)</option>
                <option value="strategic">Strategic Partnership</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div className="form-group">
              <textarea
                name="message"
                placeholder="Tell us about your investment goals and interests"
                value={formData.message}
                onChange={handleChange}
                rows="4"
                className="form-textarea"
              />
            </div>
            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="walkthrough_requested"
                  checked={formData.walkthrough_requested}
                  onChange={handleChange}
                />
                <span className="checkbox-custom"></span>
                Request exclusive VR experience walkthrough
              </label>
            </div>
            <button type="submit" className="form-submit-btn">
              Schedule Investment Discussion
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

const App = () => {
  const [chapters, setChapters] = useState([]);
  const [sacredSites, setSacredSites] = useState([]);
  const [currentView, setCurrentView] = useState('home');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeData();
  }, []);

  const initializeData = async () => {
    try {
      // Initialize sample data
      await axios.post(`${API}/initialize-data`);
      
      // Fetch chapters and sites
      const [chaptersRes, sitesRes] = await Promise.all([
        axios.get(`${API}/trilogy-chapters`),
        axios.get(`${API}/sacred-sites`)
      ]);
      
      setChapters(chaptersRes.data);
      setSacredSites(sitesRes.data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="cosmic-loader">
          <div className="loader-sphere"></div>
          <p>Initializing Quanta Mars...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <nav className="nav-bar">
        <div className="nav-logo">
          <span className="logo-text">QUANTA MARS</span>
        </div>
        <div className="nav-links">
          <button 
            className={currentView === 'home' ? 'nav-link active' : 'nav-link'}
            onClick={() => setCurrentView('home')}
          >
            Home
          </button>
          <button 
            className={currentView === 'trilogy' ? 'nav-link active' : 'nav-link'}
            onClick={() => setCurrentView('trilogy')}
          >
            Trilogy
          </button>
          <button 
            className={currentView === 'sites' ? 'nav-link active' : 'nav-link'}
            onClick={() => setCurrentView('sites')}
          >
            Sacred Sites
          </button>
          <button 
            className={currentView === 'invest' ? 'nav-link active' : 'nav-link'}
            onClick={() => setCurrentView('invest')}
          >
            Invest
          </button>
        </div>
      </nav>

      {currentView === 'home' && (
        <>
          <HeroSection onBeginExperience={() => setCurrentView('trilogy')} />
          <TrilogyBrowser chapters={chapters.slice(0, 3)} />
          <SacredSitesGallery sites={sacredSites.slice(0, 6)} />
          <BackerEngagementSection />
        </>
      )}

      {currentView === 'trilogy' && (
        <div className="page-container">
          <TrilogyBrowser chapters={chapters} />
        </div>
      )}

      {currentView === 'sites' && (
        <div className="page-container">
          <SacredSitesGallery sites={sacredSites} />
        </div>
      )}

      {currentView === 'invest' && (
        <div className="page-container">
          <BackerEngagementSection />
        </div>
      )}

      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2025 Quanta Mars - The Harmonic Trilogy Experience</p>
          <p>Designed for The Sphere, Las Vegas | 16K Immersive Reality</p>
        </div>
      </footer>
    </div>
  );
};

export default App;