<script setup>

</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="#">About us</a></li>
          <li><a href="#">Terms & Conditions</a></li>
          <li><a href="#">Privacy policy</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>For customer</h4>
        <ul>
          <li><a href="#">FAQ</a></li>
          <li><a href="#">Support</a></li>
          <li><a href="#">Contact us</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>For partners</h4>
        <ul>
          <li><a href="#">Become a partner</a></li>
          <li><a href="#">Partner login</a></li>
          <li><a href="#">Partner support</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Follow us</h4>
        <div class="social-links">
          <a href="#"><i class="ri-facebook-fill"></i></a>
          <a href="#"><i class="ri-twitter-x-fill"></i></a>
          <a href="#"><i class="ri-instagram-line"></i></a>
          <a href="#"><i class="ri-linkedin-fill"></i></a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: var(--footer-bg-color, #151515);
  color: var(--footer-text-color, #fff);
  padding: 4rem 0 2rem;
  border-top: solid 1px;
  border-color: var(--accent-color);
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  padding: 0 2rem;
}

.footer-col {
  width: 100%;
  margin-bottom: 2rem;
}

.footer-col h4 {
  font-size: 1.2rem;
  color: var(--footer-heading-color, #fff);
  text-transform: capitalize;
  margin-bottom: 2rem;
  font-weight: 500;
  position: relative;
}

.footer-col h4::before {
  content: '';
  position: absolute;
  left: 0;
  bottom: -10px;
  background-color: var(--accent-color);
  height: 2px;
  width: 50px;
}

.footer-col ul {
  list-style: none;
  padding: 0;
}

.footer-col ul li:not(:last-child) {
  margin-bottom: 10px;
}

.footer-col ul li a {
  font-size: 1rem;
  text-transform: capitalize;
  color: var(--footer-link-color, #bbbbbb);
  text-decoration: none;
  font-weight: 300;
  display: block;
  transition: all 0.3s ease;
}

.footer-col ul li a:hover {
  color: var(--footer-link-hover-color, #ffffff);
  padding-left: 8px;
}

.footer-col .social-links a {
  display: inline-block;
  height: 40px;
  width: 40px;
  background-color: rgba(255, 255, 255, 0.2);
  margin: 0 10px 10px 0;
  text-align: center;
  line-height: 40px;
  border-radius: 50%;
  color: var(--footer-social-icon-color, #ffffff);
  transition: all 0.5s ease;
}

.footer-col .social-links a:hover {
  color: var(--footer-social-icon-hover-color, #24262b);
  background-color: var(--footer-social-bg-hover-color, #ffffff);
}

@media (min-width: 576px) {
  .footer-col {
    width: 50%;
  }
}

@media (min-width: 768px) {
  .footer-col {
    width: 25%;
  }
}
</style>