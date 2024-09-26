var Ot = Object.defineProperty;
var xt = (t, e, n) => e in t ? Ot(t, e, { enumerable: !0, configurable: !0, writable: !0, value: n }) : t[e] = n;
var tt = (t, e, n) => (xt(t, typeof e != "symbol" ? e + "" : e, n), n);
function D() {
}
function _t(t) {
  return t();
}
function lt() {
  return /* @__PURE__ */ Object.create(null);
}
function X(t) {
  t.forEach(_t);
}
function gt(t) {
  return typeof t == "function";
}
function at(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function At(t) {
  return Object.keys(t).length === 0;
}
function h(t, e) {
  t.appendChild(e);
}
function V(t, e, n) {
  t.insertBefore(e, n || null);
}
function I(t) {
  t.parentNode && t.parentNode.removeChild(t);
}
function k(t) {
  return document.createElement(t);
}
function z(t) {
  return document.createTextNode(t);
}
function P() {
  return z(" ");
}
function Q(t, e, n, s) {
  return t.addEventListener(e, n, s), () => t.removeEventListener(e, n, s);
}
function w(t, e, n) {
  n == null ? t.removeAttribute(e) : t.getAttribute(e) !== n && t.setAttribute(e, n);
}
function Dt(t) {
  return Array.from(t.childNodes);
}
function ft(t, e) {
  e = "" + e, t.data !== e && (t.data = /** @type {string} */
  e);
}
let W;
function B(t) {
  W = t;
}
function Tt() {
  if (!W)
    throw new Error("Function called outside component initialization");
  return W;
}
function Ct(t) {
  Tt().$$.on_mount.push(t);
}
const R = [], F = [];
let q = [];
const st = [], Nt = /* @__PURE__ */ Promise.resolve();
let ot = !1;
function jt() {
  ot || (ot = !0, Nt.then(pt));
}
function rt(t) {
  q.push(t);
}
function dt(t) {
  st.push(t);
}
const et = /* @__PURE__ */ new Set();
let U = 0;
function pt() {
  if (U !== 0)
    return;
  const t = W;
  do {
    try {
      for (; U < R.length; ) {
        const e = R[U];
        U++, B(e), Mt(e.$$);
      }
    } catch (e) {
      throw R.length = 0, U = 0, e;
    }
    for (B(null), R.length = 0, U = 0; F.length; )
      F.pop()();
    for (let e = 0; e < q.length; e += 1) {
      const n = q[e];
      et.has(n) || (et.add(n), n());
    }
    q.length = 0;
  } while (R.length);
  for (; st.length; )
    st.pop()();
  ot = !1, et.clear(), B(t);
}
function Mt(t) {
  if (t.fragment !== null) {
    t.update(), X(t.before_update);
    const e = t.dirty;
    t.dirty = [-1], t.fragment && t.fragment.p(t.ctx, e), t.after_update.forEach(rt);
  }
}
function Pt(t) {
  const e = [], n = [];
  q.forEach((s) => t.indexOf(s) === -1 ? e.push(s) : n.push(s)), n.forEach((s) => s()), q = e;
}
const Y = /* @__PURE__ */ new Set();
let Kt;
function yt(t, e) {
  t && t.i && (Y.delete(t), t.i(e));
}
function Ut(t, e, n, s) {
  if (t && t.o) {
    if (Y.has(t))
      return;
    Y.add(t), Kt.c.push(() => {
      Y.delete(t);
    }), t.o(e);
  }
}
function mt(t, e, n) {
  const s = t.$$.props[e];
  s !== void 0 && (t.$$.bound[s] = n, n(t.$$.ctx[s]));
}
function Ht(t) {
  t && t.c();
}
function bt(t, e, n) {
  const { fragment: s, after_update: i } = t.$$;
  s && s.m(e, n), rt(() => {
    const c = t.$$.on_mount.map(_t).filter(gt);
    t.$$.on_destroy ? t.$$.on_destroy.push(...c) : X(c), t.$$.on_mount = [];
  }), i.forEach(rt);
}
function kt(t, e) {
  const n = t.$$;
  n.fragment !== null && (Pt(n.after_update), X(n.on_destroy), n.fragment && n.fragment.d(e), n.on_destroy = n.fragment = null, n.ctx = []);
}
function Rt(t, e) {
  t.$$.dirty[0] === -1 && (R.push(t), jt(), t.$$.dirty.fill(0)), t.$$.dirty[e / 31 | 0] |= 1 << e % 31;
}
function wt(t, e, n, s, i, c, d = null, a = [-1]) {
  const l = W;
  B(t);
  const o = t.$$ = {
    fragment: null,
    ctx: [],
    // state
    props: c,
    update: D,
    not_equal: i,
    bound: lt(),
    // lifecycle
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(e.context || (l ? l.$$.context : [])),
    // everything else
    callbacks: lt(),
    dirty: a,
    skip_bound: !1,
    root: e.target || l.$$.root
  };
  d && d(o.root);
  let p = !1;
  if (o.ctx = n ? n(t, e.props || {}, (m, _, ...u) => {
    const g = u.length ? u[0] : _;
    return o.ctx && i(o.ctx[m], o.ctx[m] = g) && (!o.skip_bound && o.bound[m] && o.bound[m](g), p && Rt(t, m)), _;
  }) : [], o.update(), p = !0, X(o.before_update), o.fragment = s ? s(o.ctx) : !1, e.target) {
    if (e.hydrate) {
      const m = Dt(e.target);
      o.fragment && o.fragment.l(m), m.forEach(I);
    } else
      o.fragment && o.fragment.c();
    e.intro && yt(t.$$.fragment), bt(t, e.target, e.anchor), pt();
  }
  B(l);
}
class vt {
  constructor() {
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    tt(this, "$$");
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    tt(this, "$$set");
  }
  /** @returns {void} */
  $destroy() {
    kt(this, 1), this.$destroy = D;
  }
  /**
   * @template {Extract<keyof Events, string>} K
   * @param {K} type
   * @param {((e: Events[K]) => void) | null | undefined} callback
   * @returns {() => void}
   */
  $on(e, n) {
    if (!gt(n))
      return D;
    const s = this.$$.callbacks[e] || (this.$$.callbacks[e] = []);
    return s.push(n), () => {
      const i = s.indexOf(n);
      i !== -1 && s.splice(i, 1);
    };
  }
  /**
   * @param {Partial<Props>} props
   * @returns {void}
   */
  $set(e) {
    this.$$set && !At(e) && (this.$$.skip_bound = !0, this.$$set(e), this.$$.skip_bound = !1);
  }
}
const qt = "4";
typeof window < "u" && (window.__svelte || (window.__svelte = { v: /* @__PURE__ */ new Set() })).v.add(qt);
const H = [];
function It(t, e = D) {
  let n;
  const s = /* @__PURE__ */ new Set();
  function i(a) {
    if (at(t, a) && (t = a, n)) {
      const l = !H.length;
      for (const o of s)
        o[1](), H.push(o, t);
      if (l) {
        for (let o = 0; o < H.length; o += 2)
          H[o][0](H[o + 1]);
        H.length = 0;
      }
    }
  }
  function c(a) {
    i(a(t));
  }
  function d(a, l = D) {
    const o = [a, l];
    return s.add(o), s.size === 1 && (n = e(i, c) || D), a(t), () => {
      s.delete(o), s.size === 0 && n && (n(), n = null);
    };
  }
  return { set: i, update: c, subscribe: d };
}
let it = { access_token: null, token_type: null };
try {
  it = JSON.parse(localStorage.getItem("authToken")) || it;
} catch (t) {
  console.error(t);
}
const Jt = It(it);
Jt.subscribe((t) => {
  t && localStorage.setItem("authToken", JSON.stringify(t));
});
const zt = () => typeof window < "u" && "document" in window && "location" in window, nt = (t) => ({
  ...t.location,
  state: t.history.state,
  key: t.history.state && t.history.state.key || "initial"
}), Bt = (t) => {
  const e = [];
  let n = nt(t);
  return {
    get location() {
      return n;
    },
    listen(s) {
      e.push(s);
      const i = () => {
        n = nt(t), s({ location: n, action: "POP" });
      };
      return t.addEventListener("popstate", i), () => {
        t.removeEventListener("popstate", i);
        const c = e.indexOf(s);
        e.splice(c, 1);
      };
    },
    navigate(s, { state: i, replace: c = !1, preserveScroll: d = !1, blurActiveElement: a = !0 } = {}) {
      i = { ...i, key: Date.now() + "" };
      try {
        c ? t.history.replaceState(i, "", s) : t.history.pushState(i, "", s);
      } catch {
        t.location[c ? "replace" : "assign"](s);
      }
      n = nt(t), e.forEach(
        (l) => l({ location: n, action: "PUSH", preserveScroll: d })
      ), a && document.activeElement.blur();
    }
  };
}, Wt = (t = "/") => {
  let e = 0;
  const n = [{ pathname: t, search: "" }], s = [];
  return {
    get location() {
      return n[e];
    },
    addEventListener(i, c) {
    },
    removeEventListener(i, c) {
    },
    history: {
      get entries() {
        return n;
      },
      get index() {
        return e;
      },
      get state() {
        return s[e];
      },
      pushState(i, c, d) {
        const [a, l = ""] = d.split("?");
        e++, n.push({ pathname: a, search: l }), s.push(i);
      },
      replaceState(i, c, d) {
        const [a, l = ""] = d.split("?");
        n[e] = { pathname: a, search: l }, s[e] = i;
      }
    }
  };
};
Bt(
  zt() ? window : Wt()
);
let Ft = 0;
const Xt = (t) => t + ++Ft, ht = (t) => JSON.parse(JSON.stringify(t)), Vt = (t) => ({
  _state: t,
  _target: new EventTarget(),
  cid: Xt("model"),
  set: function(e, n) {
    const s = ht(this._state[e]);
    this._state[e] = n, this._target.dispatchEvent(new CustomEvent("change", {
      detail: {
        data: ht(this._state),
        previous: s,
        changed: { [e]: n }
      }
    }));
  },
  get: function(e) {
    return this._state[e];
  },
  on: function(e, n) {
    this._target.addEventListener(e, n);
  }
});
function Gt(t) {
  let e;
  return {
    c() {
      e = k("div"), w(e, "class", "container min-h-96 p-5");
    },
    m(n, s) {
      V(n, e, s), t[5](e);
    },
    p: D,
    i: D,
    o: D,
    d(n) {
      n && I(e), t[5](null);
    }
  };
}
function Et(t) {
  return t.startsWith("http://") || t.startsWith("https://");
}
async function Qt(t, e) {
  let n = document.querySelector(`link[id='${e}']`);
  if (n) {
    let s = (
      /** @type {HTMLLinkElement} */
      n.cloneNode()
    );
    s.href = t, s.addEventListener("load", () => n == null ? void 0 : n.remove()), s.addEventListener("error", () => n == null ? void 0 : n.remove()), n.after(s);
    return;
  }
  return new Promise((s) => {
    let i = Object.assign(document.createElement("link"), { rel: "stylesheet", href: t, onload: s });
    document.head.appendChild(i);
  });
}
function Yt(t, e) {
  let n = document.querySelector(`style[id='${e}']`);
  if (n) {
    n.textContent = t;
    return;
  }
  let s = Object.assign(document.createElement("style"), { id: e, type: "text/css" });
  s.appendChild(document.createTextNode(t)), document.head.appendChild(s);
}
async function Zt(t, e) {
  if (!(!t || !e))
    return Et(t) ? Qt(t, e) : Yt(t, e);
}
async function $t(t) {
  if (Et(t))
    return {
      module: await import(
        /* webpackIgnore: true */
        t
      ),
      url: t
    };
  let e = URL.createObjectURL(new Blob([t], { type: "text/javascript" })), n = await import(
    /* webpackIgnore: true */
    e
  );
  return URL.revokeObjectURL(e), { module: n.default, url: e };
}
function te(t, e, n) {
  let { task: s } = e, { components: i } = e, { componentData: c } = e, { dirty: d } = e, a;
  const l = [], o = async (u) => Object.fromEntries(await Promise.all(Object.values(u).map(async ({ name: g, esm: y }) => {
    const L = await $t(y);
    return [g, L];
  }))), p = async (u) => (Object.entries(u).forEach(([g, { css: y }]) => {
    Zt(y, g);
  }), o(u)), m = async () => {
    n(0, a.innerHTML = "", a);
    const u = await p(i);
    Object.entries(s).forEach(([g, { name: y, css: L, props: O }]) => {
      const { module: T } = u[y], { render: C } = T, b = document.createElement("div");
      a.appendChild(b), O = O || {};
      const v = c[g].annotation, K = c[g].datum, A = Vt({
        datum: K,
        annotation: v,
        props: O
      });
      A.on("change", ({ detail: E }) => {
        const { data: x } = E;
        c[g].annotation !== x.annotation && (n(1, c[g].annotation = x.annotation, c), n(2, d = !0));
      });
      const r = C({ el: b, model: A });
      r && l.push(r);
    });
  };
  Ct(() => (m(), () => {
    l.forEach((u) => u());
  }));
  function _(u) {
    F[u ? "unshift" : "push"](() => {
      a = u, n(0, a);
    });
  }
  return t.$$set = (u) => {
    "task" in u && n(3, s = u.task), "components" in u && n(4, i = u.components), "componentData" in u && n(1, c = u.componentData), "dirty" in u && n(2, d = u.dirty);
  }, [a, c, d, s, i, _];
}
class ee extends vt {
  constructor(e) {
    super(), wt(this, e, te, Gt, at, {
      task: 3,
      components: 4,
      componentData: 1,
      dirty: 2
    });
  }
}
function ne(t) {
  let e;
  return {
    c() {
      e = k("div"), e.innerHTML = "<h1>Not yet marked as complete. Press submit to mark as complete.</h1>", w(e, "class", "bg-gray-100 p-3 text-gray-400");
    },
    m(n, s) {
      V(n, e, s);
    },
    d(n) {
      n && I(e);
    }
  };
}
function se(t) {
  let e;
  return {
    c() {
      e = k("div"), e.innerHTML = "<h1>Marked as skipped.</h1>", w(e, "class", "bg-red-300 p-3");
    },
    m(n, s) {
      V(n, e, s);
    },
    d(n) {
      n && I(e);
    }
  };
}
function oe(t) {
  let e;
  return {
    c() {
      e = k("div"), e.innerHTML = "<h1>Marked as complete.</h1>", w(e, "class", "bg-green-300 p-3");
    },
    m(n, s) {
      V(n, e, s);
    },
    d(n) {
      n && I(e);
    }
  };
}
function re(t) {
  let e, n, s, i, c, d, a, l, o = (
    /*lastSaved*/
    t[6] ? `Last saved ${/*lastSaved*/
    t[6]}.` : ""
  ), p, m, _, u, g, y, L, O, T, C, b, v, K, A, r, E, x, M, N, Z, ct;
  function ut(f, S) {
    return (
      /*assignment*/
      f[0].is_complete ? oe : (
        /*assignment*/
        f[0].is_skipped ? se : ne
      )
    );
  }
  let G = ut(t), j = G(t);
  function St(f) {
    t[14](f);
  }
  function Lt(f) {
    t[15](f);
  }
  let $ = {
    task: (
      /*task*/
      t[3]
    ),
    components: (
      /*components*/
      t[2]
    )
  };
  return (
    /*componentData*/
    t[4] !== void 0 && ($.componentData = /*componentData*/
    t[4]), /*dirty*/
    t[5] !== void 0 && ($.dirty = /*dirty*/
    t[5]), s = new ee({ props: $ }), F.push(() => mt(s, "componentData", St)), F.push(() => mt(s, "dirty", Lt)), {
      c() {
        e = k("main"), j.c(), n = P(), Ht(s.$$.fragment), d = P(), a = k("div"), l = k("span"), p = z(o), m = P(), _ = k("div"), u = P(), g = k("span"), y = k("a"), L = z("@"), O = z(
          /*datum*/
          t[1]
        ), C = P(), b = k("div"), v = k("button"), K = z("Prev"), r = P(), E = k("button"), E.textContent = "Submit", x = P(), M = k("button"), M.textContent = "Skip", w(_, "class", "flex-1"), w(y, "href", T = "/annotate/" + /*datum*/
        t[1]), w(g, "class", "flex-none"), w(a, "class", "info text-sm text-gray-300 flex my-8"), w(v, "class", "btn btn-lg mx-4"), v.disabled = A = /*assignment*/
        t[0].prev === null, w(E, "class", "btn btn-lg mx-4 btn-success"), w(M, "class", "btn btn-lg mx-4 btn-error"), w(b, "class", "actions mx-auto max-w-fit svelte-19w63sy"), w(e, "class", "p-5");
      },
      m(f, S) {
        V(f, e, S), j.m(e, null), h(e, n), bt(s, e, null), h(e, d), h(e, a), h(a, l), h(l, p), h(a, m), h(a, _), h(a, u), h(a, g), h(g, y), h(y, L), h(y, O), h(e, C), h(e, b), h(b, v), h(v, K), h(b, r), h(b, E), h(b, x), h(b, M), N = !0, Z || (ct = [
          Q(
            window,
            "keydown",
            /*handleKeys*/
            t[7]
          ),
          Q(
            v,
            "click",
            /*handlePrev*/
            t[10]
          ),
          Q(
            E,
            "click",
            /*handleSubmit*/
            t[8]
          ),
          Q(
            M,
            "click",
            /*handleSkip*/
            t[9]
          )
        ], Z = !0);
      },
      p(f, [S]) {
        G !== (G = ut(f)) && (j.d(1), j = G(f), j && (j.c(), j.m(e, n)));
        const J = {};
        S & /*task*/
        8 && (J.task = /*task*/
        f[3]), S & /*components*/
        4 && (J.components = /*components*/
        f[2]), !i && S & /*componentData*/
        16 && (i = !0, J.componentData = /*componentData*/
        f[4], dt(() => i = !1)), !c && S & /*dirty*/
        32 && (c = !0, J.dirty = /*dirty*/
        f[5], dt(() => c = !1)), s.$set(J), (!N || S & /*lastSaved*/
        64) && o !== (o = /*lastSaved*/
        f[6] ? `Last saved ${/*lastSaved*/
        f[6]}.` : "") && ft(p, o), (!N || S & /*datum*/
        2) && ft(
          O,
          /*datum*/
          f[1]
        ), (!N || S & /*datum*/
        2 && T !== (T = "/annotate/" + /*datum*/
        f[1])) && w(y, "href", T), (!N || S & /*assignment*/
        1 && A !== (A = /*assignment*/
        f[0].prev === null)) && (v.disabled = A);
      },
      i(f) {
        N || (yt(s.$$.fragment, f), N = !0);
      },
      o(f) {
        Ut(s.$$.fragment, f), N = !1;
      },
      d(f) {
        f && I(e), j.d(), kt(s), Z = !1, X(ct);
      }
    }
  );
}
function ie(t, e, n) {
  let s, i, { datum: c } = e, { postAssignment: d } = e, { next: a } = e, { prev: l } = e, { assignment: o } = e, { components: p } = e, { task: m } = e, _ = !1, u;
  const g = (r) => r ? Object.fromEntries(Object.entries(r).map(([E, { annotation: x }]) => [E, JSON.stringify(x)])) : {}, y = (r) => {
    if (r.key === "Enter" && !r.ctrlKey && !r.metaKey) {
      if (r.preventDefault(), o.is_complete)
        return C();
      O();
    }
    r.key === "ArrowRight" && !r.ctrlKey && !r.metaKey && (r.preventDefault(), C()), r.key === "ArrowDown" && !r.ctrlKey && !r.metaKey && (r.preventDefault(), b()), r.key === "ArrowLeft" && !r.ctrlKey && !r.metaKey && (r.preventDefault(), v());
  }, L = async (r, E = !1, x = !1) => {
    if (!r)
      return;
    console.log("POST", r, E, x);
    const M = await d(r, c, E || !_ && o.is_complete, x);
    n(0, o = M), r = o.annotation, n(6, u = (/* @__PURE__ */ new Date()).toLocaleString());
  }, O = async () => {
    console.log("EXCUSE ME????"), console.log(i, _), await L(i, !0, !1), n(5, _ = !1);
  }, T = async () => {
    console.log("EXCUSE ME??"), await O(), await C();
  }, C = async () => (await L(i, o.is_complete, o.is_skipped), a(o)), b = async () => {
    n(5, _ = !0), await L(i, !1, !0);
  }, v = async () => (await L(i, o.is_complete, o.is_skipped), l(o));
  console.log("ANNOTATE WhEE"), console.log("A", o), console.log("A", m), console.log("A", p), console.log("A", s);
  function K(r) {
    s = r, n(4, s), n(0, o);
  }
  function A(r) {
    _ = r, n(5, _);
  }
  return t.$$set = (r) => {
    "datum" in r && n(1, c = r.datum), "postAssignment" in r && n(11, d = r.postAssignment), "next" in r && n(12, a = r.next), "prev" in r && n(13, l = r.prev), "assignment" in r && n(0, o = r.assignment), "components" in r && n(2, p = r.components), "task" in r && n(3, m = r.task);
  }, t.$$.update = () => {
    t.$$.dirty & /*assignment*/
    1 && n(4, s = o.components), t.$$.dirty & /*componentData*/
    16 && (i = g(s));
  }, [
    o,
    c,
    p,
    m,
    s,
    _,
    u,
    y,
    T,
    b,
    v,
    d,
    a,
    l,
    K,
    A
  ];
}
class ae extends vt {
  constructor(e) {
    super(), wt(this, e, ie, re, at, {
      datum: 1,
      postAssignment: 11,
      next: 12,
      prev: 13,
      assignment: 0,
      components: 2,
      task: 3
    });
  }
}
function ce(t, e) {
  return new Promise((n, s) => {
    const i = ({ name: c, data: d }) => {
      n(t.get(e)), t.off(c, i);
    };
    t.on(`on:${e}`, i), setTimeout(() => s(new Error("Timeout")), 2e3);
  });
}
const le = {
  render: ({ model: t, el: e }) => {
    const n = t.get("datum"), { task: s, components: i } = t.get("task"), c = t.get("assignment");
    t.on("change:datum", () => {
      o.$set({ datum: t.get("datum") });
    }), t.on("change:assignment", () => {
      o.$set({ assignment: t.get("assignment") });
    }), t.on("change:task", () => {
      const { task: p, components: m } = t.get("task");
      o.$set({ task: p, components: m });
    });
    const d = async (p, m, _ = !1, u = !1) => (t.set("result", {
      annotation: p,
      is_complete: _,
      is_skipped: u
    }), t.save_changes(), ce(t, "change:assignment")), a = async () => {
      t.set("datum", n + 1);
    }, l = async () => {
      t.send({ event: "prev" });
    };
    let o = new ae({
      target: e,
      props: {
        datum: n,
        task: s,
        components: i,
        assignment: c,
        postAssignment: d,
        prev: l,
        next: a
      }
    });
    return () => {
      o.$destroy();
    };
  }
};
export {
  le as default
};
//# sourceMappingURL=jupyter.js.map
