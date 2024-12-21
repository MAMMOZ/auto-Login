// ตรวจสอบ URL และส่ง API ตามเงื่อนไข
if (window.location.href === "https://www.roblox.com/th/login/securityNotification" || window.location.href === "https://www.roblox.com/login/securityNotification?nl=true") {
    // fetch("https://example.com/api", { // เปลี่ยน URL API ให้ตรงกับของคุณ
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ status: "user error" })
    // });
  
    // เปิดหน้าที่ระบุ
    chrome.runtime.sendMessage({ action: "openPages" });
} else if (window.location.href === "https://www.roblox.com/home") {
  // fetch("https://example.com/api", { // เปลี่ยน URL API ให้ตรงกับของคุณ
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ status: "login success" })
  // });
  chrome.runtime.sendMessage({ action: "clearCookies", domain: ".roblox.com" });
} else if (window.location.href === "https://www.roblox.com/Login") {
  // fetch("https://example.com/api", { // เปลี่ยน URL API ให้ตรงกับของคุณ
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ status: "login success" })
  // });
  function setInputValue(selector, value) {
    const input = document.querySelector(selector);
    if (input) {
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }
  setInputValue("#login-username", "xSawada938");
  new Promise(resolve => setTimeout(resolve, 3000));
  setInputValue("#login-password", "MugenyPD");
  new Promise(resolve => setTimeout(resolve, 2000));
  document.querySelector("#login-button").click();

  // รีโหลดหน้า
  setTimeout(() => location.reload(), 5000); // รีโหลดหลังจาก 5 วินาที
}