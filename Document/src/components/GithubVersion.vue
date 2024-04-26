<script setup lang="ts">

import {onMounted, ref} from 'vue'
import axios from 'axios';

const props = defineProps({
  branch: {
    type: String,
    required: true,
  },
});

const github_resource_base = "https://raw.githubusercontent.com"
const github_repo = "a645162/shmtu-auth"

const version_url =
    ref(
        `${github_resource_base}/${github_repo}/${props.branch}/version.txt`
    )

const versionFileContent = ref('');

onMounted(async () => {
  try {
    const response = await axios.get<string>(version_url.value);
    versionFileContent.value = response.data;
  } catch (error) {
    console.error('Error fetching file content:', error);
  }
});

</script>

<template>


  <p>{{ version_url }}</p>
  <p>{{ versionFileContent }}</p>

</template>

<style scoped>

</style>
