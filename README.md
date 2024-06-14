以MDN Web DocS中，用Django來建一個簡單圖書館的[教學](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django "Link")為基礎，建立一個簡易的訂便當網頁。
<br>
<br>
### 首頁
首頁帶有Database內Model的數量計算(便當種類、訂單數)、由Session記錄訪問次數、側邊欄導向不同頁面的連結
<!--  ![index](/images/index.png "index") -->
<img src="/images/index.png" width="600" height="auto"> <br>
### 點擊"便當種類"
由ListView取得便當種類，並條列出來<br>
<img src="/images/lunchbox_list.png" width="600" height="auto">
<br>
### 點擊""便當名稱
由DetailView取得單個便當Model內的各項Field內容(品項名稱、簡介、價格)並列出，此外使用statics file的方式能夠附上便當圖片(此用卡通圖示取代)供人參考<br>
![Detail](/images/lunchbox_detail.png "detail")
<br>
### 點擊"訂購表單"
透過Form取得使用者訂購資訊(名字、電話、數量)，若數量有負數或兩者皆為0會警告訂購者相應的錯誤，view取得使用者POST的表單資訊後，會透過數量計算金額<br>
<img src="/images/order_form.png" width="600" height="auto">
<br>
### 點擊"查詢歷史表單"
透過Form讓使用者輸入電話號碼，可以取得此電話過去訂購的內容(名字、電話、數量、金額、日期)，若訂購次數超過1次，所有訂購歷史都會呈現出來<br>
<img src="/images/check_orderhistory.png" width="600" height="auto">
<br>
### 點擊"Login"(Staff 登入)
運用Django內建的accounts view搭建login/logout，可以作為店員或顧客的區分(就算顧客也有帳號，也能由admin給予不同權限)<br>
<img src="/images/staff_login.png" width="600" height="auto">
<br>
### 點擊"Orderlist"(Staff 權限)
擁有staff權限的人，能夠由ListView取得所有訂單的資訊，另外有加入paginate，當object數量多時能夠換頁。<br>
<img src="/images/staffview_orderlist.png" width="600" height="auto">
<br>
