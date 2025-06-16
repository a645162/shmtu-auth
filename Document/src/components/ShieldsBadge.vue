<script setup lang="ts">

import {computed, ref} from "vue";

const props = defineProps({
  text1: {
    type: String,
    required: true,
  },
  text2: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    required: true,
  },
  logo: {
    type: String,
    required: true,
  },
  logoColor: {
    type: String,
    default: "",
  },
  style: {
    type: String,
    default: "flat-square",
  },
});

const base_url = "https://img.shields.io/badge/"

const newColor = computed(() => {
  return props.color.trim().startsWith("#") ?
      props.color.trim().substring(1)
      :
      props.color.trim()
});

const newLogoColor = computed(() => {
  const originalColor = props.logoColor.trim();

  if (originalColor.length <= 1) {
    return newColor.value;
  }

  if (originalColor.startsWith("#")) {
    return originalColor.substring(1);
  }

  return originalColor;
});

const url = computed(() => {
  return `${base_url}${props.text1}-${props.text2}-${newColor}` +
      `?style=${props.style}&logo=${props.logo}&logoColor=${newLogoColor}`
});

const isValid = computed(() => {
  return props.text1.trim() !== "" &&
      props.text2.trim() !== "" &&
      props.color.trim() !== "" &&
      props.logo.trim() !== ""
});

</script>

<template>

  <img
      v-if="isValid"
      :src="url"
      alt="text-badge"
  />

</template>

<style scoped>

</style>
