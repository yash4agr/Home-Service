<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const searchQuery = ref('')

const services = computed(() => store.getters['module2/servicesList'])
const popularServices = computed(() => store.getters['module2/servicesPopular'])


const filteredServices = computed(() => {
  const query = searchQuery.value.toLowerCase()
  const results = services.value.filter(service => 
    service.name.toLowerCase().includes(query) ||
    service.tags.some(cat => cat.toLowerCase().includes(query)) ||
    service.description.toLowerCase().includes(query)
  )
  return results.length > 4 ? results.slice(0, 4) : results
})

const addToCart = (service) => {
  store.dispatch('module2/addToCart', service)
}

onMounted(() => {
  store.dispatch('module2/fetchServices')
  store.dispatch('module2/fetchCategories')
})
</script>

<template>
  <div class="app-container">
    <!-- Main Content -->
    <section id="home">
      <div class="hero">
        <div class="hero-content">
          <h1>Professional Home Services</h1>
          <p>Expert services at your doorstep</p>
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery"
              placeholder="Search for services..."
            >
            <button>Search</button>
          </div>
        </div>
      </div>
    </section>

    <section id="categories">
      <div class="container">
        <h2>Our Services</h2>
        <div class="service-grid">
          <div v-for="service in filteredServices" 
               :key="service.id" 
               class="service-card"
               :class="{ 'animate-card': true }">
            <div class="service-image">
              <img :src="service.img" :alt="service.name">
              <div class="service-overlay">
                <button class="book-now" @click="addToCart(service)">Add to Cart</button>
              </div>
            </div>
            <div class="service-info">
              <h3>{{ service.name }}</h3>
              <p class="service-description">{{ service.description }}</p>
              <div class="rating">
                <span class="stars">
                  <span v-for="i in Math.floor(service.rating)">
                  <i class="ri-star-fill" /></span>

                  <span v-if="service.rating % 1 !== 0">
                    <i class="ri-star-half-fill" /></span>

                    <span v-for="i in 5 - Math.ceil(service.rating)">
                      <i class="ri-star-line" /></span>
                </span>
                <span class="rating-number">{{ service.rating }}/5</span>
              </div>
              <div class="price">
                Starting from ₹{{ service.base_price }}
              </div>
              <div class="categories">
                <span v-for="(tag, index) in service.tags" :key="index">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="popular">
      <div class="container">
        <h2>Popular Services</h2>
        <div class="service-grid">
          <div v-for="service in popularServices" 
               :key="service.id" 
               class="service-card"
               :class="{ 'animate-card': true }">
            <div class="service-image">
              <img :src="service.img" :alt="service.name">
              <div class="service-overlay">
                <button class="book-now" @click="addToCart(service)">Add to Cart</button>
              </div>
            </div>
            <div class="service-info">
              <h3>{{ service.name }}</h3>
              <p class="service-description">{{ service.description }}</p>
              <div class="rating">
                <span class="stars">
                  <span v-for="i in Math.floor(service.rating)">
                  <i class="ri-star-fill" /></span>

                  <span v-if="service.rating % 1 !== 0">
                    <i class="ri-star-half-fill" /></span>

                    <span v-for="i in 5 - Math.ceil(service.rating)">
                      <i class="ri-star-line" /></span>
                </span>
                <span class="rating-number">{{ service.rating }}/5</span>
              </div>
              <div class="price">
                Starting from ₹{{ service.base_price }}
              </div>
              <div class="categories">
                <span v-for="(tags, index) in service.tags" :key="index">
                  {{ tags }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

/* 
:root {
  --primary-color: #2563eb;
  --secondary-color: #1e40af;
  --text-color: #1f2937;
  --light-gray: #f3f4f6;
  --white: #ffffff;
  --transition-speed: 0.3s;
} */

.app-container {
  position: relative;
  min-height: 100vh;
}

/* Enhanced Container Styles */
.container {
  max-width: 1200px;
  width: 90%;
  margin: 0 auto;
  padding: 2rem 0;
}

.container {
  color: var(--primary-color);
}

/* Enhanced Hero Section */
.hero {
  height: 500px;
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('/src/assets/home-bg.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--primary-color);
  position: relative;
}

.hero-content {
  padding: 2rem;
  animation: fadeInUp 1s ease-out;
}

.hero-content h1 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* Enhanced Search Box */
.search-box {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  position: relative;
}

.search-box input {
  flex: 1;
  padding: 1.2rem;
  border: none;
  border-radius: 4px 0 0 4px;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.search-box button {
  padding: 1.2rem 2rem;
  background: var(--accent-color);
  color: var(--white);
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  transition: var(--bg-color) var(--transition-speed);
}

.search-box button:hover {
  background: var(--secondary-color);
}

/* Enhanced Service Grid */
.service-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.service-card {
  background: var(--container-color);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform var(--transition-speed);
  position: relative;
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-speed);
}

.service-card:hover .service-image img {
  transform: scale(1.05);
}

.service-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--transition-speed);
}

.service-card:hover .service-overlay {
  opacity: 1;
}

.book-now {
  padding: 0.8rem 1.5rem;
  background: var(--accent-color);
  color: var(--white);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color var(--transition-speed);
}

.book-now:hover {
  background: var(--secondary-color);
}

.service-info {
  padding: 1.5rem;
}

.service-info h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.service-description {
  font-size: 0.9rem;
  color: var(--accent-color);
  margin-bottom: 1rem;
  line-height: 1.5;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.stars {
  /* color: #ffd700; */
  color: var(--secondary-color);
  letter-spacing: 2px;
}

.rating-number {
  color: #666;
  font-size: 0.9rem;
}

.price {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.categories span {
  background: var(--accent-color);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: var(--text-color);
}

/* Empty Cart State */
.empty-cart {
  text-align: center;
  padding: 2rem;
  color: #666;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-content h1 {
    font-size: 2.8rem;
  }
  
  .cart-sidebar {
    width: 350px;
    right: -350px;
  }
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.2rem;
  }
  
  .hero-content p {
    font-size: 1rem;
  }
  
  .search-box {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-box input,
  .search-box button {
    border-radius: 4px;
  }
  
  .cart-sidebar {
    width: 100%;
    right: -100%;
  }
  
  .service-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero-content h1 {
    font-size: 1.8rem;
  }
  
  .container {
    width: 95%;
  }
  
  .cart-toggle {
    width: 50px;
    height: 50px;
    font-size: 1rem;
    bottom: 1rem;
    right: 1rem;
  }
  
  .service-image {
    height: 180px;
  }
  
  .service-info {
    padding: 1rem;
  }
}

/* Touch Device Optimizations */
@media (hover: none) {
  .service-overlay {
    opacity: 1;
    background: rgba(0, 0, 0, 0.3);
  }
  
  .service-card:hover {
    transform: none;
  }
  
  .service-card:hover .service-image img {
    transform: none;
  }
}
</style>