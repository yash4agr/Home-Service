<script>
</script>

<template>
    <div class="login" id="login">
      <form action="" class="login__form">
        <h2>Log In</h2>

        <div class="login__group">
            <div class="login__item">
                <label for="email" class="login__label">Email</label>
                <input type="email" class="login__input" placeholder="Enter your email" id="email">
            </div>

            <div class="login__item">
                <label for="password" class="login__label">Password</label>
                <input type="password" class="login__input" placeholder="Enter your password" id="password">
            </div>
        </div>

        <div class="login__register">
            <p class="login__signup">
                Don't have an account? <RouterLink to="/register">Sign up</RouterLink>
            </p>

            <a href="/forgot_password" class="login__forgot">
                Forgot password?
            </a>

            <button class="login__button" type="submit">Log In</button>
        </div>
      </form>

      <router-link class="ri-close-line login__close" id="login-close" to="/"></router-link>
    </div>
    
</template>

<style scoped>

.login {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: var(--z-modal);
    background-color: var(--background-color-blur);
    -webkit-backdrop-filter: blur(24px);
    backdrop-filter: blur(24px);
    padding: 8rem 1.5rem 0;
    opacity: 1;
    /* pointer-events: none; */
    transition: opacity 0.2s;
}

.login__close {
    position: absolute;
    top: 2rem;
    /* right: 2rem; */
    left: 50%;
    transform: translateX(-50%);
    font-size: 1.5rem;
    color: var(--title-color);
    cursor: pointer;
}

/* .login__close {
    width: -moz-max-content;
    width: max-content;
    top: 5rem;
    left: 0;
    right: 0;
    margin-inline: auto;
    font-size: 2rem;
    color: #fff;
    z-index: 10000000;
  } */

.login__form{
    display: grid;
    background-color: var(--container-color);
    padding: 3rem 2rem 3.5rem;
    box-shadow: 0 8px 32px var(--background-color-blur);
    border-radius: 1rem;
    row-gap: 1.25rem;
    text-align: center;
    transform: translateY(-1rem);
    transition: transform 0.2s;
    max-width: 400px;
    margin-inline: auto;
}

.login__title {
    font-size: var(--h2-font-size);
    color: var(--title-color);
}

.login__group{
    display: grid;
    row-gap: 1rem;
}

.login__label {
    display: block;
    text-align: initial;
    color: var(--title-color);
    font-weight: var(--font-medium);
    margin-bottom: 0.25;    
}
.login__input {
  width: 100%;
  background-color: var(--container-color);
  border: 2px solid var(--border-color);
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--text-color);
}
.login__input::-moz-placeholder {
  color: var(--text-color);
}
.login__input::placeholder {
  color: var(--text-color);
}
.login__signup {
  margin-bottom: 0.5rem;
}
.login__signup a {
  color: var(--first-color);
}
.login__forgot {
  display: inline-block;
  color: var(--first-color);
  margin-bottom: 1.25rem;
}
.login__button {
  display: inline-block;
  background-color: var(--first-color);
  width: 100%;
  color: #fff;
  font-weight: var(--font-semi-bold);
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: box-shadow 0.4s;
}
.login__button:hover {
  box-shadow: 0 4px 24px hsla(230, 75%, 40%, 0.4);
}

</style>