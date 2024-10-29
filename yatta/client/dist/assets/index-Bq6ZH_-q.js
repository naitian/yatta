var Ke=Object.defineProperty;var We=(e,t,s)=>t in e?Ke(e,t,{enumerable:!0,configurable:!0,writable:!0,value:s}):e[t]=s;var Kt=(e,t,s)=>(We(e,typeof t!="symbol"?t+"":t,s),s);(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))n(o);new MutationObserver(o=>{for(const r of o)if(r.type==="childList")for(const l of r.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&n(l)}).observe(document,{childList:!0,subtree:!0});function s(o){const r={};return o.integrity&&(r.integrity=o.integrity),o.referrerPolicy&&(r.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?r.credentials="include":o.crossOrigin==="anonymous"?r.credentials="omit":r.credentials="same-origin",r}function n(o){if(o.ep)return;o.ep=!0;const r=s(o);fetch(o.href,r)}})();function $(){}const ye=e=>e;function vt(e,t){for(const s in t)e[s]=t[s];return e}function ze(e){return!!e&&(typeof e=="object"||typeof e=="function")&&typeof e.then=="function"}function we(e){return e()}function te(){return Object.create(null)}function x(e){e.forEach(we)}function gt(e){return typeof e=="function"}function G(e,t){return e!=e?t==t:e!==t||e&&typeof e=="object"||typeof e=="function"}function qe(e){return Object.keys(e).length===0}function ve(e,...t){if(e==null){for(const n of t)n(void 0);return $}const s=e.subscribe(...t);return s.unsubscribe?()=>s.unsubscribe():s}function ot(e,t,s){e.$$.on_destroy.push(ve(t,s))}function jt(e,t,s,n){if(e){const o=$e(e,t,s,n);return e[0](o)}}function $e(e,t,s,n){return e[1]&&n?vt(s.ctx.slice(),e[1](n(t))):s.ctx}function Dt(e,t,s,n){if(e[2]&&n){const o=e[2](n(s));if(t.dirty===void 0)return o;if(typeof o=="object"){const r=[],l=Math.max(t.dirty.length,o.length);for(let a=0;a<l;a+=1)r[a]=t.dirty[a]|o[a];return r}return t.dirty|o}return t.dirty}function Ht(e,t,s,n,o,r){if(o){const l=$e(t,s,n,r);e.p(l,o)}}function It(e){if(e.ctx.length>32){const t=[],s=e.ctx.length/32;for(let n=0;n<s;n++)t[n]=-1;return t}return-1}function ee(e){const t={};for(const s in e)s[0]!=="$"&&(t[s]=e[s]);return t}function $t(e){return e&&gt(e.destroy)?e.destroy:$}const Ee=typeof window<"u";let Le=Ee?()=>window.performance.now():()=>Date.now(),Xt=Ee?e=>requestAnimationFrame(e):$;const pt=new Set;function Se(e){pt.forEach(t=>{t.c(e)||(pt.delete(t),t.f())}),pt.size!==0&&Xt(Se)}function Oe(e){let t;return pt.size===0&&Xt(Se),{promise:new Promise(s=>{pt.add(t={c:e,f:s})}),abort(){pt.delete(t)}}}function c(e,t){e.appendChild(t)}function Ce(e){if(!e)return document;const t=e.getRootNode?e.getRootNode():e.ownerDocument;return t&&t.host?t:e.ownerDocument}function Be(e){const t=w("style");return t.textContent="/* empty */",Ge(Ce(e),t),t.sheet}function Ge(e,t){return c(e.head||e,t),t.sheet}function I(e,t,s){e.insertBefore(t,s||null)}function M(e){e.parentNode&&e.parentNode.removeChild(e)}function w(e){return document.createElement(e)}function K(e){return document.createTextNode(e)}function N(){return K(" ")}function st(){return K("")}function V(e,t,s,n){return e.addEventListener(t,s,n),()=>e.removeEventListener(t,s,n)}function Ne(e){return function(t){return t.preventDefault(),e.call(this,t)}}function b(e,t,s){s==null?e.removeAttribute(t):e.getAttribute(t)!==s&&e.setAttribute(t,s)}function Fe(e){return Array.from(e.childNodes)}function tt(e,t){t=""+t,e.data!==t&&(e.data=t)}function Y(e,t){e.value=t??""}function Je(e,t,{bubbles:s=!1,cancelable:n=!1}={}){return new CustomEvent(e,{detail:t,bubbles:s,cancelable:n})}function ne(e,t){return new e(t)}const Tt=new Map;let Rt=0;function Ye(e){let t=5381,s=e.length;for(;s--;)t=(t<<5)-t^e.charCodeAt(s);return t>>>0}function Ve(e,t){const s={stylesheet:Be(t),rules:{}};return Tt.set(e,s),s}function Te(e,t,s,n,o,r,l,a=0){const i=16.666/n;let u=`{
`;for(let h=0;h<=1;h+=i){const E=t+(s-t)*r(h);u+=h*100+`%{${l(E,1-E)}}
`}const m=u+`100% {${l(s,1-s)}}
}`,f=`__svelte_${Ye(m)}_${a}`,p=Ce(e),{stylesheet:d,rules:_}=Tt.get(p)||Ve(p,e);_[f]||(_[f]=!0,d.insertRule(`@keyframes ${f} ${m}`,d.cssRules.length));const y=e.style.animation||"";return e.style.animation=`${y?`${y}, `:""}${f} ${n}ms linear ${o}ms 1 both`,Rt+=1,f}function Gt(e,t){const s=(e.style.animation||"").split(", "),n=s.filter(t?r=>r.indexOf(t)<0:r=>r.indexOf("__svelte")===-1),o=s.length-n.length;o&&(e.style.animation=n.join(", "),Rt-=o,Rt||Qe())}function Qe(){Xt(()=>{Rt||(Tt.forEach(e=>{const{ownerNode:t}=e.stylesheet;t&&M(t)}),Tt.clear())})}let Et;function et(e){Et=e}function Ot(){if(!Et)throw new Error("Function called outside component initialization");return Et}function Zt(e){Ot().$$.on_mount.push(e)}function Xe(e){Ot().$$.on_destroy.push(e)}function Wt(e,t){return Ot().$$.context.set(e,t),t}function Ft(e){return Ot().$$.context.get(e)}const dt=[],Lt=[];let _t=[];const Jt=[],Ze=Promise.resolve();let Yt=!1;function xe(){Yt||(Yt=!0,Ze.then(xt))}function ht(e){_t.push(e)}function se(e){Jt.push(e)}const zt=new Set;let ut=0;function xt(){if(ut!==0)return;const e=Et;do{try{for(;ut<dt.length;){const t=dt[ut];ut++,et(t),tn(t.$$)}}catch(t){throw dt.length=0,ut=0,t}for(et(null),dt.length=0,ut=0;Lt.length;)Lt.pop()();for(let t=0;t<_t.length;t+=1){const s=_t[t];zt.has(s)||(zt.add(s),s())}_t.length=0}while(dt.length);for(;Jt.length;)Jt.pop()();Yt=!1,zt.clear(),et(e)}function tn(e){if(e.fragment!==null){e.update(),x(e.before_update);const t=e.dirty;e.dirty=[-1],e.fragment&&e.fragment.p(e.ctx,t),e.after_update.forEach(ht)}}function en(e){const t=[],s=[];_t.forEach(n=>e.indexOf(n)===-1?t.push(n):s.push(n)),s.forEach(n=>n()),_t=t}let yt;function Re(){return yt||(yt=Promise.resolve(),yt.then(()=>{yt=null})),yt}function At(e,t,s){e.dispatchEvent(Je(`${t?"intro":"outro"}${s}`))}const Nt=new Set;let rt;function lt(){rt={r:0,c:[],p:rt}}function it(){rt.r||x(rt.c),rt=rt.p}function C(e,t){e&&e.i&&(Nt.delete(e),e.i(t))}function T(e,t,s,n){if(e&&e.o){if(Nt.has(e))return;Nt.add(e),rt.c.push(()=>{Nt.delete(e),n&&(s&&e.d(1),n())}),e.o(t)}else n&&n()}const Ae={duration:0};function nn(e,t,s){const n={direction:"in"};let o=t(e,s,n),r=!1,l,a,i=0;function u(){l&&Gt(e,l)}function m(){const{delay:p=0,duration:d=300,easing:_=ye,tick:y=$,css:h}=o||Ae;h&&(l=Te(e,0,1,d,p,_,h,i++)),y(0,1);const E=Le()+p,L=E+d;a&&a.abort(),r=!0,ht(()=>At(e,!0,"start")),a=Oe(S=>{if(r){if(S>=L)return y(1,0),At(e,!0,"end"),u(),r=!1;if(S>=E){const R=_((S-E)/d);y(R,1-R)}}return r})}let f=!1;return{start(){f||(f=!0,Gt(e),gt(o)?(o=o(n),Re().then(m)):m())},invalidate(){f=!1},end(){r&&(u(),r=!1)}}}function sn(e,t,s){const n={direction:"out"};let o=t(e,s,n),r=!0,l;const a=rt;a.r+=1;let i;function u(){const{delay:m=0,duration:f=300,easing:p=ye,tick:d=$,css:_}=o||Ae;_&&(l=Te(e,1,0,f,m,p,_));const y=Le()+m,h=y+f;ht(()=>At(e,!1,"start")),"inert"in e&&(i=e.inert,e.inert=!0),Oe(E=>{if(r){if(E>=h)return d(0,1),At(e,!1,"end"),--a.r||x(a.c),!1;if(E>=y){const L=p((E-y)/f);d(1-L,L)}}return r})}return gt(o)?Re().then(()=>{o=o(n),u()}):u(),{end(m){m&&"inert"in e&&(e.inert=i),m&&o.tick&&o.tick(1,0),r&&(l&&Gt(e,l),r=!1)}}}function Pt(e,t){const s=t.token={};function n(o,r,l,a){if(t.token!==s)return;t.resolved=a;let i=t.ctx;l!==void 0&&(i=i.slice(),i[l]=a);const u=o&&(t.current=o)(i);let m=!1;t.block&&(t.blocks?t.blocks.forEach((f,p)=>{p!==r&&f&&(lt(),T(f,1,1,()=>{t.blocks[p]===f&&(t.blocks[p]=null)}),it())}):t.block.d(1),u.c(),C(u,1),u.m(t.mount(),t.anchor),m=!0),t.block=u,t.blocks&&(t.blocks[r]=u),m&&xt()}if(ze(e)){const o=Ot();if(e.then(r=>{et(o),n(t.then,1,t.value,r),et(null)},r=>{if(et(o),n(t.catch,2,t.error,r),et(null),!t.hasCatch)throw r}),t.current!==t.pending)return n(t.pending,0),!0}else{if(t.current!==t.then)return n(t.then,1,t.value,e),!0;t.resolved=e}}function Pe(e,t,s){const n=t.slice(),{resolved:o}=e;e.current===e.then&&(n[e.value]=o),e.current===e.catch&&(n[e.error]=o),e.block.p(n,s)}function oe(e,t){const s={},n={},o={$$scope:1};let r=e.length;for(;r--;){const l=e[r],a=t[r];if(a){for(const i in l)i in a||(n[i]=1);for(const i in a)o[i]||(s[i]=a[i],o[i]=1);e[r]=a}else for(const i in l)o[i]=1}for(const l in n)l in s||(s[l]=void 0);return s}function Ct(e){return typeof e=="object"&&e!==null?e:{}}function re(e,t,s){const n=e.$$.props[t];n!==void 0&&(e.$$.bound[n]=s,s(e.$$.ctx[n]))}function F(e){e&&e.c()}function q(e,t,s){const{fragment:n,after_update:o}=e.$$;n&&n.m(t,s),ht(()=>{const r=e.$$.on_mount.map(we).filter(gt);e.$$.on_destroy?e.$$.on_destroy.push(...r):x(r),e.$$.on_mount=[]}),o.forEach(ht)}function B(e,t){const s=e.$$;s.fragment!==null&&(en(s.after_update),x(s.on_destroy),s.fragment&&s.fragment.d(t),s.on_destroy=s.fragment=null,s.ctx=[])}function on(e,t){e.$$.dirty[0]===-1&&(dt.push(e),xe(),e.$$.dirty.fill(0)),e.$$.dirty[t/31|0]|=1<<t%31}function Q(e,t,s,n,o,r,l=null,a=[-1]){const i=Et;et(e);const u=e.$$={fragment:null,ctx:[],props:r,update:$,not_equal:o,bound:te(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(t.context||(i?i.$$.context:[])),callbacks:te(),dirty:a,skip_bound:!1,root:t.target||i.$$.root};l&&l(u.root);let m=!1;if(u.ctx=s?s(e,t.props||{},(f,p,...d)=>{const _=d.length?d[0]:p;return u.ctx&&o(u.ctx[f],u.ctx[f]=_)&&(!u.skip_bound&&u.bound[f]&&u.bound[f](_),m&&on(e,f)),p}):[],u.update(),m=!0,x(u.before_update),u.fragment=n?n(u.ctx):!1,t.target){if(t.hydrate){const f=Fe(t.target);u.fragment&&u.fragment.l(f),f.forEach(M)}else u.fragment&&u.fragment.c();t.intro&&C(e.$$.fragment),q(e,t.target,t.anchor),xt()}et(i)}class X{constructor(){Kt(this,"$$");Kt(this,"$$set")}$destroy(){B(this,1),this.$destroy=$}$on(t,s){if(!gt(s))return $;const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(s),()=>{const o=n.indexOf(s);o!==-1&&n.splice(o,1)}}$set(t){this.$$set&&!qe(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}const rn="4";typeof window<"u"&&(window.__svelte||(window.__svelte={v:new Set})).v.add(rn);const ct=[];function ln(e,t){return{subscribe:mt(e,t).subscribe}}function mt(e,t=$){let s;const n=new Set;function o(a){if(G(e,a)&&(e=a,s)){const i=!ct.length;for(const u of n)u[1](),ct.push(u,e);if(i){for(let u=0;u<ct.length;u+=2)ct[u][0](ct[u+1]);ct.length=0}}}function r(a){o(a(e))}function l(a,i=$){const u=[a,i];return n.add(u),n.size===1&&(s=t(o,r)||$),a(e),()=>{n.delete(u),n.size===0&&s&&(s(),s=null)}}return{set:o,update:r,subscribe:l}}function an(e,t,s){const n=!Array.isArray(e),o=n?[e]:e;if(!o.every(Boolean))throw new Error("derived() expects stores as input, got a falsy value");const r=t.length<2;return ln(s,(l,a)=>{let i=!1;const u=[];let m=0,f=$;const p=()=>{if(m)return;f();const _=t(n?u[0]:u,l,a);r?l(_):f=gt(_)?_:$},d=o.map((_,y)=>ve(_,h=>{u[y]=h,m&=~(1<<y),i&&p()},()=>{m|=1<<y}));return i=!0,p(),function(){x(d),f(),i=!1}})}const Mt=mt(null),le={},Vt={},un={},Me=/^:(.+)/,ie=4,cn=3,fn=2,dn=1,mn=1,Qt=e=>e.replace(/(^\/+|\/+$)/g,"").split("/"),qt=e=>e.replace(/(^\/+|\/+$)/g,""),pn=(e,t)=>{const s=e.default?0:Qt(e.path).reduce((n,o)=>(n+=ie,o===""?n+=mn:Me.test(o)?n+=fn:o[0]==="*"?n-=ie+dn:n+=cn,n),0);return{route:e,score:s,index:t}},_n=e=>e.map(pn).sort((t,s)=>t.score<s.score?1:t.score>s.score?-1:t.index-s.index),ae=(e,t)=>{let s,n;const[o]=t.split("?"),r=Qt(o),l=r[0]==="",a=_n(e);for(let i=0,u=a.length;i<u;i++){const m=a[i].route;let f=!1;if(m.default){n={route:m,params:{},uri:t};continue}const p=Qt(m.path),d={},_=Math.max(r.length,p.length);let y=0;for(;y<_;y++){const h=p[y],E=r[y];if(h&&h[0]==="*"){const S=h==="*"?"*":h.slice(1);d[S]=r.slice(y).map(decodeURIComponent).join("/");break}if(typeof E>"u"){f=!0;break}const L=Me.exec(h);if(L&&!l){const S=decodeURIComponent(E);d[L[1]]=S}else if(h!==E){f=!0;break}}if(!f){s={route:m,params:d,uri:"/"+r.slice(0,y).join("/")};break}}return s||n||null},ue=(e,t)=>`${qt(t==="/"?e:`${qt(e)}/${qt(t)}`)}/`,hn=e=>!e.defaultPrevented&&e.button===0&&!(e.metaKey||e.altKey||e.ctrlKey||e.shiftKey),gn=e=>{const t=location.host;return e.host===t||e.href.indexOf(`https://${t}`)===0||e.href.indexOf(`http://${t}`)===0},je=()=>typeof window<"u"&&"document"in window&&"location"in window,bn=e=>({params:e&4}),ce=e=>({params:e[2]});function fe(e){let t,s,n,o;const r=[yn,kn],l=[];function a(i,u){return i[0]?0:1}return t=a(e),s=l[t]=r[t](e),{c(){s.c(),n=st()},m(i,u){l[t].m(i,u),I(i,n,u),o=!0},p(i,u){let m=t;t=a(i),t===m?l[t].p(i,u):(lt(),T(l[m],1,1,()=>{l[m]=null}),it(),s=l[t],s?s.p(i,u):(s=l[t]=r[t](i),s.c()),C(s,1),s.m(n.parentNode,n))},i(i){o||(C(s),o=!0)},o(i){T(s),o=!1},d(i){i&&M(n),l[t].d(i)}}}function kn(e){let t;const s=e[8].default,n=jt(s,e,e[7],ce);return{c(){n&&n.c()},m(o,r){n&&n.m(o,r),t=!0},p(o,r){n&&n.p&&(!t||r&132)&&Ht(n,s,o,o[7],t?Dt(s,o[7],r,bn):It(o[7]),ce)},i(o){t||(C(n,o),t=!0)},o(o){T(n,o),t=!1},d(o){n&&n.d(o)}}}function yn(e){let t,s,n,o={ctx:e,current:null,token:null,hasCatch:!1,pending:$n,then:vn,catch:wn,value:12,blocks:[,,,]};return Pt(s=e[0],o),{c(){t=st(),o.block.c()},m(r,l){I(r,t,l),o.block.m(r,o.anchor=l),o.mount=()=>t.parentNode,o.anchor=t,n=!0},p(r,l){e=r,o.ctx=e,l&1&&s!==(s=e[0])&&Pt(s,o)||Pe(o,e,l)},i(r){n||(C(o.block),n=!0)},o(r){for(let l=0;l<3;l+=1){const a=o.blocks[l];T(a)}n=!1},d(r){r&&M(t),o.block.d(r),o.token=null,o=null}}}function wn(e){return{c:$,m:$,p:$,i:$,o:$,d:$}}function vn(e){var a;let t,s,n;const o=[e[2],e[3]];var r=((a=e[12])==null?void 0:a.default)||e[12];function l(i,u){let m={};for(let f=0;f<o.length;f+=1)m=vt(m,o[f]);return u!==void 0&&u&12&&(m=vt(m,oe(o,[u&4&&Ct(i[2]),u&8&&Ct(i[3])]))),{props:m}}return r&&(t=ne(r,l(e))),{c(){t&&F(t.$$.fragment),s=st()},m(i,u){t&&q(t,i,u),I(i,s,u),n=!0},p(i,u){var m;if(u&1&&r!==(r=((m=i[12])==null?void 0:m.default)||i[12])){if(t){lt();const f=t;T(f.$$.fragment,1,0,()=>{B(f,1)}),it()}r?(t=ne(r,l(i,u)),F(t.$$.fragment),C(t.$$.fragment,1),q(t,s.parentNode,s)):t=null}else if(r){const f=u&12?oe(o,[u&4&&Ct(i[2]),u&8&&Ct(i[3])]):{};t.$set(f)}},i(i){n||(t&&C(t.$$.fragment,i),n=!0)},o(i){t&&T(t.$$.fragment,i),n=!1},d(i){i&&M(s),t&&B(t,i)}}}function $n(e){return{c:$,m:$,p:$,i:$,o:$,d:$}}function En(e){let t,s,n=e[1]&&e[1].route===e[5]&&fe(e);return{c(){n&&n.c(),t=st()},m(o,r){n&&n.m(o,r),I(o,t,r),s=!0},p(o,[r]){o[1]&&o[1].route===o[5]?n?(n.p(o,r),r&2&&C(n,1)):(n=fe(o),n.c(),C(n,1),n.m(t.parentNode,t)):n&&(lt(),T(n,1,1,()=>{n=null}),it())},i(o){s||(C(n),s=!0)},o(o){T(n),s=!1},d(o){o&&M(t),n&&n.d(o)}}}function Ln(e,t,s){let n,{$$slots:o={},$$scope:r}=t,{path:l=""}=t,{component:a=null}=t,i={},u={};const{registerRoute:m,unregisterRoute:f,activeRoute:p}=Ft(Vt);ot(e,p,_=>s(1,n=_));const d={path:l,default:l===""};return m(d),Xe(()=>{f(d)}),e.$$set=_=>{s(11,t=vt(vt({},t),ee(_))),"path"in _&&s(6,l=_.path),"component"in _&&s(0,a=_.component),"$$scope"in _&&s(7,r=_.$$scope)},e.$$.update=()=>{if(n&&n.route===d){s(2,i=n.params);const{component:_,path:y,...h}=t;s(3,u=h),_&&(_.toString().startsWith("class ")?s(0,a=_):s(0,a=_())),je()&&!n.preserveScroll&&(window==null||window.scrollTo(0,0))}},t=ee(t),[a,n,i,u,p,d,l,r,o]}class ft extends X{constructor(t){super(),Q(this,t,Ln,En,G,{path:6,component:0})}}const Bt=e=>({...e.location,state:e.history.state,key:e.history.state&&e.history.state.key||"initial"}),Sn=e=>{const t=[];let s=Bt(e);return{get location(){return s},listen(n){t.push(n);const o=()=>{s=Bt(e),n({location:s,action:"POP"})};return e.addEventListener("popstate",o),()=>{e.removeEventListener("popstate",o);const r=t.indexOf(n);t.splice(r,1)}},navigate(n,{state:o,replace:r=!1,preserveScroll:l=!1,blurActiveElement:a=!0}={}){o={...o,key:Date.now()+""};try{r?e.history.replaceState(o,"",n):e.history.pushState(o,"",n)}catch{e.location[r?"replace":"assign"](n)}s=Bt(e),t.forEach(i=>i({location:s,action:"PUSH",preserveScroll:l})),a&&document.activeElement.blur()}}},On=(e="/")=>{let t=0;const s=[{pathname:e,search:""}],n=[];return{get location(){return s[t]},addEventListener(o,r){},removeEventListener(o,r){},history:{get entries(){return s},get index(){return t},get state(){return n[t]},pushState(o,r,l){const[a,i=""]=l.split("?");t++,s.push({pathname:a,search:i}),n.push(o)},replaceState(o,r,l){const[a,i=""]=l.split("?");s[t]={pathname:a,search:i},n[t]=o}}}},De=Sn(je()?window:On()),{navigate:nt}=De,Cn=e=>({route:e&4,location:e&2}),de=e=>({route:e[2]&&e[2].uri,location:e[1]}),Nn=e=>({route:e&4,location:e&2}),me=e=>({route:e[2]&&e[2].uri,location:e[1]});function Tn(e){let t;const s=e[15].default,n=jt(s,e,e[14],de);return{c(){n&&n.c()},m(o,r){n&&n.m(o,r),t=!0},p(o,r){n&&n.p&&(!t||r&16390)&&Ht(n,s,o,o[14],t?Dt(s,o[14],r,Cn):It(o[14]),de)},i(o){t||(C(n,o),t=!0)},o(o){T(n,o),t=!1},d(o){n&&n.d(o)}}}function Rn(e){let t=e[1].pathname,s,n,o=pe(e);return{c(){o.c(),s=st()},m(r,l){o.m(r,l),I(r,s,l),n=!0},p(r,l){l&2&&G(t,t=r[1].pathname)?(lt(),T(o,1,1,$),it(),o=pe(r),o.c(),C(o,1),o.m(s.parentNode,s)):o.p(r,l)},i(r){n||(C(o),n=!0)},o(r){T(o),n=!1},d(r){r&&M(s),o.d(r)}}}function pe(e){let t,s,n,o;const r=e[15].default,l=jt(r,e,e[14],me);return{c(){t=w("div"),l&&l.c()},m(a,i){I(a,t,i),l&&l.m(t,null),o=!0},p(a,i){l&&l.p&&(!o||i&16390)&&Ht(l,r,a,a[14],o?Dt(r,a[14],i,Nn):It(a[14]),me)},i(a){o||(C(l,a),a&&ht(()=>{o&&(n&&n.end(1),s=nn(t,e[3],{}),s.start())}),o=!0)},o(a){T(l,a),s&&s.invalidate(),a&&(n=sn(t,e[3],{})),o=!1},d(a){a&&M(t),l&&l.d(a),a&&n&&n.end()}}}function An(e){let t,s,n,o;const r=[Rn,Tn],l=[];function a(i,u){return i[0]?0:1}return t=a(e),s=l[t]=r[t](e),{c(){s.c(),n=st()},m(i,u){l[t].m(i,u),I(i,n,u),o=!0},p(i,[u]){let m=t;t=a(i),t===m?l[t].p(i,u):(lt(),T(l[m],1,1,()=>{l[m]=null}),it(),s=l[t],s?s.p(i,u):(s=l[t]=r[t](i),s.c()),C(s,1),s.m(n.parentNode,n))},i(i){o||(C(s),o=!0)},o(i){T(s),o=!1},d(i){i&&M(n),l[t].d(i)}}}function Pn(e,t,s){let n,o,r,l,{$$slots:a={},$$scope:i}=t,{basepath:u="/"}=t,{url:m=null}=t,{viewtransition:f=null}=t,{history:p=De}=t;const d=(k,P,D)=>{const O=f(D);return typeof(O==null?void 0:O.fn)=="function"?O.fn(k,O):O};Wt(un,p);const _=Ft(le),y=Ft(Vt),h=mt([]);ot(e,h,k=>s(12,o=k));const E=mt(null);ot(e,E,k=>s(2,l=k));let L=!1;const S=_||mt(m?{pathname:m}:p.location);ot(e,S,k=>s(1,n=k));const R=y?y.routerBase:mt({path:u,uri:u});ot(e,R,k=>s(13,r=k));const A=an([R,E],([k,P])=>{if(!P)return k;const{path:D}=k,{route:O,uri:z}=P;return{path:O.default?D:O.path.replace(/\*.*$/,""),uri:z}}),U=k=>{const{path:P}=r;let{path:D}=k;if(k._path=D,k.path=ue(P,D),typeof window>"u"){if(L)return;const O=ae([k],n.pathname);O&&(E.set(O),L=!0)}else h.update(O=>[...O,k])},v=k=>{h.update(P=>P.filter(D=>D!==k))};let g=!1;return _||(Zt(()=>p.listen(P=>{s(11,g=P.preserveScroll||!1),S.set(P.location)})),Wt(le,S)),Wt(Vt,{activeRoute:E,base:R,routerBase:A,registerRoute:U,unregisterRoute:v}),e.$$set=k=>{"basepath"in k&&s(8,u=k.basepath),"url"in k&&s(9,m=k.url),"viewtransition"in k&&s(0,f=k.viewtransition),"history"in k&&s(10,p=k.history),"$$scope"in k&&s(14,i=k.$$scope)},e.$$.update=()=>{if(e.$$.dirty&8192){const{path:k}=r;h.update(P=>P.map(D=>Object.assign(D,{path:ue(k,D._path)})))}if(e.$$.dirty&6146){const k=ae(o,n.pathname);E.set(k&&{...k,preserveScroll:g})}},[f,n,l,d,h,E,S,R,u,m,p,g,o,r,i,a]}class Mn extends X{constructor(t){super(),Q(this,t,Pn,An,G,{basepath:8,url:9,viewtransition:0,history:10})}}const St=e=>{const t=s=>{const n=s.currentTarget;(n.target===""||n.target==="_self")&&gn(n)&&hn(s)&&(s.preventDefault(),nt(n.pathname+n.search,{replace:n.hasAttribute("replace"),preserveScroll:n.hasAttribute("preserveScroll")}))};return e.addEventListener("click",t),{destroy(){e.removeEventListener("click",t)}}},wt=async(e,t,s=!1)=>{const n={...t.headers},o=await fetch(e,{...t,headers:n});if(o.ok)return await o.json();if(o.status===401||o.status===400)return nt("/login");{const r=await o.json();console.error(r)}},jn=async(e,t)=>{const s=await fetch("/api/login",{method:"POST",body:JSON.stringify({username:e,password:t}),headers:{"Content-Type":"application/json"}}),n=await s.json();return s.ok?nt("/"):{data:n,success:!1}},Dn=async(e,t,s,n)=>{const o=await fetch("/api/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({first_name:e,last_name:t,username:s,password:n})}),r=await o.json();return o.ok?{data:r,success:!0}:{data:r,success:!1}},Hn=()=>{wt("/api/logout",{method:"GET"})};function In(e){let t,s,n,o,r,l,a,i,u,m,f,p,d,_,y,h,E;return{c(){t=w("main"),s=w("form"),n=w("label"),o=w("div"),o.innerHTML='<span class="label-text">Username</span>',r=N(),l=w("input"),a=N(),i=w("label"),u=w("div"),u.innerHTML='<span class="label-text">Password</span>',m=N(),f=w("input"),p=N(),d=w("button"),d.textContent="Login",_=N(),y=w("a"),y.textContent="Register",b(o,"class","label"),b(l,"type","text"),b(l,"class","input input-bordered w-full max-w-xs"),b(n,"for","username"),b(n,"class","form-control w-full max-w-xs"),b(u,"class","label"),b(f,"type","password"),b(f,"class","input input-bordered w-full max-w-xs"),b(i,"for","password"),b(i,"class","form-control w-full max-w-xs"),b(d,"class","btn btn-primary my-3"),b(y,"href","/register"),b(y,"class","btn btn-link")},m(L,S){I(L,t,S),c(t,s),c(s,n),c(n,o),c(n,r),c(n,l),Y(l,e[0]),c(s,a),c(s,i),c(i,u),c(i,m),c(i,f),Y(f,e[1]),c(t,p),c(t,d),c(t,_),c(t,y),h||(E=[V(l,"input",e[3]),V(f,"input",e[4]),V(d,"click",Ne(e[2])),$t(St.call(null,y))],h=!0)},p(L,[S]){S&1&&l.value!==L[0]&&Y(l,L[0]),S&2&&f.value!==L[1]&&Y(f,L[1])},i:$,o:$,d(L){L&&M(t),h=!1,x(E)}}}function Un(e,t,s){let n="",o="";const r=async()=>{const{success:i}=await jn(n,o);i&&nt("/")};function l(){n=this.value,s(0,n)}function a(){o=this.value,s(1,o)}return[n,o,r,l,a]}class Kn extends X{constructor(t){super(),Q(this,t,Un,In,G,{})}}function _e(e){let t;const s=e[2].default,n=jt(s,e,e[1],null);return{c(){n&&n.c()},m(o,r){n&&n.m(o,r),t=!0},p(o,r){n&&n.p&&(!t||r&2)&&Ht(n,s,o,o[1],t?Dt(s,o[1],r,null):It(o[1]),null)},i(o){t||(C(n,o),t=!0)},o(o){T(n,o),t=!1},d(o){n&&n.d(o)}}}function Wn(e){let t,s,n=e[0]&&_e(e);return{c(){n&&n.c(),t=st()},m(o,r){n&&n.m(o,r),I(o,t,r),s=!0},p(o,[r]){o[0]?n?(n.p(o,r),r&1&&C(n,1)):(n=_e(o),n.c(),C(n,1),n.m(t.parentNode,t)):n&&(lt(),T(n,1,1,()=>{n=null}),it())},i(o){s||(C(n),s=!0)},o(o){T(n),s=!1},d(o){o&&M(t),n&&n.d(o)}}}function zn(e,t,s){let n;ot(e,Mt,a=>s(0,n=a));let{$$slots:o={},$$scope:r}=t;const l=async()=>{const a=await wt("/api/user",{method:"GET"},!0);Mt.set(a)};return e.$$set=a=>{"$$scope"in a&&s(1,r=a.$$scope)},l(),[n,r,o]}class He extends X{constructor(t){super(),Q(this,t,zn,Wn,G,{})}}function he(e){let t,s,n,o,r;return{c(){t=w("a"),s=w("button"),s.textContent="Start annotating",b(s,"class","btn btn-primary btn-sm"),b(t,"href",n="/annotate/"+e[0].next_assignment)},m(l,a){I(l,t,a),c(t,s),o||(r=$t(St.call(null,t)),o=!0)},p(l,a){a&1&&n!==(n="/annotate/"+l[0].next_assignment)&&b(t,"href",n)},d(l){l&&M(t),o=!1,r()}}}function qn(e){let t,s,n,o=e[0].first_name+"",r,l,a,i,u,m=e[0].num_completed+"",f,p,d=e[0].num_assigned+"",_,y,h=e[0].num_skipped+"",E,L,S=e[0].num_assigned+"",R,A,U,v,g,k=e[0].num_assigned-e[0].num_completed-e[0].num_skipped+"",P,D,O=e[0].num_assigned+"",z,at,bt,W=e[0].next_assignment!==null&&he(e);return{c(){t=w("main"),s=w("h1"),n=K("Hey, "),r=K(o),l=K("!"),a=N(),i=w("p"),u=K("You have completed "),f=K(m),p=K(" / "),_=K(d),y=K(" annotations. You have skipped "),E=K(h),L=K(`
			/ `),R=K(S),A=K(" annotations."),U=N(),v=w("p"),g=K("You have "),P=K(k),D=K(" / "),z=K(O),at=K(`
			assignments left to view.`),bt=N(),W&&W.c(),b(s,"class","text-lg font-bold"),b(i,"class","my-3"),b(v,"class","my-3"),b(t,"class","p-10")},m(H,J){I(H,t,J),c(t,s),c(s,n),c(s,r),c(s,l),c(t,a),c(t,i),c(i,u),c(i,f),c(i,p),c(i,_),c(i,y),c(i,E),c(i,L),c(i,R),c(i,A),c(t,U),c(t,v),c(v,g),c(v,P),c(v,D),c(v,z),c(v,at),c(t,bt),W&&W.m(t,null)},p(H,J){J&1&&o!==(o=H[0].first_name+"")&&tt(r,o),J&1&&m!==(m=H[0].num_completed+"")&&tt(f,m),J&1&&d!==(d=H[0].num_assigned+"")&&tt(_,d),J&1&&h!==(h=H[0].num_skipped+"")&&tt(E,h),J&1&&S!==(S=H[0].num_assigned+"")&&tt(R,S),J&1&&k!==(k=H[0].num_assigned-H[0].num_completed-H[0].num_skipped+"")&&tt(P,k),J&1&&O!==(O=H[0].num_assigned+"")&&tt(z,O),H[0].next_assignment!==null?W?W.p(H,J):(W=he(H),W.c(),W.m(t,null)):W&&(W.d(1),W=null)},d(H){H&&M(t),W&&W.d()}}}function Bn(e){let t,s;return t=new He({props:{$$slots:{default:[qn]},$$scope:{ctx:e}}}),{c(){F(t.$$.fragment)},m(n,o){q(t,n,o),s=!0},p(n,[o]){const r={};o&3&&(r.$$scope={dirty:o,ctx:n}),t.$set(r)},i(n){s||(C(t.$$.fragment,n),s=!0)},o(n){T(t.$$.fragment,n),s=!1},d(n){B(t,n)}}}function Gn(e,t,s){let n;return ot(e,Mt,o=>s(0,n=o)),[n]}class Fn extends X{constructor(t){super(),Q(this,t,Gn,Bn,G,{})}}function Jn(e){let t,s,n,o,r,l,a,i,u,m,f,p,d,_,y,h,E,L,S,R,A,U,v,g,k,P,D;return{c(){t=w("main"),s=w("form"),n=w("label"),o=w("div"),o.innerHTML='<span class="label-text">First Name</span>',r=N(),l=w("input"),a=N(),i=w("label"),u=w("div"),u.innerHTML='<span class="label-text">Last Name</span>',m=N(),f=w("input"),p=N(),d=w("label"),_=w("div"),_.innerHTML='<span class="label-text">Username</span>',y=N(),h=w("input"),E=N(),L=w("label"),S=w("div"),S.innerHTML='<span class="label-text">Password</span>',R=N(),A=w("input"),U=N(),v=w("button"),v.textContent="Create account",g=N(),k=w("a"),k.textContent="Log in instead",b(o,"class","label"),b(l,"type","text"),b(l,"class","input input-bordered w-full max-w-xs"),b(n,"for","first_name"),b(n,"class","form-control w-full max-w-xs"),b(u,"class","label"),b(f,"type","text"),b(f,"class","input input-bordered w-full max-w-xs"),b(i,"for","last_name"),b(i,"class","form-control w-full max-w-xs"),b(_,"class","label"),b(h,"type","text"),b(h,"class","input input-bordered w-full max-w-xs"),b(d,"for","username"),b(d,"class","form-control w-full max-w-xs"),b(S,"class","label"),b(A,"type","password"),b(A,"class","input input-bordered w-full max-w-xs"),b(L,"for","password"),b(L,"class","form-control w-full max-w-xs"),b(v,"class","btn btn-primary my-3"),b(k,"href","/login"),b(k,"class","btn btn-link")},m(O,z){I(O,t,z),c(t,s),c(s,n),c(n,o),c(n,r),c(n,l),Y(l,e[0]),c(s,a),c(s,i),c(i,u),c(i,m),c(i,f),Y(f,e[1]),c(s,p),c(s,d),c(d,_),c(d,y),c(d,h),Y(h,e[2]),c(s,E),c(s,L),c(L,S),c(L,R),c(L,A),Y(A,e[3]),c(t,U),c(t,v),c(t,g),c(t,k),P||(D=[V(l,"input",e[5]),V(f,"input",e[6]),V(h,"input",e[7]),V(A,"input",e[8]),V(v,"click",Ne(e[4]))],P=!0)},p(O,[z]){z&1&&l.value!==O[0]&&Y(l,O[0]),z&2&&f.value!==O[1]&&Y(f,O[1]),z&4&&h.value!==O[2]&&Y(h,O[2]),z&8&&A.value!==O[3]&&Y(A,O[3])},i:$,o:$,d(O){O&&M(t),P=!1,x(D)}}}function Yn(e,t,s){let n="",o="",r="",l="";const a=async()=>{const{success:p}=await Dn(n,o,r,l);p&&nt("/login")};function i(){n=this.value,s(0,n)}function u(){o=this.value,s(1,o)}function m(){r=this.value,s(2,r)}function f(){l=this.value,s(3,l)}return[n,o,r,l,a,i,u,m,f]}class Vn extends X{constructor(t){super(),Q(this,t,Yn,Jn,G,{})}}function Qn(e){const t=async()=>{Hn(),nt("/login",{replace:!0})};return Zt(()=>{t()}),[]}class Xn extends X{constructor(t){super(),Q(this,t,Qn,null,G,{})}}function Zn(e){let t;return{c(){t=w("main"),t.innerHTML=`<h1 class="text-lg font-bold">Uh oh! We couldn&#39;t find this page.</h1>

	Go back <a href="/" class="link">home</a>.`,b(t,"class","p-10")},m(s,n){I(s,t,n)},p:$,i:$,o:$,d(s){s&&M(t)}}}class xn extends X{constructor(t){super(),Q(this,t,null,Zn,G,{})}}let ts=0;const es=e=>e+ ++ts,ge=e=>JSON.parse(JSON.stringify(e)),ns=e=>({_state:e,_target:new EventTarget,cid:es("model"),set:function(t,s){const n=ge(this._state[t]);this._state[t]=s,this._target.dispatchEvent(new CustomEvent("change",{detail:{data:ge(this._state),previous:n,changed:{[t]:s}}}))},get:function(t){return this._state[t]},on:function(t,s){this._target.addEventListener(t,s)}});function ss(e){let t;return{c(){t=w("div"),b(t,"class","container min-h-96 p-5")},m(s,n){I(s,t,n),e[5](t)},p:$,i:$,o:$,d(s){s&&M(t),e[5](null)}}}function Ie(e){return e.startsWith("http://")||e.startsWith("https://")}async function os(e,t){let s=document.querySelector(`link[id='${t}']`);if(s){let n=s.cloneNode();n.href=e,n.addEventListener("load",()=>s==null?void 0:s.remove()),n.addEventListener("error",()=>s==null?void 0:s.remove()),s.after(n);return}return new Promise(n=>{let o=Object.assign(document.createElement("link"),{rel:"stylesheet",href:e,onload:n});document.head.appendChild(o)})}function rs(e,t){let s=document.querySelector(`style[id='${t}']`);if(s){s.textContent=e;return}let n=Object.assign(document.createElement("style"),{id:t,type:"text/css"});n.appendChild(document.createTextNode(e)),document.head.appendChild(n)}async function ls(e,t){if(!(!e||!t))return Ie(e)?os(e,t):rs(e,t)}async function is(e){if(Ie(e))return{module:await import(e),url:e};let t=URL.createObjectURL(new Blob([e],{type:"text/javascript"})),s=await import(t);return URL.revokeObjectURL(t),{module:s.default,url:t}}function as(e,t,s){let{task:n}=t,{components:o}=t,{componentData:r}=t,{dirty:l}=t,a;const i=[],u=async d=>Object.fromEntries(await Promise.all(Object.values(d).map(async({name:_,esm:y})=>{const h=await is(y);return[_,h]}))),m=async d=>(Object.entries(d).forEach(([_,{css:y}])=>{ls(y,_)}),u(d)),f=async()=>{s(0,a.innerHTML="",a);const d=await m(o);n.forEach(({field:_,component:y})=>{let{name:h,props:E}=y;const{module:L}=d[h],{render:S}=L,R=document.createElement("div");a.appendChild(R),E=E||{};const A=r[_].annotation,U=r[_].datum,v=ns({datum:U,annotation:A,props:E});v.on("change",({detail:k})=>{const{data:P}=k;r[_].annotation!==P.annotation&&(s(1,r[_].annotation=P.annotation,r),s(2,l=!0))});const g=S({el:R,model:v});g&&i.push(g)})};Zt(()=>(f(),()=>{i.forEach(d=>d())}));function p(d){Lt[d?"unshift":"push"](()=>{a=d,s(0,a)})}return e.$$set=d=>{"task"in d&&s(3,n=d.task),"components"in d&&s(4,o=d.components),"componentData"in d&&s(1,r=d.componentData),"dirty"in d&&s(2,l=d.dirty)},[a,r,l,n,o,p]}class us extends X{constructor(t){super(),Q(this,t,as,ss,G,{task:3,components:4,componentData:1,dirty:2})}}function cs(e){let t;return{c(){t=w("div"),t.innerHTML="<h1>Not yet marked as complete. Press submit to mark as complete.</h1>",b(t,"class","bg-gray-100 p-3 text-gray-400")},m(s,n){I(s,t,n)},d(s){s&&M(t)}}}function fs(e){let t;return{c(){t=w("div"),t.innerHTML="<h1>Marked as skipped.</h1>",b(t,"class","bg-red-300 p-3")},m(s,n){I(s,t,n)},d(s){s&&M(t)}}}function ds(e){let t;return{c(){t=w("div"),t.innerHTML="<h1>Marked as complete.</h1>",b(t,"class","bg-green-300 p-3")},m(s,n){I(s,t,n)},d(s){s&&M(t)}}}function ms(e){let t,s,n,o,r,l,a,i,u=e[6]?`Last saved ${e[6]}.`:"",m,f,p,d,_,y,h,E,L,S,R,A,U,v,g,k,P,D,O,z,at;function bt(j,Z){return j[0].is_complete?ds:j[0].is_skipped?fs:cs}let W=bt(e),H=W(e);function J(j){e[14](j)}function Ue(j){e[15](j)}let Ut={task:e[3],components:e[2]};return e[4]!==void 0&&(Ut.componentData=e[4]),e[5]!==void 0&&(Ut.dirty=e[5]),n=new us({props:Ut}),Lt.push(()=>re(n,"componentData",J)),Lt.push(()=>re(n,"dirty",Ue)),{c(){t=w("main"),H.c(),s=N(),F(n.$$.fragment),l=N(),a=w("div"),i=w("span"),m=K(u),f=N(),p=w("div"),d=N(),_=w("span"),y=w("a"),h=K("@"),E=K(e[1]),S=N(),R=w("div"),A=w("button"),U=K("Prev"),g=N(),k=w("button"),k.textContent="Submit",P=N(),D=w("button"),D.textContent="Skip",b(p,"class","flex-1"),b(y,"href",L="/annotate/"+e[1]),b(_,"class","flex-none"),b(a,"class","info text-sm text-gray-300 flex my-8"),b(A,"class","btn btn-lg mx-4"),A.disabled=v=e[0].prev===null,b(k,"class","btn btn-lg mx-4 btn-success"),b(D,"class","btn btn-lg mx-4 btn-error"),b(R,"class","actions mx-auto max-w-fit svelte-19w63sy"),b(t,"class","p-5")},m(j,Z){I(j,t,Z),H.m(t,null),c(t,s),q(n,t,null),c(t,l),c(t,a),c(a,i),c(i,m),c(a,f),c(a,p),c(a,d),c(a,_),c(_,y),c(y,h),c(y,E),c(t,S),c(t,R),c(R,A),c(A,U),c(R,g),c(R,k),c(R,P),c(R,D),O=!0,z||(at=[V(window,"keydown",e[7]),V(A,"click",e[10]),V(k,"click",e[8]),V(D,"click",e[9])],z=!0)},p(j,[Z]){W!==(W=bt(j))&&(H.d(1),H=W(j),H&&(H.c(),H.m(t,s)));const kt={};Z&8&&(kt.task=j[3]),Z&4&&(kt.components=j[2]),!o&&Z&16&&(o=!0,kt.componentData=j[4],se(()=>o=!1)),!r&&Z&32&&(r=!0,kt.dirty=j[5],se(()=>r=!1)),n.$set(kt),(!O||Z&64)&&u!==(u=j[6]?`Last saved ${j[6]}.`:"")&&tt(m,u),(!O||Z&2)&&tt(E,j[1]),(!O||Z&2&&L!==(L="/annotate/"+j[1]))&&b(y,"href",L),(!O||Z&1&&v!==(v=j[0].prev===null))&&(A.disabled=v)},i(j){O||(C(n.$$.fragment,j),O=!0)},o(j){T(n.$$.fragment,j),O=!1},d(j){j&&M(t),H.d(),B(n),z=!1,x(at)}}}function ps(e,t,s){let n,o,{datum:r}=t,{postAssignment:l}=t,{next:a}=t,{prev:i}=t,{assignment:u}=t,{components:m}=t,{task:f}=t,p=!1,d;const _=g=>g?Object.fromEntries(Object.entries(g).map(([k,{annotation:P}])=>[k,JSON.stringify(P)])):{},y=g=>{if(g.key==="Enter"&&!g.ctrlKey&&!g.metaKey){if(g.preventDefault(),u.is_complete)return S();E()}g.key==="ArrowRight"&&!g.ctrlKey&&!g.metaKey&&(g.preventDefault(),S()),g.key==="ArrowDown"&&!g.ctrlKey&&!g.metaKey&&(g.preventDefault(),R()),g.key==="ArrowLeft"&&!g.ctrlKey&&!g.metaKey&&(g.preventDefault(),A())},h=async(g,k=!1,P=!1)=>{if(!g)return;console.log("POST",g,k,P);const D=await l(g,r,k||!p&&u.is_complete,P);s(0,u=D),g=u.annotation,s(6,d=new Date().toLocaleString())},E=async()=>{await h(o,!0,!1),s(5,p=!1)},L=async()=>{await E(),await S()},S=async()=>(await h(o,u.is_complete,u.is_skipped),a(u)),R=async()=>{s(5,p=!0),await h(o,!1,!0)},A=async()=>(await h(o,u.is_complete,u.is_skipped),i(u));function U(g){n=g,s(4,n),s(0,u)}function v(g){p=g,s(5,p)}return e.$$set=g=>{"datum"in g&&s(1,r=g.datum),"postAssignment"in g&&s(11,l=g.postAssignment),"next"in g&&s(12,a=g.next),"prev"in g&&s(13,i=g.prev),"assignment"in g&&s(0,u=g.assignment),"components"in g&&s(2,m=g.components),"task"in g&&s(3,f=g.task)},e.$$.update=()=>{e.$$.dirty&1&&s(4,n=u.components),e.$$.dirty&16&&(o=_(n))},[u,r,m,f,n,p,d,y,L,R,A,l,a,i,U,v]}class _s extends X{constructor(t){super(),Q(this,t,ps,ms,G,{datum:1,postAssignment:11,next:12,prev:13,assignment:0,components:2,task:3})}}function be(e){e[9]=e[12].task,e[10]=e[12].components,e[11]=e[12].assignment}function hs(e){return{c:$,m:$,p:$,i:$,o:$,d:$}}function gs(e){be(e);let t,s;return t=new _s({props:{task:e[9],components:e[10],assignment:e[11],postAssignment:e[3],next:e[4],prev:e[5],datum:e[0]}}),{c(){F(t.$$.fragment)},m(n,o){q(t,n,o),s=!0},p(n,o){be(n);const r={};o&1&&(r.task=n[9]),o&1&&(r.components=n[10]),o&1&&(r.assignment=n[11]),o&1&&(r.datum=n[0]),t.$set(r)},i(n){s||(C(t.$$.fragment,n),s=!0)},o(n){T(t.$$.fragment,n),s=!1},d(n){B(t,n)}}}function bs(e){return{c:$,m:$,p:$,i:$,o:$,d:$}}function ke(e){let t,s,n,o={ctx:e,current:null,token:null,hasCatch:!1,pending:bs,then:gs,catch:hs,value:12,blocks:[,,,]};return Pt(s=e[2](e[0]),o),{c(){t=st(),o.block.c()},m(r,l){I(r,t,l),o.block.m(r,o.anchor=l),o.mount=()=>t.parentNode,o.anchor=t,n=!0},p(r,l){e=r,o.ctx=e,l&1&&s!==(s=e[2](e[0]))&&Pt(s,o)||Pe(o,e,l)},i(r){n||(C(o.block),n=!0)},o(r){for(let l=0;l<3;l+=1){const a=o.blocks[l];T(a)}n=!1},d(r){r&&M(t),o.block.d(r),o.token=null,o=null}}}function ks(e){let t=e[1],s,n,o=ke(e);return{c(){o.c(),s=st()},m(r,l){o.m(r,l),I(r,s,l),n=!0},p(r,l){l&2&&G(t,t=r[1])?(lt(),T(o,1,1,$),it(),o=ke(r),o.c(),C(o,1),o.m(s.parentNode,s)):o.p(r,l)},i(r){n||(C(o),n=!0)},o(r){T(o),n=!1},d(r){r&&M(s),o.d(r)}}}function ys(e){let t,s;return t=new He({props:{$$slots:{default:[ks]},$$scope:{ctx:e}}}),{c(){F(t.$$.fragment)},m(n,o){q(t,n,o),s=!0},p(n,[o]){const r={};o&8195&&(r.$$scope={dirty:o,ctx:n}),t.$set(r)},i(n){s||(C(t.$$.fragment,n),s=!0)},o(n){T(t.$$.fragment,n),s=!1},d(n){B(t,n)}}}function ws(e,t,s){let{datum:n}=t,o=!1,r;(()=>{r=new WebSocket(`ws://${window.location.host}/hmr`);const p=()=>{console.log("[HMR] Reloading..."),s(1,o=!o)},d=()=>{let h=0;const E=()=>{if(r&&(r.readyState===WebSocket.OPEN||r.readyState===WebSocket.CONNECTING)){p();return}if(h>=10){console.error("[HMR] Could not reconnect to server");return}h++,console.log(`[HMR] Attempting to reconnect... (${h})`),r=new WebSocket(`ws://${window.location.host}/hmr`),r.addEventListener("open",()=>{console.log("[HMR] Reconnected")}),r.addEventListener("message",L=>{L.data==="reload"&&p()}),r.addEventListener("close",d),setTimeout(E,1e3)};E()};r.addEventListener("open",()=>{console.info(`[HMR] Listening for HMR updates at ${r.url}`)}),r.addEventListener("message",_=>{_.data==="reload"&&p()}),r.addEventListener("close",()=>{d()})})();const l=async()=>{let{task:p,components:d}=await wt("/api/task",{method:"GET"},!0);return{task:p,components:d}},a=async p=>await wt(`/api/annotate/${p}`,{method:"GET"},!0),i=async p=>{const{task:d,components:_}=await l(),y=await a(p);return{task:d,components:_,assignment:y}},u=async(p,d,_=!1,y=!1)=>p?await wt(`/api/annotate/${d}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({annotation:p,is_complete:_,is_skipped:y})},!0):void 0,m=async p=>p.next===null?nt("/"):nt(`/annotate/${p.next}`),f=async p=>{if(p.prev!==null)return nt(`/annotate/${p.prev}`)};return e.$$set=p=>{"datum"in p&&s(0,n=p.datum)},[n,o,i,u,m,f]}class vs extends X{constructor(t){super(),Q(this,t,ws,ys,G,{datum:0})}}function $s(e){let t,s,n,o,r;return{c(){t=w("ul"),s=w("li"),n=w("a"),n.textContent="Login",b(n,"href","/login"),b(t,"class","menu menu-horizontal")},m(l,a){I(l,t,a),c(t,s),c(s,n),o||(r=$t(St.call(null,n)),o=!0)},d(l){l&&M(t),o=!1,r()}}}function Es(e){let t,s,n,o,r,l,a,i;return{c(){t=w("ul"),s=w("li"),n=w("a"),n.textContent="Home",o=N(),r=w("li"),l=w("a"),l.textContent="Logout",b(n,"href","/"),b(l,"href","/logout"),b(t,"class","menu menu-horizontal")},m(u,m){I(u,t,m),c(t,s),c(s,n),c(t,o),c(t,r),c(r,l),a||(i=[$t(St.call(null,n)),$t(St.call(null,l))],a=!0)},d(u){u&&M(t),a=!1,x(i)}}}function Ls(e){let t,s;return t=new vs({props:{datum:e[2].datum}}),{c(){F(t.$$.fragment)},m(n,o){q(t,n,o),s=!0},p(n,o){const r={};o&4&&(r.datum=n[2].datum),t.$set(r)},i(n){s||(C(t.$$.fragment,n),s=!0)},o(n){T(t.$$.fragment,n),s=!1},d(n){B(t,n)}}}function Ss(e){let t,s,n,o,r,l,a,i,u,m,f,p,d,_,y,h,E,L,S;function R(v,g){return v[1]?Es:$s}let A=R(e),U=A(e);return i=new ft({props:{path:"/annotate/:datum",$$slots:{default:[Ls,({params:v})=>({2:v}),({params:v})=>v?4:0]},$$scope:{ctx:e}}}),m=new ft({props:{path:"/login",component:Kn}}),p=new ft({props:{path:"/register",component:Vn}}),_=new ft({props:{path:"/logout",component:Xn}}),h=new ft({props:{path:"/",component:Fn}}),L=new ft({props:{component:xn}}),{c(){t=w("nav"),s=w("div"),s.innerHTML="<b>🍃 yatta</b>",n=N(),o=w("div"),r=N(),U.c(),l=N(),a=w("div"),F(i.$$.fragment),u=N(),F(m.$$.fragment),f=N(),F(p.$$.fragment),d=N(),F(_.$$.fragment),y=N(),F(h.$$.fragment),E=N(),F(L.$$.fragment),b(s,"class","flex-none text-xl"),b(o,"class","flex-1"),b(t,"class","navbar bg-accent"),b(a,"class","max-w-screen-md mx-auto")},m(v,g){I(v,t,g),c(t,s),c(t,n),c(t,o),c(t,r),U.m(t,null),I(v,l,g),I(v,a,g),q(i,a,null),c(a,u),q(m,a,null),c(a,f),q(p,a,null),c(a,d),q(_,a,null),c(a,y),q(h,a,null),c(a,E),q(L,a,null),S=!0},p(v,g){A!==(A=R(v))&&(U.d(1),U=A(v),U&&(U.c(),U.m(t,null)));const k={};g&12&&(k.$$scope={dirty:g,ctx:v}),i.$set(k)},i(v){S||(C(i.$$.fragment,v),C(m.$$.fragment,v),C(p.$$.fragment,v),C(_.$$.fragment,v),C(h.$$.fragment,v),C(L.$$.fragment,v),S=!0)},o(v){T(i.$$.fragment,v),T(m.$$.fragment,v),T(p.$$.fragment,v),T(_.$$.fragment,v),T(h.$$.fragment,v),T(L.$$.fragment,v),S=!1},d(v){v&&(M(t),M(l),M(a)),U.d(),B(i),B(m),B(p),B(_),B(h),B(L)}}}function Os(e){let t,s;return t=new Mn({props:{url:e[0],$$slots:{default:[Ss]},$$scope:{ctx:e}}}),{c(){F(t.$$.fragment)},m(n,o){q(t,n,o),s=!0},p(n,[o]){const r={};o&1&&(r.url=n[0]),o&10&&(r.$$scope={dirty:o,ctx:n}),t.$set(r)},i(n){s||(C(t.$$.fragment,n),s=!0)},o(n){T(t.$$.fragment,n),s=!1},d(n){B(t,n)}}}function Cs(e,t,s){let n;ot(e,Mt,r=>s(1,n=r));let{url:o=""}=t;return e.$$set=r=>{"url"in r&&s(0,o=r.url)},[o,n]}class Ns extends X{constructor(t){super(),Q(this,t,Cs,Os,G,{url:0})}}new Ns({target:document.getElementById("app")});
