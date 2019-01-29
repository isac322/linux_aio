[\[english\]](https://github.com/isac322/linux_aio/blob/master/README.md) | **\[한국어 (korean)\]**

# linux_aio: Python wrapper for [Linux Kernel AIO](http://lse.sourceforge.net/io/aio.html)

[![](https://img.shields.io/travis/com/isac322/linux_aio.svg?style=flat-square)](https://travis-ci.com/isac322/linux_aio)
[![](https://img.shields.io/pypi/v/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/codecov/c/github/isac322/linux_aio.svg?style=flat-square)](https://codecov.io/gh/isac322/linux_aio)
[![](https://img.shields.io/pypi/implementation/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/pyversions/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/wheel/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/l/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg?style=flat-square)](https://saythanks.io/to/isac322)

[Linux Kernel AIO](http://lse.sourceforge.net/io/aio.html)를 직접 사용하는 Python High-level wrapper 모듈.

See [linux_aio_bind](https://pypi.org/project/linux-aio-bind) if you want to handle the API directly at low-level.

## Linux Kernel AIO이란?

[Linux IO Model 정리 표](https://oxnz.github.io/2016/10/13/linux-aio/#io-models)

간단하게 줄이면 [read(2)](http://man7.org/linux/man-pages/man2/read.2.html)나 [write(2)](http://man7.org/linux/man-pages/man2/write.2.html)와 같은 Blocking IO operation들을 Non-blocking하며 비동기적으로 사용하게 해준다.


### 관련 문서

- [Linux Asynchronous I/O](https://oxnz.github.io/2016/10/13/linux-aio/)
- [Linux Kernel AIO Design Notes](http://lse.sourceforge.net/io/aionotes.txt)
- [How to use the Linux AIO feature](https://github.com/littledan/linux-aio) (in C)


### **[POSIX AIO](http://man7.org/linux/man-pages/man7/aio.7.html)와는 다르다**

POSIX AIO의 API들은 `aio_` 접두사를 가지지만, Linux Kernel AIO는 `io_` 접두사를 가진다.


비동기 입출력을 위한 [POSIX AIO API](http://man7.org/linux/man-pages/man7/aio.7.html)가 이미 존재 하지만, Linux는 user-space인 [glibc](https://www.gnu.org/software/libc/manual/html_node/Asynchronous-I_002fO.html)에서 내부적으로는 multi-threading을 사용하도록 구현하였다.
따라서, 밑에서 실험을 통해 보이겠지만 blocking IO API를 사용하는것 보다 많이 안좋은 성능을 보인다.


## 구현 및 구조

### `linux_aio` 패키지

- Linux kernel AIO의 Low-level binding인 [linux_aio_bind](https://pypi.org/project/linux-aio-bind) 패키지를 기반으로 구현
- [linux_aio_bind](https://pypi.org/project/linux-aio-bind)와 달리 `ctypes`에대한 지식 없이도 사용 가능
- [test codes](https://github.com/isac322/linux_aio/tree/master/test)의 코드들에서 예제 확인 가능


## 예제

[test](https://github.com/isac322/linux_aio/tree/master/test)의 코드들에서 예제 확인 가능


## Notes & Limits

- 당연하게도 Linux에서만 사용 가능하다
- Wrapper이기 때문에 Linux의 제약을 그대로 가져온다
	- Kernel interface로 사용되는 파일에는 사용할 수 없다. (e.g. `cgroup`)
	- [때로 Blocking으로 동작하기도 함](https://stackoverflow.com/questions/34572559/asynchronous-io-io-submit-latency-in-ubuntu-linux)
		- 해당 글 포스팅 이후 개발로 완화된 것들이 있기도 하다
	- 아직 개발중인 API이기 때문에, 기능이 추가되기도 한다
	- 또한 Linux 버전이 낮은 경우 일부 지원하지 않는 기능이 있기도 하다
		- [Linux man pages (4.16)](http://man7.org/linux/man-pages/man2/io_submit.2.html)와 그 관련 API 문서 확인 필요


## 성능 비교

[Experiment script](https://gist.github.com/isac322/8606f5c464fa390cb88b47354981cdab) (requires python 3.7)

### 실험 환경

- Distribution: Ubuntu Server 16.04.5 LTS
- Linux: 4.19.0
- CPU: 2-way Intel(R) Xeon(R) CPU E5-2683 v4 @ 2.10GHz
- MEM: total 64GB
- Storage: SK hynix SC300B SATA 512GB
- Python: 3.7.2 ([Ubuntu ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa))


- `1ms` 간격으로 총 `1000`번 읽기를 시도한다
- 파일 크기는 `1KB` ~ `100KB`로 다양하지만 작다
- 동시에 읽는 파일의 개수를 늘려가면서 실험한다
- 고성능 서버에서 실험하였기 때문에, 일반 데스크탑에서 실험할 경우 더 큰 성능차이가 있을 수 있다


### 비교 대상

- [aiofiles](https://pypi.org/project/aiofiles/) - Thread pool 사용
- [aiofile](https://pypi.org/project/aiofile/) - POSIX AIO 사용
- [libaio](https://pypi.org/project/libaio/) - [libaio](http://lse.sourceforge.net/io/aio.html) 사용
- [python built-in open()](https://docs.python.org/3/library/functions.html#open)


**완벽하게 fair한 비교는 아니다.**

`aiofiles`와 `aiofile`은 [asyncio](https://docs.python.org/ko/3/library/asyncio.html)를 지원하는 라이브러리이며, `open()`는 Blocking이기 때문에 IO를 진행하는 동안 다른 작업을 할 수 없다는 단점이 있고, `libaio`와 `linux_aio`는 Non-blocking이지만 polling을 해야한다.


### 결과

**환경마다 다를 수 있으므로 참고용으로만 사용**

#### 수행 시간

- 단위: 초

| 파일 개수 	|   1   	|   6   	|   12  	|   24  	|
|:---------:	|:-----:	|:-----:	|:-----:	|:-----:	|
|  aiofiles 	| 1.681 	| 3.318 	| 5.354 	| 9.768 	|
|  aiofile  	| 1.543 	| 1.958 	| 2.493 	| 3.737 	|
|   libaio  	| 1.311 	| 1.344 	| 1.362 	| 1.423 	|
|   open()  	| 1.252 	| 1.322 	| 1.375 	| 1.481 	|
| linux_aio 	| 1.305 	| 1.327 	| 1.353 	| 1.431 	|

#### 사용 스레드

| 파일 개수 	|  1  	|  6  	|  12 	|  24 	|
|:---------:	|:---:	|:---:	|:---:	|:---:	|
|  aiofiles 	| 321 	| 321 	| 321 	| 321 	|
|  aiofile  	|   3 	|   8 	|  15 	|  26 	|
|   libaio  	|   1 	|   1 	|   1 	|   1 	|
|   open()  	|   1 	|   1 	|   1 	|   1 	|
| linux_aio 	|   1 	|   1 	|   1 	|   1 	|

#### 사용 메모리

- 물리 메모리 (가상 메모리)

| 파일 개수 	|       1       	|       6       	|       12      	|       24      	|
|:---------:	|:-------------:	|:-------------:	|:-------------:	|:-------------:	|
|  aiofiles 	| 21MB (22.6GB) 	| 21MB (22.6GB) 	| 21MB (22.6GB) 	| 21MB (22.6GB) 	|
|  aiofile  	|  17MB (258MB) 	|  17MB (654MB) 	| 17MB (1080MB) 	| 18MB (1949MB) 	|
|   libaio  	|   17MB (76MB) 	|   17MB (76MB) 	|   17MB (76MB) 	|   17MB (76MB) 	|
|   open()  	|   17MB (76MB) 	|   17MB (76MB) 	|   17MB (76MB) 	|   17MB (76MB) 	|
| linux_aio 	|   17MB (76MB) 	|   17MB (76MB) 	|   17MB (76MB) 	|   17MB (76MB) 	|

#### CPU 점유율

| 파일 개수 	|   1   	|   6   	|   12   	|   24   	|
|:---------:	|:-----:	|:-----:	|:------:	|:------:	|
|  aiofiles 	| 42.8% 	| 85.0% 	| 102.2% 	| 113.2% 	|
|  aiofile  	| 31.4% 	| 52.4% 	|  67.0% 	|  84.0% 	|
|   libaio  	| 14.0% 	| 16.0% 	|  17.2% 	|  20.6% 	|
|   open()  	| 13.4% 	| 17.6% 	|  21.0% 	|  26.2% 	|
| linux_aio 	| 13.0% 	| 15.0% 	|  16.0% 	|  21.0% 	|