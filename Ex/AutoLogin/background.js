chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "openPages") {
    // เปิดหน้า chrome://settings/resetProfileSettings
    // chrome.tabs.create({ url: "chrome://settings/resetProfileSettings?origin=userclick" }, async (tab1) => {
    //   await new Promise(resolve => setTimeout(resolve, 2000));
    //   await chrome.tabs.update(tab1.id, { active: true });
    //   chrome.tabs.executeScript(tab1.id,{
    //       code: "document.querySelector('body > settings-ui').shadowRoot.querySelector('#main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('#advancedPage > settings-section:nth-child(12) > settings-reset-page').shadowRoot.querySelector('#reset-pages > div > settings-reset-profile-dialog').shadowRoot.querySelector('#reset').click();"
    //   });
    //   await new Promise(resolve => setTimeout(resolve, 3000));
      
    //   // Proceed to extensions page
    //   chrome.runtime.sendMessage({ action: "openExtensionsPage" });
    // });

    chrome.tabs.create({ url: "chrome://settings/resetProfileSettings?origin=userclick" }, async (tab1) => {
      await new Promise(resolve => setTimeout(resolve, 3000));
      // chrome.scripting.executeScript({
      //     target: {tabId: tab1.id, allFrames: true},
      //     files: ['a.js'],
      // });
      // chrome.tabs.query({}, allTabs => {  // get all tabs
      //   const activeTabID = allTabs.filter(t => t.active)[0].id;  // find active tab
      //   chrome.tabs.executeScript(activeTabID, {  // specify the tabID
      //     file: "a.js",
      //   });
      // });
      chrome.runtime.sendMessage({ action: "openExtensionsPage" });
    });

    
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "openExtensionsPage") {
    chrome.tabs.create({ 
      url: "chrome://extensions/" 
    }, async (tab2) => {
      console.log("Extensions tab created:", tab2.id);
      await new Promise(resolve => setTimeout(resolve, 2000));
    });
    return true;
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) =>  {
  if (message.action === "clearCookies") {
    new Promise(resolve => setTimeout(resolve, 5000));
    chrome.browsingData.remove({
      "origins": ["https://www.roblox.com"]
    }, {
      "cookies": true
    }, () => {
      console.log("Cookies for roblox.com have been cleared.");
    });
  }
});

// ฟังก์ชันสำหรับกรอกข้อมูลในฟิลด์ input
function setInputValue(selector, value) {
  const input = document.querySelector(selector);
  if (input) {
      input.value = value;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "login") {
    setInputValue("#login-username", "xSawada938");
    new Promise(resolve => setTimeout(resolve, 3000));
    setInputValue("#login-password", "MugenyPD");
    new Promise(resolve => setTimeout(resolve, 2000));
    document.querySelector("#login-button").click();
  }
});