<script setup lang="ts">
// import HelloWorld from './components/HelloWorld.vue'
import GithubVersion from "./components/GithubVersion.vue";
</script>

<template>

  <h1>shmtu-auth Doc Test</h1>

  <!--  <HelloWorld msg="Vite + Vue" />-->

  <div class="version-list">
    <GithubVersion branch="main"/>
    <GithubVersion branch="beta"/>
    <GithubVersion branch="dev"/>
  </div>

</template>

<style scoped>

</style>
