<script setup>
// Vue의 Compositon API 가져오기
import { ref, computed, watch, onMounted } from "vue";
// HTTP 요청을 위한 Axios 라이브러리 가져오기
import axios from "axios";
// 차트 컴포넌트 가져오기
import AirQualityChart from "./AirQualityChart.vue";

// axios 요청을 통해 가져온 데이터를 저장하는 배열
const airQualityData = ref([]);
// 측정소 이름 저장 변수
const stationName = ref("미사");

// 알림 권한이 없을 경우 알림 권한 요청 함수
const requestNotificationPermission = () => {
  if ("Notification" in window) {
    Notification.requestPermission().then((permission) => {
      if (permission !== "granted") {
        console.warn("알림 권한이 허용되지 않았습니다.");
      }
    });
  }
};

// 사용자에게 알림을 보내는 함수
const sendNotification = (status) => {
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification("🚨 미세먼지 경고!", {
      body: `현재 대기 상태: ${status} - 마스크 착용을 권장합니다!`,
      icon: "https://cdn-icons-png.flaticon.com/512/1995/1995429.png",
    });
  }
};

// axios 요청 함수 선언
const fetchAirQuality = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/air-quality?station_name=${stationName.value}`);
    // 최근 10개 데이터만 저장
    airQualityData.value = response.data.slice(0, 10); 
    // 미세먼지 상태가 "나쁨" 이상일 때 알림 표시
    const latestData = airQualityData.value[0];
    if (latestData && (latestData.status === "나쁨" || latestData.status === "매우 나쁨")) {
      sendNotification(latestData.status);
    }
  } catch (error) {
    console.error("API 호출 오류:", error);
  }
};

// 측정소명(stationName)이 변경될 때 새로운 데이터 요청
watch(stationName, async () => {
  await fetchAirQuality();
});

// 컴포넌트가 처음 마운트될 때 데이터 요청 및 1시간마다 자동 갱신
onMounted(() => {
  fetchAirQuality();
});

// 가장 최근 데이터만 개별적으로 표시
const latestAirQuality = computed(() => {
  return airQualityData.value.length > 0 ? airQualityData.value[0] : null;
});

// 대기오염 지수의 상태에 따른 색상 변경
const statusColor = computed(() => {
  if (!latestAirQuality.value) return "gray";
  switch (latestAirQuality.value.status) {
    case "좋음":
      return "#4CAF50"; // 초록색
    case "보통":
      return "#2196F3"; // 파란색
    case "나쁨":
      return "#FF9800"; // 주황색
    case "매우 나쁨":
      return "#F44336"; // 빨간색
    default:
      return "white";    // 회색
  }
});
</script>

<template>
  <div :style="{ transition: 'background-color 0.5s ease', padding: '20px', borderRadius: '10px', textAlign: 'center' }">
    <h2>미세먼지 정보</h2>

    <!-- 측정소 선택(지역 선택) 드롭다운 -->
    <label for="station">지역 선택:</label>
    <select id="station" v-model="stationName">
      <option value="종로구">종로구</option>
      <option value="강남구">강남구</option>
      <option value="서초구">서초구</option>
      <option value="마포구">마포구</option>
      <option value="송파구">송파구</option>
      <option value="애월읍">애월읍</option>
      <option value="노원구">노원구</option>
      <option value="미사">미사</option>
    </select>

    <!-- 가장 최근의 대기질 정보 표시 -->
    <div v-if="latestAirQuality">
      <p><strong>측정 시간:</strong> {{ latestAirQuality.dataTime }}</p>
      <p><strong>미세먼지 (PM10):</strong> {{ latestAirQuality.pm10 }} ㎍/㎥</p>
      <p><strong>초미세먼지 (PM2.5):</strong> {{ latestAirQuality.pm25 }} ㎍/㎥</p>
      <p><strong>대기오염 지수:</strong> {{ latestAirQuality.air_quality_index }}</p>
      <p><strong>상태:</strong> <span :style="{ fontWeight: 'bold', color: statusColor, fontSize: '1.2em' }">{{ latestAirQuality.status }}</span></p>

      <!-- 차트 컴포넌트 그래프를 만들기 위해 최근 10개 데이터 전달 -->
      <AirQualityChart :airQualityData="airQualityData" />
    </div>
    <div v-else>
      <p>데이터를 불러오는 중...</p>
    </div>
  </div>
</template>

<style scoped>
select {
  padding: 5px;
  font-size: 1em;
  margin-bottom: 10px;
}
h2 {
  color: white;
}
p {
  font-size: 1.1em;
  color: white;
}
</style>