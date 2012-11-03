
// ==UserScript==
// @name        MonkeyTeam error response decode script for {{ site_name }}
// @include     http*
// @grant       none
// ==/UserScript==

var CLIENT_KEY = "{{ client_key }}";
var DECODE_KEY = "{{ decode_key }}";

if (document.documentElement.outerHTML.indexOf(CLIENT_KEY) > 0) {
    {{ lib_code }}

    var pre = document.body.getElementsByTagName('pre')[0];
    var data = CryptoJS.enc.Base64.parse(pre.textContent);
    var output = CryptoJS.AES.decrypt(
        CryptoJS.enc.Base64.stringify(CryptoJS.lib.WordArray.create(data.words.slice(4))),
        CryptoJS.enc.Hex.parse(DECODE_KEY),
        {iv: CryptoJS.lib.WordArray.create(data.words.slice(0, 4))}
    ).toString(CryptoJS.enc.Latin1)
    var anchor;
    document.body.appendChild(anchor=document.createElement("a"))
    anchor.setAttribute("href", "#")
    anchor.appendChild(pre)
    anchor.addEventListener("click", function(event){
        event.preventDefault();
        event.stopPropagation();
        console.log(output);
        document.write(output);
    });
    data = pre = anchor = null;
}