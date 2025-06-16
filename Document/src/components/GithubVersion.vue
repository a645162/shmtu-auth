<script setup lang="ts">

import {computed, onMounted, ref} from 'vue'
import axios from 'axios';
import ShieldsBadge from "./ShieldsBadge.vue";

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

const isValid = computed(() => {
  const originalVersion = versionFileContent.value.trim();

  if (originalVersion.length === 0) {
    return false;
  }

  if (originalVersion.includes("404")) {
    return false;
  }

  const spilt_version = originalVersion.split('.')

  if (spilt_version.length != 3) {
    return false
  }

  for (let i = 0; i < spilt_version.length; i++) {
    if (isNaN(Number(spilt_version[i]))) {
      return false;
    }
  }

  return true;
});

onMounted(async () => {
  try {
    const response = await axios.get<string>(version_url.value);
    versionFileContent.value = response.data;
    versionFileContent.value = versionFileContent.value.trim();
  } catch (error) {
    console.error('Error fetching file content:', error);
  }
});

</script>

<template>

  <div
      class="budge-version"
      v-if="isValid"
  >
    <ShieldsBadge
        logo="python"
        color="#3776AB"
        :text1="props.branch"
        :text2="versionFileContent"
    />
  </div>

  <!--  <p>{{ version_url }}</p>-->
  <!--  <p>{{ versionFileContent }}</p>-->

</template>

<style scoped>

</style>
