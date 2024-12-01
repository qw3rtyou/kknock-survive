FROM node:18 as builder

WORKDIR /usr/src/app

# 소스 코드 복사 및 종속성 설치
COPY ./src .
RUN npm install

# 루트 디렉토리로 이동하여 flag 파일 처리
WORKDIR /

# flag 파일 복사 및 nonce 생성 후 이름 변경
COPY flag flag
RUN nonce=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 16) && \
    mv flag "flag_${nonce}" && \
    echo "${nonce}" > nonce.txt

# 두 번째 단계: 최종 이미지 생성
FROM node:18

WORKDIR /usr/src/app

# 앱 파일 복사
COPY --from=builder /usr/src/app . 

# flag 파일과 nonce.txt 복사
COPY --from=builder /flag_* /flag_*
COPY --from=builder /nonce.txt /nonce.txt

RUN ls -l /flag_*

# 포트 노출 및 앱 실행
EXPOSE 8888
CMD ["node", "index.js"]


