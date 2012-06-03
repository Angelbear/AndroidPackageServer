reset:
	mv repo/com.tencent.qq/ new/
	mv repo/smpxg.crystallight new/

copy: 
	mv new/* repo/

update:
	echo 2 > repo/aiCharts.webChart/version

downgrade:
	echo 1 > repo/aiCharts.webChart/version


