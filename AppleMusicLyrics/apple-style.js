/**
 * Apple Style Synced Lyrics Component (apple-style.js)
 * High-performance animated syllable & line synchronization.
 */
function __decorate(t,e,i,s){var r,n=arguments.length,a=n<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(t,e,i,s);else for(var o=t.length-1;o>=0;o--)(r=t[o])&&(a=(n<3?r(a):n>3?r(e,i,a):r(e,i))||a);return n>3&&a&&Object.defineProperty(e,i,a),a}"function"==typeof SuppressedError&&SuppressedError;
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t$1=globalThis,e$4=t$1.ShadowRoot&&(void 0===t$1.ShadyCSS||t$1.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s$2=Symbol(),o$4=new WeakMap;let n$3=class{constructor(t,e,i){if(this._$cssResult$=!0,i!==s$2)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(e$4&&void 0===t){const i=void 0!==e&&1===e.length;i&&(t=o$4.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&o$4.set(e,t))}return t}toString(){return this.cssText}};const r$4=t=>new n$3("string"==typeof t?t:t+"",void 0,s$2),i$3=(t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new n$3(i,t,s$2)},S$1=(t,e)=>{if(e$4)t.adoptedStyleSheets=e.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const i of e){const e=document.createElement("style"),s=t$1.litNonce;void 0!==s&&e.setAttribute("nonce",s),e.textContent=i.cssText,t.appendChild(e)}},c$2=e$4?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return r$4(e)})(t):t,{is:i$2,defineProperty:e$3,getOwnPropertyDescriptor:h$1,getOwnPropertyNames:r$3,getOwnPropertySymbols:o$3,getPrototypeOf:n$2}=Object,a$1=globalThis,c$1=a$1.trustedTypes,l$1=c$1?c$1.emptyScript:"",p$1=a$1.reactiveElementPolyfillSupport,d$1=(t,e)=>t,u$1={toAttribute(t,e){switch(e){case Boolean:t=t?l$1:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},f$1=(t,e)=>!i$2(t,e),b$1={attribute:!0,type:String,converter:u$1,reflect:!1,useDefault:!1,hasChanged:f$1};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */Symbol.metadata??=Symbol("metadata"),a$1.litPropertyMetadata??=new WeakMap;let y$1=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=b$1){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&e$3(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:r}=h$1(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const n=s?.call(this);r?.call(this,e),this.requestUpdate(t,n,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??b$1}static _$Ei(){if(this.hasOwnProperty(d$1("elementProperties")))return;const t=n$2(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(d$1("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(d$1("properties"))){const t=this.properties,e=[...r$3(t),...o$3(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(c$2(t))}else void 0!==t&&e.push(c$2(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return S$1(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const r=(void 0!==i.converter?.toAttribute?i.converter:u$1).toAttribute(e,i.type);this._$Em=t,null==r?this.removeAttribute(s):this.setAttribute(s,r),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),r="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:u$1;this._$Em=s;const n=r.fromAttribute(e,t.type);this[s]=n??this._$Ej?.get(s)??n,this._$Em=null}}requestUpdate(t,e,i,s=!1,r){if(void 0!==t){const n=this.constructor;if(!1===s&&(r=this[t]),i??=n.getPropertyOptions(t),!((i.hasChanged??f$1)(r,e)||i.useDefault&&i.reflect&&r===this._$Ej?.get(t)&&!this.hasAttribute(n._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:r},n){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,n??e??this[t]),!0!==r||void 0!==n)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};y$1.elementStyles=[],y$1.shadowRootOptions={mode:"open"},y$1[d$1("elementProperties")]=new Map,y$1[d$1("finalized")]=new Map,p$1?.({ReactiveElement:y$1}),(a$1.reactiveElementVersions??=[]).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t=globalThis,i$1=t=>t,s$1=t.trustedTypes,e$2=s$1?s$1.createPolicy("lit-html",{createHTML:t=>t}):void 0,h="$lit$",o$2=`lit$${Math.random().toFixed(9).slice(2)}$`,n$1="?"+o$2,r$2=`<${n$1}>`,l=document,c=()=>l.createComment(""),a=t=>null===t||"object"!=typeof t&&"function"!=typeof t,u=Array.isArray,d=t=>u(t)||"function"==typeof t?.[Symbol.iterator],f="[ \t\n\f\r]",v=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,_=/-->/g,m=/>/g,p=RegExp(`>|${f}(?:([^\\s"'>=/]+)(${f}*=${f}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),g=/'/g,$=/"/g,y=/^(?:script|style|textarea|title)$/i,x=t=>(e,...i)=>({_$litType$:t,strings:e,values:i}),b=x(1),w=x(2),E=Symbol.for("lit-noChange"),A=Symbol.for("lit-nothing"),C=new WeakMap,P=l.createTreeWalker(l,129);function V(t,e){if(!u(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==e$2?e$2.createHTML(e):e}const N=(t,e)=>{const i=t.length-1,s=[];let r,n=2===e?"<svg>":3===e?"<math>":"",a=v;for(let e=0;e<i;e++){const i=t[e];let o,l,c=-1,d=0;for(;d<i.length&&(a.lastIndex=d,l=a.exec(i),null!==l);)d=a.lastIndex,a===v?"!--"===l[1]?a=_:void 0!==l[1]?a=m:void 0!==l[2]?(y.test(l[2])&&(r=RegExp("</"+l[2],"g")),a=p):void 0!==l[3]&&(a=p):a===p?">"===l[0]?(a=r??v,c=-1):void 0===l[1]?c=-2:(c=a.lastIndex-l[2].length,o=l[1],a=void 0===l[3]?p:'"'===l[3]?$:g):a===$||a===g?a=p:a===_||a===m?a=v:(a=p,r=void 0);const u=a===p&&t[e+1].startsWith("/>")?" ":"";n+=a===v?i+r$2:c>=0?(s.push(o),i.slice(0,c)+h+i.slice(c)+o$2+u):i+o$2+(-2===c?e:u)}return[V(t,n+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]};class S{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let r=0,n=0;const a=t.length-1,o=this.parts,[l,d]=N(t,e);if(this.el=S.createElement(l,i),P.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=P.nextNode())&&o.length<a;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(h)){const e=d[n++],i=s.getAttribute(t).split(o$2),a=/([.?@])?(.*)/.exec(e);o.push({type:1,index:r,name:a[2],strings:i,ctor:"."===a[1]?I:"?"===a[1]?L:"@"===a[1]?z:H}),s.removeAttribute(t)}else t.startsWith(o$2)&&(o.push({type:6,index:r}),s.removeAttribute(t));if(y.test(s.tagName)){const t=s.textContent.split(o$2),e=t.length-1;if(e>0){s.textContent=s$1?s$1.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],c()),P.nextNode(),o.push({type:2,index:++r});s.append(t[e],c())}}}else if(8===s.nodeType)if(s.data===n$1)o.push({type:2,index:r});else{let t=-1;for(;-1!==(t=s.data.indexOf(o$2,t+1));)o.push({type:7,index:r}),t+=o$2.length-1}r++}}static createElement(t,e){const i=l.createElement("template");return i.innerHTML=t,i}}function M(t,e,i=t,s){if(e===E)return e;let r=void 0!==s?i._$Co?.[s]:i._$Cl;const n=a(e)?void 0:e._$litDirective$;return r?.constructor!==n&&(r?._$AO?.(!1),void 0===n?r=void 0:(r=new n(t),r._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=r:i._$Cl=r),void 0!==r&&(e=M(t,r._$AS(t,e.values),r,s)),e}class R{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??l).importNode(e,!0);P.currentNode=s;let r=P.nextNode(),n=0,a=0,o=i[0];for(;void 0!==o;){if(n===o.index){let e;2===o.type?e=new k(r,r.nextSibling,this,t):1===o.type?e=new o.ctor(r,o.name,o.strings,this,t):6===o.type&&(e=new Z(r,this,t)),this._$AV.push(e),o=i[++a]}n!==o?.index&&(r=P.nextNode(),n++)}return P.currentNode=l,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class k{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=A,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=M(this,t,e),a(t)?t===A||null==t||""===t?(this._$AH!==A&&this._$AR(),this._$AH=A):t!==this._$AH&&t!==E&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):d(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==A&&a(this._$AH)?this._$AA.nextSibling.data=t:this.T(l.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=S.createElement(V(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new R(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=C.get(t.strings);return void 0===e&&C.set(t.strings,e=new S(t)),e}k(t){u(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const r of t)s===e.length?e.push(i=new k(this.O(c()),this.O(c()),this,this.options)):i=e[s],i._$AI(r),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=i$1(t).nextSibling;i$1(t).remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class H{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,r){this.type=1,this._$AH=A,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=r,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=A}_$AI(t,e=this,i,s){const r=this.strings;let n=!1;if(void 0===r)t=M(this,t,e,0),n=!a(t)||t!==this._$AH&&t!==E,n&&(this._$AH=t);else{const s=t;let o,l;for(t=r[0],o=0;o<r.length-1;o++)l=M(this,s[i+o],e,o),l===E&&(l=this._$AH[o]),n||=!a(l)||l!==this._$AH[o],l===A?t=A:t!==A&&(t+=(l??"")+r[o+1]),this._$AH[o]=l}n&&!s&&this.j(t)}j(t){t===A?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class I extends H{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===A?void 0:t}}class L extends H{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==A)}}class z extends H{constructor(t,e,i,s,r){super(t,e,i,s,r),this.type=5}_$AI(t,e=this){if((t=M(this,t,e,0)??A)===E)return;const i=this._$AH,s=t===A&&i!==A||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,r=t!==A&&(i===A||s);s&&this.element.removeEventListener(this.name,this,i),r&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class Z{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){M(this,t)}}const B=t.litHtmlPolyfillSupport;B?.(S,k),(t.litHtmlVersions??=[]).push("3.3.2");const D=(t,e,i)=>{const s=i?.renderBefore??e;let r=s._$litPart$;if(void 0===r){const t=i?.renderBefore??null;s._$litPart$=r=new k(e.insertBefore(c(),t),t,void 0,i??{})}return r._$AI(t),r
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */},s=globalThis;class i extends y$1{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=D(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return E}}i._$litElement$=!0,i.finalized=!0,s.litElementHydrateSupport?.({LitElement:i});const o$1=s.litElementPolyfillSupport;o$1?.({LitElement:i}),(s.litElementVersions??=[]).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const o={attribute:!0,type:String,converter:u$1,reflect:!1,hasChanged:f$1},r$1=(t=o,e,i)=>{const{kind:s,metadata:r}=i;let n=globalThis.litPropertyMetadata.get(r);if(void 0===n&&globalThis.litPropertyMetadata.set(r,n=new Map),"setter"===s&&((t=Object.create(t)).wrapped=!0),n.set(i.name,t),"accessor"===s){const{name:s}=i;return{set(i){const r=e.get.call(this);e.set.call(this,i),this.requestUpdate(s,r,t,!0,i)},init(e){return void 0!==e&&this.C(s,void 0,t,e),e}}}if("setter"===s){const{name:s}=i;return function(i){const r=this[s];e.call(this,i),this.requestUpdate(s,r,t,!0,i)}}throw Error("Unsupported decorator location: "+s)};function n(t){return(e,i)=>"object"==typeof i?r$1(t,e,i):((t,e,i)=>{const s=e.hasOwnProperty(i);return e.constructor.createProperty(i,t),s?Object.getOwnPropertyDescriptor(e,i):void 0})(t,e,i)}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function r(t){return n({...t,state:!0,attribute:!1})}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const e$1=(t,e,i)=>(i.configurable=!0,i.enumerable=!0,Reflect.decorate&&"object"!=typeof e&&Object.defineProperty(t,e,i),i);
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function e(t,e){return(e,i,s)=>e$1(e,i,{get(){return(e=>e.renderRoot?.querySelector(t)??null)(this)}})}const CONFIG={GOOGLE:{MAX_RETRIES:3,RETRY_DELAY_MS:1e3,FETCH_TIMEOUT_MS:6e3}};class GoogleService{static delay(t){return new Promise(e=>{setTimeout(e,t)})}static fetchWithTimeout(t,e=CONFIG.GOOGLE.FETCH_TIMEOUT_MS){const i=new AbortController,s=setTimeout(()=>i.abort(),e);return fetch(t,{signal:i.signal}).finally(()=>clearTimeout(s))}static isPurelyLatinScript(t){return/^[\u0000-\u007F\u0080-\u00FF\u0100-\u017F\u0180-\u024F]*$/.test(t)}static async translate(t,e){if(!t||Array.isArray(t)&&0===t.length)return Array.isArray(t)?[]:"";const i=Array.isArray(t),s=i?t:[t],r=[],n=[];if(s.forEach((t,e)=>{t&&t.trim()&&(r.push(e),n.push(t))}),0===n.length)return i?s:s[0];const a=new Array(n.length).fill("");let o=[],l=[],c=0;const h=async(t,i)=>{if(0===t.length)return;const s=t.join("\n");let r=0,n=!1;for(;r<CONFIG.GOOGLE.MAX_RETRIES&&!n;)try{const r=`https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${e}&dt=t&q=${encodeURIComponent(s)}`,o=await GoogleService.fetchWithTimeout(r);if(!o.ok)throw new Error(`Status ${o.status}`);const l=await o.json(),c=(l?.[0]?.map(t=>t?.[0]).join("")||"").split("\n");i.forEach((e,i)=>{i<c.length?a[e]=c[i]:a[e]=t[i]}),n=!0}catch(e){r+=1,r<CONFIG.GOOGLE.MAX_RETRIES?await GoogleService.delay(CONFIG.GOOGLE.RETRY_DELAY_MS*2**(r-1)):i.forEach((e,i)=>{a[e]=t[i]})}};for(let t=0;t<n.length;t+=1){const e=n[t];c+e.length>1500&&(await h(o,l),o=[],l=[],c=0),o.push(e),l.push(t),c+=e.length}o.length>0&&await h(o,l);const d=[...s];return r.forEach((t,e)=>{d[t]=a[e]}),i?d:d[0]}static async romanize(t){const e=Array.isArray(t)?t:t.data||t.content||[];if(!e||0===e.length)return Array.isArray(t)?t:[];const i=e.some(t=>!1!==t.isWordSynced&&Array.isArray(t.text)&&t.text.length>1);return i?this.romanizeWordSynced(e):this.romanizeLineSynced(e)}static async romanizeWordSynced(t){return Promise.all(t.map(async t=>{if(!t.text||!Array.isArray(t.text)||0===t.text.length||t.romanizedText)return t;const e=t.text.map(t=>t.text).join(""),[i]=await this.romanizeTexts([e]),s=t.text.map(t=>({...t,romanizedText:t.romanizedText}));return{...t,text:s,romanizedText:i||""}}))}static async romanizeLineSynced(t){const e=t.map(t=>t.romanizedText?"":Array.isArray(t.text)&&t.text.length>0?t.text.map(t=>t.text).join(""):""),i=await this.romanizeTexts(e);return t.map((t,e)=>({...t,romanizedText:i[e]||""}))}static async romanizeTexts(t){const e=t.join(" ");if(GoogleService.isPurelyLatinScript(e))return t;const i=[];for(const e of t)if(!e||GoogleService.isPurelyLatinScript(e))i.push(e);else{let t=0,s=!1,r=null;for(;t<CONFIG.GOOGLE.MAX_RETRIES&&!s;)try{const t=`https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=rm&q=${encodeURIComponent(e)}`,r=await GoogleService.fetchWithTimeout(t),n=await r.json(),a=n?.[0]?.[0]?.[3]||e;i.push(a),s=!0}catch(i){r=i,console.warn(`GoogleService: Error romanizing text "${e}" (attempt ${t+1}/${CONFIG.GOOGLE.MAX_RETRIES}):`,i),t+=1,t<CONFIG.GOOGLE.MAX_RETRIES&&await GoogleService.delay(CONFIG.GOOGLE.RETRY_DELAY_MS*2**(t-1))}s||(console.error(`GoogleService: Failed to romanize text "${e}" after ${CONFIG.GOOGLE.MAX_RETRIES} attempts. Last error:`,r),i.push(e))}return i}}const VERSION="1.5.4",INSTRUMENTAL_THRESHOLD_MS=7e3,FETCH_TIMEOUT_MS=8e3,SEEK_THRESHOLD_MS=500,SCROLL_ANIMATION_DURATION_MS=350,GAP_PULSE_DURATION_MS=4e3,GAP_PULSE_CYCLE_MS=8e3,GAP_EXIT_LEAD_MS=600,GAP_MIN_SCALE=.85;function fetchWithTimeout(t,e={},i=8e3){const s=new AbortController,r=setTimeout(()=>s.abort(),i);return fetch(t,{...e,signal:s.signal}).finally(()=>clearTimeout(r))}const KPOE_SERVERS=["https://lyricsplus.binimum.org","https://lyricsplus-seven.vercel.app","https://lyricsplus.prjktla.workers.dev","https://lyrics-plus-backend.vercel.app"],DEFAULT_KPOE_SOURCE_ORDER="apple,lyricsplus,musixmatch,spotify,qq,deezer,musixmatch-word",GENIUS_WORKER_URL="https://fetch-genius.samidy.workers.dev/";class AmLyrics extends i{constructor(){super(...arguments),this.downloadFormat="auto",this.highlightColor="#ffffff",this.autoScroll=!0,this.interpolate=!0,this.showRomanization=!1,this.showTranslation=!1,this._currentTime=0,this.isLoading=!1,this.activeLineIndices=[],this.activeMainWordIndices=new Map,this.activeBackgroundWordIndices=new Map,this.mainWordProgress=new Map,this.backgroundWordProgress=new Map,this.lyricsSource=null,this.availableSources=[],this.currentSourceIndex=0,this.isFetchingAlternatives=!1,this.hasFetchedAllProviders=!1,this.mainWordAnimations=new Map,this.backgroundWordAnimations=new Map,this.lastInstrumentalIndex=null,this.isUserScrolling=!1,this.isProgrammaticScroll=!1,this.isClickSeeking=!1,this.cachedLyricsLines=[],this.cachedLineArray=[],this.lineElementCache=new Map,this.gapElementCache=new Map,this.cachedAllGaps=[],this.cachedIsUnsynced=!1,this.cachedLineData=null,this.activeLineIds=new Set,this.currentPrimaryActiveLine=null,this.lastPrimaryActiveLine=null,this.scrollAnimationState=null,this.currentScrollOffset=0,this.animatingLines=[],this.lastActiveIndex=0,this.visibleLineIds=new Set,this.cachedScrollPaddingTop=null,this.preActiveLineElements=[],this.positionedLineElements=[],this.activeGapLineElements=[],this._boundHandleUserScroll=this.handleUserScroll.bind(this),this._boundAnimateProgress=this.animateProgress.bind(this)}async toggleRomanization(){this.showRomanization=!this.showRomanization,await this.applyRomanization()}async applyRomanization(){if(this.showRomanization&&this.lyrics){const t=this.lyrics.some(t=>!(t.romanizedText||t.text&&t.text.some(t=>t.romanizedText)));if(t){this.isLoading=!0;try{const t=await GoogleService.romanize(this.lyrics);this.lyrics=t}catch(t){console.error("Romanization failed",t)}finally{this.isLoading=!1}}}}async toggleTranslation(){this.showTranslation=!this.showTranslation,await this.applyTranslation()}async applyTranslation(){if(this.showTranslation&&this.lyrics){const t=this.lyrics.some(t=>!t.translation);if(t){this.isLoading=!0;try{const t=this.lyrics.map(t=>t.translation?"":t.text.map(t=>t.text).join(""));if(t.every(t=>!t))return void(this.isLoading=!1);const e=await GoogleService.translate(t,"en"),i=Array.isArray(e)?e:[e],s=this.lyrics.map((t,e)=>t.translation?t:{...t,translation:i[e]||void 0});this.lyrics=s}catch(t){console.error("Translation failed",t)}finally{this.isLoading=!1}}}}set currentTime(t){const e=this._currentTime;if(t<e&&e-t>1e3&&this.lyrics&&(this.activeLineIndices=[],this.activeMainWordIndices.clear(),this.activeBackgroundWordIndices.clear(),this.mainWordProgress.clear(),this.backgroundWordProgress.clear(),this.mainWordAnimations.clear(),this.backgroundWordAnimations.clear(),this.preActiveLineElements=[],this.positionedLineElements=[],this.activeGapLineElements=[],this.lyricsContainer)){this.lyricsContainer.querySelectorAll(".lyrics-line.active, .lyrics-line.pre-active, .lyrics-line.bg-expanded").forEach(t=>{t.classList.remove("active","pre-active","bg-expanded"),AmLyrics.resetSyllables(t)});this.lyricsContainer.querySelectorAll(".lyrics-gap.active, .lyrics-gap.gap-exiting").forEach(t=>t.classList.remove("active","gap-exiting")),this.gapElementCache.clear()}this._currentTime=t,e!==t&&this.lyrics&&this._onTimeChanged(e,t)}get currentTime(){return this._currentTime}_updateFooter(){const t=this.shadowRoot?.querySelector(".lyrics-footer");if(!t)return;const e=t.querySelector(".source-switch-btn"),i=t.querySelector(".source-switch-svg"),s=t.querySelector(".source-switch-label");e&&(e.disabled=this.isFetchingAlternatives),i&&i.setAttribute("style","margin-right: 4px; "+(this.isFetchingAlternatives?"animation: spin 1s linear infinite;":"")),s&&(s.textContent=this.isFetchingAlternatives?"Switching...":"Switch")}connectedCallback(){super.connectedCallback(),this.fetchLyrics()}disconnectedCallback(){super.disconnectedCallback(),this.animationFrameId&&(cancelAnimationFrame(this.animationFrameId),this.animationFrameId=void 0),this.userScrollTimeoutId&&(clearTimeout(this.userScrollTimeoutId),this.userScrollTimeoutId=void 0),this.clickSeekTimeout&&(clearTimeout(this.clickSeekTimeout),this.clickSeekTimeout=void 0),this.scrollAnimationTimeout&&(clearTimeout(this.scrollAnimationTimeout),this.scrollAnimationTimeout=void 0),this.scrollUnlockTimeout&&(clearTimeout(this.scrollUnlockTimeout),this.scrollUnlockTimeout=void 0),this.fetchAbortController?.abort(),this.fetchAbortController=void 0,this.lyricsContainer&&(this.lyricsContainer.removeEventListener("wheel",this._boundHandleUserScroll),this.lyricsContainer.removeEventListener("touchmove",this._boundHandleUserScroll)),this.preActiveLineElements=[],this.positionedLineElements=[],this.activeGapLineElements=[],this.visibilityObserver?.disconnect(),this.visibilityObserver=void 0}async fetchLyrics(){this.fetchAbortController?.abort();const t=new AbortController;this.fetchAbortController=t,this.isLoading=!0,this.lyrics=void 0,this.lyricsSource=null,this.availableSources=[],this.currentSourceIndex=0,this.isFetchingAlternatives=!1,this.hasFetchedAllProviders=!1,this._updateFooter();try{if(this.ttml){const t=AmLyrics.parseTTML(this.ttml);if(t&&t.lines.length>0)return this.lyrics=t.lines,this.lyricsSource="Local",t.songwriters&&(this.songwriters=t.songwriters),this.availableSources=[{lines:this.lyrics,source:"Local",songwriters:this.songwriters}],this.currentSourceIndex=0,this.hasFetchedAllProviders=!0,this._updateFooter(),void await this.onLyricsLoaded()}const e=await this.resolveSongMetadata();if(t.signal.aborted)return;const i=Boolean(this.musicId)&&!this.songTitle&&!this.songArtist&&!this.query&&!this.isrc,s=[];if(e?.metadata&&!i){const t=e.metadata.title?.trim()||"",i=e.metadata.artist?.trim()||"",r=await AmLyrics.fetchLyricsFromBiniLyrics(t,i,e.catalogIsrc,e.metadata);r&&r.lines.length>0&&s.push(r);const n=t=>t.some(t=>t.lines.some(t=>t.isWordSynced||t.text&&t.text.length>1));if(0===s.length||!n(s)){const t=await AmLyrics.fetchLyricsFromUnison(e.metadata);t&&t.lines.length>0&&s.push(t)}if(0===s.length||!n(s)){const r=await AmLyrics.fetchLyricsFromYouLyPlus(t,i,e.catalogIsrc,e.metadata,!0);r&&r.length>0&&s.push(...r)}}const r=t=>t.some(t=>t.lines.some(t=>t.timestamp>0||t.endtime>0));if((0===s.length||!r(s))&&e?.metadata){const t=await AmLyrics.fetchLyricsFromLrclib(e.metadata);t&&t.lines.length>0&&s.push({lines:t.lines,source:"LRCLIB"})}if(0===s.length&&e?.metadata){const t=await AmLyrics.fetchLyricsFromGenius(e.metadata);t&&t.lines.length>0&&s.push({lines:t.lines,source:"Genius"})}if(this.hasFetchedAllProviders=0===s.length||s.some(t=>"LRCLIB"===t.source||"Genius"===t.source),this._updateFooter(),s.length>0){this.availableSources=AmLyrics.mergeAndSortSources(s),this.currentSourceIndex=0;const t=this.availableSources[0];return this.lyrics=t.lines,this.lyricsSource=t.source,t.songwriters&&(this.songwriters=t.songwriters),void await this.onLyricsLoaded()}this.lyrics=void 0,this.lyricsSource=null}finally{t.signal.aborted||(this.isLoading=!1)}}async onLyricsLoaded(){this.activeLineIndices=[],this.activeMainWordIndices.clear(),this.activeBackgroundWordIndices.clear(),this.mainWordProgress.clear(),this.backgroundWordProgress.clear(),this.mainWordAnimations.clear(),this.backgroundWordAnimations.clear(),this.preActiveLineElements=[],this.positionedLineElements=[],this.activeGapLineElements=[],this.lyricsContainer&&(this.isProgrammaticScroll=!0,this.lyricsContainer.scrollTop=0,window.setTimeout(()=>{this.isProgrammaticScroll=!1},100)),await this.autoProcessLyrics()}async autoProcessLyrics(){this.showRomanization&&await this.applyRomanization(),this.showTranslation&&await this.applyTranslation()}static getRankForCollected(t,e){const i=t.toLowerCase(),s=e.some(t=>t.text&&Array.isArray(t.text)&&t.text.length>1),r=e.length>0&&e.every(t=>0===t.timestamp&&0===t.endtime),n=i.includes("qq")||i.includes("lyricsplus");return i.includes("apple")&&s?1:i.includes("bini")&&s?2:i.includes("unison")&&s?3:n&&s?4:i.includes("musixmatch")&&s?5:i.includes("lrclib")&&s?6:s?7:!i.includes("apple")||s||r?!i.includes("bini")||s||r?!i.includes("unison")||s||r?!n||s||r?!i.includes("musixmatch")||s||r?!i.includes("lrclib")||s||r?s||r?i.includes("apple")&&r?15:i.includes("bini")&&r?16:i.includes("unison")&&r?17:n&&r?18:i.includes("musixmatch")&&r?19:i.includes("lrclib")&&r?20:i.includes("genius")?21:30:14:13:12:11:10:9:8}static mergeAndSortSources(t){const e=new Map;for(const i of t){const t=i.source.toLowerCase().includes("lyricsplus")?"QQ":i.source;e.has(t)||e.set(t,{...i,source:t})}return Array.from(e.values()).sort((t,e)=>AmLyrics.getRankForCollected(t.source,t.lines)-AmLyrics.getRankForCollected(e.source,e.lines))}async switchSource(){if(!this.isFetchingAlternatives){if(!this.hasFetchedAllProviders){this.isFetchingAlternatives=!0,this._updateFooter();try{const t=await this.resolveSongMetadata();if(t?.metadata){const e=[];if(!this.availableSources.some(t=>t.source.toLowerCase().includes("unison"))){const i=await AmLyrics.fetchLyricsFromUnison(t.metadata);i&&i.lines.length>0&&e.push(i)}if(!this.availableSources.some(t=>t.source.toLowerCase().includes("apple")||t.source.toLowerCase().includes("qq"))){const i=t.metadata.title?.trim()||"",s=t.metadata.artist?.trim()||"",r=await AmLyrics.fetchLyricsFromYouLyPlus(i,s,t.catalogIsrc,t.metadata,!0);r&&r.length>0&&e.push(...r)}if(!this.availableSources.some(t=>t.source.toLowerCase().includes("lrclib"))){const i=await AmLyrics.fetchLyricsFromLrclib(t.metadata);i&&i.lines.length>0&&e.push({lines:i.lines,source:"LRCLIB"})}if(!this.availableSources.some(t=>t.source.toLowerCase().includes("genius"))){const i=await AmLyrics.fetchLyricsFromGenius(t.metadata);i&&i.lines.length>0&&e.push({lines:i.lines,source:"Genius"})}e.length>0&&(this.availableSources=AmLyrics.mergeAndSortSources([...this.availableSources,...e]),this.currentSourceIndex=this.availableSources.findIndex(t=>t.source===this.lyricsSource),-1===this.currentSourceIndex&&(this.currentSourceIndex=0))}}finally{this.hasFetchedAllProviders=!0,this.isFetchingAlternatives=!1,this._updateFooter()}}if(this.availableSources.length>1){this.currentSourceIndex=(this.currentSourceIndex+1)%this.availableSources.length;const t=this.availableSources[this.currentSourceIndex];this.lyrics=t.lines,this.lyricsSource=t.source,t.songwriters&&(this.songwriters=t.songwriters),await this.onLyricsLoaded()}}}async resolveSongMetadata(){const t={title:this.songTitle?.trim()??"",artist:this.songArtist?.trim()??"",album:this.songAlbum?.trim()||void 0,songwriters:this.songwriters?.trim()||void 0,durationMs:void 0};"number"==typeof this.songDurationMs&&this.songDurationMs>0?t.durationMs=this.songDurationMs:"number"==typeof this.duration&&this.duration>0&&(t.durationMs=this.duration);let e=this.musicId,i=this.isrc;if(this.query&&(!t.title||!t.artist||!t.album)){const e=AmLyrics.parseQueryMetadata(this.query);e&&(!t.title&&e.title&&(t.title=e.title),!t.artist&&e.artist&&(t.artist=e.artist),!t.album&&e.album&&(t.album=e.album))}let s=null;!this.query||t.title&&t.artist||(s=await AmLyrics.searchLyricsPlusCatalog(this.query),s&&(!t.title&&s.title&&(t.title=s.title),!t.artist&&s.artist&&(t.artist=s.artist),!t.album&&s.album&&(t.album=s.album),!t.songwriters&&s.songwriters&&(t.songwriters=s.songwriters),null==t.durationMs&&"number"==typeof s.durationMs&&s.durationMs>0&&(t.durationMs=s.durationMs),!e&&s.id?.appleMusic&&(e=s.id.appleMusic),!i&&s.isrc&&(i=s.isrc)));const r=t.title?.trim()??"",n=t.artist?.trim()??"",a=t.album?.trim(),o="number"==typeof t.durationMs&&Number.isFinite(t.durationMs)&&t.durationMs>0?Math.round(t.durationMs):void 0;return{metadata:r&&n?{title:r,artist:n,album:a||void 0,durationMs:o}:void 0,appleId:e,appleSong:null,catalogIsrc:i}}static parseQueryMetadata(t){const e=t?.trim();if(!e)return null;const i={},s=e.split(/\s[-–—]\s/);if(s.length>=2){const[t,...e]=s,r=e.join(" - "),n=t.trim(),a=r.trim();if(n&&a)return i.title=n,i.artist=a,i}const r=e.split(/\s+[bB]y\s+/);if(2===r.length){const[t,e]=r.map(t=>t.trim());if(t&&e)return i.title=t,i.artist=e,i}return null}static async searchLyricsPlusCatalog(t){const e=t?.trim();if(!e)return null;for(const t of KPOE_SERVERS){const i=`${t.endsWith("/")?t.slice(0,-1):t}/v1/songlist/search?q=${encodeURIComponent(e)}`;try{const t=await fetchWithTimeout(i);if(t.ok){const e=await t.json();let i=[];const s=e;if(Array.isArray(s?.results)?i=s.results:Array.isArray(e)&&(i=e),i.length>0){return i.find(t=>t?.id&&t.id.appleMusic)??i[0]}}}catch(t){}}return null}static async fetchLyricsFromBiniLyrics(t,e,i,s={}){if(!(t&&e||i))return null;try{let r=null;if(i)try{const t=`https://lyrics-api.binimum.org/?isrc=${encodeURIComponent(i)}`,e=await fetchWithTimeout(t);if(e.ok){const t=await e.json();t.results&&t.results.length>0&&(r=t)}}catch{}if(!r&&t&&e){const i=new URLSearchParams({track:t,artist:e});s.album&&i.append("album",s.album),s.durationMs&&s.durationMs>0&&i.append("duration",Math.round(s.durationMs/1e3).toString());const n=`https://lyrics-api.binimum.org/?${i.toString()}`,a=await fetchWithTimeout(n);a.ok&&(r=await a.json())}if(r&&r.results&&r.results.length>0){const t=r.results[0];if(t.lyricsUrl){const e=await fetchWithTimeout(t.lyricsUrl);if(e.ok){const t=await e.text(),i=AmLyrics.parseTTML(t);if(i&&i.lines.length>0)return{lines:i.lines,source:"BiniLyrics",songwriters:i.songwriters}}}}}catch(t){console.error("Cache API failed",t)}return null}static async fetchLyricsFromYouLyPlus(t,e,i,s={},r=!1){if(!(t&&e||i))return[];const n=new URLSearchParams;t&&n.append("title",t),e&&n.append("artist",e),i&&n.append("isrc",i),s.album&&n.append("album",s.album),s.durationMs&&s.durationMs>0&&n.append("duration",Math.round(s.durationMs/1e3).toString()),DEFAULT_KPOE_SOURCE_ORDER.includes("apple")||n.append("source",DEFAULT_KPOE_SOURCE_ORDER);const a=(t,e)=>{const i=t.toLowerCase(),s=e.some(t=>t.text&&Array.isArray(t.text)&&t.text.length>1),r=e.length>0&&e.every(t=>0===t.timestamp&&0===t.endtime),n=i.includes("qq")||i.includes("lyricsplus");return i.includes("apple")&&s?1:i.includes("bini")&&s?2:i.includes("unison")&&s?3:n&&s?4:i.includes("musixmatch")&&s?5:s?6:!i.includes("apple")||s||r?!i.includes("bini")||s||r?!i.includes("unison")||s||r?!n||s||r?!i.includes("musixmatch")||s||r?s||r?i.includes("apple")&&r?13:i.includes("bini")&&r?14:i.includes("unison")&&r?15:n&&r?16:i.includes("musixmatch")&&r?17:30:12:11:10:9:8:7},o=[];if(!r){const r=await AmLyrics.fetchLyricsFromBiniLyrics(t,e,i,s);if(r)return o.push(r),o}const l=[...KPOE_SERVERS].sort(()=>Math.random()-.5).slice(0,3);for(const t of l){const e=`${t.endsWith("/")?t.slice(0,-1):t}/v2/lyrics/get?${n.toString()}`;let i=null;try{const t=await fetchWithTimeout(e);t.ok&&(i=await t.json())}catch{i=null}if(i){const t=AmLyrics.convertKPoeLyrics(i);if(t&&t.length>0){const e=i?.metadata?.source||i?.metadata?.provider||"LyricsPlus (KPoe)",s=a(e,t),r={lines:t,source:e};if(o.push(r),1===s)break}}}const c=o.some(t=>a(t.source,t.lines)<=2);if(!c)try{const t=`https://lyricsplus.binimum.org/v2/lyrics/get?${new URLSearchParams(n).toString()}`,e=await fetchWithTimeout(t);if(e.ok){const t=await e.json();if(t){const e=AmLyrics.convertKPoeLyrics(t),i=t?.metadata?.source||t?.metadata?.provider||"LyricsPlus (KPoe)",s=e?.some(t=>t.text&&Array.isArray(t.text)&&t.text.length>1);e&&e.length>0&&s&&o.push({lines:e,source:i})}}}catch(t){}return o}static parseLrcSubtitles(t){if(!t||"string"!=typeof t)return[];const e=[],i=t.split("\n"),s=[];for(const t of i){const e=t.match(/^\[(\d{1,3}):(\d{2})\.(\d{2,3})\]\s?(.*)$/);if(!e)continue;const i=parseInt(e[1],10),r=parseInt(e[2],10);let n=parseInt(e[3],10);3===e[3].length&&(n=Math.round(n/10));const a=1e3*(60*i+r)+10*n,o=e[4]||"";s.push({timestamp:a,text:o})}for(let t=0;t<s.length;t+=1){const{timestamp:i,text:r}=s[t],n=t+1<s.length?s[t+1].timestamp:i+5e3;if(!r.trim())continue;const a={text:r,part:!1,timestamp:i,endtime:n,lineSynced:!0};e.push({text:[a],background:!1,backgroundText:[],oppositeTurn:!1,timestamp:i,endtime:n,isWordSynced:!1})}return e}static async fetchLyricsFromLrclib(t){const e=t.title?.trim(),i=t.artist?.trim();if(!e||!i)return null;try{const t=`${i} ${e}`,s=new URLSearchParams({q:t}),r=await fetchWithTimeout(`https://lrclib.net/api/search?${s.toString()}`,{headers:{"User-Agent":"apple-music-web-components/1.5.4"}});if(!r.ok)return null;const n=await r.json();if(!Array.isArray(n)||0===n.length)return null;const a=n.find(t=>t.syncedLyrics&&"string"==typeof t.syncedLyrics),o=a||n[0];if(o.syncedLyrics){const t=AmLyrics.parseLrcSubtitles(o.syncedLyrics);if(t.length>0)return{lines:t,source:"LRCLIB"}}if(o.plainLyrics&&"string"==typeof o.plainLyrics){const t=o.plainLyrics.split("\n").filter(t=>t.trim());if(t.length>0){return{lines:t.map(t=>({text:[{text:t,part:!1,timestamp:0,endtime:0}],background:!1,backgroundText:[],oppositeTurn:!1,timestamp:0,endtime:0,isWordSynced:!1})),source:"LRCLIB (unsynced)"}}}}catch{}return null}static async fetchLyricsFromGenius(t){const e=t.title?.trim(),i=t.artist?.trim();if(!e||!i)return null;try{const t=new URLSearchParams({title:e,artist:i}),s=await fetchWithTimeout(`${GENIUS_WORKER_URL}?${t.toString()}`);if(!s.ok)return null;const r=await s.json();if(r.lyrics){const t=r.lyrics.split("\n").map(t=>t.trim()).filter(t=>t&&!t.startsWith("["));if(t.length>0){return{lines:t.map(t=>({text:[{text:t,part:!1,timestamp:0,endtime:0}],background:!1,backgroundText:[],oppositeTurn:!1,timestamp:0,endtime:0,isWordSynced:!1})),source:"Genius"}}}}catch{}return null}static async fetchLyricsFromUnison(t){const e=t.title?.trim(),i=t.artist?.trim();if(!e||!i)return null;const s=new URLSearchParams;s.append("song",e),s.append("artist",i),t.album&&s.append("album",t.album),t.durationMs&&t.durationMs>0&&s.append("duration",Math.round(t.durationMs/1e3).toString());try{const t=await fetchWithTimeout(`https://unison.boidu.dev/lyrics?${s.toString()}`);if(!t.ok)return null;const e=await t.json();if(!e.success||!e.data?.lyrics)return null;const i=e.data,r=i.format||"lrc",n=i.syncType||"linesync",a=i.lyrics;if("ttml"===r){const t=AmLyrics.parseTTML(a);if(t&&t.lines.length>0)return{lines:t.lines,source:"Unison",songwriters:t.songwriters}}if("lrc"===r)if("plain"===n){const t=a.split("\n").map(t=>t.trim()).filter(t=>t);if(t.length>0){return{lines:t.map(t=>({text:[{text:t,part:!1,timestamp:0,endtime:0}],background:!1,backgroundText:[],oppositeTurn:!1,timestamp:0,endtime:0,isWordSynced:!1})),source:"Unison (unsynced)"}}}else{const t=AmLyrics.parseLrcSubtitles(a);if(t.length>0)return{lines:t,source:"Unison"}}}catch{}return null}static calculateLineAlignments(t,e){const i=new Array(t.length).fill(void 0);let s=!0,r=null,n=0,a=0;if(t.forEach((t,o)=>{let l;if(t){let i=e[t];i||(i="v1000"===t?"group":"v2000"===t?"other":"person"),"group"===i?l="start":(null===r?s="other"!==i:t!==r&&(s=!s),l=s?"start":"end",r=t)}l&&(a+=1,"end"===l&&(n+=1)),i[o]=l}),a>0&&Math.round(n/a*100)>=85){const t=t=>"start"===t?"end":"end"===t?"start":t;for(let e=0;e<i.length;e+=1)i[e]=t(i[e])}return i}static parseTTML(t){try{const e=(new DOMParser).parseFromString(t,"text/xml"),i={},s={},r={},n=e.getElementsByTagName("ttm:agent");for(let t=0;t<n.length;t+=1){const e=n[t],i=e.getAttribute("xml:id"),s=e.getAttribute("type");i&&s&&(r[i]=s)}let a;const o=e.getElementsByTagName("songwriter");if(o.length>0){const t=[];for(let e=0;e<o.length;e+=1)o[e].textContent&&t.push(o[e].textContent);t.length>0&&(a=t.join(", "))}const l=e.getElementsByTagName("translation");for(let t=0;t<l.length;t+=1){const e=l[t].getElementsByTagName("text");for(let t=0;t<e.length;t+=1){const s=e[t],r=s.getAttribute("for");r&&s.textContent&&(i[r]=s.textContent)}}const c=t=>{if(!t)return 0;const e=t.split(":");let i=0;return i=2===e.length?60*parseInt(e[0],10)+parseFloat(e[1]):3===e.length?3600*parseInt(e[0],10)+60*parseInt(e[1],10)+parseFloat(e[2]):parseFloat(e[0]),Math.round(1e3*i)},h=e.getElementsByTagName("transliteration");for(let t=0;t<h.length;t+=1){const e=h[t].getElementsByTagName("text");for(let t=0;t<e.length;t+=1){const i=e[t],r=i.getAttribute("for");if(!r)continue;const n=Array.from(i.getElementsByTagName("span")).filter(t=>t.getAttribute("begin"));if(n.length>0){const t=[];let e="";for(let i=0;i<n.length;i+=1){const s=n[i],r=s.getAttribute("begin"),a=s.getAttribute("end");let o=s.textContent||"";const l=s.nextSibling;l&&3===l.nodeType&&/^\s/.test(l.textContent||"")&&!o.endsWith(" ")&&(o+=" "),""!==o.trim()&&(t.push({time:c(r),duration:c(a)-c(r),text:o}),e+=o)}s[r]={text:e.trim(),syllabus:t}}else i.textContent&&(s[r]={text:i.textContent.trim().replace(/\s+/g," ")})}}const d=[],p=e.getElementsByTagName("p"),m=[];for(let t=0;t<p.length;t+=1)m.push(p[t].getAttribute("ttm:agent")||void 0);const u=AmLyrics.calculateLineAlignments(m,r);for(let t=0;t<p.length;t+=1){const e=p[t],r=e.getAttribute("itunes:key"),n=c(e.getAttribute("begin")),a=c(e.getAttribute("end"));let o;e.parentNode&&"div"===e.parentNode.tagName&&(o=e.parentNode.getAttribute("itunes:songPart")||void 0);const l=[],h=[],m=e.getElementsByTagName("span");if(m.length>0)for(let t=0;t<m.length;t+=1){const e=m[t];if("x-bg"===e.getAttribute("ttm:role")){const t=e.getElementsByTagName("span");for(let e=0;e<t.length;e+=1){const i=t[e];let s=i.textContent||"";const r=i.nextSibling;r&&3===r.nodeType&&/^\s/.test(r.textContent||"")&&!s.endsWith(" ")&&(s+=" "),h.push({text:s,timestamp:c(i.getAttribute("begin")),endtime:c(i.getAttribute("end")),part:!/\s$/.test(s)})}continue}if(e.parentNode&&"x-bg"===e.parentNode.getAttribute?.("ttm:role"))continue;let i=e.textContent||"";const s=e.nextSibling;s&&3===s.nodeType&&/^\s/.test(s.textContent||"")&&!i.endsWith(" ")&&(i+=" "),l.push({text:i,timestamp:c(e.getAttribute("begin")),endtime:c(e.getAttribute("end")),part:!/\s$/.test(i)})}else l.push({text:e.textContent?.trim()||"",timestamp:n,endtime:a,part:!1,lineSynced:!0});const y=u[t],g=r?s[r]:void 0;if(g&&l.length>1&&m.length>0)if(g.syllabus&&g.syllabus.length===l.length)l.forEach((t,e)=>{t.romanizedText=g.syllabus[e].text});else{const t=g.text.split(/\s+/).filter(Boolean),e=[];for(let t=0;t<l.length;t+=1)l[t].part&&e.length>0?e[e.length-1].push(t):e.push([t]);const i=/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]/.test(l.map(t=>t.text).join(""));if(t.length===e.length)e.forEach((e,i)=>{l[e[0]].romanizedText=t[i]});else if(t.length===l.length)l.forEach((e,i)=>{e.romanizedText=t[i]});else if(i){let i=0;for(const s of e){const e=l[s[0]],r=s.map(t=>l[t].text).join(""),n=(r.match(/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7afA-Za-z0-9]/g)||[]).length;n>0&&i<t.length&&(e.romanizedText=t.slice(i,i+n).join(" "),i+=n)}}}d.push({text:l,background:h.length>0,backgroundText:h,timestamp:n,endtime:a,isWordSynced:m.length>0,alignment:y,songPart:o,translation:r?i[r]:void 0,romanizedText:g?.text,oppositeTurn:"end"===y})}return{lines:d,songwriters:a}}catch(t){return console.error("Failed to parse TTML",t),null}}static convertKPoeLyrics(t){if(!t)return null;let e=null;if(Array.isArray(t?.lyrics)?e=t.lyrics:Array.isArray(t?.data?.lyrics)?e=t.data.lyrics:Array.isArray(t?.data)&&(e=t.data),!e||0===e.length)return null;const i=e.filter(t=>Boolean(t)),s=[],r="Line"===t.type||"line"===t.type,n={};t.metadata?.agents&&Object.entries(t.metadata.agents).forEach(([t,e])=>{const i=e.alias||t;n[i]=e.type});const a=i.map(t=>t.element?.singer),o=AmLyrics.calculateLineAlignments(a,n);for(let t=0;t<i.length;t+=1){const e=i[t],n=AmLyrics.toMilliseconds(e.time),a=AmLyrics.toMilliseconds(e.duration),l=o[t],c="string"==typeof e.text?e.text:"",h=AmLyrics.toMilliseconds(e.time),d=AmLyrics.toMilliseconds(e.duration),p=AmLyrics.toMilliseconds(e.endTime)||h+(d||0);let m=[];Array.isArray(e.syllabus)?m=e.syllabus.filter(t=>Boolean(t)):Array.isArray(e.words)&&(m=e.words.filter(t=>Boolean(t)));const u=[],y=[];if(!r&&m.length>0)for(const t of m){const e=AmLyrics.toMilliseconds(t.time,h),i=AmLyrics.toMilliseconds(t.duration),s=0===i&&1===m.length?p:e+i,r={text:"string"==typeof t.text?t.text:"",part:Boolean(t.part),timestamp:e,endtime:s};t.isBackground?y.push(r):u.push(r)}0===u.length&&c&&u.push({text:c,part:!1,timestamp:h,endtime:p||h,lineSynced:r});const g=u.length>0||y.length>0,{transliteration:f}=e;let v;f&&(v=f.text,Array.isArray(f.syllabus)&&f.syllabus.length===u.length&&f.syllabus.forEach((t,e)=>{u[e].romanizedText=t.text}));const b=e.translation?.text,x={text:u,background:y.length>0,backgroundText:y,oppositeTurn:"end"===l||!!Array.isArray(e.element)&&(e.element.includes("opposite")||e.element.includes("right")),timestamp:h,endtime:n+a,isWordSynced:!r&&g,alignment:l,songPart:e.element?.songPart,romanizedText:v,translation:b};s.push(x)}return s}static toMilliseconds(t,e=0){const i=Number(t);return!Number.isFinite(i)||Number.isNaN(i)?e:Number.isInteger(i)?Math.max(0,Math.round(i)):Math.round(1e3*i)}firstUpdated(){this.lyricsContainer&&(this.lyricsContainer.addEventListener("wheel",this._boundHandleUserScroll,{passive:!0}),this.lyricsContainer.addEventListener("touchmove",this._boundHandleUserScroll,{passive:!0}))}_onTimeChanged(t,e){const i=Math.abs(e-t)>500,s=this.findActiveLineIndices(e),r=this.activeLineIndices;if(!AmLyrics.arraysEqual(s,r)||i){if(this.lyricsContainer){for(const t of r)if(!s.includes(t)){const s=this._getLineElement(t);if(s){i||this.isUserScrolling?AmLyrics.unfinishSyllables(s):AmLyrics.finishSyllablesUpToTime(s,e),s.classList.remove("active","bg-expanded"),s.classList.contains("pre-active")&&s.classList.remove("pre-active");const t=this.preActiveLineElements.indexOf(s);-1!==t&&this.preActiveLineElements.splice(t,1)}}for(const t of s)if(!r.includes(t)){const e=this._getLineElement(t);if(e){e.classList.add("active","bg-expanded"),e.classList.remove("pre-active");const t=this.preActiveLineElements.indexOf(e);-1!==t&&this.preActiveLineElements.splice(t,1)}}for(const t of this.preActiveLineElements){const e=AmLyrics.getLineIndexFromElement(t);(null===e||!s.includes(e)&&t!==this.currentPrimaryActiveLine)&&t.classList.remove("pre-active")}this.preActiveLineElements=this.preActiveLineElements.filter(t=>t.classList.contains("pre-active"))}this.startAnimationFromTime(e)}if(this._handleActiveLineScroll(r,i),this.clearPastLineHighlights(),this.lyricsContainer){for(const t of this.activeLineIndices){const i=this._getLineElement(t);i&&AmLyrics.updateSyllablesForLine(i,e)}for(const t of this.activeGapLineElements)AmLyrics.updateSyllablesForLine(t,e);if(this.gapElementCache.size>0)for(const[,t]of this.gapElementCache){const s=t._cachedStartTime??parseFloat(t.getAttribute("data-start-time")||"0"),r=t._cachedEndTime??parseFloat(t.getAttribute("data-end-time")||"0"),n=e>=s&&e<r,a=t.classList.contains("active"),o=t.classList.contains("gap-exiting"),l=600;if(!n||a&&!i||o)if(a&&!o&&e>=r-l){t.classList.remove("active"),t.offsetWidth,t.classList.add("gap-exiting");const e=this.activeGapLineElements.indexOf(t);-1!==e&&this.activeGapLineElements.splice(e,1),setTimeout(()=>{t.classList.remove("gap-exiting")},600)}else if(n||!a&&!o)o&&e<r-l&&t.classList.remove("gap-exiting");else{t.classList.remove("active"),t.classList.remove("gap-exiting");const e=this.activeGapLineElements.indexOf(t);-1!==e&&this.activeGapLineElements.splice(e,1)}else{t.classList.remove("gap-exiting"),i&&a&&(t.classList.remove("active"),t.offsetWidth);const n=r-s,o=AmLyrics.getGapLoopDelay(n)+(e-s);t.style.setProperty("--gap-loop-delay",`-${o}ms`),t.classList.add("active"),this.activeGapLineElements.includes(t)||this.activeGapLineElements.push(t);t.querySelectorAll(".lyrics-syllable").forEach(t=>{const i=parseFloat(t.getAttribute("data-start-time")||"0"),s=parseFloat(t.getAttribute("data-end-time")||"0");e>s?(t.classList.add("finished"),t.classList.contains("highlight")||AmLyrics.updateSyllableAnimation(t,e-i)):e>=i&&e<=s&&AmLyrics.updateSyllableAnimation(t,e-i)})}}else if(this.lyricsContainer){this.lyricsContainer.querySelectorAll(".lyrics-gap").forEach(t=>{const s=parseFloat(t.getAttribute("data-start-time")||"0"),r=parseFloat(t.getAttribute("data-end-time")||"0"),n=e>=s&&e<r,a=t.classList.contains("active"),o=t.classList.contains("gap-exiting");if(!n||a&&!i||o)if(a&&!o&&e>=r-600){t.classList.remove("active"),t.offsetWidth,t.classList.add("gap-exiting");const e=this.activeGapLineElements.indexOf(t);-1!==e&&this.activeGapLineElements.splice(e,1),setTimeout(()=>{t.classList.remove("gap-exiting")},600)}else if(n||!a&&!o)o&&e<r-600&&t.classList.remove("gap-exiting");else{t.classList.remove("active"),t.classList.remove("gap-exiting");const e=this.activeGapLineElements.indexOf(t);-1!==e&&this.activeGapLineElements.splice(e,1)}else{t.classList.remove("gap-exiting"),i&&a&&(t.classList.remove("active"),t.offsetWidth);const n=r-s,o=AmLyrics.getGapLoopDelay(n)+(e-s);t.style.setProperty("--gap-loop-delay",`-${o}ms`),t.classList.add("active"),this.activeGapLineElements.includes(t)||this.activeGapLineElements.push(t)}})}const t=this.findInstrumentalGapAt(e);if(t){if(this.lastInstrumentalIndex=t.insertBeforeIndex,t.insertBeforeIndex>0){const e=this._getLineElement(t.insertBeforeIndex-1);e&&e.classList.contains("persist-highlight")&&!e.classList.contains("active")&&AmLyrics.unfinishSyllables(e)}}else null!==this.lastInstrumentalIndex&&(this.lastInstrumentalIndex=null);const s=this.lyrics&&this.lyrics.length>0?this.lyrics[this.lyrics.length-1]:null,r=this.lyricsContainer.querySelector(".lyrics-footer");if(r&&s&&s.endtime>0){const t=e>s.endtime+200;if(t&&!r.classList.contains("active")){r.classList.add("active");const t=this.lyricsContainer.querySelector(".lyrics-line:last-of-type");if(t){t.classList.remove("pre-active");const e=this.preActiveLineElements.indexOf(t);-1!==e&&this.preActiveLineElements.splice(e,1)}!this.autoScroll||this.isUserScrolling||this.isClickSeeking||this.focusLine(r)}else!t&&r.classList.contains("active")&&r.classList.remove("active")}}}updated(t){if(t.has("lyrics")&&(this._invalidateCaches(),this._ensureLineDataCache(),this._updateCachedIsUnsynced(),this._updateCharTimingData(),this.lyricsContainer&&this.lyrics)){const t=this.findActiveLineIndices(this.currentTime);for(const e of t){const t=this._getLineElement(e);t&&t.classList.add("active","bg-expanded")}if(this._onTimeChanged(0,this.currentTime),0===this.positionedLineElements.length){const t=this.lyricsContainer.querySelector(".lyrics-line");t&&this.updatePositionClasses(t)}this.visibilityObserver?.disconnect(),this.visibilityObserver=new IntersectionObserver(t=>{t.forEach(t=>{t.target.classList.toggle("far-line",!t.isIntersecting)})},{root:this.lyricsContainer,rootMargin:"200px",threshold:0});this.lyricsContainer.querySelectorAll(".lyrics-line").forEach(t=>this.visibilityObserver.observe(t))}if(t.has("duration")&&-1===this.duration)return this.currentTime=0,this.activeLineIndices=[],this.activeMainWordIndices.clear(),this.activeBackgroundWordIndices.clear(),this.mainWordProgress.clear(),this.backgroundWordProgress.clear(),this.mainWordAnimations.clear(),this.backgroundWordAnimations.clear(),this.preActiveLineElements=[],this.positionedLineElements=[],this.activeGapLineElements=[],this.setUserScrolling(!1),this.animationFrameId&&(cancelAnimationFrame(this.animationFrameId),this.animationFrameId=void 0),this.userScrollTimeoutId&&(clearTimeout(this.userScrollTimeoutId),this.userScrollTimeoutId=void 0),this.scrollUnlockTimeout&&(clearTimeout(this.scrollUnlockTimeout),this.scrollUnlockTimeout=void 0),this.scrollAnimationTimeout&&(clearTimeout(this.scrollAnimationTimeout),this.scrollAnimationTimeout=void 0),void(this.lyricsContainer&&(this.lyricsContainer.scrollTop=0));(t.has("query")||t.has("musicId")||t.has("isrc")||t.has("ttml")||t.has("songTitle")||t.has("songArtist")||t.has("songAlbum")||t.has("songDurationMs"))&&!t.has("currentTime")&&this.fetchLyrics(),t.has("currentTime")&&this.lyrics}_handleActiveLineScroll(t,e=!1){if(!this.lyricsContainer||!this.lyrics||0===this.lyrics.length)return;const i=this.lyricsContainer.querySelector(".lyrics-footer");if(i?.classList.contains("active"))return;let s=350,r=-1;for(let t=0;t<this.lyrics.length;t+=1)if(this.lyrics[t].timestamp>this.currentTime){r=t-1;break}if(-1===r&&this.lyrics.length>0&&this.currentTime>=this.lyrics[this.lyrics.length-1].timestamp&&(r=this.lyrics.length-1),-1!==r&&r+1<this.lyrics.length){const t=this.lyrics[r],e=this.lyrics[r+1].timestamp-t.endtime;s=Math.min(500,Math.max(350,e))}const n=this.currentTime+s,a=this.findActiveLineIndices(n);let o=null;if(a.length>0){const t=this.getPrimaryScrollLineIndex(a,n);null!==t&&-1!==t&&(o=this._getLineElement(t))}if(!o){const t=this.getLineIndexAtTime(n,0);null!==t&&-1!==t&&(o=this._getLineElement(t))}if(!o)return;o.classList.contains("active")||(o.classList.add("pre-active"),this.preActiveLineElements.includes(o)||this.preActiveLineElements.push(o));const l=s;this.focusLine(o,e,l)}_getTextWidth(t,e){return this._textWidthCanvas||(this._textWidthCanvas=document.createElement("canvas"),this._textWidthCtx=this._textWidthCanvas.getContext("2d",{willReadFrequently:!0})),this._textWidthCtx?(this._textWidthCtx.font=e,this._textWidthCtx.measureText(t).width):0}_rebuildDomCache(){if(!this.lyricsContainer)return;if(this.lineElementCache.clear(),this.gapElementCache.clear(),this.cachedLineArray=[],!this.lyrics)return;for(let t=0;t<this.lyrics.length;t+=1){const e=this.lyricsContainer.querySelector(`#lyrics-line-${t}`);e&&this.lineElementCache.set(t,e);const i=this.lyricsContainer.querySelector(`#gap-${t}`);i&&(i._cachedStartTime=parseFloat(i.getAttribute("data-start-time")||"0"),i._cachedEndTime=parseFloat(i.getAttribute("data-end-time")||"0"),this.gapElementCache.set(t,i))}const t=this.lyricsContainer.querySelectorAll(".lyrics-line");this.cachedLineArray=Array.from(t)}_getLineElement(t){const e=this.lineElementCache.get(t);if(e)return e;if(!this.lyricsContainer)return null;const i=this.lyricsContainer.querySelector(`#lyrics-line-${t}`);return i&&this.lineElementCache.set(t,i),i}_getGapElement(t){const e=this.gapElementCache.get(t);if(e)return e;if(!this.lyricsContainer)return null;const i=this.lyricsContainer.querySelector(`#gap-${t}`);return i&&this.gapElementCache.set(t,i),i}_invalidateCaches(){this.cachedAllGaps=[],this.cachedIsUnsynced=!1,this.cachedLineData=null,this.lineElementCache.clear(),this.gapElementCache.clear(),this.cachedLineArray=[],this.cachedScrollPaddingTop=null,this.preActiveLineElements=[],this.positionedLineElements=[],this.activeGapLineElements=[],this.visibilityObserver?.disconnect(),this.visibilityObserver=void 0}_updateCachedIsUnsynced(){this.cachedIsUnsynced=!!(this.lyrics&&this.lyrics.length>0)&&this.lyrics.every(t=>0===t.timestamp&&0===t.endtime)}_ensureLineDataCache(){!this.cachedLineData&&this.lyrics&&(this.cachedLineData=this.lyrics.map(t=>{const e=[];let i=[];t.text.forEach((s,r)=>{i.push(s);const n=t.text[r+1];(!n||!1===s.part||/\s$/.test(s.text)||n&&s.isBackground!==n.isBackground)&&(e.push(i),i=[])}),i.length>0&&e.push(i);const s=new Array(e.length).fill(!1),r=new Array(e.length).fill(!1),n=new Array(e.length).fill(!1),a=new Array(e.length).fill(""),o=new Array(e.length).fill(0),l=new Array(e.length).fill(0),c=new Array(e.length).fill(0),h=new Array(e.length).fill(0);let d=!1,p=0;for(;p<e.length;){let i=p;for(;i<e.length-1;){const t=e[i],s=t[t.length-1].text;if(/\s$/.test(s))break;i+=1}const m=e.slice(p,i+1).flatMap(t=>t.map(t=>t.text)).join("").trim(),u=e[p][0].timestamp,y=e[i],g=y[y.length-1].endtime,f=g-u,v=/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]/.test(m),b=/[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\u0590-\u05FF]/.test(m);b&&(d=!0);const x=m.includes("-"),A=m.length,L=!v&&!b&&!x&&A>0,w=!1===t.isWordSynced||t.text.some(t=>t.lineSynced);let $=L&&A>0&&A<=7;$&&($=A<3?f>=1050&&f>=525*A:f>=850&&f>=190*A);const S=f>=Math.max(700,85*A),T=A>=4&&f>=Math.max(1300,260*A),k=L&&!w&&!$&&(A>=8&&S||A<8&&T),_=$&&!w;let E=0;for(let t=p;t<=i;t+=1){s[t]=$,r[t]=_,n[t]=k,a[t]=m,o[t]=f,l[t]=E,c[t]=u,h[t]=g;const i=e[t].map(t=>t.text).join("");E+=i.replace(/\s/g,"").length}p=i+1}return{wordGroups:e,groupGrowable:s,groupGlowing:r,groupCharRise:n,vwFullText:a,vwFullDuration:o,vwCharOffset:l,vwStartMs:c,vwEndMs:h,lineIsRTL:d}}))}_updateCharTimingData(){if(!this.shadowRoot)return;this._rebuildDomCache();const t=this.shadowRoot.querySelector(".lyrics-syllable");if(!t)return;const e=getComputedStyle(t),{font:i}=e,s=parseFloat(e.fontSize),r=this.shadowRoot.querySelectorAll(".lyrics-word.growable, .lyrics-word.char-rise");r&&r.forEach(t=>{const e=t.querySelectorAll(".lyrics-syllable-wrap"),r=[];e.forEach(t=>{const e=t.querySelector(".lyrics-syllable");e&&r.push(e)}),r.forEach(t=>{const e=t.querySelectorAll(".char");if(0===e.length)return;const r=Array.from(e).map(t=>t.textContent||"").map(t=>this._getTextWidth(t,i)),n=r.reduce((t,e)=>t+e,0),a=parseFloat(t.dataset.duration||"0"),o=a>0?n/a:0,l=o>0?.375*s/o:100;let c=0;e.forEach((t,e)=>{const i=r[e],s=t;if(n>0){const t=c/n,e=i/n;s.dataset.wipeStart=t.toFixed(4),s.dataset.wipeDuration=e.toFixed(4),s.dataset.preWipeArrival=(a*t).toFixed(2),s.dataset.preWipeDuration=l.toFixed(2)}c+=i})})})}static arraysEqual(t,e){return t.length===e.length&&t.every((t,i)=>t===e[i])}static getLineIndexFromElement(t){if(!t)return null;const e=t.id.match(/^lyrics-line-(\d+)$/);return e?parseInt(e[1],10):null}static getGapLoopDelay(t){return((4e3-((t-600)%8e3+8e3)%8e3)%8e3+8e3)%8e3}clearPreActiveClasses(t=null){if(!this.lyricsContainer)return;const e=[];for(const i of this.preActiveLineElements){AmLyrics.getLineIndexFromElement(i)===t?e.push(i):i.classList.remove("pre-active")}this.preActiveLineElements=e}getPrimaryActiveLineIndex(t){if(0===t.length)return null;const e=t[0],i=t[t.length-1];let s=Math.max(e,i-2);const r=AmLyrics.getLineIndexFromElement(this.currentPrimaryActiveLine);return null!==r&&t.includes(r)&&(t.length<=3||s<r)&&(s=r),s}getPrimaryScrollLineIndex(t,e){if(!this.lyrics||0===this.lyrics.length)return null;const i=this.getLineIndexAtTime(e,this.lastActiveIndex);if(-1===i)return null;const s=AmLyrics.getLineIndexFromElement(this.currentPrimaryActiveLine);if(null!==s&&i>s&&this.lyrics[s]&&this.lyrics[i]&&this.lyrics[s].endtime===this.lyrics[i].endtime){if(this.findActiveLineIndices(e).length<=3)return s}return i}getOverlapClusterForActiveIndices(t,e){if(!this.lyrics||0===t.length)return null;let i=t[0];for(;i>0&&this.lyrics[i-1].endtime>=this.lyrics[i].timestamp;)i-=1;let s=i,r=this.lyrics[i].endtime;for(;s+1<this.lyrics.length&&this.lyrics[s+1].timestamp<=r;)s+=1,r=Math.max(r,this.lyrics[s].endtime);let n=i,a=this.lyrics[i].endtime;for(let t=i;t<=s&&this.lyrics[t].timestamp<=e;t+=1)n=t,a=Math.max(a,this.lyrics[t].endtime);return{start:i,end:s,startedEnd:n,startedEndTime:a}}focusLine(t,e=!1,i=void 0,s=!1,r=!1){const n=t!==this.currentPrimaryActiveLine;if(n&&!r){this.lastPrimaryActiveLine=this.currentPrimaryActiveLine,this.currentPrimaryActiveLine=t;const e=AmLyrics.getLineIndexFromElement(t);null!==e&&(this.lastActiveIndex=e)}(n||e)&&this.updatePositionClasses(t),s||!(e||n||r)||!this.autoScroll||this.isUserScrolling||this.isClickSeeking||this.scrollToActiveLineYouLy(t,e,i)}setUserScrolling(t){this.isUserScrolling=t,t?this.lyricsContainer?.classList.add("user-scrolling"):this.lyricsContainer?.classList.remove("user-scrolling")}handleUserScroll(){this.isProgrammaticScroll||this.isClickSeeking||(this.setUserScrolling(!0),this.clearPastLineHighlights(),this.userScrollTimeoutId&&clearTimeout(this.userScrollTimeoutId),this.userScrollTimeoutId=window.setTimeout(()=>{this.setUserScrolling(!1),this.userScrollTimeoutId=void 0,this.activeLineIndices.length>0&&this._handleActiveLineScroll([],!1)},2e3))}clearPastLineHighlights(){if(!this.lyricsContainer)return;const t=this.cachedLineArray.length?this.cachedLineArray:Array.from(this.lyricsContainer.querySelectorAll(".lyrics-line:not(.lyrics-gap)")),e=this.lyricsContainer.getBoundingClientRect().top+this.getScrollPaddingTop();for(let i=0;i<t.length;i+=1){const s=t[i],r=s.classList.contains("active"),n=s.getBoundingClientRect().bottom<e-2;!r&&n&&AmLyrics.unfinishSyllables(s)}}getLineIndexAtTime(t,e=0){if(!this.lyrics||0===this.lyrics.length)return-1;const i=this.lyrics.length,s=Math.max(0,Math.min(e,i-1));for(let e=s;e<i;e+=1){const i=this.lyrics[e];if(i.timestamp>t)break;if(t>=i.timestamp&&t<i.endtime)return e}for(let e=s-1;e>=0;e-=1){const i=this.lyrics[e];if(t>=i.timestamp&&t<i.endtime)return e;if(i.endtime<t)break}for(let e=0;e<i;e+=1){const i=this.lyrics[e];if(i.timestamp>t)break;if(t>=i.timestamp&&t<i.endtime)return e}return-1}findActiveLineIndices(t){if(!this.lyrics||0===this.lyrics.length)return[];const e=[];for(let i=0;i<this.lyrics.length;i+=1){const s=this.lyrics[i];if(s.timestamp>t)break;t>=s.timestamp&&t<s.endtime&&e.push(i)}return e}findInstrumentalGapAt(t){if(!this.lyrics||0===this.lyrics.length)return null;const e=this.lyrics[0];if(t>=0&&t<e.timestamp){const t=0,i=e.timestamp;return i-t>=7e3?{insertBeforeIndex:0,gapStart:t,gapEnd:i}:null}for(let e=0;e<this.lyrics.length-1;e+=1){const i=this.lyrics[e],s=this.lyrics[e+1],r=i.endtime,n=s.timestamp;if(t>r&&t<n)return n-r>=7e3?{insertBeforeIndex:e+1,gapStart:r,gapEnd:n}:null}return null}findAllInstrumentalGaps(){if(this.cachedAllGaps.length>0)return this.cachedAllGaps;if(!this.lyrics||0===this.lyrics.length)return[];const t=[],e=this.lyrics[0];e.timestamp>=7e3&&t.push({insertBeforeIndex:0,gapStart:0,gapEnd:e.timestamp});for(let e=0;e<this.lyrics.length-1;e+=1){const i=this.lyrics[e],s=this.lyrics[e+1],r=i.endtime,n=s.timestamp;n-r>=7e3&&t.push({insertBeforeIndex:e+1,gapStart:r,gapEnd:n})}return this.cachedAllGaps=t,t}startAnimationFromTime(t){if(this.animationFrameId&&(cancelAnimationFrame(this.animationFrameId),this.animationFrameId=void 0),!this.lyrics)return;const e=this.findActiveLineIndices(t);if(AmLyrics.arraysEqual(e,this.activeLineIndices)||(this.activeLineIndices=e),this.activeMainWordIndices.clear(),this.activeBackgroundWordIndices.clear(),this.mainWordAnimations.clear(),this.backgroundWordAnimations.clear(),this.mainWordProgress.clear(),this.backgroundWordProgress.clear(),0!==e.length){for(const i of e){const e=this.lyrics[i];let s=-1;for(let i=0;i<e.text.length;i+=1)if(t>=e.text[i].timestamp&&t<=e.text[i].endtime){s=i;break}this.activeMainWordIndices.set(i,s);let r=-1;if(e.backgroundText)for(let i=0;i<e.backgroundText.length;i+=1)if(t>=e.backgroundText[i].timestamp&&t<=e.backgroundText[i].endtime){r=i;break}this.activeBackgroundWordIndices.set(i,r)}this.setupAnimations(),this.interpolate&&this.animateProgress()}}updateActiveLineAndWords(){if(!this.lyrics)return;const t=this.findActiveLineIndices(this.currentTime);AmLyrics.arraysEqual(t,this.activeLineIndices)||(this.activeLineIndices=t),this.activeMainWordIndices.clear(),this.activeBackgroundWordIndices.clear();for(const e of t){const t=this.lyrics[e];let i=-1;for(let e=0;e<t.text.length;e+=1)if(this.currentTime>=t.text[e].timestamp&&this.currentTime<=t.text[e].endtime){i=e;break}this.activeMainWordIndices.set(e,i);let s=-1;if(t.backgroundText)for(let e=0;e<t.backgroundText.length;e+=1)if(this.currentTime>=t.backgroundText[e].timestamp&&this.currentTime<=t.backgroundText[e].endtime){s=e;break}this.activeBackgroundWordIndices.set(e,s)}}setupAnimations(){if(0===this.activeLineIndices.length||!this.lyrics)return this.mainWordAnimations.clear(),void this.backgroundWordAnimations.clear();for(const t of this.activeLineIndices){const e=this.lyrics[t],i=this.activeMainWordIndices.get(t)??-1,s=this.activeBackgroundWordIndices.get(t)??-1;if(-1!==i){const s=e.text[i],r=s.endtime-s.timestamp,n=this.currentTime-s.timestamp;this.mainWordAnimations.set(t,{startTime:performance.now()-n,duration:r})}else this.mainWordAnimations.set(t,{startTime:0,duration:0});if(-1!==s&&e.backgroundText){const i=e.backgroundText[s],r=i.endtime-i.timestamp,n=this.currentTime-i.timestamp;this.backgroundWordAnimations.set(t,{startTime:performance.now()-n,duration:r})}else this.backgroundWordAnimations.set(t,{startTime:0,duration:0})}}handleLineClick(t){if(this.lyricsContainer){this.lyricsContainer.querySelectorAll(".lyrics-line").forEach(t=>{AmLyrics.resetSyllables(t),t.classList.remove("scroll-animate"),t.style.removeProperty("--scroll-delta"),t.style.removeProperty("--lyrics-line-delay")}),this.lyricsContainer.classList.remove("wheel-scrolling")}this.scrollAnimationState&&(this.scrollAnimationState.isAnimating=!1,this.scrollAnimationState.pendingUpdate=null),this.scrollAnimationTimeout&&(clearTimeout(this.scrollAnimationTimeout),this.scrollAnimationTimeout=void 0),this.userScrollTimeoutId&&(clearTimeout(this.userScrollTimeoutId),this.userScrollTimeoutId=void 0),this.setUserScrolling(!1),this.currentPrimaryActiveLine=null,this.lastPrimaryActiveLine=null,this.activeLineIds.clear(),this.animatingLines=[];const e=this.lyricsContainer?.querySelector(`.lyrics-line[data-start-time="${t.text[0]?.timestamp||0}"]`);e&&this.lyricsContainer&&(this.currentPrimaryActiveLine=e,this.currentScrollOffset=-this.lyricsContainer.scrollTop,this.isClickSeeking=!0,this.clickSeekTimeout&&clearTimeout(this.clickSeekTimeout),this.clickSeekTimeout=setTimeout(()=>{this.isClickSeeking=!1},800),this.scrollToActiveLineYouLy(e,!0));const i=new CustomEvent("line-click",{detail:{timestamp:t.timestamp},bubbles:!0,composed:!0});this.dispatchEvent(i)}static getBackgroundTextPlacement(t){if(!t.backgroundText||0===t.backgroundText.length||0===t.text.length)return"after";const e=t.text[0].timestamp;return t.backgroundText[0].timestamp<e?"before":"after"}scrollToActiveLine(){if(!this.lyricsContainer||0===this.activeLineIndices.length)return;const t=Math.min(...this.activeLineIndices),e=this.lyricsContainer.querySelector(`.lyrics-line:nth-child(${t+1})`);if(e){const t=this.lyricsContainer.clientHeight,i=e.offsetTop,s=e.clientHeight,r=e.querySelector(".background-text.before");let n=0;if(r){n=r.clientHeight/2}const a=i-t/2+s/2-n;requestAnimationFrame(()=>{this.isProgrammaticScroll=!0,this.lyricsContainer?.scrollTo({top:a,behavior:"smooth"}),setTimeout(()=>{this.isProgrammaticScroll=!1},100)})}}scrollToInstrumental(t){if(!this.lyricsContainer)return;const e=this.lyricsContainer.querySelector(`#gap-${t}`);if(e){const t=this.getScrollPaddingTop()-e.offsetTop;this.isProgrammaticScroll=!0,this.clearPastLineHighlights(),this.animateScrollYouLy(t,!1),setTimeout(()=>{this.isProgrammaticScroll=!1},250)}}getScrollPaddingTop(){if(null!==this.cachedScrollPaddingTop)return this.cachedScrollPaddingTop;if(!this.lyricsContainer)return 0;const t=getComputedStyle(this).getPropertyValue("--lyrics-scroll-padding-top")||"25%";let e;return e=t.includes("%")?this.lyricsContainer.clientHeight*(parseFloat(t)/100):parseFloat(t)||0,this.cachedScrollPaddingTop=e,e}animateScrollYouLy(t,e=!1,i=void 0){if(!this.lyricsContainer)return;const s=this.lyricsContainer,r=Math.max(0,-t);this.scrollAnimationState||(this.scrollAnimationState={isAnimating:!1,pendingUpdate:null},this.animatingLines=[]);const n=this.scrollAnimationState;if(n.isAnimating&&!e){const e=null===n.pendingUpdate?null:Math.max(0,-n.pendingUpdate);if(Math.abs(s.scrollTop-r)<2||null!==e&&Math.abs(e-r)<2)return;return void(n.pendingUpdate=t)}this.scrollAnimationTimeout&&(clearTimeout(this.scrollAnimationTimeout),this.scrollAnimationTimeout=void 0),this.scrollUnlockTimeout&&(clearTimeout(this.scrollUnlockTimeout),this.scrollUnlockTimeout=void 0);const{animatingLines:a}=this,o=-r,l=-s.scrollTop-o;if(this.currentScrollOffset=o,Math.abs(s.scrollTop-r)<1&&Math.abs(l)<1)return n.isAnimating=!1,void(n.pendingUpdate=null);if(e){for(const t of a)t.classList.remove("scroll-animate"),t.style.removeProperty("--scroll-delta"),t.style.removeProperty("--lyrics-line-delay"),t.style.removeProperty("--scroll-duration");return a.length=0,s.scrollTo({top:r,behavior:"smooth"}),n.isAnimating=!1,void(n.pendingUpdate=null)}for(const t of a)t.classList.remove("scroll-animate"),t.style.removeProperty("--scroll-delta"),t.style.removeProperty("--lyrics-line-delay"),t.style.removeProperty("--scroll-duration");if(a.length=0,0===this.cachedLineArray.length){const t=this.lyricsContainer.querySelectorAll(".lyrics-line");this.cachedLineArray=Array.from(t)}const c=this.cachedLineArray,h=this.currentPrimaryActiveLine||this.lastPrimaryActiveLine||c[0];if(!h)return;const d=c.indexOf(h);if(-1===d)return;const p=Math.min(450,i??350),m=.1*p,u=c.length,y=Math.max(0,d-20),g=Math.min(u,d+20);let f=0;const v=[];if(l>=0){let t=0;for(let e=y;e<g;e+=1){const i=c[e],s=e>=d?t*m:0;e>=d&&!i.classList.contains("lyrics-gap")&&(t+=1),i.style.setProperty("--scroll-delta",`${l}px`),i.style.setProperty("--lyrics-line-delay",`${s}ms`),i.style.setProperty("--scroll-duration",`${p+100}ms`),v.push(i);const r=p+s;r>f&&(f=r)}}else{let t=0;for(let e=g-1;e>=y;e-=1){const i=c[e],s=e<=d?t*m:0;e<=d&&!i.classList.contains("lyrics-gap")&&(t+=1),i.style.setProperty("--scroll-delta",`${l}px`),i.style.setProperty("--lyrics-line-delay",`${s}ms`),i.style.setProperty("--scroll-duration",`${p+100}ms`),v.push(i);const r=p+s;r>f&&(f=r)}}s.offsetHeight;for(const t of v)t.classList.add("scroll-animate"),a.push(t);n.isAnimating=!0;this.scrollUnlockTimeout=setTimeout(()=>{if(n.isAnimating=!1,null!==n.pendingUpdate){const t=n.pendingUpdate;n.pendingUpdate=null,this.animateScrollYouLy(t,!1,i)}},400),this.scrollAnimationTimeout=setTimeout(()=>{for(let t=0;t<a.length;t+=1){const e=a[t];e.classList.remove("scroll-animate"),e.style.removeProperty("--scroll-delta"),e.style.removeProperty("--lyrics-line-delay"),e.style.removeProperty("--scroll-duration")}a.length=0,this.scrollAnimationTimeout=void 0},f+50),s.scrollTo({top:r,behavior:"instant"})}updatePositionClasses(t){if(!this.lyricsContainer)return;const e=["lyrics-activest","post-active-line","next-active-line","prev-1","prev-2","prev-3","prev-4","next-1","next-2","next-3","next-4"];for(const t of this.positionedLineElements)t.classList.remove(...e);this.positionedLineElements=[],t.classList.add("lyrics-activest"),this.positionedLineElements.push(t),0===this.cachedLineArray.length&&(this.cachedLineArray=Array.from(this.lyricsContainer.querySelectorAll(".lyrics-line")));const i=this.cachedLineArray,s=i.indexOf(t);if(-1!==s)for(let t=Math.max(0,s-4);t<=Math.min(i.length-1,s+4);t+=1){const e=t-s;if(0!==e){const s=i[t];-1===e?s.classList.add("post-active-line"):1===e?s.classList.add("next-active-line"):e<0?s.classList.add(`prev-${Math.abs(e)}`):s.classList.add(`next-${e}`),this.positionedLineElements.push(s)}}}scrollToActiveLineYouLy(t,e=!1,i=void 0){if(!t||!this.lyricsContainer)return;const s=this.getScrollPaddingTop(),r=s-t.offsetTop,n=this.lyricsContainer.getBoundingClientRect().top;if(!e&&Math.abs(t.getBoundingClientRect().top-n-s)<1)return;if(!e&&!t.classList.contains("lyrics-footer")){const e=this.lyricsContainer,i=e.scrollTop+e.clientHeight>=e.scrollHeight-50,r=Math.max(0,-(s-t.offsetTop));if(i&&r>e.scrollTop-50)return}this.lyricsContainer.classList.remove("not-focused","user-scrolling"),this.isProgrammaticScroll=!0,this.setUserScrolling(!1),this.userScrollTimeoutId&&(clearTimeout(this.userScrollTimeoutId),this.userScrollTimeoutId=void 0),this.clearPastLineHighlights();setTimeout(()=>{this.isProgrammaticScroll=!1},(i??350)+160),this.animateScrollYouLy(r,e,i)}static updateSyllableAnimation(t,e=0){if(t.classList.contains("highlight"))return;const{classList:i}=t,s=i.contains("rtl-text"),r=Array.from(t.querySelectorAll("span.char")),n=t.parentElement?.parentElement,a=n?.dataset.virtualWordId;let o=[];a&&n?.parentElement?o=Array.from(n.parentElement.querySelectorAll(".lyrics-word")).filter(t=>t.dataset.virtualWordId===a):n&&(o=[n]);const l=o.flatMap(t=>Array.from(t.querySelectorAll("span.char"))),c=n?.classList.contains("growable"),h=n?.classList.contains("char-rise"),d="0"===t.getAttribute("data-syllable-index"),p=parseFloat(t.getAttribute("data-start-time")||"0"),m=parseFloat(n?.dataset.virtualWordStart||""),u=d&&(!Number.isFinite(m)||Math.abs(p-m)<.5),y=d,g=null!==t.closest(".lyrics-gap"),f=parseFloat(t.getAttribute("data-duration")||"0")||300,v=parseFloat(t.getAttribute("data-word-duration")||t.getAttribute("data-duration")||"0")||f,b=new Map,x=[];if(c&&u&&l.length>0){const t=.09*v,e=1.5*v;l.forEach(i=>{const s=i.dataset.matrixScale||"1.1",r=i.dataset.charOffsetX||"0",n=i.dataset.shadowIntensity||"0.6",a=i.dataset.translateYPeak||"-2",o=parseFloat(i.dataset.syllableCharIndex||"0"),l=t*o;b.set(i,`grow-dynamic ${e}ms ease-in-out ${l}ms forwards`),x.push({element:i,property:"--matrix-scale",value:s}),x.push({element:i,property:"--char-offset-x",value:`${r}px`}),x.push({element:i,property:"--shadow-intensity",value:n}),x.push({element:i,property:"--translate-y-peak",value:`${a}px`})})}if(h&&u&&l.length>0){const t=Math.max(v,f),e=.09*t,i=1.5*t;l.forEach(t=>{const s=parseFloat(t.dataset.syllableCharIndex||"0"),r=e*s;b.set(t,`rise-char ${i}ms ease-in-out ${r}ms forwards`)})}if(r.length>0)r.forEach((t,i)=>{const r=parseFloat(t.dataset.wipeStart||"0"),n=parseFloat(t.dataset.wipeDuration||"0"),a=f*r-e,o=f*n;let l="wipe";l=y&&0===i?s?"start-wipe-rtl":"start-wipe":s?"wipe-rtl":"wipe";const c=b.get(t)||t.style.animation||"",h=[];if(c&&(c.includes("grow-dynamic")||c.includes("rise-char"))&&h.push(c.split(",")[0].trim()),i>0&&a>0&&o>0){const i=(t.dataset.preWipeArrival?parseFloat(t.dataset.preWipeArrival):f*r)-e,s=parseFloat(t.dataset.preWipeDuration||"100"),n=Math.min(s,.9*o,.08*f,i),a=i-n;n>=16&&h.push(`pre-wipe-char ${n}ms linear ${a}ms none`)}o>0&&h.push(`${l} ${o}ms linear ${a}ms forwards`),h.length>0&&b.set(t,h.join(", "))});else{const i=parseFloat(t.getAttribute("data-wipe-ratio")||"1"),r=f*i;let n="wipe";if(n=y?s?"start-wipe-rtl":"start-wipe":s?"wipe-rtl":"wipe",t.classList.contains("line-synced"))return;const a=g?"fade-gap":n;t.style.animation=`${a} ${r}ms ${g?"ease-out":"linear"} ${-e}ms forwards`}i.remove("pre-highlight"),i.add("highlight");for(const[t,e]of b.entries())t.style.willChange="transform",t.style.animation=e;for(const t of x)t.element.style.setProperty(t.property,t.value)}static resetSyllable(t){if(!t)return;t.style.animation="",t.style.removeProperty("--pre-wipe-duration"),t.style.removeProperty("--pre-wipe-delay"),t.style.transition="none",t.style.backgroundColor="var(--lyplus-text-secondary)";const e=t.querySelectorAll("span.char");for(let t=0;t<e.length;t+=1){const i=e[t];i.style.animation="",i.style.transition="none",i.style.backgroundColor="var(--lyplus-text-secondary)"}t.classList.remove("highlight","finished","pre-highlight","cleanup")}static resetSyllables(t){if(!t)return;t.classList.remove("persist-highlight"),t._cachedSyllableElements=null;const e=t.getElementsByClassName("lyrics-syllable");for(let t=0;t<e.length;t+=1)AmLyrics.resetSyllable(e[t]);requestAnimationFrame(()=>{for(let t=0;t<e.length;t+=1){const i=e[t];i.style.removeProperty("background-color"),i.style.removeProperty("transition");const s=i.querySelectorAll("span.char");for(let t=0;t<s.length;t+=1){const e=s[t];e.style.removeProperty("background-color"),e.style.removeProperty("transition"),e.style.removeProperty("will-change")}}})}static unfinishSyllables(t){if(!t)return;t.classList.remove("persist-highlight");const e=t.getElementsByClassName("lyrics-syllable");for(let t=0;t<e.length;t+=1){const i=e[t];i.classList.remove("highlight","finished","pre-highlight","cleanup"),i.style.animation="",i.style.removeProperty("--pre-wipe-duration"),i.style.removeProperty("--pre-wipe-delay"),i.style.removeProperty("background-color"),i.style.removeProperty("transition");const s=i.querySelectorAll("span.char");for(let t=0;t<s.length;t+=1){const e=s[t];e.style.animation="",e.style.removeProperty("will-change"),e.style.removeProperty("background-color"),e.style.removeProperty("transition"),e.style.removeProperty("filter")}}}static finishSyllablesUpToTime(t,e){if(!t)return;let i=!1,s=t._cachedSyllableElements;if(!s){s=Array.from(t.querySelectorAll(".lyrics-syllable"));for(let t=0;t<s.length;t+=1){const e=s[t];e._cachedStartTime=parseFloat(e.getAttribute("data-start-time")||"0"),e._cachedEndTime=parseFloat(e.getAttribute("data-end-time")||"0")}t._cachedSyllableElements=s}for(let t=0;t<s.length;t+=1){const r=s[t],n=r._cachedStartTime;if(Number.isFinite(n)&&e>=n){const{classList:t}=r;t.contains("finished")||(t.contains("highlight")||AmLyrics.updateSyllableAnimation(r,Math.max(0,e-n)),t.add("finished")),i=!0,t.remove("highlight"),t.remove("pre-highlight"),t.add("cleanup"),r.style.animation="",r.style.removeProperty("--pre-wipe-duration"),r.style.removeProperty("--pre-wipe-delay");const s=r.querySelectorAll("span.char");for(let t=0;t<s.length;t+=1){const e=s[t],i=e.style.animation||"";if(i.includes("grow-dynamic")||i.includes("rise-char")){const t=i.split(",").map(t=>t.trim()),s=t.find(t=>t.includes("grow-dynamic")||t.includes("rise-char"));e.style.animation=s||""}else e.style.animation=""}}}i?t.classList.add("persist-highlight"):t.classList.remove("persist-highlight")}static updateSyllablesForLine(t,e){let i=t._cachedSyllableElements;if(!i){i=Array.from(t.querySelectorAll(".lyrics-syllable"));for(let t=0;t<i.length;t+=1){const e=i[t];e._cachedStartTime=parseFloat(e.getAttribute("data-start-time")||"0"),e._cachedEndTime=parseFloat(e.getAttribute("data-end-time")||"0")}t._cachedSyllableElements=i}for(let t=0;t<i.length;t+=1){const s=i[t],r=s._cachedStartTime,n=s._cachedEndTime;if(Number.isFinite(r)&&Number.isFinite(n)){const{classList:a}=s,o=a.contains("highlight"),l=a.contains("finished"),c=a.contains("pre-highlight");if(!(e<r-1e3)||(o||l||c)){let h=!1;if(c&&t>0){i[t-1].classList.contains("highlight")||(a.remove("pre-highlight"),s.style.removeProperty("--pre-wipe-duration"),s.style.removeProperty("--pre-wipe-delay"),s.style.animation="",h=!0)}h||(e>=r&&e<=n?(o||AmLyrics.updateSyllableAnimation(s,e-r),l&&a.remove("finished")):e>n?l||(o||AmLyrics.updateSyllableAnimation(s,e-r),a.add("finished")):(o||l)&&AmLyrics.resetSyllable(s))}}}}animateProgress(){const t=performance.now();let e=!1;if(this.lyrics&&0!==this.activeLineIndices.length){for(const i of this.activeLineIndices){const s=this.lyrics[i],r=this.mainWordAnimations.get(i);if(r&&r.duration>0){const n=t-r.startTime;if(n>=0){const t=Math.min(1,n/r.duration);if(this.mainWordProgress.set(i,t),t<1)e=!0;else{const t=this.activeMainWordIndices.get(i)??-1,r=t+1;if(-1!==t&&r<s.text.length){const n=s.text[t],a=s.text[r];this.activeMainWordIndices.set(i,r);const o=a.timestamp-n.endtime,l=a.endtime-a.timestamp;this.mainWordAnimations.set(i,{startTime:performance.now()+o,duration:l}),e=!0}else this.mainWordAnimations.set(i,{startTime:0,duration:0})}}else this.mainWordProgress.set(i,0),e=!0}const n=this.backgroundWordAnimations.get(i);if(n&&n.duration>0){const r=t-n.startTime;if(r>=0){const t=Math.min(1,r/n.duration);if(this.backgroundWordProgress.set(i,t),t<1)e=!0;else{const t=this.activeBackgroundWordIndices.get(i)??-1;if(s.backgroundText&&-1!==t&&t<s.backgroundText.length-1){const r=t+1,n=s.backgroundText[t],a=s.backgroundText[r];this.activeBackgroundWordIndices.set(i,r);const o=a.timestamp-n.endtime,l=a.endtime-a.timestamp;this.backgroundWordAnimations.set(i,{startTime:performance.now()+o,duration:l}),e=!0}else this.backgroundWordAnimations.set(i,{startTime:0,duration:0})}}else this.backgroundWordProgress.set(i,0),e=!0}}e?this.animationFrameId=requestAnimationFrame(this._boundAnimateProgress):this.animationFrameId&&(cancelAnimationFrame(this.animationFrameId),this.animationFrameId=void 0)}else this.animationFrameId&&(cancelAnimationFrame(this.animationFrameId),this.animationFrameId=void 0)}generateLRC(){if(!this.lyrics)return"";let t="";this.songTitle&&(t+=`[ti:${this.songTitle}]\n`),this.songArtist&&(t+=`[ar:${this.songArtist}]\n`),this.songAlbum&&(t+=`[al:${this.songAlbum}]\n`),this.lyricsSource&&(t+=`[re:${this.lyricsSource}]\n`);for(const e of this.lyrics)if(e.text&&e.text.length>0){const i=AmLyrics.formatTimestampLRC(e.timestamp),s=e.text.map(t=>t.text).join("").trim();t+=`[${i}]${s}\n`}return t}generateTTML(){if(!this.lyrics)return"";let t,e='<?xml version="1.0" encoding="UTF-8"?>\n';e+='<tt xmlns="http://www.w3.org/ns/ttml" xmlns:itunes="http://music.apple.com/lyrics">\n',e+="  <body>\n";for(let i=0;i<this.lyrics.length;i+=1){const s=this.lyrics[i],r=s.songPart;r===t&&0!==i||(i>0&&(e+="    </div>\n"),t=r,e+=t?`    <div itunes:song-part="${t}">\n`:"    <div>\n");e+=`      <p begin="${AmLyrics.formatTimestampTTML(s.timestamp)}" end="${AmLyrics.formatTimestampTTML(s.endtime)}">\n`;for(const t of s.text){e+=`        <span begin="${AmLyrics.formatTimestampTTML(t.timestamp)}" end="${AmLyrics.formatTimestampTTML(t.endtime)}">${t.text.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}</span>\n`}e+="      </p>\n"}return this.lyrics.length>0&&(e+="    </div>\n"),e+="  </body>\n",e+="</tt>",e}static formatTimestampLRC(t){const e=t/1e3,i=Math.floor(e/60),s=Math.floor(e%60),r=Math.floor(t%1e3/10),n=t=>t.toString().padStart(2,"0");return`${n(i)}:${n(s)}.${n(r)}`}static formatTimestampTTML(t){const e=t/1e3,i=Math.floor(e/3600),s=Math.floor(e%3600/60),r=Math.floor(e%60),n=Math.floor(t%1e3),a=(t,e=2)=>t.toString().padStart(e,"0");return`${a(i)}:${a(s)}:${a(r)}.${a(n,3)}`}downloadLyrics(){if(!this.lyrics||0===this.lyrics.length)return;const t=this.lyrics.some(t=>!1!==t.isWordSynced);let e="",i=this.downloadFormat;"auto"===i&&(i=t?"ttml":"lrc");let s="";if("ttml"===i?(e=this.generateTTML(),s="application/xml"):(e=this.generateLRC(),s="text/plain"),!e)return;const r=new Blob([e],{type:s}),n=URL.createObjectURL(r),a=document.createElement("a");a.href=n;const o=this.songTitle?`${this.songTitle}${this.songArtist?` - ${this.songArtist}`:""}.${i}`:`lyrics.${i}`;a.download=o,document.body.appendChild(a),a.click(),document.body.removeChild(a),URL.revokeObjectURL(n)}render(){this.fontFamily&&(this.style.fontFamily=this.fontFamily),this.style.setProperty("--highlight-color",this.highlightColor);const t=this.lyricsSource??"Unavailable",e=this.cachedIsUnsynced;return b`
      <div
        class="lyrics-container ${e?"is-unsynced":"blur-inactive-enabled"}"
      >
        ${!this.isLoading&&this.lyrics&&this.lyrics.length>0?b`
              <div class="lyrics-header">
                <div class="header-controls">
                  <button
                    class="download-button ${this.showRomanization?"active":""}"
                    @click=${this.toggleRomanization}
                    title="Toggle Romanization"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="lucide lucide-speech-icon lucide-speech"
                    >
                      <path
                        d="M8.8 20v-4.1l1.9.2a2.3 2.3 0 0 0 2.164-2.1V8.3A5.37 5.37 0 0 0 2 8.25c0 2.8.656 3.054 1 4.55a5.77 5.77 0 0 1 .029 2.758L2 20"
                      />
                      <path d="M19.8 17.8a7.5 7.5 0 0 0 .003-10.603" />
                      <path d="M17 15a3.5 3.5 0 0 0-.025-4.975" />
                    </svg>
                  </button>
                  <button
                    class="download-button ${this.showTranslation?"active":""}"
                    @click=${this.toggleTranslation}
                    title="Toggle Translation"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="lucide lucide-languages-icon lucide-languages"
                    >
                      <path d="m5 8 6 6" />
                      <path d="m4 14 6-6 2-3" />
                      <path d="M2 5h12" />
                      <path d="M7 2h1" />
                      <path d="m22 22-5-10-5 10" />
                      <path d="M14 18h6" />
                    </svg>
                  </button>
                </div>
                <div class="download-controls">
                  <select
                    class="format-select"
                    @change=${t=>{this.downloadFormat=t.target.value}}
                    .value=${this.downloadFormat}
                    @click=${t=>t.stopPropagation()}
                  >
                    <option value="auto">Auto</option>
                    <option value="lrc">LRC</option>
                    <option value="ttml">TTML</option>
                  </select>
                  <button
                    class="download-button"
                    @click=${this.downloadLyrics}
                    title="Download Lyrics"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="lucide lucide-download-icon lucide-download"
                    >
                      <path d="M12 15V3" />
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <path d="m7 10 5 5 5-5" />
                    </svg>
                  </button>
                </div>
              </div>
            `:""}
        ${(()=>{if(this.isLoading)return b`
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
        `;if(!this.lyrics||0===this.lyrics.length)return b`<div class="no-lyrics">No lyrics found.</div>`;const t=this.findAllInstrumentalGaps(),e=new Map(t.map(t=>[t.insertBeforeIndex,t]));return this.lyrics.map((t,i)=>{const s=`lyrics-line-${i}`,r=t.text[0]?.timestamp||0,n=t.text[t.text.length-1]?.endtime||0,a=t.backgroundText&&t.backgroundText.length>0,o=a?b`<p class="background-vocal-container">
              <span class="background-vocal-wrap">
                ${t.backgroundText.map((t,e)=>{const i=t.timestamp,s=t.endtime,r=s-i,n=this.showRomanization&&t.romanizedText&&t.romanizedText.trim()!==t.text.trim()?b`<span
                          class="lyrics-syllable transliteration no-chars ${t.lineSynced?"line-synced":""}"
                          data-start-time="${i}"
                          data-end-time="${s}"
                          data-duration="${r}"
                          data-syllable-index="0"
                          data-wipe-ratio="1"
                          >${t.romanizedText}</span
                        >`:"";return b`<span class="lyrics-word"
                    ><span
                      class="lyrics-syllable-wrap${n?" has-transliteration":""}"
                      ><span
                        class="lyrics-syllable no-chars${t.lineSynced?" line-synced":""}"
                        data-start-time="${i}"
                        data-end-time="${s}"
                        data-duration="${r}"
                        data-syllable-index="${e}"
                        data-wipe-ratio="1"
                        >${t.text}</span
                      >${n}</span
                    ></span
                  >`})}
              </span>
            </p>`:"",l=a?AmLyrics.getBackgroundTextPlacement(t):"after",c=this.cachedLineData?.[i],h=c?.wordGroups??[],d=c?.groupGrowable??[],p=c?.groupGlowing??[],m=c?.groupCharRise??[],u=c?.vwFullText??[],y=c?.vwFullDuration??[],g=c?.vwCharOffset??[],f=c?.vwStartMs??[],v=c?.vwEndMs??[],x=c?.lineIsRTL??!1,A=b`<p
          class="main-vocal-container ${x?"rtl-text":""}"
        >
          ${h.map((t,e)=>{const s=d[e],r=p[e],n=m[e],a=s||n,o=t.some(t=>t.lineSynced),l=a?u[e]:"",c=a?y[e]:0,h=l.length,x=a?g[e]:0,A=a?`${i}:${f[e]}:${v[e]}`:"",L=a?f[e]:"",w=a?v[e]:"";let $=0;const S=t.map(t=>t.text).join(""),T=S.trim().length>=16||/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]/.test(S),k=t[0].timestamp,_=t[t.length-1].endtime-k,E=Math.max(1.2,Math.min(2.5,1.2+_/1e3*.6));return b`<span
              class="lyrics-word${s?" growable":""}${n?" char-rise":""}${r?" glowing":""}${T?" allow-break":""}"
              data-virtual-word-id="${A}"
              data-virtual-word-start="${L}"
              data-virtual-word-end="${w}"
              style="--rise-duration: ${E}s"
              >${t.map((t,e)=>{const i=t.timestamp,s=t.endtime,n=s-i,l=t.text||"",d=this.showRomanization&&t.romanizedText&&t.romanizedText.trim()!==t.text.trim()?b`<span
                        class="lyrics-syllable transliteration no-chars ${o?"line-synced":""}"
                        data-start-time="${i}"
                        data-end-time="${s}"
                        data-duration="${n}"
                        data-syllable-index="0"
                        data-wipe-ratio="1"
                        >${t.romanizedText}</span
                      >`:"";let p=l;if(a){let t=0;const e=l.replace(/\s/g,"").length||1;p=b`${l.split("").map(i=>{if(" "===i)return" ";const s=x+$,a=t/e;$+=1,t+=1;const o=Math.min(1,Math.max(0,(c-400)/2600))**3,l=h>5,d=c<1200;let p=0;if(l||d){let t=0;l&&(t+=.4*Math.min((h-5)/5,1)),d&&h>3?t+=.3*Math.max(0,1-(c-800)/400):d&&h<=3&&(t+=.1*Math.max(0,1-(c-800)/400)),p=Math.min(t,.7)}const m=o*(1-(h>1?s/(h-1):0)*p),u=1+(h<=3?.05:.04)+.08*m,y=Math.min(1.1,c/1500);let g=1;h<=3?g=.85:h>=6&&(g=1.1);const f=r?(.35+.45*m)*(y*g):0,v=(u-1)/.1,A=(c+2*n)/3,L=2*Math.min(1,Math.max(.3,A/2e3))*-v,w=2*((s+.5)/h-.5)*(25*(u-1));return b`<span
                      class="char"
                      data-char-index="${s}"
                      data-syllable-char-index="${s}"
                      data-wipe-start="${a.toFixed(4)}"
                      data-wipe-duration="${(1/e).toFixed(4)}"
                      data-horizontal-offset="${w.toFixed(2)}"
                      data-max-scale="${u.toFixed(3)}"
                      data-matrix-scale="${(.98*u).toFixed(3)}"
                      data-char-offset-x="${(.98*w).toFixed(2)}"
                      data-shadow-intensity="${f.toFixed(3)}"
                      data-translate-y-peak="${L.toFixed(3)}"
                      >${i}</span
                    >`})}`}return b`<span
                  class="lyrics-syllable-wrap${d?" has-transliteration":""}"
                  ><span
                    class="lyrics-syllable${o?" line-synced":""}${a?" has-chars":" no-chars"}"
                    data-start-time="${i}"
                    data-end-time="${s}"
                    data-duration="${n}"
                    data-word-duration="${c}"
                    data-syllable-index="${e}"
                    data-wipe-ratio="1"
                    >${p}</span
                  >${d}</span
                >`})}</span
            >`})}
        </p>`,L=t.text.map(t=>t.text).join("").trim(),w=this.showTranslation&&t.translation&&t.translation.trim()!==L?b`<div class="lyrics-translation-container">
                ${t.translation}
              </div>`:"",$=this.showRomanization&&t.romanizedText&&!t.text.some(t=>t.romanizedText)&&t.romanizedText.trim()!==L?b`<div
                class="lyrics-romanization-container ${x?"rtl-text":""}"
              >
                ${t.romanizedText}
              </div>`:"";let S=null;const T=e.get(i);if(T){const t=T.gapEnd-T.gapStart,e=t/3,s=AmLyrics.getGapLoopDelay(t);S=b`<div
            id="gap-${i}"
            class="lyrics-line lyrics-gap"
            data-start-time="${T.gapStart}"
            data-end-time="${T.gapEnd}"
            style="--gap-pulse-duration: ${4e3}ms; --gap-loop-delay: -${s}ms; --gap-exit-duration: ${600}ms; --gap-exit-scale: ${.85};"
          >
            <p class="main-vocal-container">
              <span class="lyrics-word"
                ><span class="lyrics-syllable-wrap"
                  ><span
                    class="lyrics-syllable"
                    data-start-time="${T.gapStart}"
                    data-end-time="${T.gapStart+e}"
                    data-duration="${e}"
                    data-wipe-ratio="1"
                    data-syllable-index="0"
                  ></span></span
                ><span class="lyrics-syllable-wrap"
                  ><span
                    class="lyrics-syllable"
                    data-start-time="${T.gapStart+e}"
                    data-end-time="${T.gapStart+2*e}"
                    data-duration="${e}"
                    data-wipe-ratio="1"
                    data-syllable-index="1"
                  ></span></span
                ><span class="lyrics-syllable-wrap"
                  ><span
                    class="lyrics-syllable"
                    data-start-time="${T.gapStart+2*e}"
                    data-end-time="${T.gapEnd}"
                    data-duration="${e}"
                    data-wipe-ratio="1"
                    data-syllable-index="2"
                  ></span></span
              ></span>
            </p>
          </div>`}return b`
          ${S}
          <div
            id="${s}"
            class="lyrics-line ${"end"===t.alignment?"singer-right":"singer-left"} ${x?"rtl-text":""}"
            data-start-time="${r}"
            data-end-time="${n}"
            @click=${()=>this.handleLineClick(t)}
            tabindex="0"
            @keydown=${e=>{"Enter"!==e.key&&" "!==e.key||this.handleLineClick(t)}}
          >
            <div class="lyrics-line-container ${x?"rtl-text":""}">
              ${"before"===l?o:""}
              ${A}
              ${"after"===l?o:""}
              ${$} ${w}
            </div>
          </div>
        `})})()}
        ${this.isLoading?"":b`
              <footer class="lyrics-footer lyrics-line">
                <div class="footer-content">
                  <span
                    class="source-info"
                    style="display: flex; align-items: center; gap: 8px;"
                  >
                    <b style="font-weight: 750;">Source</b> ${t}
                    ${this.availableSources&&this.availableSources.length>1||!this.hasFetchedAllProviders?b`
                          <button
                            class="download-button source-switch-btn"
                            title="Switch Lyrics Source"
                            style="font-family: inherit; font-size: 11px; padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(255, 255, 255, 0.2); background: transparent; cursor: pointer; color: #aaa; display: inline-flex; align-items: center;"
                            @click=${this.switchSource}
                            ?disabled=${this.isFetchingAlternatives}
                          >
                            <svg
                              class="source-switch-svg lucide lucide-arrow-down-up-icon lucide-arrow-down-up"
                              style="margin-right: 4px;"
                              xmlns="http://www.w3.org/2000/svg"
                              width="12"
                              height="12"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              stroke-width="2"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            >
                              ${this.isFetchingAlternatives?w`<path
                                    d="M21 12a9 9 0 1 1-6.219-8.56"
                                  ></path>`:w`<path d="m3 16 4 4 4-4"></path
                                    ><path d="M7 20V4"></path
                                    ><path d="m21 8-4-4-4 4"></path
                                    ><path d="M17 4v16"></path>`}
                            </svg>
                            <span class="source-switch-label"
                              >${this.isFetchingAlternatives?"Switching...":"Switch"}</span
                            >
                          </button>
                        `:""}
                  </span>
                  ${this.songwriters?b`<span
                        class="songwriters-info"
                        style="margin-top: 4px; font-weight: normal; font-size: 0.9em;"
                      >
                        <b style="font-weight: 750;">Songwriters</b> ${this.songwriters}
                      </span>`:""}
                  <span class="version-info"></span>
                </div>
              </footer>
            `}
      </div>
    `}}AmLyrics.styles=i$3`
    /* ==========================================================================
       APPLE STYLE STYLING - Design Tokens & Variables
       ========================================================================== */
    :host {
      --lyplus-lyrics-palette: var(
        --am-lyrics-highlight-color,
        var(--highlight-color, #ffffff)
      );
      --lyplus-text-primary: var(--lyplus-lyrics-palette);
      /* Use color-mix with the text color rather than just opacity so it adapts */
      --lyplus-text-secondary: color-mix(
        in srgb,
        var(--lyplus-lyrics-palette),
        transparent 45%
      );

      --lyplus-padding-base: 1em;
      --lyplus-padding-line: 10px;
      --lyplus-padding-gap: 0.3em;
      --lyplus-border-radius-base: 0.6em;
      --lyplus-gap-dot-size: 0.4em;
      --lyplus-gap-dot-margin: 0.08em;

      --lyplus-font-size-base: 32px;
      --lyplus-font-size-base-grow: 24.5;
      --lyplus-font-size-subtext: 0.6em;
      --char-rise-y: calc(-0.035 * var(--lyplus-font-size-base));

      --lyplus-blur-amount: 0.07em;
      --lyplus-blur-amount-near: 0.035em;
      --lyplus-fade-gap-timing-function: ease-out;

      --lyrics-scroll-padding-top: 25%;

      display: block;
      font-family:
        -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
        Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      background: transparent;
      height: 100%;
      overflow: hidden;
      font-weight: bold;
      color: var(--lyplus-text-primary);
    }

    /* ==========================================================================
       CONTAINER & SCROLL BEHAVIOR
       ========================================================================== */
    .lyrics-container {
      padding: 20px;
      padding-top: 80px;
      border-radius: 8px;
      background-color: transparent;
      width: 100%;
      height: 100%;
      max-height: 100vh;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      box-sizing: border-box;
      scrollbar-width: none;
      overflow-anchor: none;
    }

    .lyrics-container::-webkit-scrollbar {
      display: none;
    }

    /* Disable transitions during touch-scrolling for 1:1 feedback */
    .lyrics-container.touch-scrolling .lyrics-line,
    .lyrics-container.touch-scrolling .lyrics-plus-metadata {
      transition: none !important;
      filter: none !important;
    }

    /* Apply smooth gliding transition for mouse-wheel scrolling */
    .lyrics-container.wheel-scrolling .lyrics-line {
      transition: transform 0.3s ease-out !important;
      filter: none !important;
    }

    .lyrics-line.scroll-animate {
      /* Preserve the graceful fade duration; the keyframe handles the
         transform, so we only need to keep opacity/filter transitions
         alive without !important overriding the base rule. */
      transition:
        opacity 0.7s ease,
        filter 0.7s ease,
        transform 0.4s cubic-bezier(0.41, 0, 0.12, 0.99)
          var(--lyrics-line-delay, 0ms);
      animation-name: lyrics-scroll;
      animation-duration: var(--scroll-duration, 400ms);
      animation-timing-function: cubic-bezier(0.41, 0, 0.12, 0.99);
      animation-fill-mode: both;
      animation-delay: var(--lyrics-line-delay, 0ms);
    }

    .lyrics-container.user-scrolling .lyrics-line {
      --lyrics-line-delay: 0ms !important;
      transition-delay: 0ms !important;
    }

    /* ==========================================================================
       LYRICS LINE BASE STYLES
       ========================================================================== */
    .lyrics-line {
      padding: var(--lyplus-padding-line);
      opacity: 0.8;
      color: var(--lyplus-text-secondary);
      font-size: var(--lyplus-font-size-base);
      cursor: pointer;
      transform-origin: left;
      /* Graceful 0.7 s fade so the line stays mostly bright while the
         0.4 s scroll animation runs, then settles into the inactive state. */
      transition:
        opacity 0.7s ease,
        transform 0.4s cubic-bezier(0.41, 0, 0.12, 0.99)
          var(--lyrics-line-delay, 0ms),
        filter 0.7s ease;
      content-visibility: auto;
      contain: layout style;
      text-rendering: optimizeLegibility;
    }

    .lyrics-line:not(.scroll-animate) {
      animation: none;
    }

    /* --- Line Container & Vocal Containers --- */
    .lyrics-line-container {
      overflow-wrap: break-word;
      transform-origin: left;
      transform: translateZ(0);
      transition:
        transform 0.7s ease,
        background-color 0.7s,
        color 0.7s;
    }

    .lyrics-line.active .lyrics-line-container,
    .lyrics-line.pre-active .lyrics-line-container {
      transform: translateZ(0);
      transition:
        transform 0.5s ease,
        background-color 0.18s,
        color 0.18s;
    }

    .main-vocal-container {
      transform-origin: 5% 50%;
      margin: 0;
    }

    .background-vocal-container {
      max-height: 0;
      overflow: hidden;
      opacity: 0;
      font-size: var(--lyplus-font-size-subtext);
      line-height: 1.15;
      color: color-mix(in srgb, var(--lyplus-text-secondary) 80%, transparent);
      transition:
        max-height var(--scroll-duration, 400ms)
          cubic-bezier(0.41, 0, 0.12, 0.99),
        opacity var(--scroll-duration, 400ms) cubic-bezier(0.41, 0, 0.12, 0.99);
      margin: 0;
      pointer-events: none;
    }

    .background-vocal-wrap {
      display: block;
      padding-top: 0;
      padding-bottom: 0;
      transition: padding-top var(--scroll-duration, 400ms)
        cubic-bezier(0.41, 0, 0.12, 0.99);
    }

    .lyrics-line.singer-right .background-vocal-container,
    .lyrics-line.rtl-text .background-vocal-container {
      margin-left: auto;
      margin-right: 0;
    }

    /* Background vocals expand only when .bg-expanded is present.
       This is separate from .active so bg vocals can collapse immediately
       while .active stays to keep text white until the scroll passes. */
    .lyrics-line.bg-expanded .background-vocal-container {
      max-height: 4em;
      opacity: 1;
      will-change: max-height, opacity;
    }

    .lyrics-line.bg-expanded .background-vocal-wrap {
      padding-top: 0.26em;
    }

    /* --- Line States & Modifiers --- */
    .lyrics-line.active {
      opacity: 1;
      color: var(--lyplus-text-primary);
    }

    .lyrics-line.pre-active {
      opacity: 1;
    }

    .lyrics-line.persist-highlight {
      filter: none !important;
      opacity: 1;
    }

    .lyrics-line.persist-highlight .lyrics-syllable.finished,
    .lyrics-line.persist-highlight .lyrics-syllable.finished span.char {
      transition: none !important;
    }

    .lyrics-line.singer-right {
      text-align: end;
    }

    .lyrics-line.singer-right .lyrics-line-container,
    .lyrics-line.singer-right .main-vocal-container {
      transform-origin: right;
    }

    .lyrics-line.rtl-text {
      direction: rtl;
      text-align: right !important;
      transform-origin: right;
    }

    .lyrics-line.rtl-text .lyrics-line-container,
    .lyrics-line.rtl-text .main-vocal-container {
      transform-origin: right;
    }

    .lyrics-line.rtl-text .lyrics-romanization-container,
    .lyrics-line.rtl-text .lyrics-translation-container {
      text-align: right;
    }

    /* --- Unsynced (Plain Text) Lyrics Overrides --- */
    .lyrics-container.is-unsynced .lyrics-line {
      opacity: 1 !important;
      color: var(--lyplus-text-primary) !important;
      filter: none !important;
      transform: none !important;
      cursor: default;
    }

    .lyrics-container.is-unsynced .lyrics-line-container {
      transform: none !important;
      background-color: transparent !important;
    }

    .lyrics-container.is-unsynced .lyrics-syllable {
      color: var(--lyplus-text-primary) !important;
      background-color: transparent !important;
      -webkit-background-clip: unset !important;
      background-clip: unset !important;
      -webkit-text-fill-color: unset !important;
      text-fill-color: unset !important;
      text-shadow: none !important;
      filter: none !important;
      opacity: 1 !important;
      transform: none !important;
    }

    @media (hover: hover) and (pointer: fine) {
      .lyrics-line:hover {
        filter: none !important;
        opacity: 1 !important;
      }
      .lyrics-container.is-unsynced .lyrics-line:hover {
        background: transparent !important;
      }
    }

    /* --- Blur Effect for Inactive Lines --- */
    .lyrics-container.blur-inactive-enabled:not(.not-focused)
      .lyrics-line:not(.active):not(.pre-active):not(.lyrics-gap):not(
        .persist-highlight
      ) {
      filter: blur(var(--lyplus-blur-amount));
    }

    /* Viewport Virtualization: Strip expensive filters and animations from
       offscreen lines.  IntersectionObserver toggles this class. */
    .lyrics-line.far-line {
      filter: none !important;
      will-change: auto !important;
      animation: none !important;
    }

    .lyrics-container.blur-inactive-enabled:not(.not-focused)
      .lyrics-line.post-active-line:not(.lyrics-gap):not(.active):not(
        .pre-active
      ):not(.persist-highlight),
    .lyrics-container.blur-inactive-enabled:not(.not-focused)
      .lyrics-line.next-active-line:not(.lyrics-gap):not(.active):not(
        .pre-active
      ):not(.persist-highlight),
    .lyrics-container.blur-inactive-enabled:not(.not-focused)
      .lyrics-line.lyrics-activest:not(.active):not(.lyrics-gap):not(
        .pre-active
      ):not(.persist-highlight) {
      filter: blur(var(--lyplus-blur-amount-near));
    }

    /* Unblur all lines when user is scrolling */
    .lyrics-container.user-scrolling .lyrics-line {
      transition: none !important;
      filter: none !important;
      opacity: 0.8 !important;
    }

    /* Unblur early for pre-active lines */
    .lyrics-container.blur-inactive-enabled .lyrics-line.pre-active {
      filter: blur(0px) !important;
      opacity: 1;
    }

    /* ==========================================================================
       WORD & SYLLABLE STYLES
       ========================================================================== */
    .lyrics-word:not(.allow-break) {
      display: inline-block;
      vertical-align: baseline;
      white-space: nowrap;
    }

    .lyrics-word.allow-break {
      display: inline;
    }

    .lyrics-word.char-rise {
      display: inline-block;
      vertical-align: baseline;
      white-space: nowrap;
    }

    .lyrics-word.char-rise.allow-break {
      display: inline;
      white-space: normal;
    }

    .lyrics-syllable-wrap {
      display: inline;
    }

    .lyrics-syllable-wrap.has-transliteration {
      display: inline-flex;
      flex-direction: column;
      align-items: start;
    }

    .lyrics-syllable {
      display: inline-block;
      vertical-align: baseline;
      color: transparent;
      background-color: var(--lyplus-text-secondary);
      white-space: pre-wrap;
      font-variant-ligatures: none;
      font-feature-settings: 'liga' 0;
      background-clip: text;
      -webkit-background-clip: text;
      transition:
        color 0.7s,
        background-color 0.7s,
        transform 0.7s ease;
    }

    /* --- Syllable States --- */
    .lyrics-syllable.finished {
      background-color: var(--lyplus-text-primary);
      /* Unified transition: transform keeps its 1s glow decay, while
         background-color and color fade at 0.7s so everything dims
         together when the line becomes inactive. */
      transition:
        transform 1s ease,
        background-color 0.7s ease,
        color 0.7s ease;
    }

    .lyrics-syllable.finished.has-chars {
      background-color: transparent;
    }

    .lyrics-line.active:not(.lyrics-gap) .lyrics-syllable {
      transition:
        transform 1s ease,
        background-color 0.5s,
        color 0.5s;
    }

    /* --- Wipe Highlight Effect --- */
    .lyrics-line.active:not(.lyrics-gap) .lyrics-syllable.highlight.no-chars,
    .lyrics-line.active:not(.lyrics-gap)
      .lyrics-syllable.pre-highlight.no-chars {
      background-repeat: no-repeat;
      background-image:
        linear-gradient(
          90deg,
          #ffffff00 0%,
          var(--lyplus-text-primary, #fff) 50%,
          #0000 100%
        ),
        linear-gradient(
          90deg,
          var(--lyplus-text-primary, #fff) 100%,
          #0000 100%
        );
      background-size:
        0.5em 100%,
        0% 100%;
      background-position:
        -0.5em 0%,
        -0.25em 0%;
    }

    .lyrics-line.active:not(.lyrics-gap) .lyrics-syllable.highlight.rtl-text,
    .lyrics-line.active:not(.lyrics-gap)
      .lyrics-syllable.pre-highlight.rtl-text {
      direction: rtl;
      background-image:
        linear-gradient(
          -90deg,
          var(--lyplus-text-primary) 0%,
          transparent 100%
        ),
        linear-gradient(
          -90deg,
          var(--lyplus-text-primary) 100%,
          transparent 100%
        );
      background-position:
        calc(100% + 0.5em) 0%,
        right 0%;
    }

    /* Background vocals: muted gray wipe instead of white.
       Must match specificity of the main .active .highlight rule (0,3,1). */
    .lyrics-line.active
      .background-vocal-container
      .lyrics-syllable.highlight.no-chars,
    .lyrics-line.active
      .background-vocal-container
      .lyrics-syllable.pre-highlight.no-chars,
    .lyrics-line.pre-active
      .background-vocal-container
      .lyrics-syllable.highlight.no-chars,
    .lyrics-line.pre-active
      .background-vocal-container
      .lyrics-syllable.pre-highlight.no-chars {
      background-image:
        linear-gradient(
          90deg,
          #ffffff00 0%,
          color-mix(in srgb, var(--lyplus-text-primary, #fff) 50%, #888888) 50%,
          #0000 100%
        ),
        linear-gradient(
          90deg,
          color-mix(in srgb, var(--lyplus-text-primary, #fff) 50%, #888888) 100%,
          #0000 100%
        );
    }

    .lyrics-line.active
      .background-vocal-container
      .lyrics-syllable.highlight.rtl-text,
    .lyrics-line.active
      .background-vocal-container
      .lyrics-syllable.pre-highlight.rtl-text,
    .lyrics-line.pre-active
      .background-vocal-container
      .lyrics-syllable.highlight.rtl-text,
    .lyrics-line.pre-active
      .background-vocal-container
      .lyrics-syllable.pre-highlight.rtl-text {
      background-image:
        linear-gradient(
          -90deg,
          color-mix(in srgb, var(--lyplus-text-primary) 50%, #888888) 0%,
          transparent 100%
        ),
        linear-gradient(
          -90deg,
          color-mix(in srgb, var(--lyplus-text-primary) 50%, #888888) 100%,
          transparent 100%
        );
    }

    /* Non-growable words float up with a gentle curve */
    .lyrics-line.active:not(.lyrics-gap)
      .lyrics-word:not(.growable)
      .lyrics-syllable.highlight {
      transform: translate3d(0, var(--char-rise-y, -1.12px), 0);
    }

    .lyrics-line.persist-highlight:not(.lyrics-gap)
      .lyrics-word:not(.growable)
      .lyrics-syllable.finished {
      transform: translate3d(0, var(--char-rise-y, -1.12px), 0);
    }

    .lyrics-word.growable .lyrics-syllable.cleanup .char {
      transform: translate3d(0, var(--char-rise-y, -1.12px), 0);
    }

    .lyrics-word.char-rise .lyrics-syllable.cleanup .char {
      transform: translate3d(0, var(--char-rise-y, -1.12px), 0);
    }

    .lyrics-line.persist-highlight
      .lyrics-word.growable
      .lyrics-syllable.finished
      .char,
    .lyrics-line.persist-highlight
      .lyrics-word.char-rise
      .lyrics-syllable.finished
      .char {
      transform: translate3d(0, var(--char-rise-y, -1.12px), 0);
    }

    /* Background vocal overrides — placed AFTER main rules so they win
       on equal specificity. */
    .background-vocal-container .lyrics-syllable {
      background-color: color-mix(
        in srgb,
        var(--lyplus-text-secondary) 50%,
        #888888
      );
    }

    .lyrics-line.active:not(.lyrics-gap)
      .background-vocal-container
      .lyrics-syllable.finished,
    .lyrics-line.pre-active
      .background-vocal-container
      .lyrics-syllable.finished {
      background-color: color-mix(
        in srgb,
        var(--lyplus-text-primary) 50%,
        #888888
      );
    }

    .background-vocal-container .lyrics-syllable.line-synced {
      color: color-mix(
        in srgb,
        var(--lyplus-text-secondary) 50%,
        #888888
      ) !important;
    }

    .lyrics-line.active:not(.lyrics-gap)
      .background-vocal-container
      .lyrics-syllable.line-synced,
    .lyrics-line.pre-active
      .background-vocal-container
      .lyrics-syllable.line-synced {
      color: color-mix(
        in srgb,
        var(--lyplus-text-primary) 50%,
        #888888
      ) !important;
    }

    .lyrics-line.active:not(.lyrics-gap)
      .background-vocal-container
      .lyrics-syllable.line-synced.finished,
    .lyrics-line.pre-active
      .background-vocal-container
      .lyrics-syllable.line-synced.finished {
      color: color-mix(
        in srgb,
        var(--lyplus-text-primary) 50%,
        #888888
      ) !important;
    }

    .lyrics-syllable.pre-highlight {
      animation-name: pre-wipe-universal;
      animation-duration: var(--pre-wipe-duration);
      animation-delay: var(--pre-wipe-delay);
      animation-timing-function: linear;
      animation-fill-mode: forwards;
    }

    .lyrics-syllable.pre-highlight.rtl-text {
      animation-name: pre-wipe-universal-rtl;
    }

    .lyrics-syllable.transliteration {
      font-size: var(--lyplus-font-size-subtext);
      white-space: pre-wrap;
      pointer-events: none;
      user-select: none;
    }

    /* Syllable with chars: make syllable transparent, chars handle color */
    .lyrics-line .lyrics-syllable.has-chars:not(.finished) {
      background-color: transparent;
      color: transparent;
    }

    .lyrics-syllable span.char {
      display: inline-block;
      background-color: var(--lyplus-text-secondary);
      white-space: break-spaces;
      font-variant-ligatures: none;
      font-feature-settings: 'liga' 0;
      background-clip: text;
      -webkit-background-clip: text;
      backface-visibility: hidden;
      transform-origin: 50% 80%;
      transition:
        color 0.7s,
        background-color 0.7s,
        transform 0.7s ease;
    }

    .lyrics-syllable.finished span.char {
      background-color: var(--lyplus-text-primary);
      transition:
        color 0.7s,
        background-color 0.7s,
        transform 0.7s ease;
    }

    /* Active char spans: structural only, wipe animation sets gradient */
    .lyrics-line.active .lyrics-syllable span.char {
      background-clip: text;
      -webkit-background-clip: text;
      background-repeat: no-repeat;
      background-image:
        linear-gradient(
          90deg,
          #ffffff00 0%,
          var(--lyplus-text-primary, #fff) 50%,
          #0000 100%
        ),
        linear-gradient(
          90deg,
          var(--lyplus-text-primary, #fff) 100%,
          #0000 100%
        );
      background-size:
        0.5em 100%,
        0% 100%;
      background-position:
        -0.5em 0%,
        -0.25em 0%;
      transition:
        transform 0.7s ease,
        color 0.18s;
    }

    .lyrics-line.active .lyrics-syllable span.char.highlight {
      background-image:
        linear-gradient(
          -90deg,
          var(--lyplus-text-primary, #fff) 0%,
          #0000 100%
        ),
        linear-gradient(
          -90deg,
          var(--lyplus-text-primary, #fff) 100%,
          #0000 100%
        );
      background-position:
        calc(100% + 0.5em) 0%,
        calc(100% + 0.25em) 0%;
    }

    .lyrics-line.active .lyrics-syllable.pre-highlight span.char {
      background-image:
        linear-gradient(
          90deg,
          #ffffff00 0%,
          var(--lyplus-text-primary, #fff) 50%,
          #0000 100%
        ),
        linear-gradient(
          90deg,
          var(--lyplus-text-primary, #fff) 100%,
          #0000 100%
        );
      background-size:
        0.75em 100%,
        0% 100%;
      background-position:
        -0.85em 0%,
        -0.25em 0%;
    }

    /* ==========================================================================
       INSTRUMENTAL GAP STYLES
       ========================================================================== */
    .lyrics-gap {
      max-height: 1.6em;
      padding: var(--lyplus-padding-gap);
      overflow: visible;
      opacity: 0;
      box-sizing: content-box;
      background-clip: unset;
      transform-origin: top;
      content-visibility: visible !important;
      contain: none !important;
      transition:
        opacity 160ms ease-out,
        transform var(--scroll-duration, 280ms) var(--lyrics-line-delay, 0ms);
    }

    .lyrics-gap.active {
      opacity: 1;
      transition:
        opacity 160ms ease-out,
        transform var(--scroll-duration, 280ms);
    }

    /* Exiting state: quickly collapse width and height so dots don't distort page, or remove max-height transition */
    .lyrics-gap.gap-exiting {
      opacity: 1;
    }

    .lyrics-gap .main-vocal-container {
      transform: translateY(-25%) scale(1);
      transition: transform 400ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    .lyrics-gap:not(.active):not(.gap-exiting) .main-vocal-container {
      transform: translateY(-25%) scale(0);
    }

    /* Pulse — must come BEFORE .gap-exiting so exiting wins via specificity+order */
    .lyrics-gap.active .main-vocal-container {
      animation: gap-loop var(--gap-pulse-duration, 4000ms) ease-in-out infinite
        alternate;
      animation-delay: var(--gap-loop-delay, 0ms);
    }

    /* Jump animation plays during exit — disable transition so animation wins.
       Placed AFTER .active so it wins when both classes are present briefly. */
    .lyrics-gap.gap-exiting .main-vocal-container {
      animation: gap-ended var(--gap-exit-duration, 360ms)
        cubic-bezier(0.33, 1, 0.68, 1) forwards;
      transition: none !important;
    }

    .lyrics-gap .lyrics-syllable {
      display: inline-block;
      width: var(--lyplus-gap-dot-size);
      height: var(--lyplus-gap-dot-size);
      background-color: var(--lyplus-text-primary);
      border-radius: 50%;
      margin: 0 var(--lyplus-gap-dot-margin);
    }

    /* Line-synced lyrics should fade in instantly/quickly instead of wiping */
    .lyrics-syllable.line-synced {
      background: transparent !important;
      color: var(--lyplus-text-secondary) !important;
    }

    .lyrics-line.active .lyrics-syllable.line-synced {
      animation: fade-in-line 0.2s ease-out forwards !important;
      color: var(--lyplus-text-primary) !important;
    }

    .lyrics-line.pre-active .lyrics-syllable.line-synced {
      animation: fade-in-line 0.14s ease-out forwards !important;
      color: var(--lyplus-text-primary) !important;
    }

    .lyrics-line.active .lyrics-syllable.line-synced span.char,
    .lyrics-line.pre-active .lyrics-syllable.line-synced span.char {
      background-image: none !important;
      background-color: var(--lyplus-text-primary) !important;
      transition: background-color 120ms ease-out !important;
    }

    @keyframes fade-in-line {
      from {
        opacity: 0.5;
        color: var(--lyplus-text-secondary);
      }
      to {
        opacity: 1;
        color: var(--lyplus-lyrics-palette);
      }
    }

    .lyrics-gap .lyrics-syllable {
      background-color: var(--lyplus-text-secondary);
      background-clip: unset;
    }

    .lyrics-gap.active .lyrics-syllable.finished,
    .lyrics-gap.gap-exiting .lyrics-syllable.finished,
    .lyrics-gap:not(.active):not(.gap-exiting).post-active-line
      .lyrics-syllable,
    .lyrics-gap:not(.active):not(.gap-exiting).lyrics-activest
      .lyrics-syllable {
      background-color: var(--lyplus-text-primary);
      animation: none !important;
      opacity: 1;
    }

    /* ==========================================================================
       METADATA & FOOTER STYLES
       ========================================================================== */
    .lyrics-plus-metadata {
      display: block;
      position: relative;
      box-sizing: border-box;
      font-weight: normal;
      transform: translateY(var(--lyrics-scroll-offset, 0px));
      transition:
        opacity 0.3s ease,
        transform 0.6s cubic-bezier(0.23, 1, 0.32, 1)
          var(--lyrics-line-delay, 0ms),
        filter 0.3s ease;
    }

    .lyrics-plus-empty {
      display: block;
      height: 100vh;
      transform: translateY(var(--lyrics-scroll-offset, 0px));
    }

    .lyrics-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      text-align: left;
      font-size: calc(var(--lyplus-font-size-base) * 0.5);
      color: var(--lyplus-text-secondary);
      padding: 20px 0 50vh 0;
      margin-top: 10px;
      font-weight: 400;
      opacity: 0.8;
      transition:
        opacity 0.3s ease,
        transform 0.5s cubic-bezier(0.41, 0, 0.12, 0.99),
        filter 0.3s ease;
      transform-origin: left;
    }

    .lyrics-footer.lyrics-line {
      font-size: calc(var(--lyplus-font-size-base) * 0.5);
      padding: 20px var(--lyplus-padding-line) 50vh var(--lyplus-padding-line);
      margin-top: 0;
    }

    .lyrics-footer.active {
      opacity: 1;
      color: rgba(255, 255, 255, 0.5); /* Grey instead of primary */
    }

    .lyrics-footer.scroll-animate {
      transition: none !important;
      animation-name: lyrics-scroll;
      animation-duration: var(--scroll-duration, 280ms);
      animation-timing-function: cubic-bezier(0.41, 0, 0.12, 0.99);
      animation-fill-mode: both;
      animation-delay: var(--lyrics-line-delay, 0ms);
    }

    .lyrics-container.blur-inactive-enabled:not(.not-focused)
      .lyrics-footer:not(.active) {
      filter: blur(var(--lyplus-blur-amount));
      opacity: 0.5;
    }

    .lyrics-container.user-scrolling .lyrics-footer {
      transition: none !important;
      filter: none !important;
      opacity: 0.8 !important;
    }

    .lyrics-footer p {
      margin: 5px 0;
    }

    .lyrics-footer a {
      color: var(--lyplus-text-primary); /* Stand out using primary color */
      text-underline-offset: 2px;
      opacity: 0.8;
      transition: opacity 0.2s;
    }

    .lyrics-footer a:hover {
      opacity: 1;
    }

    .footer-content {
      display: flex;
      align-items: flex-start;
      flex-direction: column;
      gap: 8px;
    }

    .footer-controls {
      display: flex;
      align-items: center;
    }

    /* ==========================================================================
       HEADER & CONTROLS
       ========================================================================== */
    .lyrics-header {
      display: flex;
      padding: 10px 0;
      margin-bottom: 10px;
      gap: 10px;
      justify-content: space-between;
      align-items: center;
    }

    .lyrics-header .download-button {
      background: none;
      border: none;
      cursor: pointer;
      color: #aaa;
      padding: 0;
      margin-left: 10px;
      vertical-align: middle;
      display: inline-flex;
      align-items: center;
      font-family: inherit;
    }

    .lyrics-header .download-button:hover {
      color: rgba(255, 255, 255, 0.9);
    }

    .header-controls {
      display: flex;
      gap: 8px;
    }

    .download-controls {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .control-button {
      background: transparent;
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 4px;
      padding: 2px 8px;
      font-size: 0.8em;
      color: rgba(255, 255, 255, 0.6);
      cursor: pointer;
      transition: all 0.2s;
      font-weight: normal;
    }

    .control-button:hover {
      color: rgba(255, 255, 255, 0.9);
      border-color: rgba(255, 255, 255, 0.5);
    }

    .control-button.active {
      background-color: var(--lyplus-text-primary);
      border-color: var(--lyplus-text-primary);
      color: #000;
    }

    .format-select {
      background: transparent;
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 4px;
      color: rgba(255, 255, 255, 0.6);
      font-size: 0.8em;
      margin-left: 10px;
      padding: 2px 5px;
      cursor: pointer;
      font-weight: normal;
      font-family: inherit;
    }

    .format-select:hover {
      color: rgba(255, 255, 255, 0.9);
      border-color: rgba(255, 255, 255, 0.5);
    }

    .format-select option {
      background: #1a1a1a;
      color: #fff;
    }

    /* ==========================================================================
       TRANSLATION & ROMANIZATION
       ========================================================================== */
    .lyrics-translation-container,
    .lyrics-romanization-container {
      padding-top: 0.2em;
      opacity: 0.8;
      font-size: var(--lyplus-font-size-subtext);
      overflow-wrap: break-word;
      pointer-events: none;
      user-select: none;
      transition:
        opacity 0.3s ease,
        color 0.3s;
      font-weight: normal;
    }

    .lyrics-romanization-container {
      direction: ltr !important;
    }

    .lyrics-romanization-container.rtl-text {
      direction: rtl !important;
      text-align: right;
    }

    .lyrics-romanization-container .lyrics-syllable {
      white-space: pre-wrap;
    }

    .lyrics-translation-container {
      opacity: 0.5;
    }

    .main-line-wrapper.small {
      font-size: 0.5em;
      opacity: 0.8;
      display: block;
      margin-bottom: 0px;
    }

    .translation-line {
      font-size: 1em;
      font-weight: bold;
      display: block;
      margin-top: 0px;
      line-height: 1.1;
    }

    .romanized-line {
      font-size: 0.5em;
      color: rgba(255, 255, 255, 0.5);
      display: block;
      margin-top: 2px;
      font-weight: normal;
    }

    /* ==========================================================================
       SKELETON LOADING
       ========================================================================== */
    @keyframes skeleton-loading {
      0% {
        background-color: rgba(255, 255, 255, 0.1);
      }
      100% {
        background-color: rgba(255, 255, 255, 0.2);
      }
    }

    .skeleton-line {
      height: 2.5em;
      margin: 20px 0;
      border-radius: 8px;
      animation: skeleton-loading 1s linear infinite alternate;
      opacity: 0.7;
      width: 60%;
    }

    .skeleton-line:nth-child(even) {
      width: 80%;
    }
    .skeleton-line:nth-child(3n) {
      width: 50%;
    }
    .skeleton-line:nth-child(5n) {
      width: 70%;
    }

    .no-lyrics {
      color: rgba(255, 255, 255, 0.5);
      font-size: 1.2em;
      text-align: center;
      padding: 2em;
      font-weight: normal;
    }

    /* ==========================================================================
       KEYFRAME ANIMATIONS
       ========================================================================== */

    /* Wipe animation for syllables */
    @keyframes wipe {
      from {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          -0.375em 0%,
          left;
      }
      to {
        background-size:
          0.75em 100%,
          100% 100%;
        background-position:
          calc(100% + 0.375em) 0%,
          left;
      }
    }

    @keyframes start-wipe {
      0% {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          -0.75em 0%,
          -0.375em 0%;
      }
      100% {
        background-size:
          0.75em 100%,
          100% 100%;
        background-position:
          calc(100% + 0.375em) 0%,
          left;
      }
    }

    @keyframes wipe-rtl {
      from {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          calc(100% + 0.375em) 0%,
          calc(100% + 0.36em) 0%;
      }
      to {
        background-size:
          0.75em 100%,
          100% 100%;
        background-position:
          -0.75em 0%,
          right 0%;
      }
    }

    @keyframes start-wipe-rtl {
      0% {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          calc(100% + 0.75em) 0%,
          calc(100% + 0.5em) 0%;
      }
      100% {
        background-size:
          0.75em 100%,
          100% 100%;
        background-position:
          -0.75em 0%,
          right 0%;
      }
    }

    @keyframes pre-wipe-universal {
      from {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          -0.75em 0%,
          left;
      }
      to {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          -0.375em 0%,
          left;
      }
    }

    @keyframes pre-wipe-universal-rtl {
      from {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          calc(100% + 0.75em) 0%,
          right 0%;
      }
      to {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          calc(100% + 0.375em) 0%,
          right 0%;
      }
    }

    @keyframes pre-wipe-char {
      from {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          -0.75em 0%,
          left;
      }
      to {
        background-size:
          0.75em 100%,
          0% 100%;
        background-position:
          -0.375em 0%,
          left;
      }
    }

    /* Gap dot animations */
    @keyframes gap-loop {
      from {
        transform: translateY(-25%) scale(1.12);
      }
      to {
        transform: translateY(-25%) scale(var(--gap-exit-scale, 0.85));
      }
    }

    @keyframes gap-ended {
      0% {
        transform: translateY(-25%) scale(var(--gap-exit-scale, 0.85));
      }
      35% {
        transform: translateY(-25%) scale(1.2);
      }
      100% {
        transform: translateY(-25%) scale(0);
      }
    }

    @keyframes fade-gap {
      from {
        background-color: var(--lyplus-text-secondary);
      }
      to {
        background-color: var(--lyplus-text-primary);
      }
    }

    /* Scroll animation — class is removed and re-added (with a forced
       reflow in between) to reliably restart the animation each time */
    @keyframes lyrics-scroll {
      from {
        transform: translate3d(0, var(--scroll-delta), 0);
      }
      to {
        transform: translate3d(0, 0, 0);
      }
    }

    /* Character grow animation — translate3d+scale3d for smooth transform,
       drop-shadow for glow */
    @keyframes grow-dynamic {
      0% {
        transform: translate3d(0, 0, 0) scale3d(1, 1, 1);
        filter: drop-shadow(
          0 0 0
            color-mix(in srgb, var(--lyplus-lyrics-palette), transparent 100%)
        );
      }
      25%,
      30% {
        transform: translate3d(
            var(--char-offset-x, 0px),
            var(--translate-y-peak, -2px),
            0
          )
          scale3d(var(--matrix-scale, 1.1), var(--matrix-scale, 1.1), 1);
        filter: drop-shadow(
          0 0 0.1em
            color-mix(
              in srgb,
              var(--lyplus-lyrics-palette),
              transparent calc((1 - var(--shadow-intensity, 1)) * 100%)
            )
        );
      }
      75%,
      100% {
        transform: translate3d(0, var(--char-rise-y, -1.12px), 0)
          scale3d(1, 1, 1);
        filter: drop-shadow(
          0 0 0
            color-mix(in srgb, var(--lyplus-lyrics-palette), transparent 100%)
        );
      }
    }

    @keyframes rise-char {
      0% {
        transform: translate3d(0, 0, 0);
      }
      65%,
      100% {
        transform: translate3d(0, var(--char-rise-y, -1.12px), 0);
      }
    }

    @keyframes grow-static {
      0%,
      100% {
        transform: scale3d(1.01, 1.01, 1.1) translateY(-0.05%);
        text-shadow: 0 0 0
          color-mix(in srgb, var(--lyplus-lyrics-palette), transparent 100%);
      }
      30%,
      40% {
        transform: scale3d(1.1, 1.1, 1.1) translateY(-0.05%);
        text-shadow: 0 0 0.3em
          color-mix(in srgb, var(--lyplus-lyrics-palette), transparent 50%);
      }
    }

    /* Fade in animation */
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 0.7;
        transform: translateY(0);
      }
    }

    /* Legacy support */
    .opposite-turn {
      text-align: right;
    }

    .singer-right {
      text-align: right;
      justify-content: flex-end;
    }

    .singer-left {
      text-align: left;
      justify-content: flex-start;
    }

    /* Legacy progress-text for backward compatibility */
    .progress-text {
      position: relative;
      display: inline-block;
      background: linear-gradient(
        to right,
        var(--lyplus-text-primary) 0%,
        var(--lyplus-text-primary) var(--line-progress, 0%),
        var(--lyplus-text-secondary) var(--line-progress, 0%),
        var(--lyplus-text-secondary) 100%
      );
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      color: var(--lyplus-text-secondary);
      transform: translate3d(0, 0, 0);
      will-change: background-size;
    }

    .progress-text::before {
      display: none;
    }

    .active-line {
      font-weight: bold;
    }

    .background-text {
      display: block;
      color: var(--lyplus-text-secondary);
      font-size: 0.8em;
      font-style: normal;
      margin: 0;
      flex-shrink: 0;
      line-height: 1.1;
    }

    .background-text.before {
      order: -1;
    }

    .background-text.after {
      order: 1;
    }

    .instrumental-line {
      display: inline-flex;
      align-items: baseline;
      gap: 8px;
      color: var(--lyplus-text-secondary);
      font-size: 0.9em;
      padding: 4px 10px;
      animation: fadeInUp 220ms ease;
      font-weight: normal;
    }

    .instrumental-duration {
      color: var(--lyplus-text-secondary);
      font-size: 0.8em;
    }
  `,__decorate([n({type:String})],AmLyrics.prototype,"query",void 0),__decorate([n({type:String})],AmLyrics.prototype,"musicId",void 0),__decorate([n({type:String})],AmLyrics.prototype,"isrc",void 0),__decorate([n({type:String})],AmLyrics.prototype,"ttml",void 0),__decorate([n({type:String,attribute:"song-title"})],AmLyrics.prototype,"songTitle",void 0),__decorate([r()],AmLyrics.prototype,"downloadFormat",void 0),__decorate([n({type:String,attribute:"song-artist"})],AmLyrics.prototype,"songArtist",void 0),__decorate([n({type:String,attribute:"song-album"})],AmLyrics.prototype,"songAlbum",void 0),__decorate([n({type:String,attribute:"songwriters"})],AmLyrics.prototype,"songwriters",void 0),__decorate([n({type:Number,attribute:"song-duration"})],AmLyrics.prototype,"songDurationMs",void 0),__decorate([n({type:String,attribute:"highlight-color"})],AmLyrics.prototype,"highlightColor",void 0),__decorate([n({type:String,attribute:"font-family"})],AmLyrics.prototype,"fontFamily",void 0),__decorate([n({type:Boolean})],AmLyrics.prototype,"autoScroll",void 0),__decorate([n({type:Boolean})],AmLyrics.prototype,"interpolate",void 0),__decorate([r()],AmLyrics.prototype,"showRomanization",void 0),__decorate([r()],AmLyrics.prototype,"showTranslation",void 0),__decorate([n({type:Number})],AmLyrics.prototype,"duration",void 0),__decorate([n({type:Number,attribute:"currenttime",hasChanged:()=>!1})],AmLyrics.prototype,"currentTime",null),__decorate([r()],AmLyrics.prototype,"isLoading",void 0),__decorate([r()],AmLyrics.prototype,"lyrics",void 0),__decorate([r()],AmLyrics.prototype,"lyricsSource",void 0),__decorate([r()],AmLyrics.prototype,"availableSources",void 0),__decorate([r()],AmLyrics.prototype,"currentSourceIndex",void 0),__decorate([e(".lyrics-container")],AmLyrics.prototype,"lyricsContainer",void 0),window.customElements.define("am-lyrics",AmLyrics);
//# sourceMappingURL=/sm/0f8e19231ec5d3fc1ae96e348d364ccf95698d5aa2ad16b6807327143557922d.map