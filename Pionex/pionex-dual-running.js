// 🧪 使用方式：
// 打开 Pionex 并登录页面：https://www.pionex.com/zh-CN/structured-finance/running
// 在浏览器按 F12 → Console 粘贴代码回车
window.baseUrl = "https://www.pionex.com/financial/api/fmapis/v1/structured/invest/records/";

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
      window.baseUrl = url.replace("/dual/index/", "/structured/invest/records/").replace(/&base_quote=.*/ig, "")
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
                type: "",   // 所有产品
                status: 1   // 1=运行中，2=已结束
            })
        });

        const data = await res.json();
        const records = data?.data?.records || [];
        const nextToken = data?.data?.next_token;

        if (records.length === 0) break;

        allRecords.push(...records);
        console.log(`📄 已抓取第 ${page} 页，共 ${records.length} 条`);
        page++;

        if (!nextToken) break;
        page_token = nextToken;
    }

    // 合计金额
    let total = allRecords.reduce((sum, r) => sum + parseFloat(r.data.origin_invest_amount || 0), 0);
    let income = allRecords.reduce((sum, r) => sum + parseFloat(r.data.auto_static.income || 0), 0);
    let uincome = allRecords.reduce((sum, r) => sum + parseFloat(r.data.auto_static.unsettle_income || 0), 0);
    let cincome = allRecords.reduce((sum, r) => sum + parseFloat(r.data.latest_hour_balance.cycle_income || 0), 0);
    
    let tomorrow = new Date().getTime() + 86400000;
    let tincome = allRecords.reduce((sum, r) => new Date(r.data?.auto_static?.static_time) < tomorrow ? sum + parseFloat(r.data.auto_static.unsettle_income || 0) : sum, 0);

    // 输出明细表
    console.table(allRecords.map(r => ({
        币种: r.data.base,
        开单金额: r.data.origin_invest_amount,
        下次预计收入: r.data.auto_static.unsettle_income,
        预计结算收入: r.data.auto_static.income,
        上次预计收入: r.data.latest_hour_balance.cycle_income,
        创建时间: new Date(r.data.create_time).toLocaleString(),
        下次结算时间: new Date(r.data.auto_static.static_time).toLocaleString(),
    })));
    
    console.log(`\n✅ 共 ${allRecords.length} 条记录`);
    console.log(`💰 合计投入金额（运行中）：${total.toFixed(2)} USDT`);
    console.log(`💰 预计16点结算（运行中）：${tincome.toFixed(2)} USDT`);
    console.log(`💰 预计下次结算（运行中）：${uincome.toFixed(2)} USDT`);
    console.log(`💰 上次预计结算（运行中）：${cincome.toFixed(2)} USDT`);
    console.log(`💰 全部预计结算（运行中）：${income.toFixed(2)} USDT`);
}, 5000);
