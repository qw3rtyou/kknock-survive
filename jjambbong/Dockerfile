# Node.js 베이스 이미지
FROM node:18

# 작업 디렉토리 생성
WORKDIR /usr/src/app

# package.json과 package-lock.json 복사
COPY package*.json ./

# 의존성 설치
RUN npm install

# 애플리케이션 파일 복사
COPY . .

# 컨테이너가 노출할 포트 설정
EXPOSE 8888

# 애플리케이션 실행
CMD ["node", "index.js"]
