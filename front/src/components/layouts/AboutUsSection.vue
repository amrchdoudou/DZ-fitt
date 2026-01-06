<script setup>
import iconsImg from '../../images/icons.png'
import footerBg from '../../images/footerbg.png'
import { i18n } from '../../i18n.js'

const $i18n = i18n;
</script>

<template>
  <div>
    <section id="about-us" class="about-us">
      <div class="about-container">
        <img :src="iconsImg" alt="DZ-Fit icons" class="about-icons" />
        
        <div class="about-content-wrapper">
          <div class="about-content-box">
            <div class="about-grid-pattern"></div>
            <div class="about-accent-glow"></div>
            
            <h2 class="about-title">{{ $i18n.t('about.title') }}</h2>
            
            <div class="about-text">
              <p>{{ $i18n.t('about.p1') }}</p>
              <p>{{ $i18n.t('about.p2') }}</p>
              <p class="about-mission">{{ $i18n.t('about.mission') }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <footer class="footer">
      <div class="footer-bg">
        <img :src="footerBg" alt="Footer background" class="footer-bg-img" />
      </div>
      
      <div class="footer-content">
        <div class="footer-grid">
          <div class="footer-section">
            <h3 class="footer-brand">DZ-Fit</h3>
            <p class="footer-description">
              Your ultimate guide to finding the perfect gym in Algeria. Compare, explore, and start your fitness journey today.
            </p>
          </div>
          
          <div class="footer-section">
            <h4 class="footer-heading">{{ $i18n.t('navbar.home') }}</h4>
            <ul class="footer-links">
              <li><router-link to="/">{{ $i18n.t('navbar.home') }}</router-link></li>
              <li><router-link to="/SearchResult">{{ $i18n.t('navbar.search') }}</router-link></li>
              <li><a href="mailto:contact@dz-fit.com">Contact</a></li>
              <li><router-link to="/login">{{ $i18n.t('navbar.login') }}</router-link></li>
            </ul>
          </div>
          
          <div class="footer-section">
            <h4 class="footer-heading">Get in Touch</h4>
            <div class="footer-contact">
              <p>Email: contact@dz-fit.com</p>
              <p>Phone: +213 XXX XXX XXX</p>
              <div class="footer-social">
                <a href="#" class="social-icon" aria-label="Facebook">
                  <svg class="social-svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                </a>
                <a href="#" class="social-icon" aria-label="Instagram">
                  <svg class="social-svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p class="footer-copyright">
            © 2024 DZ-Fit. All rights reserved. Built with 💪 in Algeria.
          </p>
        </div>
      </div>

      <!-- Wave decoration -->
      <div class="footer-wave">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
          <path d="M0 120L60 110C120 100 240 80 360 73.3C480 67 600 73 720 76.7C840 80 960 80 1080 73.3C1200 67 1320 53 1380 46.7L1440 40V0H1380C1320 0 1200 0 1080 0C960 0 840 0 720 0C600 0 480 0 360 0C240 0 120 0 60 0H0V120Z" fill="#B3F90F"/>
        </svg>
      </div>
    </footer>
  </div>
</template>


<style scoped>
.about-us {
  border-top: 1px solid rgba(179, 249, 15, 0.4);
  background-color: #0940BE;
  padding: 96px 0;
}

.about-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.about-icons {
  width: 100%;
  object-fit: contain;
  opacity: 0.9;
}

.about-content-wrapper {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
}

.about-content-box {
  position: relative;
  width: 100%;
  max-width: 800px;
  padding: 56px 40px 64px;
  text-align: center;
  background: rgba(9, 64, 190, 0.85);
  backdrop-filter: blur(8px);
  border-radius: 24px;
  border: 1px solid rgba(179, 249, 15, 0.4);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  margin: 0 auto;
}

.about-grid-pattern {
  position: absolute;
  inset: 0;
  border-radius: 24px;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

.about-accent-glow {
  position: absolute;
  top: -80px;
  left: 50%;
  transform: translateX(-50%);
  width: 160px;
  height: 160px;
  background: rgba(179, 249, 15, 0.2);
  border-radius: 50%;
  filter: blur(60px);
  pointer-events: none;
}

.about-title {
  position: relative;
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  color: white;
  margin: 0 0 32px 0;
  font-family: 'Roboto Flex', sans-serif;
  letter-spacing: -0.5px;
}

.about-text {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 24px;
  font-size: clamp(16px, 2vw, 18px);
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.95);
}

.about-text p {
  margin: 0;
}

.about-mission {
  font-weight: 600;
  color: #B3F90F;
  font-size: clamp(18px, 2.2vw, 20px);
  margin-top: 8px;
}

.footer {
  position: relative;
  background-color: #0940BE;
  overflow: hidden;
  min-height: 500px;
}

.footer-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
}

.footer-bg-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.footer-content {
  position: relative;
  z-index: 10;
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 24px 100px;
  overflow: visible;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 56px 40px;
  max-width: 100%;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 100%;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.footer-brand {
  font-size: clamp(26px, 3vw, 30px);
  font-weight: 700;
  color: #0940BE;
  margin: 0 0 14px 0;
  font-family: 'Roboto Flex', sans-serif;
}

.footer-description {
  font-size: clamp(15px, 1.8vw, 17px);
  line-height: 1.7;
  color: rgba(9, 64, 190, 0.75);
  margin: 0;
  max-width: 100%;
  word-wrap: break-word;
}

.footer-contact p {
  font-size: clamp(15px, 1.8vw, 17px);
  line-height: 1.7;
  color: rgba(9, 64, 190, 0.85);
  margin: 0 0 8px 0;
  word-wrap: break-word;
}

.footer-heading {
  font-size: clamp(19px, 2.2vw, 21px);
  font-weight: 600;
  color: #B3F90F;
  margin: 0 0 16px 0;
  font-family: 'Roboto Flex', sans-serif;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-links a {
  font-size: clamp(15px, 1.8vw, 17px);
  color: rgba(9, 64, 190, 0.8);
  text-decoration: none;
  transition: all 0.3s;
  display: block;
  word-wrap: break-word;
  font-weight: 500;
}

.footer-links a:hover {
  color: #0940BE;
  transform: translateX(4px);
}

.footer-contact {
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-size: clamp(15px, 1.8vw, 17px);
  color: rgba(9, 64, 190, 0.85);
  max-width: 100%;
}

.footer-social {
  display: flex;
  gap: 16px;
  padding-top: 8px;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(9, 64, 190, 0.15);
  color: #0940BE;
  transition: all 0.3s;
}

.social-icon:hover {
  background-color: #B3F90F;
  color: #0940BE;
}

.social-svg {
  width: 20px;
  height: 20px;
}

.footer-bottom {
  margin-top: 48px;
  padding-top: 32px;
  border-top: 1px solid rgba(9, 64, 190, 0.15);
  text-align: center;
}

.footer-copyright {
  font-size: clamp(15px, 1.8vw, 17px);
  color: rgba(9, 64, 190, 0.65);
  margin: 0;
  word-wrap: break-word;
  max-width: 100%;
  font-weight: 400;
}

.footer-wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px;
  z-index: 5;
}

.footer-wave svg {
  display: block;
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .about-us {
    padding: 60px 0;
  }
  
  .about-title {
    font-size: clamp(28px, 6vw, 36px);
  }
  
  .about-text {
    font-size: clamp(15px, 3vw, 17px);
    gap: 20px;
  }
  
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 40px 0;
  }

  .footer-content {
    padding: 60px 20px 80px;
  }

  .footer-section {
    gap: 16px;
  }
}
</style>