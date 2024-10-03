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
    function delay() {
       GM_xmlhttpRequest({
            method: "GET",
            synchronous: false,
            url: "https://python.server/",
            onload: function(e) {
                //alert("loaded!");
                console.log(e);
            },
            onerror: function(err) {
                //alert("GM_xmlhttpRequest error");
                console.log(err);
            }
        });
        //window.clearInterval(timer);
    }
    var timer = window.setInterval(delay, 5000); //needs around 5 seconds to insure all elements loaded
    // Your code here...
})();
