<template>
  <div id="app">
    <DatasetExplorer />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DatasetExplorer from "./components/DatasetExplorer.vue";

export default defineComponent({
  name: "App",
  components: {
    DatasetExplorer,
  },
});
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  padding: 20px;
}
</style>
