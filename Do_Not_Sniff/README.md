# - 문제 제목
Do Not Sniff!!
# - Description
제 서버에 공격이 들어왔어요..ㅠ
분명 공격자가 저의 소중한 flag를 유출시켰을 거에요..
flag를 찾아주세요!
# - Write-Up
```
- DNS 카빙 문제
- DNS TXT 레코드에 base64 인코딩된 데이터가 청크단위로 쪼개서 들어감
- 코드를 잘 짜서 복원하면 됨
```
# - Flag
`KCTF{(끄덕) 그것이 생존이니까..}`