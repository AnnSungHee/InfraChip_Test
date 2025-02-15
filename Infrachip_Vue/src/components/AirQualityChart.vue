<script setup>
// Vue의 Composition API에서 반응형 상태 및 감시 기능 가져오기
import { reactive, watch, onMounted } from "vue";
// Chart.js 모듈 가져오기
import { Chart, registerables } from "chart.js";
// Vue에서 사용할 라인 차트 컴포넌트 가져오기
import { LineChart } from "vue-chart-3";

// Chart.js 모듈 등록
Chart.register(...registerables);

// 부모 컴포넌트(AirQuality.vue)에서 전달받은 변수 정의 (측정소에서 가져온 최근 10개의 데이터)
const props = defineProps(["airQualityData"]);

// 차트 데이터를 `reactive()`로 저장하여 자동 업데이트되도록 변경
const chartData = reactive({
  // 차트의 x축 (시간)
  labels: [],
  
  // label: 데이터셋 라벨
  // data: 데이터 저장
  // borderColor: 선 색상
  // backgroundColor: 배경 색상
  // fill: 배경 색상 채우기 여부
  // tension: 선의 부드러움 정도
  datasets: [
    {
      label: "미세먼지 (PM10)",
      data: [],
      borderColor: "rgba(255, 99, 132, 1)",
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      fill: true,
      tension: 0.3,
    },
    {
      label: "초미세먼지 (PM2.5)",
      data: [],
      borderColor: "rgba(54, 162, 235, 1)",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      fill: true,
      tension: 0.3,
    },
  ],
});

// 처음 데이터를 로드할때 차트 생성
onMounted(() => {
  if (props.airQualityData.length > 0) {
    chartData.labels = props.airQualityData.map((item) => item.dataTime).reverse();
    chartData.datasets[0].data = props.airQualityData.map((item) => item.pm10).reverse();
    chartData.datasets[1].data = props.airQualityData.map((item) => item.pm25).reverse();
  }
});

// 최신 데이터가 오른쪽에 표시되도록 배열을 역순으로 변경
watch(
  () => props.airQualityData,
  (newData) => {
    if (newData.length > 0) {
      chartData.labels = newData.map((item) => item.dataTime).reverse(); 
      chartData.datasets[0].data = newData.map((item) => item.pm10).reverse();
      chartData.datasets[1].data = newData.map((item) => item.pm25).reverse();
    }
  },
  // airQualityData의 내부 속성이 변경되어도 watch가 실행되도록 설정
  { deep: true }
);

// 차트 옵션 설정
const chartOptions = {
  // 반응형으로 설정
  responsive: true,
  // 종횡비 유지 해제
  maintainAspectRatio: false,
  // 애니메이션 설정
  animation: {
    // 지속시간 1초
    duration: 1000,
    // easeInOutQuad 효과 설정 
    easing: "easeInSine",
  },
  // 차트의 크기 설정
  scales: {
    y: {
      // Y축의 최솟값 0으로설정
      beginAtZero: true,
      // Y축의 최대값을 100으로 설정
      suggestedMax: 100,
    },
  },
};
</script>

<template>
  <div class="chart-container">
    <!-- LineChart 컴포넌트 렌더링 차트 데이터와 차트 렌더링 옵션 전달 -->
    <LineChart :chart-data="chartData" :chart-options="chartOptions" />
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
  margin: auto;
}
</style>
