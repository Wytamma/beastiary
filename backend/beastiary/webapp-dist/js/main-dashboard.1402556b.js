(window.webpackJsonp=window.webpackJsonp||[]).push([["main-dashboard"],{f021:function(t,e,r){"use strict";r.r(e);var o=r("9ab4"),n=r("60a3"),i=r("2963");function _typeof(t){return(_typeof="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function _typeof(t){return typeof t}:function _typeof(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function _classCallCheck(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function _defineProperties(t,e){for(var r=0;r<e.length;r++){var o=e[r];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,o.key,o)}}function _setPrototypeOf(t,e){return(_setPrototypeOf=Object.setPrototypeOf||function _setPrototypeOf(t,e){return t.__proto__=e,t})(t,e)}function _createSuper(t){var e=function _isNativeReflectConstruct(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function _createSuperInternal(){var r,o=_getPrototypeOf(t);if(e){var n=_getPrototypeOf(this).constructor;r=Reflect.construct(o,arguments,n)}else r=o.apply(this,arguments);return _possibleConstructorReturn(this,r)}}function _possibleConstructorReturn(t,e){return!e||"object"!==_typeof(e)&&"function"!=typeof e?function _assertThisInitialized(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t):e}function _getPrototypeOf(t){return(_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function _getPrototypeOf(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}var a=function(t){!function _inherits(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&_setPrototypeOf(t,e)}(Dashboard,t);var e=_createSuper(Dashboard);function Dashboard(){return _classCallCheck(this,Dashboard),e.apply(this,arguments)}return function _createClass(t,e,r){return e&&_defineProperties(t.prototype,e),r&&_defineProperties(t,r),t}(Dashboard,[{key:"greetedUser",get:function get(){var t=Object(i.h)(this.$store);if(t)return t.full_name?t.full_name:t.email}}]),Dashboard}(n.b),s=a=Object(o.a)([n.a],a),c=r("2877"),f=Object(c.a)(s,(function(){var t=this.$createElement,e=this._self._c||t;return e("v-container",{attrs:{fluid:""}},[e("v-card",{staticClass:"ma-3 pa-3"},[e("v-card-title",{attrs:{"primary-title":""}},[e("div",{staticClass:"headline primary--text"},[this._v("Dashboard")])]),e("v-card-text",[e("div",{staticClass:"headline font-weight-light ma-5"},[this._v("Welcome "+this._s(this.greetedUser))])]),e("v-card-actions",[e("v-btn",{attrs:{to:"/main/profile/view"}},[this._v("View Profile")]),e("v-btn",{attrs:{to:"/main/profile/edit"}},[this._v("Edit Profile")]),e("v-btn",{attrs:{to:"/main/profile/password"}},[this._v("Change Password")])],1)],1)],1)}),[],!1,null,null,null);e.default=f.exports}}]);
//# sourceMappingURL=main-dashboard.1402556b.js.map