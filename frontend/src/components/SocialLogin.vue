<script setup>
import { ref, onMounted } from 'vue';
import { decodeCredential, GoogleLogin } from 'vue3-google-login';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const isGoogleLoaded = ref(false);
const store = useStore();
const router = useRouter();

const callback = async (response) => {
  try {
    const userData = decodeCredential(response.credential);
    await store.dispatch('module1/googleLogin', userData);
    router.push('/');

  } catch (error) {
    console.error('Google Login Error:', error);
  }
};

onMounted(() => {
  setTimeout(() => {
    isGoogleLoaded.value = true;
  }, 100);
});
</script>

<template>
  <div class="social-login-container">
    <div v-if="!isGoogleLoaded" class="google-placeholder">
      Loading...
    </div>
    
    <div :class="['google-button-wrapper', { 'loaded': isGoogleLoaded }]">
      <GoogleLogin 
        :callback="callback" 
        prompt 
        auto-login
      />
    </div>
  </div>
</template>

<style scoped>
.social-login-container {
  min-height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.google-button-wrapper {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.google-button-wrapper.loaded {
  opacity: 1;
}

.google-placeholder {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-color-light);
}
</style>