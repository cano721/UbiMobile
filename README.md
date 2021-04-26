# UbiMobile(유비모빌)

#### 프로젝트 개요

- 자율주행 자동차 프로젝트
  - 자동차와 IT의 융합이 가속화 되면서 운전자의 안전과 편의성이 향상된 스마트카가 속속 개발되고 있다. 최근의 스마트카는 IoT기술을 적용하여 자동차의 안정성을 극대화하면서 운전자의 편의성을 추구 할 수 있는 자동차의 패러다임을 변화시킬수 있는 기술을 적용하고 있다. 이러한 흐름에 맞춰 다양한 기능을 추가해 모델링한 UbiMobile을 통해 자율주행에 접근한다.



#### 주요 기능

- 차선 인식하여 자율주행(영상처리)

- 차량 간격 제어(초음파센서)

- 충격 감지 시스템(충격감지센서)

  - 발생 시 핸드폰으로 알림 전송

- 졸음 운전 방지(맥박센서)

  - 핸들쪽에 맥박센서 설치 - 심박 수 일정수치 이하 부저 소리나게

- 차량 문 제어(서보모터)

- 주차관리(압력패드) - 주차패드 위 압력패드 - 라인트레이서 연결

  

- 미구현 

  - 신호등 인식하여 자율주행
  - 차량 이동구간 확인(GPS)
  - 차량 관리 내용(주행km, 차량정비날짜 등)



#### 개발 환경

- 라즈베리파이 (https://www.raspberrypi.org/)
  - Raspberry Pi OS with desktop and recommended software / Kernel version: 5.10
- 아두이노 (https://www.arduino.cc/)
  - Arduino IDE 1.8.13
- 안드로이드 스튜디오 (https://developer.android.com/studio?hl=ko)
  - 4.1.1

- 파이썬
  - 3.6.4

- 파이참 (https://www.jetbrains.com/pycharm/)
  - Community Version
- MongoDB (https://www.mongodb.com/)
  - windows_x86_64 x64
- Mosquitto (https://mosquitto.org/)
  - [mosquitto-2.0.10-install-windows-x64.exe](https://mosquitto.org/files/binary/win64/mosquitto-2.0.10-install-windows-x64.exe) (64-bit build, Windows Vista and up, built with Visual Studio Community 2019)



#### 사용장비

- 압력센서(http://www.11st.co.kr/products/3126172027) 9,900*2
- 맥박센서(https://www.devicemart.co.kr/goods/view?no=12319052) 4,000*1
- 진동센서(https://www.devicemart.co.kr/goods/view?no=1278061) 1,200*1
- 시프트 레지스터 74HC165([https://www.devicemart.co.kr/goods/view?no=11980](https://www.devicemart.co.kr/goods/view?no=11980#goods_qna)) 220*4
- DIP 스위치(https://www.devicemart.co.kr/goods/view?no=1781) 480*3
- 라즈베리파이 카메라
- 서보모터*2
- 초음파센서
- 주행장(차선, 신호등)



#### ERD (https://www.erdcloud.com/d/P4moJLikcMExetmtD)
![image](https://user-images.githubusercontent.com/77091144/116164023-ee699680-a733-11eb-8cc7-594c83829af3.png)





#### 개발 일정

| 년.월   | 일       | 내용               |
| ------- | -------- | ------------------ |
| 2021.03 | 25~04.05 | 프로젝트 주제 설정 |
| 2021.04 | 05~11    | 화면설계           |
|         | 12       | ERD 설계           |
|         | 13~18    | 기능구현           |
|         | 19~25    | 모델링             |
|         | 27       | 최종완성           |



#### 개발자 정보

계해범 [**cano721**](https://github.com/cano721)

목민수 [**angriff1**](https://github.com/angriff1)

박수민 [**soomin98**](https://github.com/soomin98)

배경륜 [**bicycle92**](https://github.com/bicycle92)



#### 노션 : [3조 2차 프로젝트(3월25일~4월27일) (notion.so)](https://www.notion.so/3-2-3-25-4-27-4da63a880d24465ab0edf36432a2017a)

#### GitHub : https://github.com/cano721/UbiMobile


