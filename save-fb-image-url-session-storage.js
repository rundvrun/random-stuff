// ==UserScript==
// @name         Save Image FB
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.facebook.com/photo/*
// @match        https://www.facebook.com/*/photos/*
// @match        https://www.facebook.com/photo.php*
// @match        https://www.facebook.com/photo*fbid*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=facebook.com
// @grant GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';
    
    // Your code here...
    setInterval(() => {
        try
        {
            let imagesSaved = JSON.parse(sessionStorage.getItem("imagesSaved") || '[]');
            let cnt = imagesSaved.length;
            //console.log(document.querySelector('[data-visualcompletion="media-vc-image"]').src);
            imagesSaved = imagesSaved.concat([...document.querySelectorAll('img[data-visualcompletion="media-vc-image"]')].map(t => t.src).filter(t => t.indexOf('stp=dst-') == -1 && t.indexOf('stp=cp6_dst-jpg_p') == -1));
            imagesSaved = [...new Set(imagesSaved)];
            sessionStorage.setItem("imagesSaved", JSON.stringify(imagesSaved));
            if (cnt < imagesSaved.length) {
                console.log("image count", imagesSaved.length);
                delay(document.querySelector('img[data-visualcompletion="media-vc-image"]').src);
            }
        }
        catch (e)
        {
            console.log(e);
        }
    }, 200);
})();
