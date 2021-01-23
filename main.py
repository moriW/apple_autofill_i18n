#! python3
# 
#
# @file: main
# @time: 2021/01/23
# @author: Mori
#

import os
import csv
import time
import logging
from selenium import webdriver

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
INPUT_AREA_XPATH = "//*[@id='whatsNew']"
LAN_OPTIONS_XPATH = "//*[@id='appstore']/div[1]/div[2]/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/ul[1]/li/button"
SELECT_LAN_BTN_XPATH = "//*[@id='appstore']/div[1]/div[2]/div/div[2]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/button"
SAVE_BTN_XPATH = "//*[@id='heading-buttons']/button[1]"
TRIGGER_JS = """
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["reactTriggerChange"] = factory();
	else
		root["reactTriggerChange"] = factory();
})(this, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;
/******/
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// Trigger React's synthetic change events on input, textarea and select elements
// https://github.com/facebook/react/pull/4051 - React 15 fix
// https://github.com/facebook/react/pull/5746 - React 16 fix



// Constants and functions are declared inside the closure.
// In this way, reactTriggerChange can be passed directly to executeScript in Selenium.
module.exports = function reactTriggerChange(node) {
  var supportedInputTypes = {
    color: true,
    date: true,
    datetime: true,
    'datetime-local': true,
    email: true,
    month: true,
    number: true,
    password: true,
    range: true,
    search: true,
    tel: true,
    text: true,
    time: true,
    url: true,
    week: true
  };
  var nodeName = node.nodeName.toLowerCase();
  var type = node.type;
  var event;
  var descriptor;
  var initialValue;
  var initialChecked;
  var initialCheckedRadio;

  // Do not try to delete non-configurable properties.
  // Value and checked properties on DOM elements are non-configurable in PhantomJS.
  function deletePropertySafe(elem, prop) {
    var desc = Object.getOwnPropertyDescriptor(elem, prop);
    if (desc && desc.configurable) {
      delete elem[prop];
    }
  }

  // In IE10 propertychange is not dispatched on range input if invalid
  // value is set.
  function changeRangeValue(range) {
    var initMin = range.min;
    var initMax = range.max;
    var initStep = range.step;
    var initVal = Number(range.value);

    range.min = initVal;
    range.max = initVal + 1;
    range.step = 1;
    range.value = initVal + 1;
    deletePropertySafe(range, 'value');
    range.min = initMin;
    range.max = initMax;
    range.step = initStep;
    range.value = initVal;
  }

  function getCheckedRadio(radio) {
    var name = radio.name;
    var radios;
    var i;
    if (name) {
      radios = document.querySelectorAll('input[type="radio"][name="' + name + '"]');
      for (i = 0; i < radios.length; i += 1) {
        if (radios[i].checked) {
          return radios[i] !== radio ? radios[i] : null;
        }
      }
    }
    return null;
  }

  function preventChecking(e) {
    e.preventDefault();
    if (!initialChecked) {
      e.target.checked = false;
    }
    if (initialCheckedRadio) {
      initialCheckedRadio.checked = true;
    }
  }

  if (nodeName === 'select' ||
    (nodeName === 'input' && type === 'file')) {
    // IE9-IE11, non-IE
    // Dispatch change.
    event = document.createEvent('HTMLEvents');
    event.initEvent('change', true, false);
    node.dispatchEvent(event);
  } else if ((nodeName === 'input' && supportedInputTypes[type]) ||
    nodeName === 'textarea') {
    // React 16
    // Cache artificial value property descriptor.
    // Property doesn't exist in React <16, descriptor is undefined.
    descriptor = Object.getOwnPropertyDescriptor(node, 'value');

    // React 0.14: IE9
    // React 15: IE9-IE11
    // React 16: IE9
    // Dispatch focus.
    event = document.createEvent('UIEvents');
    event.initEvent('focus', false, false);
    node.dispatchEvent(event);

    // React 0.14: IE9
    // React 15: IE9-IE11
    // React 16
    // In IE9-10 imperative change of node value triggers propertychange event.
    // Update inputValueTracking cached value.
    // Remove artificial value property.
    // Restore initial value to trigger event with it.
    if (type === 'range') {
      changeRangeValue(node);
    } else {
      initialValue = node.value;
      node.value = initialValue + '#';
      deletePropertySafe(node, 'value');
      node.value = initialValue;
    }

    // React 15: IE11
    // For unknown reason React 15 added listener for propertychange with addEventListener.
    // This doesn't work, propertychange events are deprecated in IE11,
    // but allows us to dispatch fake propertychange which is handled by IE11.
    event = document.createEvent('HTMLEvents');
    event.initEvent('propertychange', false, false);
    event.propertyName = 'value';
    node.dispatchEvent(event);

    // React 0.14: IE10-IE11, non-IE
    // React 15: non-IE
    // React 16: IE10-IE11, non-IE
    event = document.createEvent('HTMLEvents');
    event.initEvent('input', true, false);
    node.dispatchEvent(event);

    // React 16
    // Restore artificial value property descriptor.
    if (descriptor) {
      Object.defineProperty(node, 'value', descriptor);
    }
  } else if (nodeName === 'input' && type === 'checkbox') {
    // Invert inputValueTracking cached value.
    node.checked = !node.checked;

    // Dispatch click.
    // Click event inverts checked value.
    event = document.createEvent('MouseEvents');
    event.initEvent('click', true, true);
    node.dispatchEvent(event);
  } else if (nodeName === 'input' && type === 'radio') {
    // Cache initial checked value.
    initialChecked = node.checked;

    // Find and cache initially checked radio in the group.
    initialCheckedRadio = getCheckedRadio(node);

    // React 16
    // Cache property descriptor.
    // Invert inputValueTracking cached value.
    // Remove artificial checked property.
    // Restore initial value, otherwise preventDefault will eventually revert the value.
    descriptor = Object.getOwnPropertyDescriptor(node, 'checked');
    node.checked = !initialChecked;
    deletePropertySafe(node, 'checked');
    node.checked = initialChecked;

    // Prevent toggling during event capturing phase.
    // Set checked value to false if initialChecked is false,
    // otherwise next listeners will see true.
    // Restore initially checked radio in the group.
    node.addEventListener('click', preventChecking, true);

    // Dispatch click.
    // Click event inverts checked value.
    event = document.createEvent('MouseEvents');
    event.initEvent('click', true, true);
    node.dispatchEvent(event);

    // Remove listener to stop further change prevention.
    node.removeEventListener('click', preventChecking, true);

    // React 16
    // Restore artificial checked property descriptor.
    if (descriptor) {
      Object.defineProperty(node, 'checked', descriptor);
    }
  }
};


/***/ })
/******/ ]);
});
"""
SKIP_TIME = 0.5

def init_browser():
    logging.info("正在启动chrome")
    browser = webdriver.Chrome()

    logging.info("正在打开商店")
    browser.get("https://appstoreconnect.apple.com/")

    logging.info("正在加载react")
    browser.execute_script(TRIGGER_JS)

    logging.info("请手动登陆 并移动至多语言页面")
    return browser

def init_conf():
    global SKIP_TIME
    logging.info(f"当自动注入开始后，为了保障网络成功，会在所有操作后停顿{SKIP_TIME}")
    logging.info(f"如需修改 请输入一个数值(不改给老子回车就行, 么么么)")
    input_skip_time = input()
    try:
        SKIP_TIME = float(input_skip_time)
    except Exception as e:
        logging.error(f"设置失败, {e}")
    finally:
        logging.info(f"停顿时间为 [{SKIP_TIME}]")

def init_csv():
    logging.info("需要输入CSV文件")
    logging.info("可以直接将内容拖入此处，但请确保文件路径正确")
    file_path = input()
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        logging.error("csv文件路径错误")
        return

    logging.info("正在加载csv...")

    try:
        lan_dict = {}
        have_error = False
        with open(file_path, "r") as _csv_f:
            _csv_f.readline()
            reader = csv.reader(_csv_f)
            row = 2
            for _, lan, content, *_ in reader:
                if lan in lan_dict:
                    logging.error(f"多语言配置重复出现 [{lan}]")
                    have_error = True
                if lan == "" or content == "":
                    logging.error(f"多语言配置 语言或内容 缺失 第[{row}]行")
                    have_error = True

                lan_dict[lan] = content
            if have_error:
                logging.info("本次多语言配置出现问题，有可能会出现问题，请确认仍要操作(y/n)")
                if (input()).lower() != 'y':
                    return
            logging.info(f"csv 文件已经读取完毕，共计加载 [{len(lan_dict)}] 个有效多语言")
            return lan_dict
    except Exception as e:
        logging.error(f"csv处理错误，正在退出 - {str(e)}")
        return



def do_fill_all_lan(lan_dict, browser):
    global SKIP_TIME
    processed_lan = []

    while True:
        logging.info("准备开始注入多语言信息，请确保当前网络环境和当前页面已经加载完成(y/n)")
        if input().lower() == "y":
            break
        else:
            continue

    def _do_select_lan():
        select_btn = browser.find_element_by_xpath(SELECT_LAN_BTN_XPATH)
        select_btn.click()
        time.sleep(SKIP_TIME)

        for btn in browser.find_elements_by_xpath(LAN_OPTIONS_XPATH):
            btn_text = btn.text
            if "英文（美国）" in btn_text:
                btn_text = "英文（美国）"
            if btn_text != "" and btn_text not in processed_lan and btn_text in lan_dict:
                processed_lan.append(btn_text)
                return btn, lan_dict[btn_text]

    while True:
        btn_and_content = _do_select_lan()
        if btn_and_content is None:
            logging.info("处理完成 储存中")
            browser.find_element_by_xpath(SAVE_BTN_XPATH).click()
            time.sleep(SKIP_TIME)
            not_process_lan = [lan for lan in processed_lan if lan not in lan_dict]
            logging.info(f"处理完成 [{[', '.join(not_process_lan)]}]")
            input()
            return
        btn, content = btn_and_content
        btn.click()
        time.sleep(SKIP_TIME)
        input_area = browser.find_element_by_xpath(INPUT_AREA_XPATH)
        input_area.clear()
        time.sleep(SKIP_TIME)
        input_area.send_keys(content)
        time.sleep(SKIP_TIME)

def main():
    init_conf()
    browser = init_browser()
    lan_dict = init_csv()
    do_fill_all_lan(lan_dict, browser)

if __name__ == '__main__':
    main()