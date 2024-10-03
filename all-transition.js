// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      2024-05-21
// @description  try to take over the world!
// @author       You
// @match        *://*/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=stackoverflow.com
// @grant GM_xmlhttpRequest
// @connect 127.0.0.1
// ==/UserScript==

(function() {
    'use strict';
    // Your code here...
    document.head.insertAdjacentHTML('beforeend', '<meta name="view-transition" content="same-origin">');
})();
