// 🧪 使用方式：
// 打开 Pionex 并登录页面：https://www.pionex.com/zh-CN/structured-finance/history
// 在浏览器按 F12 → Console 粘贴代码回车
window.baseUrl = "https://www.pionex.com/financial/api/fmapis/v1/structured/invest/paids/";

(function() {
  window.originalOpen = window.originalOpen||XMLHttpRequest.prototype.open;
  window.originalSend = window.originalSend||XMLHttpRequest.prototype.send;
  window.originalSetRequestHeader = window.originalSetRequestHeader||XMLHttpRequest.prototype.setRequestHeader;

  const requestHeaders = new WeakMap();

  XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
    this._url = url;
    return window.originalOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
    if (!requestHeaders.has(this)) {
      requestHeaders.set(this, {});
    }
    const headers = requestHeaders.get(this);
    headers[header] = value;
    return window.originalSetRequestHeader.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function(body) {
    const url = this._url || '';
    const headers = requestHeaders.get(this) || {};
    const auth = headers["Authorization"];

    if (url.includes("/dual/index/") && auth) {
      // console.log("🔍 Intercepted /dual/index Authorization:");
      // console.log("🔐 Authorization:", auth);
      // console.log("🌍 URL:", url);
      // 可选：复制到剪贴板
      // navigator.clipboard.writeText(auth);
      window.Authorization = auth
      window.baseUrl = url.replace("/dual/index/", "/structured/invest/paids/").replace(/&base_quote=.*/ig, "")
    }

    return window.originalSend.apply(this, arguments);
  };
})();
setTimeout(async () => {
    const baseUrl = window.baseUrl;

    let page_token = "";
    const per_page = 20;
    let allRecords = [];
    let page = 1;

    while (true) {
        const res = await fetch(baseUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": window.Authorization
            },
            body: JSON.stringify({
                page_token,
                per_page,
            })
        });

        const data = await res.json();
        const records = data?.data?.records || [];
        const nextToken = data?.data?.next_token;

        if (records.length === 0) break;
        allRecords.push(...records.filter(r => r?.data?.auto_static?.static_time >= from_date));
        console.log(`📄 已抓取第 ${page} 页，共 ${records.length} 条`);
        page++;

        if (records[records.length-1].data.auto_static.static_time < from_date) break;
        if (!nextToken || page >= 1000) break;
        page_token = nextToken;
    }

    // 合计金额
    let total = allRecords.reduce((sum, r) => sum + parseFloat(r.data.origin_invest_amount || 0), 0);
    let income = allRecords.reduce((sum, r) => sum + parseFloat(r.data.auto_static.income || 0), 0);
    let aincome = allRecords.reduce((sum, r) => sum + parseFloat(r.data.latest_hour_balance.total_balance || 0) - parseFloat(r.data.latest_hour_balance.invest_amount || 0), 0);
    // let fincome = allRecords.reduce((sum, r) => new Date(r.data?.auto_static?.static_time) > from_date ? sum + parseFloat(r.data.auto_static.income || 0) : sum, 0);

    // 输出明细表
    console.table(allRecords.map(r => ({
        币种: r.data.base,
        开单金额: r.data.origin_invest_amount,
        预计结算: (r.data.latest_hour_balance.total_balance - r.data.latest_hour_balance.invest_amount).toFixed(2),
        实际结算: r.data.auto_static.income,
        创建时间: new Date(r.data.create_time).toLocaleString(),
        结算时间: new Date(r.data.auto_static.static_time).toLocaleString(),
    })));
    
    console.log(`\n✅ 共 ${days} 天 ${allRecords.length} 条记录`);
    console.log(`💰 累计开单金额：${total.toFixed(2)} USDT`);
    console.log(`💰 预计结算金额：${aincome.toFixed(2)} USDT`);
    console.log(`💰 实际结算金额：${income.toFixed(2)} USDT`);
}, 5000);

let days = 30;
let from_date = new Date().setHours(0,0,0,0) - days * 86400000;
