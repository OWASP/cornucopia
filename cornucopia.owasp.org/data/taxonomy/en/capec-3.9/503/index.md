# CAPEC™ 503: WebView Exposure

## Description

An adversary, through a malicious web page, accesses application specific functionality by leveraging interfaces registered through WebView's addJavascriptInterface API. Once an interface is registered to WebView through addJavascriptInterface, it becomes global and all pages loaded in the WebView can call this interface.

Source: [CAPEC™ 503](https://capec.mitre.org/data/definitions/503.html)

