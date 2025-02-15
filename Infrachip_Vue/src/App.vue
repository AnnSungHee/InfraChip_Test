<script setup>
import AirQuality from "./components/AirQuality.vue";
</script>

<!-- 화면에 보여질 요소 설정 -->
<template>
  <div>
    <h1>실시간 미세먼지 정보</h1>
    <AirQuality />
  </div>
</template>

<!-- template 블록의 요소들 CSS 설정 -->
<style scoped>
h1 {
  text-align: center;
  color: #2c3e50;
}
</style>
