# - 문제 제목
The Lord of LFI
# - Description
[The Lord of SQLI](https://los.rubiya.kr/)를 이을 The Lord of LFI?!?!?!?!?
# - Write-Up
```
1. stage1 -> 그냥 필터링 제외 아무 확장자로 PHP 파일 업로드 후 LFI
2. stage2 -> PHP filter gadget chain 이용해 LFI
3. stage3 -> data wrapper는 file_exists 같은 stat 계열 함수를 지원하지 않는다는 점을 이용해 LFI
```
# - Flag
`KCTF{LF1_w1th_th3_PHP_F1lt3r_Ch41n_1s_pr3tty_1nt3r3st1ng}`