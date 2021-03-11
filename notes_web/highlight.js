/*! highlight.js v9.13.1 | BSD3 License | git.io/hljslicense
 * 本文件是从 Markdeep.js 中提取出来，并格式化了一遍的结果。
 * 多文件的源码:  https://github.com/isagalaev/highlight.js
 * 涵盖的高亮语言：
 *  armasm/arm, bash/sh/zsh, coffeescript/coffee/cson/iced, cpp/c/cc/h/c++/h++/hpp, cs/csharp/c#,
 *  css, glsl, go/golang, haskell/hs, http/https, java/jsp, javascript/js/jsx, json,
 *  kotlin/kt, lisp, lua, makefile/mk/mak, xml/html/xhtml/rss/atom/xjb/xsd/xsl/plist,
 *  markdown/md/mkdown/mkd, matlab, objectivec/mm/objc/obj-c, perl, php/php3/php4/php5/php6/php7,
 *  plaintext, python/py/gyp/ipython, pyxlscript, r, ruby/rb/gemspec/podspec/thor/irb,
 *  rust/rs, scheme, shell/console, sql, swift, tex, typescript/ts, yaml/yml/YAML
 */
!function(e) {
    var t = "object" == typeof window && window || "object" == typeof self && self;
    "undefined" != typeof exports ? e(exports) : t && (t.hljs = e({}), "function" == typeof define && define.amd && define([],
    function() {
        return t.hljs
    }))
} (function(e) {
    function t(e) {
        return e.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    }
    function r(e) {
        return e.nodeName.toLowerCase()
    }
    function a(e, t) {
        var r = e && e.exec(t);
        return r && 0 === r.index
    }
    function n(e) {
        return E.test(e)
    }
    function i(e) {
        var t, r, a, i, s = e.className + " ";
        if (s += e.parentNode ? e.parentNode.className: "", r = A.exec(s)) return v(r[1]) ? r[1] : "no-highlight";
        for (s = s.split(/\s+/), t = 0, a = s.length; a > t; t++) if (i = s[t], n(i) || v(i)) return i
    }
    function s(e) {
        var t, r = {},
        a = Array.prototype.slice.call(arguments, 1);
        for (t in e) r[t] = e[t];
        return a.forEach(function(e) {
            for (t in e) r[t] = e[t]
        }),
        r
    }
    function o(e) {
        var t = [];
        return function a(e, n) {
            for (var i = e.firstChild; i; i = i.nextSibling) 3 === i.nodeType ? n += i.nodeValue.length: 1 === i.nodeType && (t.push({
                event: "start",
                offset: n,
                node: i
            }), n = a(i, n), r(i).match(/br|hr|img|input/) || t.push({
                event: "stop",
                offset: n,
                node: i
            }));
            return n
        } (e, 0),
        t
    }
    function c(e, a, n) {
        function i() {
            return e.length && a.length ? e[0].offset !== a[0].offset ? e[0].offset < a[0].offset ? e: a: "start" === a[0].event ? e: a: e.length ? e: a
        }
        function s(e) {
            function a(e) {
                return " " + e.nodeName + '="' + t(e.value).replace('"', "&quot;") + '"'
            }
            u += "<" + r(e) + N.map.call(e.attributes, a).join("") + ">"
        }
        function o(e) {
            u += "</" + r(e) + ">"
        }
        function c(e) { ("start" === e.event ? s: o)(e.node)
        }
        for (var l = 0,
        u = "",
        d = []; e.length || a.length;) {
            var b = i();
            if (u += t(n.substring(l, b[0].offset)), l = b[0].offset, b === e) {
                d.reverse().forEach(o);
                do c(b.splice(0, 1)[0]),
                b = i();
                while (b === e && b.length && b[0].offset === l);
                d.reverse().forEach(s)
            } else "start" === b[0].event ? d.push(b[0].node) : d.pop(),
            c(b.splice(0, 1)[0])
        }
        return u + t(n.substr(l))
    }
    function l(e) {
        return e.v && !e.cached_variants && (e.cached_variants = e.v.map(function(t) {
            return s(e, {
                v: null
            },
            t)
        })),
        e.cached_variants || e.eW && [s(e)] || [e]
    }
    function u(e) {
        function t(e) {
            return e && e.source || e
        }
        function r(r, a) {
            return new RegExp(t(r), "m" + (e.cI ? "i": "") + (a ? "g": ""))
        }
        function a(n, i) {
            if (!n.compiled) {
                if (n.compiled = !0, n.k = n.k || n.bK, n.k) {
                    var s = {},
                    o = function(t, r) {
                        e.cI && (r = r.toLowerCase()),
                        r.split(" ").forEach(function(e) {
                            var r = e.split("|");
                            s[r[0]] = [t, r[1] ? Number(r[1]) : 1]
                        })
                    };
                    "string" == typeof n.k ? o("keyword", n.k) : C(n.k).forEach(function(e) {
                        o(e, n.k[e])
                    }),
                    n.k = s
                }
                n.lR = r(n.l || /\w+/, !0),
                i && (n.bK && (n.b = "\\b(" + n.bK.split(" ").join("|") + ")\\b"), n.b || (n.b = /\B|\b/), n.bR = r(n.b), n.endSameAsBegin && (n.e = n.b), n.e || n.eW || (n.e = /\B|\b/), n.e && (n.eR = r(n.e)), n.tE = t(n.e) || "", n.eW && i.tE && (n.tE += (n.e ? "|": "") + i.tE)),
                n.i && (n.iR = r(n.i)),
                null == n.r && (n.r = 1),
                n.c || (n.c = []),
                n.c = Array.prototype.concat.apply([], n.c.map(function(e) {
                    return l("self" === e ? n: e)
                })),
                n.c.forEach(function(e) {
                    a(e, n)
                }),
                n.starts && a(n.starts, i);
                var c = n.c.map(function(e) {
                    return e.bK ? "\\.?(" + e.b + ")\\.?": e.b
                }).concat([n.tE, n.i]).map(t).filter(Boolean);
                n.t = c.length ? r(c.join("|"), !0) : {
                    exec: function() {
                        return null
                    }
                }
            }
        }
        a(e)
    }
    function d(e, r, n, i) {
        function s(e) {
            return new RegExp(e.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&"), "m")
        }
        function o(e, t) {
            var r, n;
            for (r = 0, n = t.c.length; n > r; r++) if (a(t.c[r].bR, e)) return t.c[r].endSameAsBegin && (t.c[r].eR = s(t.c[r].bR.exec(e)[0])),
            t.c[r]
        }
        function c(e, t) {
            if (a(e.eR, t)) {
                for (; e.endsParent && e.parent;) e = e.parent;
                return e
            }
            return e.eW ? c(e.parent, t) : void 0
        }
        function l(e, t) {
            return ! n && a(t.iR, e)
        }
        function p(e, t) {
            var r = y.cI ? t[0].toLowerCase() : t[0];
            return e.k.hasOwnProperty(r) && e.k[r]
        }
        function m(e, t, r, a) {
            var n = a ? "": L.classPrefix,
            i = '<span class="' + n,
            s = r ? "": S;
            return i += e + '">',
            i + t + s
        }
        function g() {
            var e, r, a, n;
            if (!N.k) return t(E);
            for (n = "", r = 0, N.lR.lastIndex = 0, a = N.lR.exec(E); a;) n += t(E.substring(r, a.index)),
            e = p(N, a),
            e ? (A += e[1], n += m(e[0], t(a[0]))) : n += t(a[0]),
            r = N.lR.lastIndex,
            a = N.lR.exec(E);
            return n + t(E.substr(r))
        }
        function f() {
            var e = "string" == typeof N.sL;
            if (e && !M[N.sL]) return t(E);
            var r = e ? d(N.sL, E, !0, C[N.sL]) : b(E, N.sL.length ? N.sL: void 0);
            return N.r > 0 && (A += r.r),
            e && (C[N.sL] = r.top),
            m(r.language, r.value, !1, !0)
        }
        function _() {
            k += null != N.sL ? f() : g(),
            E = ""
        }
        function h(e) {
            k += e.cN ? m(e.cN, "", !0) : "",
            N = Object.create(e, {
                parent: {
                    value: N
                }
            })
        }
        function x(e, t) {
            if (E += e, null == t) return _(),
            0;
            var r = o(t, N);
            if (r) return r.skip ? E += t: (r.eB && (E += t), _(), r.rB || r.eB || (E = t)),
            h(r, t),
            r.rB ? 0 : t.length;
            var a = c(N, t);
            if (a) {
                var n = N;
                n.skip ? E += t: (n.rE || n.eE || (E += t), _(), n.eE && (E = t));
                do N.cN && (k += S),
                N.skip || N.sL || (A += N.r),
                N = N.parent;
                while (N !== a.parent);
                return a.starts && (a.endSameAsBegin && (a.starts.eR = a.eR), h(a.starts, "")),
                n.rE ? 0 : t.length
            }
            if (l(t, N)) throw new Error('Illegal lexeme "' + t + '" for mode "' + (N.cN || "<unnamed>") + '"');
            return E += t,
            t.length || 1
        }
        var y = v(e);
        if (!y) throw new Error('Unknown language: "' + e + '"');
        u(y);
        var w, N = i || y,
        C = {},
        k = "";
        for (w = N; w !== y; w = w.parent) w.cN && (k = m(w.cN, "", !0) + k);
        var E = "",
        A = 0;
        try {
            for (var B, I, T = 0;;) {
                if (N.t.lastIndex = T, B = N.t.exec(r), !B) break;
                I = x(r.substring(T, B.index), B[0]),
                T = B.index + I
            }
            for (x(r.substr(T)), w = N; w.parent; w = w.parent) w.cN && (k += S);
            return {
                r: A,
                value: k,
                language: e,
                top: N
            }
        } catch(R) {
            if (R.message && -1 !== R.message.indexOf("Illegal")) return {
                r: 0,
                value: t(r)
            };
            throw R
        }
    }
    function b(e, r) {
        r = r || L.languages || C(M);
        var a = {
            r: 0,
            value: t(e)
        },
        n = a;
        return r.filter(v).filter(w).forEach(function(t) {
            var r = d(t, e, !1);
            r.language = t,
            r.r > n.r && (n = r),
            r.r > a.r && (n = a, a = r)
        }),
        n.language && (a.second_best = n),
        a
    }
    function p(e) {
        return L.tabReplace || L.useBR ? e.replace(B,
        function(e, t) {
            return L.useBR && "\n" === e ? "<br>": L.tabReplace ? t.replace(/\t/g, L.tabReplace) : ""
        }) : e
    }
    function m(e, t, r) {
        var a = t ? k[t] : r,
        n = [e.trim()];
        return e.match(/\bhljs\b/) || n.push("hljs"),
        -1 === e.indexOf(a) && n.push(a),
        n.join(" ").trim()
    }
    function g(e) {
        var t, r, a, s, l, u = i(e);
        n(u) || (L.useBR ? (t = document.createElementNS("http://www.w3.org/1999/xhtml", "div"), t.innerHTML = e.innerHTML.replace(/\n/g, "").replace(/<br[ \/]*>/g, "\n")) : t = e, l = t.textContent, a = u ? d(u, l, !0) : b(l), r = o(t), r.length && (s = document.createElementNS("http://www.w3.org/1999/xhtml", "div"), s.innerHTML = a.value, a.value = c(r, o(s), l)), a.value = p(a.value), e.innerHTML = a.value, e.className = m(e.className, u, a.language), e.result = {
            language: a.language,
            re: a.r
        },
        a.second_best && (e.second_best = {
            language: a.second_best.language,
            re: a.second_best.r
        }))
    }
    function f(e) {
        L = s(L, e)
    }
    function _() {
        if (!_.called) {
            _.called = !0;
            var e = document.querySelectorAll("pre code");
            N.forEach.call(e, g)
        }
    }
    function h() {
        addEventListener("DOMContentLoaded", _, !1),
        addEventListener("load", _, !1)
    }
    function x(t, r) {
        var a = M[t] = r(e);
        a.aliases && a.aliases.forEach(function(e) {
            k[e] = t
        })
    }
    function y() {
        return C(M)
    }
    function v(e) {
        return e = (e || "").toLowerCase(),
        M[e] || M[k[e]]
    }
    function w(e) {
        var t = v(e);
        return t && !t.disableAutodetect
    }
    var N = [],
    C = Object.keys,
    M = {},
    k = {},
    E = /^(no-?highlight|plain|text)$/i,
    A = /\blang(?:uage)?-([\w-]+)\b/i,
    B = /((^(<[^>]+>|\t|)+|(?:\n)))/gm,
    S = "</span>",
    L = {
        classPrefix: "hljs-",
        tabReplace: null,
        useBR: !1,
        languages: void 0
    };
    return e.highlight = d,
    e.highlightAuto = b,
    e.fixMarkup = p,
    e.highlightBlock = g,
    e.configure = f,
    e.initHighlighting = _,
    e.initHighlightingOnLoad = h,
    e.registerLanguage = x,
    e.listLanguages = y,
    e.getLanguage = v,
    e.autoDetection = w,
    e.inherit = s,
    e.IR = "[a-zA-Z]\\w*",
    e.UIR = "[a-zA-Z_]\\w*",
    e.NR = "\\b\\d+(\\.\\d+)?",
    e.CNR = "(-?)(\\b0[xX][a-fA-F0-9]+|(\\b\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]?\\d+)?)",
    e.BNR = "\\b(0b[01]+)",
    e.RSR = "!|!=|!==|%|%=|&|&&|&=|\\*|\\*=|\\+|\\+=|,|-|-=|/=|/|:|;|<<|<<=|<=|<|===|==|=|>>>=|>>=|>=|>>>|>>|>|\\?|\\[|\\{|\\(|\\^|\\^=|\\||\\|=|\\|\\||~",
    e.BE = {
        b: "\\\\[\\s\\S]",
        r: 0
    },
    e.ASM = {
        cN: "string",
        b: "'",
        e: "'",
        i: "\\n",
        c: [e.BE]
    },
    e.QSM = {
        cN: "string",
        b: '"',
        e: '"',
        i: "\\n",
        c: [e.BE]
    },
    e.PWM = {
        b: /\b(a|an|the|are|I'm|isn't|don't|doesn't|won't|but|just|should|pretty|simply|enough|gonna|going|wtf|so|such|will|you|your|they|like|more)\b/
    },
    e.C = function(t, r, a) {
        var n = e.inherit({
            cN: "comment",
            b: t,
            e: r,
            c: []
        },
        a || {});
        return n.c.push(e.PWM),
        n.c.push({
            cN: "doctag",
            b: "(?:TODO|FIXME|NOTE|BUG|XXX):",
            r: 0
        }),
        n
    },
    e.CLCM = e.C("//", "$"),
    e.CBCM = e.C("/\\*", "\\*/"),
    e.HCM = e.C("#", "$"),
    e.NM = {
        cN: "number",
        b: e.NR,
        r: 0
    },
    e.CNM = {
        cN: "number",
        b: e.CNR,
        r: 0
    },
    e.BNM = {
        cN: "number",
        b: e.BNR,
        r: 0
    },
    e.CSSNM = {
        cN: "number",
        b: e.NR + "(%|em|ex|ch|rem|vw|vh|vmin|vmax|cm|mm|in|pt|pc|px|deg|grad|rad|turn|s|ms|Hz|kHz|dpi|dpcm|dppx)?",
        r: 0
    },
    e.RM = {
        cN: "regexp",
        b: /\//,
        e: /\/[gimuy]*/,
        i: /\n/,
        c: [e.BE, {
            b: /\[/,
            e: /\]/,
            r: 0,
            c: [e.BE]
        }]
    },
    e.TM = {
        cN: "title",
        b: e.IR,
        r: 0
    },
    e.UTM = {
        cN: "title",
        b: e.UIR,
        r: 0
    },
    e.METHOD_GUARD = {
        b: "\\.\\s*" + e.UIR,
        r: 0
    },
    e.registerLanguage("armasm",
    function(e) {
        return {
            cI: !0,
            aliases: ["arm"],
            l: "\\.?" + e.IR,
            k: {
                meta: ".2byte .4byte .align .ascii .asciz .balign .byte .code .data .else .end .endif .endm .endr .equ .err .exitm .extern .global .hword .if .ifdef .ifndef .include .irp .long .macro .rept .req .section .set .skip .space .text .word .arm .thumb .code16 .code32 .force_thumb .thumb_func .ltorg ALIAS ALIGN ARM AREA ASSERT ATTR CN CODE CODE16 CODE32 COMMON CP DATA DCB DCD DCDU DCDO DCFD DCFDU DCI DCQ DCQU DCW DCWU DN ELIF ELSE END ENDFUNC ENDIF ENDP ENTRY EQU EXPORT EXPORTAS EXTERN FIELD FILL FUNCTION GBLA GBLL GBLS GET GLOBAL IF IMPORT INCBIN INCLUDE INFO KEEP LCLA LCLL LCLS LTORG MACRO MAP MEND MEXIT NOFP OPT PRESERVE8 PROC QN READONLY RELOC REQUIRE REQUIRE8 RLIST FN ROUT SETA SETL SETS SN SPACE SUBT THUMB THUMBX TTL WHILE WEND ",
                built_in: "r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 pc lr sp ip sl sb fp a1 a2 a3 a4 v1 v2 v3 v4 v5 v6 v7 v8 f0 f1 f2 f3 f4 f5 f6 f7 p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 q0 q1 q2 q3 q4 q5 q6 q7 q8 q9 q10 q11 q12 q13 q14 q15 cpsr_c cpsr_x cpsr_s cpsr_f cpsr_cx cpsr_cxs cpsr_xs cpsr_xsf cpsr_sf cpsr_cxsf spsr_c spsr_x spsr_s spsr_f spsr_cx spsr_cxs spsr_xs spsr_xsf spsr_sf spsr_cxsf s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 s14 s15 s16 s17 s18 s19 s20 s21 s22 s23 s24 s25 s26 s27 s28 s29 s30 s31 d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11 d12 d13 d14 d15 d16 d17 d18 d19 d20 d21 d22 d23 d24 d25 d26 d27 d28 d29 d30 d31 {PC} {VAR} {TRUE} {FALSE} {OPT} {CONFIG} {ENDIAN} {CODESIZE} {CPU} {FPU} {ARCHITECTURE} {PCSTOREOFFSET} {ARMASM_VERSION} {INTER} {ROPI} {RWPI} {SWST} {NOSWST} . @"
            },
            c: [{
                cN: "keyword",
                b: "\\b(adc|(qd?|sh?|u[qh]?)?add(8|16)?|usada?8|(q|sh?|u[qh]?)?(as|sa)x|and|adrl?|sbc|rs[bc]|asr|b[lx]?|blx|bxj|cbn?z|tb[bh]|bic|bfc|bfi|[su]bfx|bkpt|cdp2?|clz|clrex|cmp|cmn|cpsi[ed]|cps|setend|dbg|dmb|dsb|eor|isb|it[te]{0,3}|lsl|lsr|ror|rrx|ldm(([id][ab])|f[ds])?|ldr((s|ex)?[bhd])?|movt?|mvn|mra|mar|mul|[us]mull|smul[bwt][bt]|smu[as]d|smmul|smmla|mla|umlaal|smlal?([wbt][bt]|d)|mls|smlsl?[ds]|smc|svc|sev|mia([bt]{2}|ph)?|mrr?c2?|mcrr2?|mrs|msr|orr|orn|pkh(tb|bt)|rbit|rev(16|sh)?|sel|[su]sat(16)?|nop|pop|push|rfe([id][ab])?|stm([id][ab])?|str(ex)?[bhd]?|(qd?)?sub|(sh?|q|u[qh]?)?sub(8|16)|[su]xt(a?h|a?b(16)?)|srs([id][ab])?|swpb?|swi|smi|tst|teq|wfe|wfi|yield)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al|hs|lo)?[sptrx]?",
                e: "\\s"
            },
            e.C("[;@]", "$", {
                r: 0
            }), e.CBCM, e.QSM, {
                cN: "string",
                b: "'",
                e: "[^\\\\]'",
                r: 0
            },
            {
                cN: "title",
                b: "\\|",
                e: "\\|",
                i: "\\n",
                r: 0
            },
            {
                cN: "number",
                v: [{
                    b: "[#$=]?0x[0-9a-f]+"
                },
                {
                    b: "[#$=]?0b[01]+"
                },
                {
                    b: "[#$=]\\d+"
                },
                {
                    b: "\\b\\d+"
                }],
                r: 0
            },
            {
                cN: "symbol",
                v: [{
                    b: "^[a-z_\\.\\$][a-z0-9_\\.\\$]+"
                },
                {
                    b: "^\\s*[a-z_\\.\\$][a-z0-9_\\.\\$]+:"
                },
                {
                    b: "[=#]\\w+"
                }],
                r: 0
            }]
        }
    }),
    e.registerLanguage("bash",
    function(e) {
        var t = {
            cN: "variable",
            v: [{
                b: /\$[\w\d#@][\w\d_]*/
            },
            {
                b: /\$\{(.*?)}/
            }]
        },
        r = {
            cN: "string",
            b: /"/,
            e: /"/,
            c: [e.BE, t, {
                cN: "variable",
                b: /\$\(/,
                e: /\)/,
                c: [e.BE]
            }]
        },
        a = {
            cN: "string",
            b: /'/,
            e: /'/
        };
        return {
            aliases: ["sh", "zsh"],
            l: /\b-?[a-z\._]+\b/,
            k: {
                keyword: "if then else elif fi for while in do done case esac function",
                literal: "true false",
                built_in: "break cd continue eval exec exit export getopts hash pwd readonly return shift test times trap umask unset alias bind builtin caller command declare echo enable help let local logout mapfile printf read readarray source type typeset ulimit unalias set shopt autoload bg bindkey bye cap chdir clone comparguments compcall compctl compdescribe compfiles compgroups compquote comptags comptry compvalues dirs disable disown echotc echoti emulate fc fg float functions getcap getln history integer jobs kill limit log noglob popd print pushd pushln rehash sched setcap setopt stat suspend ttyctl unfunction unhash unlimit unsetopt vared wait whence where which zcompile zformat zftp zle zmodload zparseopts zprof zpty zregexparse zsocket zstyle ztcp",
                _: "-ne -eq -lt -gt -f -d -e -s -l -a"
            },
            c: [{
                cN: "meta",
                b: /^#![^\n]+sh\s*$/,
                r: 10
            },
            {
                cN: "function",
                b: /\w[\w\d_]*\s*\(\s*\)\s*\{/,
                rB: !0,
                c: [e.inherit(e.TM, {
                    b: /\w[\w\d_]*/
                })],
                r: 0
            },
            e.HCM, r, a, t]
        }
    }),
    e.registerLanguage("coffeescript",
    function(e) {
        var t = {
            keyword: "in if for while finally new do return else break catch instanceof throw try this switch continue typeof delete debugger super yield import export from as default await then unless until loop of by when and or is isnt not",
            literal: "true false null undefined yes no on off",
            built_in: "npm require console print module global window document"
        },
        r = "[A-Za-z$_][0-9A-Za-z$_]*",
        a = {
            cN: "subst",
            b: /#\{/,
            e: /}/,
            k: t
        },
        n = [e.BNM, e.inherit(e.CNM, {
            starts: {
                e: "(\\s*/)?",
                r: 0
            }
        }), {
            cN: "string",
            v: [{
                b: /'''/,
                e: /'''/,
                c: [e.BE]
            },
            {
                b: /'/,
                e: /'/,
                c: [e.BE]
            },
            {
                b: /"""/,
                e: /"""/,
                c: [e.BE, a]
            },
            {
                b: /"/,
                e: /"/,
                c: [e.BE, a]
            }]
        },
        {
            cN: "regexp",
            v: [{
                b: "///",
                e: "///",
                c: [a, e.HCM]
            },
            {
                b: "//[gim]*",
                r: 0
            },
            {
                b: /\/(?![ *])(\\\/|.)*?\/[gim]*(?=\W|$)/
            }]
        },
        {
            b: "@" + r
        },
        {
            sL: "javascript",
            eB: !0,
            eE: !0,
            v: [{
                b: "```",
                e: "```"
            },
            {
                b: "`",
                e: "`"
            }]
        }];
        a.c = n;
        var i = e.inherit(e.TM, {
            b: r
        }),
        s = "(\\(.*\\))?\\s*\\B[-=]>",
        o = {
            cN: "params",
            b: "\\([^\\(]",
            rB: !0,
            c: [{
                b: /\(/,
                e: /\)/,
                k: t,
                c: ["self"].concat(n)
            }]
        };
        return {
            aliases: ["coffee", "cson", "iced"],
            k: t,
            i: /\/\*/,
            c: n.concat([e.C("###", "###"), e.HCM, {
                cN: "function",
                b: "^\\s*" + r + "\\s*=\\s*" + s,
                e: "[-=]>",
                rB: !0,
                c: [i, o]
            },
            {
                b: /[:\(,=]\s*/,
                r: 0,
                c: [{
                    cN: "function",
                    b: s,
                    e: "[-=]>",
                    rB: !0,
                    c: [o]
                }]
            },
            {
                cN: "class",
                bK: "class",
                e: "$",
                i: /[:="\[\]]/,
                c: [{
                    bK: "extends",
                    eW: !0,
                    i: /[:="\[\]]/,
                    c: [i]
                },
                i]
            },
            {
                b: r + ":",
                e: ":",
                rB: !0,
                rE: !0,
                r: 0
            }])
        }
    }),
    e.registerLanguage("cpp",
    function(e) {
        var t = {
            cN: "keyword",
            b: "\\b[a-z\\d_]*_t\\b"
        },
        r = {
            cN: "string",
            v: [{
                b: '(u8?|U|L)?"',
                e: '"',
                i: "\\n",
                c: [e.BE]
            },
            {
                b: '(u8?|U|L)?R"\\(',
                e: '\\)"'
            },
            {
                b: "'\\\\?.",
                e: "'",
                i: "."
            }]
        },
        a = {
            cN: "number",
            v: [{
                b: "\\b(0b[01']+)"
            },
            {
                b: "(-?)\\b([\\d']+(\\.[\\d']*)?|\\.[\\d']+)(u|U|l|L|ul|UL|f|F|b|B)"
            },
            {
                b: "(-?)(\\b0[xX][a-fA-F0-9']+|(\\b[\\d']+(\\.[\\d']*)?|\\.[\\d']+)([eE][-+]?[\\d']+)?)"
            }],
            r: 0
        },
        n = {
            cN: "meta",
            b: /#\s*[a-z]+\b/,
            e: /$/,
            k: {
                "meta-keyword": "if else elif endif define undef warning error line pragma ifdef ifndef include"
            },
            c: [{
                b: /\\\n/,
                r: 0
            },
            e.inherit(r, {
                cN: "meta-string"
            }), {
                cN: "meta-string",
                b: /<[^\n>]*>/,
                e: /$/,
                i: "\\n"
            },
            e.CLCM, e.CBCM]
        },
        i = e.IR + "\\s*\\(",
        s = {
            keyword: "int float while private char catch import module export virtual operator sizeof dynamic_cast|10 typedef const_cast|10 const for static_cast|10 union namespace unsigned long volatile static protected bool template mutable if public friend do goto auto void enum else break extern using asm case typeid short reinterpret_cast|10 default double register explicit signed typename try this switch continue inline delete alignof constexpr decltype noexcept static_assert thread_local restrict _Bool complex _Complex _Imaginary atomic_bool atomic_char atomic_schar atomic_uchar atomic_short atomic_ushort atomic_int atomic_uint atomic_long atomic_ulong atomic_llong atomic_ullong new throw return and or not",
            built_in: "std string cin cout cerr clog stdin stdout stderr stringstream istringstream ostringstream auto_ptr deque list queue stack vector map set bitset multiset multimap unordered_set unordered_map unordered_multiset unordered_multimap array shared_ptr abort abs acos asin atan2 atan calloc ceil cosh cos exit exp fabs floor fmod fprintf fputs free frexp fscanf isalnum isalpha iscntrl isdigit isgraph islower isprint ispunct isspace isupper isxdigit tolower toupper labs ldexp log10 log malloc realloc memchr memcmp memcpy memset modf pow printf putchar puts scanf sinh sin snprintf sprintf sqrt sscanf strcat strchr strcmp strcpy strcspn strlen strncat strncmp strncpy strpbrk strrchr strspn strstr tanh tan vfprintf vprintf vsprintf endl initializer_list unique_ptr",
            literal: "true false nullptr NULL"
        },
        o = [t, e.CLCM, e.CBCM, a, r];
        return {
            aliases: ["c", "cc", "h", "c++", "h++", "hpp"],
            k: s,
            i: "</",
            c: o.concat([n, {
                b: "\\b(deque|list|queue|stack|vector|map|set|bitset|multiset|multimap|unordered_map|unordered_set|unordered_multiset|unordered_multimap|array)\\s*<",
                e: ">",
                k: s,
                c: ["self", t]
            },
            {
                b: e.IR + "::",
                k: s
            },
            {
                v: [{
                    b: /=/,
                    e: /;/
                },
                {
                    b: /\(/,
                    e: /\)/
                },
                {
                    bK: "new throw return else",
                    e: /;/
                }],
                k: s,
                c: o.concat([{
                    b: /\(/,
                    e: /\)/,
                    k: s,
                    c: o.concat(["self"]),
                    r: 0
                }]),
                r: 0
            },
            {
                cN: "function",
                b: "(" + e.IR + "[\\*&\\s]+)+" + i,
                rB: !0,
                e: /[{;=]/,
                eE: !0,
                k: s,
                i: /[^\w\s\*&]/,
                c: [{
                    b: i,
                    rB: !0,
                    c: [e.TM],
                    r: 0
                },
                {
                    cN: "params",
                    b: /\(/,
                    e: /\)/,
                    k: s,
                    r: 0,
                    c: [e.CLCM, e.CBCM, r, a, t, {
                        b: /\(/,
                        e: /\)/,
                        k: s,
                        r: 0,
                        c: ["self", e.CLCM, e.CBCM, r, a, t]
                    }]
                },
                e.CLCM, e.CBCM, n]
            },
            {
                cN: "class",
                bK: "class struct",
                e: /[{;:]/,
                c: [{
                    b: /</,
                    e: />/,
                    c: ["self"]
                },
                e.TM]
            }]),
            exports: {
                preprocessor: n,
                strings: r,
                k: s
            }
        }
    }),
    e.registerLanguage("cs",
    function(e) {
        var t = {
            keyword: "abstract as base bool break byte case catch char checked const continue decimal default delegate do double enum event explicit extern finally fixed float for foreach goto if implicit in int interface internal is lock long nameof object operator out override params private protected public readonly ref sbyte sealed short sizeof stackalloc static string struct switch this try typeof uint ulong unchecked unsafe ushort using virtual void volatile while add alias ascending async await by descending dynamic equals from get global group into join let on orderby partial remove select set value var where yield",
            literal: "null false true"
        },
        r = {
            cN: "number",
            v: [{
                b: "\\b(0b[01']+)"
            },
            {
                b: "(-?)\\b([\\d']+(\\.[\\d']*)?|\\.[\\d']+)(u|U|l|L|ul|UL|f|F|b|B)"
            },
            {
                b: "(-?)(\\b0[xX][a-fA-F0-9']+|(\\b[\\d']+(\\.[\\d']*)?|\\.[\\d']+)([eE][-+]?[\\d']+)?)"
            }],
            r: 0
        },
        a = {
            cN: "string",
            b: '@"',
            e: '"',
            c: [{
                b: '""'
            }]
        },
        n = e.inherit(a, {
            i: /\n/
        }),
        i = {
            cN: "subst",
            b: "{",
            e: "}",
            k: t
        },
        s = e.inherit(i, {
            i: /\n/
        }),
        o = {
            cN: "string",
            b: /\$"/,
            e: '"',
            i: /\n/,
            c: [{
                b: "{{"
            },
            {
                b: "}}"
            },
            e.BE, s]
        },
        c = {
            cN: "string",
            b: /\$@"/,
            e: '"',
            c: [{
                b: "{{"
            },
            {
                b: "}}"
            },
            {
                b: '""'
            },
            i]
        },
        l = e.inherit(c, {
            i: /\n/,
            c: [{
                b: "{{"
            },
            {
                b: "}}"
            },
            {
                b: '""'
            },
            s]
        });
        i.c = [c, o, a, e.ASM, e.QSM, r, e.CBCM],
        s.c = [l, o, n, e.ASM, e.QSM, r, e.inherit(e.CBCM, {
            i: /\n/
        })];
        var u = {
            v: [c, o, a, e.ASM, e.QSM]
        },
        d = e.IR + "(<" + e.IR + "(\\s*,\\s*" + e.IR + ")*>)?(\\[\\])?";
        return {
            aliases: ["csharp", "c#"],
            k: t,
            i: /::/,
            c: [e.C("///", "$", {
                rB: !0,
                c: [{
                    cN: "doctag",
                    v: [{
                        b: "///",
                        r: 0
                    },
                    {
                        b: "<!--|-->"
                    },
                    {
                        b: "</?",
                        e: ">"
                    }]
                }]
            }), e.CLCM, e.CBCM, {
                cN: "meta",
                b: "#",
                e: "$",
                k: {
                    "meta-keyword": "if else elif endif define undef warning error line region endregion pragma checksum"
                }
            },
            u, r, {
                bK: "class interface",
                e: /[{;=]/,
                i: /[^\s:,]/,
                c: [e.TM, e.CLCM, e.CBCM]
            },
            {
                bK: "namespace",
                e: /[{;=]/,
                i: /[^\s:]/,
                c: [e.inherit(e.TM, {
                    b: "[a-zA-Z](\\.?\\w)*"
                }), e.CLCM, e.CBCM]
            },
            {
                cN: "meta",
                b: "^\\s*\\[",
                eB: !0,
                e: "\\]",
                eE: !0,
                c: [{
                    cN: "meta-string",
                    b: /"/,
                    e: /"/
                }]
            },
            {
                bK: "new return throw await else",
                r: 0
            },
            {
                cN: "function",
                b: "(" + d + "\\s+)+" + e.IR + "\\s*\\(",
                rB: !0,
                e: /\s*[{;=]/,
                eE: !0,
                k: t,
                c: [{
                    b: e.IR + "\\s*\\(",
                    rB: !0,
                    c: [e.TM],
                    r: 0
                },
                {
                    cN: "params",
                    b: /\(/,
                    e: /\)/,
                    eB: !0,
                    eE: !0,
                    k: t,
                    r: 0,
                    c: [u, r, e.CBCM]
                },
                e.CLCM, e.CBCM]
            }]
        }
    }),
    e.registerLanguage("css",
    function(e) {
        var t = "[a-zA-Z-][a-zA-Z0-9_-]*",
        r = {
            b: /[A-Z\_\.\-]+\s*:/,
            rB: !0,
            e: ";",
            eW: !0,
            c: [{
                cN: "attribute",
                b: /\S/,
                e: ":",
                eE: !0,
                starts: {
                    eW: !0,
                    eE: !0,
                    c: [{
                        b: /[\w-]+\(/,
                        rB: !0,
                        c: [{
                            cN: "built_in",
                            b: /[\w-]+/
                        },
                        {
                            b: /\(/,
                            e: /\)/,
                            c: [e.ASM, e.QSM]
                        }]
                    },
                    e.CSSNM, e.QSM, e.ASM, e.CBCM, {
                        cN: "number",
                        b: "#[0-9A-Fa-f]+"
                    },
                    {
                        cN: "meta",
                        b: "!important"
                    }]
                }
            }]
        };
        return {
            cI: !0,
            i: /[=\/|'\$]/,
            c: [e.CBCM, {
                cN: "selector-id",
                b: /#[A-Za-z0-9_-]+/
            },
            {
                cN: "selector-class",
                b: /\.[A-Za-z0-9_-]+/
            },
            {
                cN: "selector-attr",
                b: /\[/,
                e: /\]/,
                i: "$"
            },
            {
                cN: "selector-pseudo",
                b: /:(:)?[a-zA-Z0-9\_\-\+\(\)"'.]+/
            },
            {
                b: "@(font-face|page)",
                l: "[a-z-]+",
                k: "font-face page"
            },
            {
                b: "@",
                e: "[{;]",
                i: /:/,
                c: [{
                    cN: "keyword",
                    b: /\w+/
                },
                {
                    b: /\s/,
                    eW: !0,
                    eE: !0,
                    r: 0,
                    c: [e.ASM, e.QSM, e.CSSNM]
                }]
            },
            {
                cN: "selector-tag",
                b: t,
                r: 0
            },
            {
                b: "{",
                e: "}",
                i: /\S/,
                c: [e.CBCM, r]
            }]
        }
    }),
    e.registerLanguage("glsl",
    function(e) {
        return {
            k: {
                keyword: "break continue discard do else for if return while switch case default attribute binding buffer ccw centroid centroid varying coherent column_major const cw depth_any depth_greater depth_less depth_unchanged early_fragment_tests equal_spacing flat fractional_even_spacing fractional_odd_spacing highp in index inout invariant invocations isolines layout line_strip lines lines_adjacency local_size_x local_size_y local_size_z location lowp max_vertices mediump noperspective offset origin_upper_left out packed patch pixel_center_integer point_mode points precise precision quads r11f_g11f_b10f r16 r16_snorm r16f r16i r16ui r32f r32i r32ui r8 r8_snorm r8i r8ui readonly restrict rg16 rg16_snorm rg16f rg16i rg16ui rg32f rg32i rg32ui rg8 rg8_snorm rg8i rg8ui rgb10_a2 rgb10_a2ui rgba16 rgba16_snorm rgba16f rgba16i rgba16ui rgba32f rgba32i rgba32ui rgba8 rgba8_snorm rgba8i rgba8ui row_major sample shared smooth std140 std430 stream triangle_strip triangles triangles_adjacency uniform varying vertices volatile writeonly",
                type: "atomic_uint bool bvec2 bvec3 bvec4 dmat2 dmat2x2 dmat2x3 dmat2x4 dmat3 dmat3x2 dmat3x3 dmat3x4 dmat4 dmat4x2 dmat4x3 dmat4x4 double dvec2 dvec3 dvec4 float iimage1D iimage1DArray iimage2D iimage2DArray iimage2DMS iimage2DMSArray iimage2DRect iimage3D iimageBufferiimageCube iimageCubeArray image1D image1DArray image2D image2DArray image2DMS image2DMSArray image2DRect image3D imageBuffer imageCube imageCubeArray int isampler1D isampler1DArray isampler2D isampler2DArray isampler2DMS isampler2DMSArray isampler2DRect isampler3D isamplerBuffer isamplerCube isamplerCubeArray ivec2 ivec3 ivec4 mat2 mat2x2 mat2x3 mat2x4 mat3 mat3x2 mat3x3 mat3x4 mat4 mat4x2 mat4x3 mat4x4 sampler1D sampler1DArray sampler1DArrayShadow sampler1DShadow sampler2D sampler2DArray sampler2DArrayShadow sampler2DMS sampler2DMSArray sampler2DRect sampler2DRectShadow sampler2DShadow sampler3D samplerBuffer samplerCube samplerCubeArray samplerCubeArrayShadow samplerCubeShadow image1D uimage1DArray uimage2D uimage2DArray uimage2DMS uimage2DMSArray uimage2DRect uimage3D uimageBuffer uimageCube uimageCubeArray uint usampler1D usampler1DArray usampler2D usampler2DArray usampler2DMS usampler2DMSArray usampler2DRect usampler3D samplerBuffer usamplerCube usamplerCubeArray uvec2 uvec3 uvec4 vec2 vec3 vec4 void",
                built_in: "gl_MaxAtomicCounterBindings gl_MaxAtomicCounterBufferSize gl_MaxClipDistances gl_MaxClipPlanes gl_MaxCombinedAtomicCounterBuffers gl_MaxCombinedAtomicCounters gl_MaxCombinedImageUniforms gl_MaxCombinedImageUnitsAndFragmentOutputs gl_MaxCombinedTextureImageUnits gl_MaxComputeAtomicCounterBuffers gl_MaxComputeAtomicCounters gl_MaxComputeImageUniforms gl_MaxComputeTextureImageUnits gl_MaxComputeUniformComponents gl_MaxComputeWorkGroupCount gl_MaxComputeWorkGroupSize gl_MaxDrawBuffers gl_MaxFragmentAtomicCounterBuffers gl_MaxFragmentAtomicCounters gl_MaxFragmentImageUniforms gl_MaxFragmentInputComponents gl_MaxFragmentInputVectors gl_MaxFragmentUniformComponents gl_MaxFragmentUniformVectors gl_MaxGeometryAtomicCounterBuffers gl_MaxGeometryAtomicCounters gl_MaxGeometryImageUniforms gl_MaxGeometryInputComponents gl_MaxGeometryOutputComponents gl_MaxGeometryOutputVertices gl_MaxGeometryTextureImageUnits gl_MaxGeometryTotalOutputComponents gl_MaxGeometryUniformComponents gl_MaxGeometryVaryingComponents gl_MaxImageSamples gl_MaxImageUnits gl_MaxLights gl_MaxPatchVertices gl_MaxProgramTexelOffset gl_MaxTessControlAtomicCounterBuffers gl_MaxTessControlAtomicCounters gl_MaxTessControlImageUniforms gl_MaxTessControlInputComponents gl_MaxTessControlOutputComponents gl_MaxTessControlTextureImageUnits gl_MaxTessControlTotalOutputComponents gl_MaxTessControlUniformComponents gl_MaxTessEvaluationAtomicCounterBuffers gl_MaxTessEvaluationAtomicCounters gl_MaxTessEvaluationImageUniforms gl_MaxTessEvaluationInputComponents gl_MaxTessEvaluationOutputComponents gl_MaxTessEvaluationTextureImageUnits gl_MaxTessEvaluationUniformComponents gl_MaxTessGenLevel gl_MaxTessPatchComponents gl_MaxTextureCoords gl_MaxTextureImageUnits gl_MaxTextureUnits gl_MaxVaryingComponents gl_MaxVaryingFloats gl_MaxVaryingVectors gl_MaxVertexAtomicCounterBuffers gl_MaxVertexAtomicCounters gl_MaxVertexAttribs gl_MaxVertexImageUniforms gl_MaxVertexOutputComponents gl_MaxVertexOutputVectors gl_MaxVertexTextureImageUnits gl_MaxVertexUniformComponents gl_MaxVertexUniformVectors gl_MaxViewports gl_MinProgramTexelOffset gl_BackColor gl_BackLightModelProduct gl_BackLightProduct gl_BackMaterial gl_BackSecondaryColor gl_ClipDistance gl_ClipPlane gl_ClipVertex gl_Color gl_DepthRange gl_EyePlaneQ gl_EyePlaneR gl_EyePlaneS gl_EyePlaneT gl_Fog gl_FogCoord gl_FogFragCoord gl_FragColor gl_FragCoord gl_FragData gl_FragDepth gl_FrontColor gl_FrontFacing gl_FrontLightModelProduct gl_FrontLightProduct gl_FrontMaterial gl_FrontSecondaryColor gl_GlobalInvocationID gl_InstanceID gl_InvocationID gl_Layer gl_LightModel gl_LightSource gl_LocalInvocationID gl_LocalInvocationIndex gl_ModelViewMatrix gl_ModelViewMatrixInverse gl_ModelViewMatrixInverseTranspose gl_ModelViewMatrixTranspose gl_ModelViewProjectionMatrix gl_ModelViewProjectionMatrixInverse gl_ModelViewProjectionMatrixInverseTranspose gl_ModelViewProjectionMatrixTranspose gl_MultiTexCoord0 gl_MultiTexCoord1 gl_MultiTexCoord2 gl_MultiTexCoord3 gl_MultiTexCoord4 gl_MultiTexCoord5 gl_MultiTexCoord6 gl_MultiTexCoord7 gl_Normal gl_NormalMatrix gl_NormalScale gl_NumSamples gl_NumWorkGroups gl_ObjectPlaneQ gl_ObjectPlaneR gl_ObjectPlaneS gl_ObjectPlaneT gl_PatchVerticesIn gl_Point gl_PointCoord gl_PointSize gl_Position gl_PrimitiveID gl_PrimitiveIDIn gl_ProjectionMatrix gl_ProjectionMatrixInverse gl_ProjectionMatrixInverseTranspose gl_ProjectionMatrixTranspose gl_SampleID gl_SampleMask gl_SampleMaskIn gl_SamplePosition gl_SecondaryColor gl_TessCoord gl_TessLevelInner gl_TessLevelOuter gl_TexCoord gl_TextureEnvColor gl_TextureMatrix gl_TextureMatrixInverse gl_TextureMatrixInverseTranspose gl_TextureMatrixTranspose gl_Vertex gl_VertexID gl_ViewportIndex gl_WorkGroupID gl_WorkGroupSize gl_in gl_out EmitStreamVertex EmitVertex EndPrimitive EndStreamPrimitive abs acos acosh all any asin asinh atan atanh atomicAdd atomicAnd atomicCompSwap atomicCounter atomicCounterDecrement atomicCounterIncrement atomicExchange atomicMax atomicMin atomicOr atomicXor barrier bitCount bitfieldExtract bitfieldInsert bitfieldReverse ceil clamp cos cosh cross dFdx dFdy degrees determinant distance dot equal exp exp2 faceforward findLSB findMSB floatBitsToInt floatBitsToUint floor fma fract frexp ftransform fwidth greaterThan greaterThanEqual groupMemoryBarrier imageAtomicAdd imageAtomicAnd imageAtomicCompSwap imageAtomicExchange imageAtomicMax imageAtomicMin imageAtomicOr imageAtomicXor imageLoad imageSize imageStore imulExtended intBitsToFloat interpolateAtCentroid interpolateAtOffset interpolateAtSample inverse inversesqrt isinf isnan ldexp length lessThan lessThanEqual log log2 matrixCompMult max memoryBarrier memoryBarrierAtomicCounter memoryBarrierBuffer memoryBarrierImage memoryBarrierShared min mix mod modf noise1 noise2 noise3 noise4 normalize not notEqual outerProduct packDouble2x32 packHalf2x16 packSnorm2x16 packSnorm4x8 packUnorm2x16 packUnorm4x8 pow radians reflect refract round roundEven shadow1D shadow1DLod shadow1DProj shadow1DProjLod shadow2D shadow2DLod shadow2DProj shadow2DProjLod sign sin sinh smoothstep sqrt step tan tanh texelFetch texelFetchOffset texture texture1D texture1DLod texture1DProj texture1DProjLod texture2D texture2DLod texture2DProj texture2DProjLod texture3D texture3DLod texture3DProj texture3DProjLod textureCube textureCubeLod textureGather textureGatherOffset textureGatherOffsets textureGrad textureGradOffset textureLod textureLodOffset textureOffset textureProj textureProjGrad textureProjGradOffset textureProjLod textureProjLodOffset textureProjOffset textureQueryLevels textureQueryLod textureSize transpose trunc uaddCarry uintBitsToFloat umulExtended unpackDouble2x32 unpackHalf2x16 unpackSnorm2x16 unpackSnorm4x8 unpackUnorm2x16 unpackUnorm4x8 usubBorrow",
                literal: "true false"
            },
            i: '"',
            c: [e.CLCM, e.CBCM, e.CNM, {
                cN: "meta",
                b: "#",
                e: "$"
            }]
        }
    }),
    e.registerLanguage("go",
    function(e) {
        var t = {
            keyword: "break default func interface select case map struct chan else goto package switch const fallthrough if range type continue for import return var go defer bool byte complex64 complex128 float32 float64 int8 int16 int32 int64 string uint8 uint16 uint32 uint64 int uint uintptr rune",
            literal: "true false iota nil",
            built_in: "append cap close complex copy imag len make new panic print println real recover delete"
        };
        return {
            aliases: ["golang"],
            k: t,
            i: "</",
            c: [e.CLCM, e.CBCM, {
                cN: "string",
                v: [e.QSM, {
                    b: "'",
                    e: "[^\\\\]'"
                },
                {
                    b: "`",
                    e: "`"
                }]
            },
            {
                cN: "number",
                v: [{
                    b: e.CNR + "[dflsi]",
                    r: 1
                },
                e.CNM]
            },
            {
                b: /:=/
            },
            {
                cN: "function",
                bK: "func",
                e: /\s*\{/,
                eE: !0,
                c: [e.TM, {
                    cN: "params",
                    b: /\(/,
                    e: /\)/,
                    k: t,
                    i: /["']/
                }]
            }]
        }
    }),
    e.registerLanguage("haskell",
    function(e) {
        var t = {
            v: [e.C("--", "$"), e.C("{-", "-}", {
                c: ["self"]
            })]
        },
        r = {
            cN: "meta",
            b: "{-#",
            e: "#-}"
        },
        a = {
            cN: "meta",
            b: "^#",
            e: "$"
        },
        n = {
            cN: "type",
            b: "\\b[A-Z][\\w']*",
            r: 0
        },
        i = {
            b: "\\(",
            e: "\\)",
            i: '"',
            c: [r, a, {
                cN: "type",
                b: "\\b[A-Z][\\w]*(\\((\\.\\.|,|\\w+)\\))?"
            },
            e.inherit(e.TM, {
                b: "[_a-z][\\w']*"
            }), t]
        },
        s = {
            b: "{",
            e: "}",
            c: i.c
        };
        return {
            aliases: ["hs"],
            k: "let in if then else case of where do module import hiding qualified type data newtype deriving class instance as default infix infixl infixr foreign export ccall stdcall cplusplus jvm dotnet safe unsafe family forall mdo proc rec",
            c: [{
                bK: "module",
                e: "where",
                k: "module where",
                c: [i, t],
                i: "\\W\\.|;"
            },
            {
                b: "\\bimport\\b",
                e: "$",
                k: "import qualified as hiding",
                c: [i, t],
                i: "\\W\\.|;"
            },
            {
                cN: "class",
                b: "^(\\s*)?(class|instance)\\b",
                e: "where",
                k: "class family instance where",
                c: [n, i, t]
            },
            {
                cN: "class",
                b: "\\b(data|(new)?type)\\b",
                e: "$",
                k: "data family type newtype deriving",
                c: [r, n, i, s, t]
            },
            {
                bK: "default",
                e: "$",
                c: [n, i, t]
            },
            {
                bK: "infix infixl infixr",
                e: "$",
                c: [e.CNM, t]
            },
            {
                b: "\\bforeign\\b",
                e: "$",
                k: "foreign import export ccall stdcall cplusplus jvm dotnet safe unsafe",
                c: [n, e.QSM, t]
            },
            {
                cN: "meta",
                b: "#!\\/usr\\/bin\\/env runhaskell",
                e: "$"
            },
            r, a, e.QSM, e.CNM, n, e.inherit(e.TM, {
                b: "^[_a-z][\\w']*"
            }), t, {
                b: "->|<-"
            }]
        }
    }),
    e.registerLanguage("http",
    function(e) {
        var t = "HTTP/[0-9\\.]+";
        return {
            aliases: ["https"],
            i: "\\S",
            c: [{
                b: "^" + t,
                e: "$",
                c: [{
                    cN: "number",
                    b: "\\b\\d{3}\\b"
                }]
            },
            {
                b: "^[A-Z]+ (.*?) " + t + "$",
                rB: !0,
                e: "$",
                c: [{
                    cN: "string",
                    b: " ",
                    e: " ",
                    eB: !0,
                    eE: !0
                },
                {
                    b: t
                },
                {
                    cN: "keyword",
                    b: "[A-Z]+"
                }]
            },
            {
                cN: "attribute",
                b: "^\\w",
                e: ": ",
                eE: !0,
                i: "\\n|\\s|=",
                starts: {
                    e: "$",
                    r: 0
                }
            },
            {
                b: "\\n\\n",
                starts: {
                    sL: [],
                    eW: !0
                }
            }]
        }
    }),
    e.registerLanguage("java",
    function(e) {
        var t = "[Ã€-Ê¸a-zA-Z_$][Ã€-Ê¸a-zA-Z_$0-9]*",
        r = t + "(<" + t + "(\\s*,\\s*" + t + ")*>)?",
        a = "false synchronized int abstract float private char boolean var static null if const for true while long strictfp finally protected import native final void enum else break transient catch instanceof byte super volatile case assert short package default double public try this switch continue throws protected public private module requires exports do",
        n = "\\b(0[bB]([01]+[01_]+[01]+|[01]+)|0[xX]([a-fA-F0-9]+[a-fA-F0-9_]+[a-fA-F0-9]+|[a-fA-F0-9]+)|(([\\d]+[\\d_]+[\\d]+|[\\d]+)(\\.([\\d]+[\\d_]+[\\d]+|[\\d]+))?|\\.([\\d]+[\\d_]+[\\d]+|[\\d]+))([eE][-+]?\\d+)?)[lLfF]?",
        i = {
            cN: "number",
            b: n,
            r: 0
        };
        return {
            aliases: ["jsp"],
            k: a,
            i: /<\/|#/,
            c: [e.C("/\\*\\*", "\\*/", {
                r: 0,
                c: [{
                    b: /\w+@/,
                    r: 0
                },
                {
                    cN: "doctag",
                    b: "@[A-Za-z]+"
                }]
            }), e.CLCM, e.CBCM, e.ASM, e.QSM, {
                cN: "class",
                bK: "class interface",
                e: /[{;=]/,
                eE: !0,
                k: "class interface",
                i: /[:"\[\]]/,
                c: [{
                    bK: "extends implements"
                },
                e.UTM]
            },
            {
                bK: "new throw return else",
                r: 0
            },
            {
                cN: "function",
                b: "(" + r + "\\s+)+" + e.UIR + "\\s*\\(",
                rB: !0,
                e: /[{;=]/,
                eE: !0,
                k: a,
                c: [{
                    b: e.UIR + "\\s*\\(",
                    rB: !0,
                    r: 0,
                    c: [e.UTM]
                },
                {
                    cN: "params",
                    b: /\(/,
                    e: /\)/,
                    k: a,
                    r: 0,
                    c: [e.ASM, e.QSM, e.CNM, e.CBCM]
                },
                e.CLCM, e.CBCM]
            },
            i, {
                cN: "meta",
                b: "@[A-Za-z]+"
            }]
        }
    }),
    e.registerLanguage("javascript",
    function(e) {
        var t = "[A-Za-z$_][0-9A-Za-z$_]*",
        r = {
            keyword: "in of if for while finally var new function do return void else break catch instanceof with throw case default try this switch continue typeof delete let yield const export super debugger as async await static import from as",
            literal: "true false null undefined NaN Infinity",
            built_in: "eval isFinite isNaN parseFloat parseInt decodeURI decodeURIComponent encodeURI encodeURIComponent escape unescape Object Function Boolean Error EvalError InternalError RangeError ReferenceError StopIteration SyntaxError TypeError URIError Number Math Date String RegExp Array Float32Array Float64Array Int16Array Int32Array Int8Array Uint16Array Uint32Array Uint8Array Uint8ClampedArray ArrayBuffer DataView JSON Intl arguments require module console window document Symbol Set Map WeakSet WeakMap Proxy Reflect Promise"
        },
        a = {
            cN: "number",
            v: [{
                b: "\\b(0[bB][01]+)"
            },
            {
                b: "\\b(0[oO][0-7]+)"
            },
            {
                b: e.CNR
            }],
            r: 0
        },
        n = {
            cN: "subst",
            b: "\\$\\{",
            e: "\\}",
            k: r,
            c: []
        },
        i = {
            cN: "string",
            b: "`",
            e: "`",
            c: [e.BE, n]
        };
        n.c = [e.ASM, e.QSM, i, a, e.RM];
        var s = n.c.concat([e.CBCM, e.CLCM]);
        return {
            aliases: ["js", "jsx"],
            k: r,
            c: [{
                cN: "meta",
                r: 10,
                b: /^\s*['"]use (strict|asm)['"]/
            },
            {
                cN: "meta",
                b: /^#!/,
                e: /$/
            },
            e.ASM, e.QSM, i, e.CLCM, e.CBCM, a, {
                b: /[{,]\s*/,
                r: 0,
                c: [{
                    b: t + "\\s*:",
                    rB: !0,
                    r: 0,
                    c: [{
                        cN: "attr",
                        b: t,
                        r: 0
                    }]
                }]
            },
            {
                b: "(" + e.RSR + "|\\b(case|return|throw)\\b)\\s*",
                k: "return throw case",
                c: [e.CLCM, e.CBCM, e.RM, {
                    cN: "function",
                    b: "(\\(.*?\\)|" + t + ")\\s*=>",
                    rB: !0,
                    e: "\\s*=>",
                    c: [{
                        cN: "params",
                        v: [{
                            b: t
                        },
                        {
                            b: /\(\s*\)/
                        },
                        {
                            b: /\(/,
                            e: /\)/,
                            eB: !0,
                            eE: !0,
                            k: r,
                            c: s
                        }]
                    }]
                },
                {
                    b: /</,
                    e: /(\/\w+|\w+\/)>/,
                    sL: "xml",
                    c: [{
                        b: /<\w+\s*\/>/,
                        skip: !0
                    },
                    {
                        b: /<\w+/,
                        e: /(\/\w+|\w+\/)>/,
                        skip: !0,
                        c: [{
                            b: /<\w+\s*\/>/,
                            skip: !0
                        },
                        "self"]
                    }]
                }],
                r: 0
            },
            {
                cN: "function",
                bK: "function",
                e: /\{/,
                eE: !0,
                c: [e.inherit(e.TM, {
                    b: t
                }), {
                    cN: "params",
                    b: /\(/,
                    e: /\)/,
                    eB: !0,
                    eE: !0,
                    c: s
                }],
                i: /\[|%/
            },
            {
                b: /\$[(.]/
            },
            e.METHOD_GUARD, {
                cN: "class",
                bK: "class",
                e: /[{;=]/,
                eE: !0,
                i: /[:"\[\]]/,
                c: [{
                    bK: "extends"
                },
                e.UTM]
            },
            {
                bK: "constructor",
                e: /\{/,
                eE: !0
            }],
            i: /#(?!!)/
        }
    }),
    e.registerLanguage("json",
    function(e) {
        var t = {
            literal: "true false null"
        },
        r = [e.QSM, e.CNM],
        a = {
            e: ",",
            eW: !0,
            eE: !0,
            c: r,
            k: t
        },
        n = {
            b: "{",
            e: "}",
            c: [{
                cN: "attr",
                b: /"/,
                e: /"/,
                c: [e.BE],
                i: "\\n"
            },
            e.inherit(a, {
                b: /:/
            })],
            i: "\\S"
        },
        i = {
            b: "\\[",
            e: "\\]",
            c: [e.inherit(a)],
            i: "\\S"
        };
        return r.splice(r.length, 0, n, i),
        {
            c: r,
            k: t,
            i: "\\S"
        }
    }),
    e.registerLanguage("kotlin",
    function(e) {
        var t = {
            keyword: "abstract as val var vararg get set class object open private protected public noinline crossinline dynamic final enum if else do while for when throw try catch finally import package is in fun override companion reified inline lateinit init interface annotation data sealed internal infix operator out by constructor super tailrec where const inner suspend typealias external expect actual trait volatile transient native default",
            built_in: "Byte Short Char Int Long Boolean Float Double Void Unit Nothing",
            literal: "true false null"
        },
        r = {
            cN: "keyword",
            b: /\b(break|continue|return|this)\b/,
            starts: {
                c: [{
                    cN: "symbol",
                    b: /@\w+/
                }]
            }
        },
        a = {
            cN: "symbol",
            b: e.UIR + "@"
        },
        n = {
            cN: "subst",
            b: "\\${",
            e: "}",
            c: [e.ASM, e.CNM]
        },
        i = {
            cN: "variable",
            b: "\\$" + e.UIR
        },
        s = {
            cN: "string",
            v: [{
                b: '"""',
                e: '"""',
                c: [i, n]
            },
            {
                b: "'",
                e: "'",
                i: /\n/,
                c: [e.BE]
            },
            {
                b: '"',
                e: '"',
                i: /\n/,
                c: [e.BE, i, n]
            }]
        },
        o = {
            cN: "meta",
            b: "@(?:file|property|field|get|set|receiver|param|setparam|delegate)\\s*:(?:\\s*" + e.UIR + ")?"
        },
        c = {
            cN: "meta",
            b: "@" + e.UIR,
            c: [{
                b: /\(/,
                e: /\)/,
                c: [e.inherit(s, {
                    cN: "meta-string"
                })]
            }]
        },
        l = "\\b(0[bB]([01]+[01_]+[01]+|[01]+)|0[xX]([a-fA-F0-9]+[a-fA-F0-9_]+[a-fA-F0-9]+|[a-fA-F0-9]+)|(([\\d]+[\\d_]+[\\d]+|[\\d]+)(\\.([\\d]+[\\d_]+[\\d]+|[\\d]+))?|\\.([\\d]+[\\d_]+[\\d]+|[\\d]+))([eE][-+]?\\d+)?)[lLfF]?",
        u = {
            cN: "number",
            b: l,
            r: 0
        };
        return {
            aliases: ["kt"],
            k: t,
            c: [e.C("/\\*\\*", "\\*/", {
                r: 0,
                c: [{
                    cN: "doctag",
                    b: "@[A-Za-z]+"
                }]
            }), e.CLCM, e.CBCM, r, a, o, c, {
                cN: "function",
                bK: "fun",
                e: "[(]|$",
                rB: !0,
                eE: !0,
                k: t,
                i: /fun\s+(<.*>)?[^\s\(]+(\s+[^\s\(]+)\s*=/,
                r: 5,
                c: [{
                    b: e.UIR + "\\s*\\(",
                    rB: !0,
                    r: 0,
                    c: [e.UTM]
                },
                {
                    cN: "type",
                    b: /</,
                    e: />/,
                    k: "reified",
                    r: 0
                },
                {
                    cN: "params",
                    b: /\(/,
                    e: /\)/,
                    endsParent: !0,
                    k: t,
                    r: 0,
                    c: [{
                        b: /:/,
                        e: /[=,\/]/,
                        eW: !0,
                        c: [{
                            cN: "type",
                            b: e.UIR
                        },
                        e.CLCM, e.CBCM],
                        r: 0
                    },
                    e.CLCM, e.CBCM, o, c, s, e.CNM]
                },
                e.CBCM]
            },
            {
                cN: "class",
                bK: "class interface trait",
                e: /[:\{(]|$/,
                eE: !0,
                i: "extends implements",
                c: [{
                    bK: "public protected internal private constructor"
                },
                e.UTM, {
                    cN: "type",
                    b: /</,
                    e: />/,
                    eB: !0,
                    eE: !0,
                    r: 0
                },
                {
                    cN: "type",
                    b: /[,:]\s*/,
                    e: /[<\(,]|$/,
                    eB: !0,
                    rE: !0
                },
                o, c]
            },
            s, {
                cN: "meta",
                b: "^#!/usr/bin/env",
                e: "$",
                i: "\n"
            },
            u]
        }
    }),
    e.registerLanguage("lisp",
    function(e) {
        var t = "[a-zA-Z_\\-\\+\\*\\/\\<\\=\\>\\&\\#][a-zA-Z0-9_\\-\\+\\*\\/\\<\\=\\>\\&\\#!]*",
        r = "\\|[^]*?\\|",
        a = "(\\-|\\+)?\\d+(\\.\\d+|\\/\\d+)?((d|e|f|l|s|D|E|F|L|S)(\\+|\\-)?\\d+)?",
        n = {
            cN: "meta",
            b: "^#!",
            e: "$"
        },
        i = {
            cN: "literal",
            b: "\\b(t{1}|nil)\\b"
        },
        s = {
            cN: "number",
            v: [{
                b: a,
                r: 0
            },
            {
                b: "#(b|B)[0-1]+(/[0-1]+)?"
            },
            {
                b: "#(o|O)[0-7]+(/[0-7]+)?"
            },
            {
                b: "#(x|X)[0-9a-fA-F]+(/[0-9a-fA-F]+)?"
            },
            {
                b: "#(c|C)\\(" + a + " +" + a,
                e: "\\)"
            }]
        },
        o = e.inherit(e.QSM, {
            i: null
        }),
        c = e.C(";", "$", {
            r: 0
        }),
        l = {
            b: "\\*",
            e: "\\*"
        },
        u = {
            cN: "symbol",
            b: "[:&]" + t
        },
        d = {
            b: t,
            r: 0
        },
        b = {
            b: r
        },
        p = {
            b: "\\(",
            e: "\\)",
            c: ["self", i, o, s, d]
        },
        m = {
            c: [s, o, l, u, p, d],
            v: [{
                b: "['`]\\(",
                e: "\\)"
            },
            {
                b: "\\(quote ",
                e: "\\)",
                k: {
                    name: "quote"
                }
            },
            {
                b: "'" + r
            }]
        },
        g = {
            v: [{
                b: "'" + t
            },
            {
                b: "#'" + t + "(::" + t + ")*"
            }]
        },
        f = {
            b: "\\(\\s*",
            e: "\\)"
        },
        _ = {
            eW: !0,
            r: 0
        };
        return f.c = [{
            cN: "name",
            v: [{
                b: t
            },
            {
                b: r
            }]
        },
        _],
        _.c = [m, g, f, i, s, o, c, l, u, b, d],
        {
            i: /\S/,
            c: [s, n, i, o, c, m, g, f, d]
        }
    }),
    e.registerLanguage("lua",
    function(e) {
        var t = "\\[=*\\[",
        r = "\\]=*\\]",
        a = {
            b: t,
            e: r,
            c: ["self"]
        },
        n = [e.C("--(?!" + t + ")", "$"), e.C("--" + t, r, {
            c: [a],
            r: 10
        })];
        return {
            l: e.UIR,
            k: {
                literal: "true false nil",
                keyword: "and break do else elseif end for goto if in local not or repeat return then until while",
                built_in: "_G _ENV _VERSION __index __newindex __mode __call __metatable __tostring __len __gc __add __sub __mul __div __mod __pow __concat __unm __eq __lt __le assert collectgarbage dofile error getfenv getmetatable ipairs load loadfile loadstringmodule next pairs pcall print rawequal rawget rawset require select setfenvsetmetatable tonumber tostring type unpack xpcall arg selfcoroutine resume yield status wrap create running debug getupvalue debug sethook getmetatable gethook setmetatable setlocal traceback setfenv getinfo setupvalue getlocal getregistry getfenv io lines write close flush open output type read stderr stdin input stdout popen tmpfile math log max acos huge ldexp pi cos tanh pow deg tan cosh sinh random randomseed frexp ceil floor rad abs sqrt modf asin min mod fmod log10 atan2 exp sin atan os exit setlocale date getenv difftime remove time clock tmpname rename execute package preload loadlib loaded loaders cpath config path seeall string sub upper len gfind rep find match char dump gmatch reverse byte format gsub lower table setn insert getn foreachi maxn foreach concat sort remove"
            },
            c: n.concat([{
                cN: "function",
                bK: "function",
                e: "\\)",
                c: [e.inherit(e.TM, {
                    b: "([_a-zA-Z]\\w*\\.)*([_a-zA-Z]\\w*:)?[_a-zA-Z]\\w*"
                }), {
                    cN: "params",
                    b: "\\(",
                    eW: !0,
                    c: n
                }].concat(n)
            },
            e.CNM, e.ASM, e.QSM, {
                cN: "string",
                b: t,
                e: r,
                c: [a],
                r: 5
            }])
        }
    }),
    e.registerLanguage("makefile",
    function(e) {
        var t = {
            cN: "variable",
            v: [{
                b: "\\$\\(" + e.UIR + "\\)",
                c: [e.BE]
            },
            {
                b: /\$[@%<?\^\+\*]/
            }]
        },
        r = {
            cN: "string",
            b: /"/,
            e: /"/,
            c: [e.BE, t]
        },
        a = {
            cN: "variable",
            b: /\$\([\w-]+\s/,
            e: /\)/,
            k: {
                built_in: "subst patsubst strip findstring filter filter-out sort word wordlist firstword lastword dir notdir suffix basename addsuffix addprefix join wildcard realpath abspath error warning shell origin flavor foreach if or and call eval file value"
            },
            c: [t]
        },
        n = {
            b: "^" + e.UIR + "\\s*[:+?]?=",
            i: "\\n",
            rB: !0,
            c: [{
                b: "^" + e.UIR,
                e: "[:+?]?=",
                eE: !0
            }]
        },
        i = {
            cN: "meta",
            b: /^\.PHONY:/,
            e: /$/,
            k: {
                "meta-keyword": ".PHONY"
            },
            l: /[\.\w]+/
        },
        s = {
            cN: "section",
            b: /^[^\s]+:/,
            e: /$/,
            c: [t]
        };
        return {
            aliases: ["mk", "mak"],
            k: "define endef undefine ifdef ifndef ifeq ifneq else endif include -include sinclude override export unexport private vpath",
            l: /[\w-]+/,
            c: [e.HCM, t, r, a, n, i, s]
        }
    }),
    e.registerLanguage("xml",
    function(e) {
        var t = "[A-Za-z0-9\\._:-]+",
        r = {
            eW: !0,
            i: /</,
            r: 0,
            c: [{
                cN: "attr",
                b: t,
                r: 0
            },
            {
                b: /=\s*/,
                r: 0,
                c: [{
                    cN: "string",
                    endsParent: !0,
                    v: [{
                        b: /"/,
                        e: /"/
                    },
                    {
                        b: /'/,
                        e: /'/
                    },
                    {
                        b: /[^\s"'=<>`]+/
                    }]
                }]
            }]
        };
        return {
            aliases: ["html", "xhtml", "rss", "atom", "xjb", "xsd", "xsl", "plist"],
            cI: !0,
            c: [{
                cN: "meta",
                b: "<!DOCTYPE",
                e: ">",
                r: 10,
                c: [{
                    b: "\\[",
                    e: "\\]"
                }]
            },
            e.C("<!--", "-->", {
                r: 10
            }), {
                b: "<\\!\\[CDATA\\[",
                e: "\\]\\]>",
                r: 10
            },
            {
                cN: "meta",
                b: /<\?xml/,
                e: /\?>/,
                r: 10
            },
            {
                b: /<\?(php)?/,
                e: /\?>/,
                sL: "php",
                c: [{
                    b: "/\\*",
                    e: "\\*/",
                    skip: !0
                },
                {
                    b: 'b"',
                    e: '"',
                    skip: !0
                },
                {
                    b: "b'",
                    e: "'",
                    skip: !0
                },
                e.inherit(e.ASM, {
                    i: null,
                    cN: null,
                    c: null,
                    skip: !0
                }), e.inherit(e.QSM, {
                    i: null,
                    cN: null,
                    c: null,
                    skip: !0
                })]
            },
            {
                cN: "tag",
                b: "<style(?=\\s|>|$)",
                e: ">",
                k: {
                    name: "style"
                },
                c: [r],
                starts: {
                    e: "</style>",
                    rE: !0,
                    sL: ["css", "xml"]
                }
            },
            {
                cN: "tag",
                b: "<script(?=\\s|>|$)",
                e: ">",
                k: {
                    name: "script"
                },
                c: [r],
                starts: {
                    e: "</script>",
                    rE: !0,
                    sL: ["actionscript", "javascript", "handlebars", "xml"]
                }
            },
            {
                cN: "tag",
                b: "</?",
                e: "/?>",
                c: [{
                    cN: "name",
                    b: /[^\/><\s]+/,
                    r: 0
                },
                r]
            }]
        }
    }),
    e.registerLanguage("markdown",
    function(e) {
        return {
            aliases: ["md", "mkdown", "mkd"],
            c: [{
                cN: "section",
                v: [{
                    b: "^#{1,6}",
                    e: "$"
                },
                {
                    b: "^.+?\\n[=-]{2,}$"
                }]
            },
            {
                b: "<",
                e: ">",
                sL: "xml",
                r: 0
            },
            {
                cN: "bullet",
                b: "^([*+-]|(\\d+\\.))\\s+"
            },
            {
                cN: "strong",
                b: "[*_]{2}.+?[*_]{2}"
            },
            {
                cN: "emphasis",
                v: [{
                    b: "\\*.+?\\*"
                },
                {
                    b: "_.+?_",
                    r: 0
                }]
            },
            {
                cN: "quote",
                b: "^>\\s+",
                e: "$"
            },
            {
                cN: "code",
                v: [{
                    b: "^```w*s*$",
                    e: "^```s*$"
                },
                {
                    b: "`.+?`"
                },
                {
                    b: "^( {4}|	)",
                    e: "$",
                    r: 0
                }]
            },
            {
                b: "^[-\\*]{3,}",
                e: "$"
            },
            {
                b: "\\[.+?\\][\\(\\[].*?[\\)\\]]",
                rB: !0,
                c: [{
                    cN: "string",
                    b: "\\[",
                    e: "\\]",
                    eB: !0,
                    rE: !0,
                    r: 0
                },
                {
                    cN: "link",
                    b: "\\]\\(",
                    e: "\\)",
                    eB: !0,
                    eE: !0
                },
                {
                    cN: "symbol",
                    b: "\\]\\[",
                    e: "\\]",
                    eB: !0,
                    eE: !0
                }],
                r: 10
            },
            {
                b: /^\[[^\n]+\]:/,
                rB: !0,
                c: [{
                    cN: "symbol",
                    b: /\[/,
                    e: /\]/,
                    eB: !0,
                    eE: !0
                },
                {
                    cN: "link",
                    b: /:\s*/,
                    e: /$/,
                    eB: !0
                }]
            }]
        }
    }),
    e.registerLanguage("matlab",
    function(e) {
        var t = "('|\\.')+",
        r = {
            r: 0,
            c: [{
                b: t
            }]
        };
        return {
            k: {
                keyword: "break case catch classdef continue else elseif end enumerated events for function global if methods otherwise parfor persistent properties return spmd switch try while",
                built_in: "sin sind sinh asin asind asinh cos cosd cosh acos acosd acosh tan tand tanh atan atand atan2 atanh sec secd sech asec asecd asech csc cscd csch acsc acscd acsch cot cotd coth acot acotd acoth hypot exp expm1 log log1p log10 log2 pow2 realpow reallog realsqrt sqrt nthroot nextpow2 abs angle complex conj imag real unwrap isreal cplxpair fix floor ceil round mod rem sign airy besselj bessely besselh besseli besselk beta betainc betaln ellipj ellipke erf erfc erfcx erfinv expint gamma gammainc gammaln psi legendre cross dot factor isprime primes gcd lcm rat rats perms nchoosek factorial cart2sph cart2pol pol2cart sph2cart hsv2rgb rgb2hsv zeros ones eye repmat rand randn linspace logspace freqspace meshgrid accumarray size length ndims numel disp isempty isequal isequalwithequalnans cat reshape diag blkdiag tril triu fliplr flipud flipdim rot90 find sub2ind ind2sub bsxfun ndgrid permute ipermute shiftdim circshift squeeze isscalar isvector ans eps realmax realmin pi i inf nan isnan isinf isfinite j why compan gallery hadamard hankel hilb invhilb magic pascal rosser toeplitz vander wilkinson max min nanmax nanmin mean nanmean type table readtable writetable sortrows sort figure plot plot3 scatter scatter3 cellfun legend intersect ismember procrustes hold num2cell "
            },
            i: '(//|"|#|/\\*|\\s+/\\w+)',
            c: [{
                cN: "function",
                bK: "function",
                e: "$",
                c: [e.UTM, {
                    cN: "params",
                    v: [{
                        b: "\\(",
                        e: "\\)"
                    },
                    {
                        b: "\\[",
                        e: "\\]"
                    }]
                }]
            },
            {
                cN: "built_in",
                b: /true|false/,
                r: 0,
                starts: r
            },
            {
                b: "[a-zA-Z][a-zA-Z_0-9]*" + t,
                r: 0
            },
            {
                cN: "number",
                b: e.CNR,
                r: 0,
                starts: r
            },
            {
                cN: "string",
                b: "'",
                e: "'",
                c: [e.BE, {
                    b: "''"
                }]
            },
            {
                b: /\]|}|\)/,
                r: 0,
                starts: r
            },
            {
                cN: "string",
                b: '"',
                e: '"',
                c: [e.BE, {
                    b: '""'
                }],
                starts: r
            },
            e.C("^\\s*\\%\\{\\s*$", "^\\s*\\%\\}\\s*$"), e.C("\\%", "$")]
        }
    }),
    e.registerLanguage("objectivec",
    function(e) {
        var t = {
            cN: "built_in",
            b: "\\b(AV|CA|CF|CG|CI|CL|CM|CN|CT|MK|MP|MTK|MTL|NS|SCN|SK|UI|WK|XC)\\w+"
        },
        r = {
            keyword: "int float while char export sizeof typedef const struct for union unsigned long volatile static bool mutable if do return goto void enum else break extern asm case short default double register explicit signed typename this switch continue wchar_t inline readonly assign readwrite self @synchronized id typeof nonatomic super unichar IBOutlet IBAction strong weak copy in out inout bycopy byref oneway __strong __weak __block __autoreleasing @private @protected @public @try @property @end @throw @catch @finally @autoreleasepool @synthesize @dynamic @selector @optional @required @encode @package @import @defs @compatibility_alias __bridge __bridge_transfer __bridge_retained __bridge_retain __covariant __contravariant __kindof _Nonnull _Nullable _Null_unspecified __FUNCTION__ __PRETTY_FUNCTION__ __attribute__ getter setter retain unsafe_unretained nonnull nullable null_unspecified null_resettable class instancetype NS_DESIGNATED_INITIALIZER NS_UNAVAILABLE NS_REQUIRES_SUPER NS_RETURNS_INNER_POINTER NS_INLINE NS_AVAILABLE NS_DEPRECATED NS_ENUM NS_OPTIONS NS_SWIFT_UNAVAILABLE NS_ASSUME_NONNULL_BEGIN NS_ASSUME_NONNULL_END NS_REFINED_FOR_SWIFT NS_SWIFT_NAME NS_SWIFT_NOTHROW NS_DURING NS_HANDLER NS_ENDHANDLER NS_VALUERETURN NS_VOIDRETURN",
            literal: "false true FALSE TRUE nil YES NO NULL",
            built_in: "BOOL dispatch_once_t dispatch_queue_t dispatch_sync dispatch_async dispatch_once"
        },
        a = /[a-zA-Z@][a-zA-Z0-9_]*/,
        n = "@interface @class @protocol @implementation";
        return {
            aliases: ["mm", "objc", "obj-c"],
            k: r,
            l: a,
            i: "</",
            c: [t, e.CLCM, e.CBCM, e.CNM, e.QSM, {
                cN: "string",
                v: [{
                    b: '@"',
                    e: '"',
                    i: "\\n",
                    c: [e.BE]
                },
                {
                    b: "'",
                    e: "[^\\\\]'",
                    i: "[^\\\\][^']"
                }]
            },
            {
                cN: "meta",
                b: "#",
                e: "$",
                c: [{
                    cN: "meta-string",
                    v: [{
                        b: '"',
                        e: '"'
                    },
                    {
                        b: "<",
                        e: ">"
                    }]
                }]
            },
            {
                cN: "class",
                b: "(" + n.split(" ").join("|") + ")\\b",
                e: "({|$)",
                eE: !0,
                k: n,
                l: a,
                c: [e.UTM]
            },
            {
                b: "\\." + e.UIR,
                r: 0
            }]
        }
    }),
    e.registerLanguage("perl",
    function(e) {
        var t = "getpwent getservent quotemeta msgrcv scalar kill dbmclose undef lc ma syswrite tr send umask sysopen shmwrite vec qx utime local oct semctl localtime readpipe do return format read sprintf dbmopen pop getpgrp not getpwnam rewinddir qqfileno qw endprotoent wait sethostent bless s|0 opendir continue each sleep endgrent shutdown dump chomp connect getsockname die socketpair close flock exists index shmgetsub for endpwent redo lstat msgctl setpgrp abs exit select print ref gethostbyaddr unshift fcntl syscall goto getnetbyaddr join gmtime symlink semget splice x|0 getpeername recv log setsockopt cos last reverse gethostbyname getgrnam study formline endhostent times chop length gethostent getnetent pack getprotoent getservbyname rand mkdir pos chmod y|0 substr endnetent printf next open msgsnd readdir use unlink getsockopt getpriority rindex wantarray hex system getservbyport endservent int chr untie rmdir prototype tell listen fork shmread ucfirst setprotoent else sysseek link getgrgid shmctl waitpid unpack getnetbyname reset chdir grep split require caller lcfirst until warn while values shift telldir getpwuid my getprotobynumber delete and sort uc defined srand accept package seekdir getprotobyname semop our rename seek if q|0 chroot sysread setpwent no crypt getc chown sqrt write setnetent setpriority foreach tie sin msgget map stat getlogin unless elsif truncate exec keys glob tied closedirioctl socket readlink eval xor readline binmode setservent eof ord bind alarm pipe atan2 getgrent exp time push setgrent gt lt or ne m|0 break given say state when",
        r = {
            cN: "subst",
            b: "[$@]\\{",
            e: "\\}",
            k: t
        },
        a = {
            b: "->{",
            e: "}"
        },
        n = {
            v: [{
                b: /\$\d/
            },
            {
                b: /[\$%@](\^\w\b|#\w+(::\w+)*|{\w+}|\w+(::\w*)*)/
            },
            {
                b: /[\$%@][^\s\w{]/,
                r: 0
            }]
        },
        i = [e.BE, r, n],
        s = [n, e.HCM, e.C("^\\=\\w", "\\=cut", {
            eW: !0
        }), a, {
            cN: "string",
            c: i,
            v: [{
                b: "q[qwxr]?\\s*\\(",
                e: "\\)",
                r: 5
            },
            {
                b: "q[qwxr]?\\s*\\[",
                e: "\\]",
                r: 5
            },
            {
                b: "q[qwxr]?\\s*\\{",
                e: "\\}",
                r: 5
            },
            {
                b: "q[qwxr]?\\s*\\|",
                e: "\\|",
                r: 5
            },
            {
                b: "q[qwxr]?\\s*\\<",
                e: "\\>",
                r: 5
            },
            {
                b: "qw\\s+q",
                e: "q",
                r: 5
            },
            {
                b: "'",
                e: "'",
                c: [e.BE]
            },
            {
                b: '"',
                e: '"'
            },
            {
                b: "`",
                e: "`",
                c: [e.BE]
            },
            {
                b: "{\\w+}",
                c: [],
                r: 0
            },
            {
                b: "-?\\w+\\s*\\=\\>",
                c: [],
                r: 0
            }]
        },
        {
            cN: "number",
            b: "(\\b0[0-7_]+)|(\\b0x[0-9a-fA-F_]+)|(\\b[1-9][0-9_]*(\\.[0-9_]+)?)|[0_]\\b",
            r: 0
        },
        {
            b: "(\\/\\/|" + e.RSR + "|\\b(split|return|print|reverse|grep)\\b)\\s*",
            k: "split return print reverse grep",
            r: 0,
            c: [e.HCM, {
                cN: "regexp",
                b: "(s|tr|y)/(\\\\.|[^/])*/(\\\\.|[^/])*/[a-z]*",
                r: 10
            },
            {
                cN: "regexp",
                b: "(m|qr)?/",
                e: "/[a-z]*",
                c: [e.BE],
                r: 0
            }]
        },
        {
            cN: "function",
            bK: "sub",
            e: "(\\s*\\(.*?\\))?[;{]",
            eE: !0,
            r: 5,
            c: [e.TM]
        },
        {
            b: "-\\w\\b",
            r: 0
        },
        {
            b: "^__DATA__$",
            e: "^__END__$",
            sL: "mojolicious",
            c: [{
                b: "^@@.*",
                e: "$",
                cN: "comment"
            }]
        }];
        return r.c = s,
        a.c = s,
        {
            aliases: ["pl", "pm"],
            l: /[\w\.]+/,
            k: t,
            c: s
        }
    }),
    e.registerLanguage("php",
    function(e) {
        var t = {
            b: "\\$+[a-zA-Z_-Ã¿][a-zA-Z0-9_-Ã¿]*"
        },
        r = {
            cN: "meta",
            b: /<\?(php)?|\?>/
        },
        a = {
            cN: "string",
            c: [e.BE, r],
            v: [{
                b: 'b"',
                e: '"'
            },
            {
                b: "b'",
                e: "'"
            },
            e.inherit(e.ASM, {
                i: null
            }), e.inherit(e.QSM, {
                i: null
            })]
        },
        n = {
            v: [e.BNM, e.CNM]
        };
        return {
            aliases: ["php", "php3", "php4", "php5", "php6", "php7"],
            cI: !0,
            k: "and include_once list abstract global private echo interface as static endswitch array null if endwhile or const for endforeach self var while isset public protected exit foreach throw elseif include __FILE__ empty require_once do xor return parent clone use __CLASS__ __LINE__ else break print eval new catch __METHOD__ case exception default die require __FUNCTION__ enddeclare final try switch continue endfor endif declare unset true false trait goto instanceof insteadof __DIR__ __NAMESPACE__ yield finally",
            c: [e.HCM, e.C("//", "$", {
                c: [r]
            }), e.C("/\\*", "\\*/", {
                c: [{
                    cN: "doctag",
                    b: "@[A-Za-z]+"
                }]
            }), e.C("__halt_compiler.+?;", !1, {
                eW: !0,
                k: "__halt_compiler",
                l: e.UIR
            }), {
                cN: "string",
                b: /<<<['"]?\w+['"]?$/,
                e: /^\w+;?$/,
                c: [e.BE, {
                    cN: "subst",
                    v: [{
                        b: /\$\w+/
                    },
                    {
                        b: /\{\$/,
                        e: /\}/
                    }]
                }]
            },
            r, {
                cN: "keyword",
                b: /\$this\b/
            },
            t, {
                b: /(::|->)+[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*/
            },
            {
                cN: "function",
                bK: "function",
                e: /[;{]/,
                eE: !0,
                i: "\\$|\\[|%",
                c: [e.UTM, {
                    cN: "params",
                    b: "\\(",
                    e: "\\)",
                    c: ["self", t, e.CBCM, a, n]
                }]
            },
            {
                cN: "class",
                bK: "class interface",
                e: "{",
                eE: !0,
                i: /[:\(\$"]/,
                c: [{
                    bK: "extends implements"
                },
                e.UTM]
            },
            {
                bK: "namespace",
                e: ";",
                i: /[\.']/,
                c: [e.UTM]
            },
            {
                bK: "use",
                e: ";",
                c: [e.UTM]
            },
            {
                b: "=>"
            },
            a, n]
        }
    }),
    e.registerLanguage("plaintext",
    function(e) {
        return {
            disableAutodetect: !0
        }
    }),
    e.registerLanguage("python",
    function(e) {
        var t = {
            keyword: "and elif is global as in if from raise for except finally print import pass return exec else break not with class assert yield try while continue del or def lambda async await nonlocal|10 None True False",
            built_in: "Ellipsis NotImplemented"
        },
        r = {
            cN: "meta",
            b: /^(>>>|\.\.\.) /
        },
        a = {
            cN: "subst",
            b: /\{/,
            e: /\}/,
            k: t,
            i: /#/
        },
        n = {
            cN: "string",
            c: [e.BE],
            v: [{
                b: /(u|b)?r?'''/,
                e: /'''/,
                c: [e.BE, r],
                r: 10
            },
            {
                b: /(u|b)?r?"""/,
                e: /"""/,
                c: [e.BE, r],
                r: 10
            },
            {
                b: /(fr|rf|f)'''/,
                e: /'''/,
                c: [e.BE, r, a]
            },
            {
                b: /(fr|rf|f)"""/,
                e: /"""/,
                c: [e.BE, r, a]
            },
            {
                b: /(u|r|ur)'/,
                e: /'/,
                r: 10
            },
            {
                b: /(u|r|ur)"/,
                e: /"/,
                r: 10
            },
            {
                b: /(b|br)'/,
                e: /'/
            },
            {
                b: /(b|br)"/,
                e: /"/
            },
            {
                b: /(fr|rf|f)'/,
                e: /'/,
                c: [e.BE, a]
            },
            {
                b: /(fr|rf|f)"/,
                e: /"/,
                c: [e.BE, a]
            },
            e.ASM, e.QSM]
        },
        i = {
            cN: "number",
            r: 0,
            v: [{
                b: e.BNR + "[lLjJ]?"
            },
            {
                b: "\\b(0o[0-7]+)[lLjJ]?"
            },
            {
                b: e.CNR + "[lLjJ]?"
            }]
        },
        s = {
            cN: "params",
            b: /\(/,
            e: /\)/,
            c: ["self", r, i, n]
        };
        return a.c = [n, i, r],
        {
            aliases: ["py", "gyp", "ipython"],
            k: t,
            i: /(<\/|->|\?)|=>/,
            c: [r, i, n, e.HCM, {
                v: [{
                    cN: "function",
                    bK: "def"
                },
                {
                    cN: "class",
                    bK: "class"
                }],
                e: /:/,
                i: /[${=;\n,]/,
                c: [e.UTM, s, {
                    b: /->/,
                    eW: !0,
                    k: "None"
                }]
            },
            {
                cN: "meta",
                b: /^[\t ]*@/,
                e: /$/
            },
            {
                b: /\b(print|exec)\(/
            }]
        }
    }),
    e.registerLanguage("pyxlscript",
    function(e) {
        var t = {
            keyword: "âŒŠ âŒ‹ âŒˆ âŒ‰ | â€– âˆŠ âˆˆ bitor pad joy bitxor bitand and because at local in if then for return while mod preserving_transform|10 else continue let|2 const break not with assert with debug_watch draw_sprite draw_text debug_print|4 while continue or nil|2 pi nan infinity true false âˆ…"
        },
        r = {
            cN: "subst",
            b: /\{/,
            e: /\}/,
            k: t
        },
        a = {
            cN: "string",
            c: [e.BE],
            v: [{
                b: /(u|r|ur)"/,
                e: /"/,
                r: 10
            },
            {
                b: /(b|br)"/,
                e: /"/
            },
            {
                b: /(fr|rf|f)"/,
                e: /"/,
                c: [e.BE, r]
            },
            e.QSM]
        },
        n = {
            cN: "section",
            r: 10,
            v: [{
                b: /^[^\n]+?\\n(-|â”€|â€”|â”|âŽ¯|=|â•|âšŒ){5,}/
            }]
        },
        i = {
            cN: "number",
            r: 0,
            v: [{
                b: /[+-]?[âˆžÎµÏ€Â½â…“â…”Â¼Â¾â…•â…–â…—â…˜â…™â…â…›â…‘â…’`]/
            },
            {
                b: /#[0-7a-fA-F]+/
            },
            {
                b: /[+-]?(\d*\.)?\d+(%|deg|Â°)?/
            },
            {
                b: /[â‚€â‚â‚‚â‚ƒâ‚„â‚…â‚†â‚‡â‚ˆâ‚‰â°Â¹Â²Â³â´âµâ¶â·â¸â¹]/
            }]
        },
        s = {
            cN: "params",
            b: /\(/,
            e: /\)/,
            c: [i, a]
        };
        return r.c = [a, i],
        {
            aliases: ["pyxlscript"],
            k: t,
            i: /(<\/|->|\?)|=>|@|\$/,
            c: [n, i, a, e.CLCM, e.CBCM, {
                v: [{
                    cN: "function",
                    bK: "def"
                }],
                e: /:/,
                i: /[${=;\n,]/,
                c: [e.UTM, s, {
                    b: /->/,
                    eW: !0,
                    k: "None"
                }]
            }]
        }
    }),
    e.registerLanguage("r",
    function(e) {
        var t = "([a-zA-Z]|\\.[a-zA-Z.])[a-zA-Z0-9._]*";
        return {
            c: [e.HCM, {
                b: t,
                l: t,
                k: {
                    keyword: "function if in break next repeat else for return switch while try tryCatch stop warning require library attach detach source setMethod setGeneric setGroupGeneric setClass ...",
                    literal: "NULL NA TRUE FALSE T F Inf NaN NA_integer_|10 NA_real_|10 NA_character_|10 NA_complex_|10"
                },
                r: 0
            },
            {
                cN: "number",
                b: "0[xX][0-9a-fA-F]+[Li]?\\b",
                r: 0
            },
            {
                cN: "number",
                b: "\\d+(?:[eE][+\\-]?\\d*)?L\\b",
                r: 0
            },
            {
                cN: "number",
                b: "\\d+\\.(?!\\d)(?:i\\b)?",
                r: 0
            },
            {
                cN: "number",
                b: "\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d*)?i?\\b",
                r: 0
            },
            {
                cN: "number",
                b: "\\.\\d+(?:[eE][+\\-]?\\d*)?i?\\b",
                r: 0
            },
            {
                b: "`",
                e: "`",
                r: 0
            },
            {
                cN: "string",
                c: [e.BE],
                v: [{
                    b: '"',
                    e: '"'
                },
                {
                    b: "'",
                    e: "'"
                }]
            }]
        }
    }),
    e.registerLanguage("ruby",
    function(e) {
        var t = "[a-zA-Z_]\\w*[!?=]?|[-+~]\\@|<<|>>|=~|===?|<=>|[<>]=?|\\*\\*|[-/+%^&*~`|]|\\[\\]=?",
        r = {
            keyword: "and then defined module in return redo if BEGIN retry end for self when next until do begin unless END rescue else break undef not super class case require yield alias while ensure elsif or include attr_reader attr_writer attr_accessor",
            literal: "true false nil"
        },
        a = {
            cN: "doctag",
            b: "@[A-Za-z]+"
        },
        n = {
            b: "#<",
            e: ">"
        },
        i = [e.C("#", "$", {
            c: [a]
        }), e.C("^\\=begin", "^\\=end", {
            c: [a],
            r: 10
        }), e.C("^__END__", "\\n$")],
        s = {
            cN: "subst",
            b: "#\\{",
            e: "}",
            k: r
        },
        o = {
            cN: "string",
            c: [e.BE, s],
            v: [{
                b: /'/,
                e: /'/
            },
            {
                b: /"/,
                e: /"/
            },
            {
                b: /`/,
                e: /`/
            },
            {
                b: "%[qQwWx]?\\(",
                e: "\\)"
            },
            {
                b: "%[qQwWx]?\\[",
                e: "\\]"
            },
            {
                b: "%[qQwWx]?{",
                e: "}"
            },
            {
                b: "%[qQwWx]?<",
                e: ">"
            },
            {
                b: "%[qQwWx]?/",
                e: "/"
            },
            {
                b: "%[qQwWx]?%",
                e: "%"
            },
            {
                b: "%[qQwWx]?-",
                e: "-"
            },
            {
                b: "%[qQwWx]?\\|",
                e: "\\|"
            },
            {
                b: /\B\?(\\\d{1,3}|\\x[A-Fa-f0-9]{1,2}|\\u[A-Fa-f0-9]{4}|\\?\S)\b/
            },
            {
                b: /<<(-?)\w+$/,
                e: /^\s*\w+$/
            }]
        },
        c = {
            cN: "params",
            b: "\\(",
            e: "\\)",
            endsParent: !0,
            k: r
        },
        l = [o, n, {
            cN: "class",
            bK: "class module",
            e: "$|;",
            i: /=/,
            c: [e.inherit(e.TM, {
                b: "[A-Za-z_]\\w*(::\\w+)*(\\?|\\!)?"
            }), {
                b: "<\\s*",
                c: [{
                    b: "(" + e.IR + "::)?" + e.IR
                }]
            }].concat(i)
        },
        {
            cN: "function",
            bK: "def",
            e: "$|;",
            c: [e.inherit(e.TM, {
                b: t
            }), c].concat(i)
        },
        {
            b: e.IR + "::"
        },
        {
            cN: "symbol",
            b: e.UIR + "(\\!|\\?)?:",
            r: 0
        },
        {
            cN: "symbol",
            b: ":(?!\\s)",
            c: [o, {
                b: t
            }],
            r: 0
        },
        {
            cN: "number",
            b: "(\\b0[0-7_]+)|(\\b0x[0-9a-fA-F_]+)|(\\b[1-9][0-9_]*(\\.[0-9_]+)?)|[0_]\\b",
            r: 0
        },
        {
            b: "(\\$\\W)|((\\$|\\@\\@?)(\\w+))"
        },
        {
            cN: "params",
            b: /\|/,
            e: /\|/,
            k: r
        },
        {
            b: "(" + e.RSR + "|unless)\\s*",
            k: "unless",
            c: [n, {
                cN: "regexp",
                c: [e.BE, s],
                i: /\n/,
                v: [{
                    b: "/",
                    e: "/[a-z]*"
                },
                {
                    b: "%r{",
                    e: "}[a-z]*"
                },
                {
                    b: "%r\\(",
                    e: "\\)[a-z]*"
                },
                {
                    b: "%r!",
                    e: "![a-z]*"
                },
                {
                    b: "%r\\[",
                    e: "\\][a-z]*"
                }]
            }].concat(i),
            r: 0
        }].concat(i);
        s.c = l,
        c.c = l;
        var u = "[>?]>",
        d = "[\\w#]+\\(\\w+\\):\\d+:\\d+>",
        b = "(\\w+-)?\\d+\\.\\d+\\.\\d(p\\d+)?[^>]+>",
        p = [{
            b: /^\s*=>/,
            starts: {
                e: "$",
                c: l
            }
        },
        {
            cN: "meta",
            b: "^(" + u + "|" + d + "|" + b + ")",
            starts: {
                e: "$",
                c: l
            }
        }];
        return {
            aliases: ["rb", "gemspec", "podspec", "thor", "irb"],
            k: r,
            i: /\/\*/,
            c: i.concat(p).concat(l)
        }
    }),
    e.registerLanguage("rust",
    function(e) {
        var t = "([ui](8|16|32|64|128|size)|f(32|64))?",
        r = "alignof as be box break const continue crate do else enum extern false fn for if impl in let loop match mod mut offsetof once priv proc pub pure ref return self Self sizeof static struct super trait true type typeof unsafe unsized use virtual while where yield move default",
        a = "drop i8 i16 i32 i64 i128 isize u8 u16 u32 u64 u128 usize f32 f64 str char bool Box Option Result String Vec Copy Send Sized Sync Drop Fn FnMut FnOnce ToOwned Clone Debug PartialEq PartialOrd Eq Ord AsRef AsMut Into From Default Iterator Extend IntoIterator DoubleEndedIterator ExactSizeIterator SliceConcatExt ToString assert! assert_eq! bitflags! bytes! cfg! col! concat! concat_idents! debug_assert! debug_assert_eq! env! panic! file! format! format_args! include_bin! include_str! line! local_data_key! module_path! option_env! print! println! select! stringify! try! unimplemented! unreachable! vec! write! writeln! macro_rules! assert_ne! debug_assert_ne!";
        return {
            aliases: ["rs"],
            k: {
                keyword: r,
                literal: "true false Some None Ok Err",
                built_in: a
            },
            l: e.IR + "!?",
            i: "</",
            c: [e.CLCM, e.C("/\\*", "\\*/", {
                c: ["self"]
            }), e.inherit(e.QSM, {
                b: /b?"/,
                i: null
            }), {
                cN: "string",
                v: [{
                    b: /r(#*)"(.|\n)*?"\1(?!#)/
                },
                {
                    b: /b?'\\?(x\w{2}|u\w{4}|U\w{8}|.)'/
                }]
            },
            {
                cN: "symbol",
                b: /'[a-zA-Z_][a-zA-Z0-9_]*/
            },
            {
                cN: "number",
                v: [{
                    b: "\\b0b([01_]+)" + t
                },
                {
                    b: "\\b0o([0-7_]+)" + t
                },
                {
                    b: "\\b0x([A-Fa-f0-9_]+)" + t
                },
                {
                    b: "\\b(\\d[\\d_]*(\\.[0-9_]+)?([eE][+-]?[0-9_]+)?)" + t
                }],
                r: 0
            },
            {
                cN: "function",
                bK: "fn",
                e: "(\\(|<)",
                eE: !0,
                c: [e.UTM]
            },
            {
                cN: "meta",
                b: "#\\!?\\[",
                e: "\\]",
                c: [{
                    cN: "meta-string",
                    b: /"/,
                    e: /"/
                }]
            },
            {
                cN: "class",
                bK: "type",
                e: ";",
                c: [e.inherit(e.UTM, {
                    endsParent: !0
                })],
                i: "\\S"
            },
            {
                cN: "class",
                bK: "trait enum struct union",
                e: "{",
                c: [e.inherit(e.UTM, {
                    endsParent: !0
                })],
                i: "[\\w\\d]"
            },
            {
                b: e.IR + "::",
                k: {
                    built_in: a
                }
            },
            {
                b: "->"
            }]
        }
    }),
    e.registerLanguage("scheme",
    function(e) {
        var t = "[^\\(\\)\\[\\]\\{\\}\",'`;#|\\\\\\s]+",
        r = "(\\-|\\+)?\\d+([./]\\d+)?",
        a = r + "[+\\-]" + r + "i",
        n = {
            "builtin-name": "case-lambda call/cc class define-class exit-handler field import inherit init-field interface let*-values let-values let/ec mixin opt-lambda override protect provide public rename require require-for-syntax syntax syntax-case syntax-error unit/sig unless when with-syntax and begin call-with-current-continuation call-with-input-file call-with-output-file case cond define define-syntax delay do dynamic-wind else for-each if lambda let let* let-syntax letrec letrec-syntax map or syntax-rules ' * + , ,@ - ... / ; < <= = => > >= ` abs acos angle append apply asin assoc assq assv atan boolean? caar cadr call-with-input-file call-with-output-file call-with-values car cdddar cddddr cdr ceiling char->integer char-alphabetic? char-ci<=? char-ci<? char-ci=? char-ci>=? char-ci>? char-downcase char-lower-case? char-numeric? char-ready? char-upcase char-upper-case? char-whitespace? char<=? char<? char=? char>=? char>? char? close-input-port close-output-port complex? cons cos current-input-port current-output-port denominator display eof-object? eq? equal? eqv? eval even? exact->inexact exact? exp expt floor force gcd imag-part inexact->exact inexact? input-port? integer->char integer? interaction-environment lcm length list list->string list->vector list-ref list-tail list? load log magnitude make-polar make-rectangular make-string make-vector max member memq memv min modulo negative? newline not null-environment null? number->string number? numerator odd? open-input-file open-output-file output-port? pair? peek-char port? positive? procedure? quasiquote quote quotient rational? rationalize read read-char real-part real? remainder reverse round scheme-report-environment set! set-car! set-cdr! sin sqrt string string->list string->number string->symbol string-append string-ci<=? string-ci<? string-ci=? string-ci>=? string-ci>? string-copy string-fill! string-length string-ref string-set! string<=? string<? string=? string>=? string>? string? substring symbol->string symbol? tan transcript-off transcript-on truncate values vector vector->list vector-fill! vector-length vector-ref vector-set! with-input-from-file with-output-to-file write write-char zero?"
        },
        i = {
            cN: "meta",
            b: "^#!",
            e: "$"
        },
        s = {
            cN: "literal",
            b: "(#t|#f|#\\\\" + t + "|#\\\\.)"
        },
        o = {
            cN: "number",
            v: [{
                b: r,
                r: 0
            },
            {
                b: a,
                r: 0
            },
            {
                b: "#b[0-1]+(/[0-1]+)?"
            },
            {
                b: "#o[0-7]+(/[0-7]+)?"
            },
            {
                b: "#x[0-9a-f]+(/[0-9a-f]+)?"
            }]
        },
        c = e.QSM,
        l = [e.C(";", "$", {
            r: 0
        }), e.C("#\\|", "\\|#")],
        u = {
            b: t,
            r: 0
        },
        d = {
            cN: "symbol",
            b: "'" + t
        },
        b = {
            eW: !0,
            r: 0
        },
        p = {
            v: [{
                b: /'/
            },
            {
                b: "`"
            }],
            c: [{
                b: "\\(",
                e: "\\)",
                c: ["self", s, c, o, u, d]
            }]
        },
        m = {
            cN: "name",
            b: t,
            l: t,
            k: n
        },
        g = {
            b: /lambda/,
            eW: !0,
            rB: !0,
            c: [m, {
                b: /\(/,
                e: /\)/,
                endsParent: !0,
                c: [u]
            }]
        },
        f = {
            v: [{
                b: "\\(",
                e: "\\)"
            },
            {
                b: "\\[",
                e: "\\]"
            }],
            c: [g, m, b]
        };
        return b.c = [s, o, c, u, d, p, f].concat(l),
        {
            i: /\S/,
            c: [i, o, c, d, p, f].concat(l)
        }
    }),
    e.registerLanguage("shell",
    function(e) {
        return {
            aliases: ["console"],
            c: [{
                cN: "meta",
                b: "^\\s{0,3}[\\w\\d\\[\\]()@-]*[>%$#]",
                starts: {
                    e: "$",
                    sL: "bash"
                }
            }]
        }
    }),
    e.registerLanguage("sql",
    function(e) {
        var t = e.C("--", "$");
        return {
            cI: !0,
            i: /[<>{}*]/,
            c: [{
                bK: "begin end start commit rollback savepoint lock alter create drop rename call delete do handler insert load replace select truncate update set show pragma grant merge describe use explain help declare prepare execute deallocate release unlock purge reset change stop analyze cache flush optimize repair kill install uninstall checksum restore check backup revoke comment values with",
                e: /;/,
                eW: !0,
                l: /[\w\.]+/,
                k: {
                    keyword: "as abort abs absolute acc acce accep accept access accessed accessible account acos action activate add addtime admin administer advanced advise aes_decrypt aes_encrypt after agent aggregate ali alia alias all allocate allow alter always analyze ancillary and anti any anydata anydataset anyschema anytype apply archive archived archivelog are as asc ascii asin assembly assertion associate asynchronous at atan atn2 attr attri attrib attribu attribut attribute attributes audit authenticated authentication authid authors auto autoallocate autodblink autoextend automatic availability avg backup badfile basicfile before begin beginning benchmark between bfile bfile_base big bigfile bin binary_double binary_float binlog bit_and bit_count bit_length bit_or bit_xor bitmap blob_base block blocksize body both bound bucket buffer_cache buffer_pool build bulk by byte byteordermark bytes cache caching call calling cancel capacity cascade cascaded case cast catalog category ceil ceiling chain change changed char_base char_length character_length characters characterset charindex charset charsetform charsetid check checksum checksum_agg child choose chr chunk class cleanup clear client clob clob_base clone close cluster_id cluster_probability cluster_set clustering coalesce coercibility col collate collation collect colu colum column column_value columns columns_updated comment commit compact compatibility compiled complete composite_limit compound compress compute concat concat_ws concurrent confirm conn connec connect connect_by_iscycle connect_by_isleaf connect_by_root connect_time connection consider consistent constant constraint constraints constructor container content contents context contributors controlfile conv convert convert_tz corr corr_k corr_s corresponding corruption cos cost count count_big counted covar_pop covar_samp cpu_per_call cpu_per_session crc32 create creation critical cross cube cume_dist curdate current current_date current_time current_timestamp current_user cursor curtime customdatum cycle data database databases datafile datafiles datalength date_add date_cache date_format date_sub dateadd datediff datefromparts datename datepart datetime2fromparts day day_to_second dayname dayofmonth dayofweek dayofyear days db_role_change dbtimezone ddl deallocate declare decode decompose decrement decrypt deduplicate def defa defau defaul default defaults deferred defi defin define degrees delayed delegate delete delete_all delimited demand dense_rank depth dequeue des_decrypt des_encrypt des_key_file desc descr descri describ describe descriptor deterministic diagnostics difference dimension direct_load directory disable disable_all disallow disassociate discardfile disconnect diskgroup distinct distinctrow distribute distributed div do document domain dotnet double downgrade drop dumpfile duplicate duration each edition editionable editions element ellipsis else elsif elt empty enable enable_all enclosed encode encoding encrypt end end-exec endian enforced engine engines enqueue enterprise entityescaping eomonth error errors escaped evalname evaluate event eventdata events except exception exceptions exchange exclude excluding execu execut execute exempt exists exit exp expire explain explode export export_set extended extent external external_1 external_2 externally extract failed failed_login_attempts failover failure far fast feature_set feature_value fetch field fields file file_name_convert filesystem_like_logging final finish first first_value fixed flash_cache flashback floor flush following follows for forall force foreign form forma format found found_rows freelist freelists freepools fresh from from_base64 from_days ftp full function general generated get get_format get_lock getdate getutcdate global global_name globally go goto grant grants greatest group group_concat group_id grouping grouping_id groups gtid_subtract guarantee guard handler hash hashkeys having hea head headi headin heading heap help hex hierarchy high high_priority hosts hour hours http id ident_current ident_incr ident_seed identified identity idle_time if ifnull ignore iif ilike ilm immediate import in include including increment index indexes indexing indextype indicator indices inet6_aton inet6_ntoa inet_aton inet_ntoa infile initial initialized initially initrans inmemory inner innodb input insert install instance instantiable instr interface interleaved intersect into invalidate invisible is is_free_lock is_ipv4 is_ipv4_compat is_not is_not_null is_used_lock isdate isnull isolation iterate java join json json_exists keep keep_duplicates key keys kill language large last last_day last_insert_id last_value lateral lax lcase lead leading least leaves left len lenght length less level levels library like like2 like4 likec limit lines link list listagg little ln load load_file lob lobs local localtime localtimestamp locate locator lock locked log log10 log2 logfile logfiles logging logical logical_reads_per_call logoff logon logs long loop low low_priority lower lpad lrtrim ltrim main make_set makedate maketime managed management manual map mapping mask master master_pos_wait match matched materialized max maxextents maximize maxinstances maxlen maxlogfiles maxloghistory maxlogmembers maxsize maxtrans md5 measures median medium member memcompress memory merge microsecond mid migration min minextents minimum mining minus minute minutes minvalue missing mod mode model modification modify module monitoring month months mount move movement multiset mutex name name_const names nan national native natural nav nchar nclob nested never new newline next nextval no no_write_to_binlog noarchivelog noaudit nobadfile nocheck nocompress nocopy nocycle nodelay nodiscardfile noentityescaping noguarantee nokeep nologfile nomapping nomaxvalue nominimize nominvalue nomonitoring none noneditionable nonschema noorder nopr nopro noprom nopromp noprompt norely noresetlogs noreverse normal norowdependencies noschemacheck noswitch not nothing notice notnull notrim novalidate now nowait nth_value nullif nulls num numb numbe nvarchar nvarchar2 object ocicoll ocidate ocidatetime ociduration ociinterval ociloblocator ocinumber ociref ocirefcursor ocirowid ocistring ocitype oct octet_length of off offline offset oid oidindex old on online only opaque open operations operator optimal optimize option optionally or oracle oracle_date oradata ord ordaudio orddicom orddoc order ordimage ordinality ordvideo organization orlany orlvary out outer outfile outline output over overflow overriding package pad parallel parallel_enable parameters parent parse partial partition partitions pascal passing password password_grace_time password_lock_time password_reuse_max password_reuse_time password_verify_function patch path patindex pctincrease pctthreshold pctused pctversion percent percent_rank percentile_cont percentile_disc performance period period_add period_diff permanent physical pi pipe pipelined pivot pluggable plugin policy position post_transaction pow power pragma prebuilt precedes preceding precision prediction prediction_cost prediction_details prediction_probability prediction_set prepare present preserve prior priority private private_sga privileges procedural procedure procedure_analyze processlist profiles project prompt protection public publishingservername purge quarter query quick quiesce quota quotename radians raise rand range rank raw read reads readsize rebuild record records recover recovery recursive recycle redo reduced ref reference referenced references referencing refresh regexp_like register regr_avgx regr_avgy regr_count regr_intercept regr_r2 regr_slope regr_sxx regr_sxy reject rekey relational relative relaylog release release_lock relies_on relocate rely rem remainder rename repair repeat replace replicate replication required reset resetlogs resize resource respect restore restricted result result_cache resumable resume retention return returning returns reuse reverse revoke right rlike role roles rollback rolling rollup round row row_count rowdependencies rowid rownum rows rtrim rules safe salt sample save savepoint sb1 sb2 sb4 scan schema schemacheck scn scope scroll sdo_georaster sdo_topo_geometry search sec_to_time second seconds section securefile security seed segment select self semi sequence sequential serializable server servererror session session_user sessions_per_user set sets settings sha sha1 sha2 share shared shared_pool short show shrink shutdown si_averagecolor si_colorhistogram si_featurelist si_positionalcolor si_stillimage si_texture siblings sid sign sin size size_t sizes skip slave sleep smalldatetimefromparts smallfile snapshot some soname sort soundex source space sparse spfile split sql sql_big_result sql_buffer_result sql_cache sql_calc_found_rows sql_small_result sql_variant_property sqlcode sqldata sqlerror sqlname sqlstate sqrt square standalone standby start starting startup statement static statistics stats_binomial_test stats_crosstab stats_ks_test stats_mode stats_mw_test stats_one_way_anova stats_t_test_ stats_t_test_indep stats_t_test_one stats_t_test_paired stats_wsr_test status std stddev stddev_pop stddev_samp stdev stop storage store stored str str_to_date straight_join strcmp strict string struct stuff style subdate subpartition subpartitions substitutable substr substring subtime subtring_index subtype success sum suspend switch switchoffset switchover sync synchronous synonym sys sys_xmlagg sysasm sysaux sysdate sysdatetimeoffset sysdba sysoper system system_user sysutcdatetime table tables tablespace tablesample tan tdo template temporary terminated tertiary_weights test than then thread through tier ties time time_format time_zone timediff timefromparts timeout timestamp timestampadd timestampdiff timezone_abbr timezone_minute timezone_region to to_base64 to_date to_days to_seconds todatetimeoffset trace tracking transaction transactional translate translation treat trigger trigger_nestlevel triggers trim truncate try_cast try_convert try_parse type ub1 ub2 ub4 ucase unarchived unbounded uncompress under undo unhex unicode uniform uninstall union unique unix_timestamp unknown unlimited unlock unnest unpivot unrecoverable unsafe unsigned until untrusted unusable unused update updated upgrade upped upper upsert url urowid usable usage use use_stored_outlines user user_data user_resources users using utc_date utc_timestamp uuid uuid_short validate validate_password_strength validation valist value values var var_samp varcharc vari varia variab variabl variable variables variance varp varraw varrawc varray verify version versions view virtual visible void wait wallet warning warnings week weekday weekofyear wellformed when whene whenev wheneve whenever where while whitespace window with within without work wrapped xdb xml xmlagg xmlattributes xmlcast xmlcolattval xmlelement xmlexists xmlforest xmlindex xmlnamespaces xmlpi xmlquery xmlroot xmlschema xmlserialize xmltable xmltype xor year year_to_month years yearweek",
                    literal: "true false null unknown",
                    built_in: "array bigint binary bit blob bool boolean char character date dec decimal float int int8 integer interval number numeric real record serial serial8 smallint text time timestamp tinyint varchar varying void"
                },
                c: [{
                    cN: "string",
                    b: "'",
                    e: "'",
                    c: [e.BE, {
                        b: "''"
                    }]
                },
                {
                    cN: "string",
                    b: '"',
                    e: '"',
                    c: [e.BE, {
                        b: '""'
                    }]
                },
                {
                    cN: "string",
                    b: "`",
                    e: "`",
                    c: [e.BE]
                },
                e.CNM, e.CBCM, t, e.HCM]
            },
            e.CBCM, t, e.HCM]
        }
    }),
    e.registerLanguage("swift",
    function(e) {
        var t = {
            keyword: "#available #colorLiteral #column #else #elseif #endif #file #fileLiteral #function #if #imageLiteral #line #selector #sourceLocation _ __COLUMN__ __FILE__ __FUNCTION__ __LINE__ Any as as! as? associatedtype associativity break case catch class continue convenience default defer deinit didSet do dynamic dynamicType else enum extension fallthrough false fileprivate final for func get guard if import in indirect infix init inout internal is lazy left let mutating nil none nonmutating open operator optional override postfix precedence prefix private protocol Protocol public repeat required rethrows return right self Self set static struct subscript super switch throw throws true try try! try? Type typealias unowned var weak where while willSet",
            literal: "true false nil",
            built_in: "abs advance alignof alignofValue anyGenerator assert assertionFailure bridgeFromObjectiveC bridgeFromObjectiveCUnconditional bridgeToObjectiveC bridgeToObjectiveCUnconditional c contains count countElements countLeadingZeros debugPrint debugPrintln distance dropFirst dropLast dump encodeBitsAsWords enumerate equal fatalError filter find getBridgedObjectiveCType getVaList indices insertionSort isBridgedToObjectiveC isBridgedVerbatimToObjectiveC isUniquelyReferenced isUniquelyReferencedNonObjC join lazy lexicographicalCompare map max maxElement min minElement numericCast overlaps partition posix precondition preconditionFailure print println quickSort readLine reduce reflect reinterpretCast reverse roundUpToAlignment sizeof sizeofValue sort split startsWith stride strideof strideofValue swap toString transcode underestimateCount unsafeAddressOf unsafeBitCast unsafeDowncast unsafeUnwrap unsafeReflect withExtendedLifetime withObjectAtPlusZero withUnsafePointer withUnsafePointerToObject withUnsafeMutablePointer withUnsafeMutablePointers withUnsafePointer withUnsafePointers withVaList zip"
        },
        r = {
            cN: "type",
            b: "\\b[A-Z][\\wÃ€-Ê¸']*",
            r: 0
        },
        a = e.C("/\\*", "\\*/", {
            c: ["self"]
        }),
        n = {
            cN: "subst",
            b: /\\\(/,
            e: "\\)",
            k: t,
            c: []
        },
        i = {
            cN: "string",
            c: [e.BE, n],
            v: [{
                b: /"""/,
                e: /"""/
            },
            {
                b: /"/,
                e: /"/
            }]
        },
        s = {
            cN: "number",
            b: "\\b([\\d_]+(\\.[\\deE_]+)?|0x[a-fA-F0-9_]+(\\.[a-fA-F0-9p_]+)?|0b[01_]+|0o[0-7_]+)\\b",
            r: 0
        };
        return n.c = [s],
        {
            k: t,
            c: [i, e.CLCM, a, r, s, {
                cN: "function",
                bK: "func",
                e: "{",
                eE: !0,
                c: [e.inherit(e.TM, {
                    b: /[A-Za-z$_][0-9A-Za-z$_]*/
                }), {
                    b: /</,
                    e: />/
                },
                {
                    cN: "params",
                    b: /\(/,
                    e: /\)/,
                    endsParent: !0,
                    k: t,
                    c: ["self", s, i, e.CBCM, {
                        b: ":"
                    }],
                    i: /["']/
                }],
                i: /\[|%/
            },
            {
                cN: "class",
                bK: "struct protocol class extension enum",
                k: t,
                e: "\\{",
                eE: !0,
                c: [e.inherit(e.TM, {
                    b: /[A-Za-z$_][\u00C0-\u02B80-9A-Za-z$_]*/
                })]
            },
            {
                cN: "meta",
                b: "(@discardableResult|@warn_unused_result|@exported|@lazy|@noescape|@NSCopying|@NSManaged|@objc|@objcMembers|@convention|@required|@noreturn|@IBAction|@IBDesignable|@IBInspectable|@IBOutlet|@infix|@prefix|@postfix|@autoclosure|@testable|@available|@nonobjc|@NSApplicationMain|@UIApplicationMain)"
            },
            {
                bK: "import",
                e: /$/,
                c: [e.CLCM, a]
            }]
        }
    }),
    e.registerLanguage("tex",
    function(e) {
        var t = {
            cN: "tag",
            b: /\\/,
            r: 0,
            c: [{
                cN: "name",
                v: [{
                    b: /[a-zA-ZÐ°-ÑÐ-Ñ]+[*]?/
                },
                {
                    b: /[^a-zA-ZÐ°-ÑÐ-Ñ0-9]/
                }],
                starts: {
                    eW: !0,
                    r: 0,
                    c: [{
                        cN: "string",
                        v: [{
                            b: /\[/,
                            e: /\]/
                        },
                        {
                            b: /\{/,
                            e: /\}/
                        }]
                    },
                    {
                        b: /\s*=\s*/,
                        eW: !0,
                        r: 0,
                        c: [{
                            cN: "number",
                            b: /-?\d*\.?\d+(pt|pc|mm|cm|in|dd|cc|ex|em)?/
                        }]
                    }]
                }
            }]
        };
        return {
            c: [t, {
                cN: "formula",
                c: [t],
                r: 0,
                v: [{
                    b: /\$\$/,
                    e: /\$\$/
                },
                {
                    b: /\$/,
                    e: /\$/
                }]
            },
            e.C("%", "$", {
                r: 0
            })]
        }
    }),
    e.registerLanguage("typescript",
    function(e) {
        var t = "[A-Za-z$_][0-9A-Za-z$_]*",
        r = {
            keyword: "in if for while finally var new function do return void else break catch instanceof with throw case default try this switch continue typeof delete let yield const class public private protected get set super static implements enum export import declare type namespace abstract as from extends async await",
            literal: "true false null undefined NaN Infinity",
            built_in: "eval isFinite isNaN parseFloat parseInt decodeURI decodeURIComponent encodeURI encodeURIComponent escape unescape Object Function Boolean Error EvalError InternalError RangeError ReferenceError StopIteration SyntaxError TypeError URIError Number Math Date String RegExp Array Float32Array Float64Array Int16Array Int32Array Int8Array Uint16Array Uint32Array Uint8Array Uint8ClampedArray ArrayBuffer DataView JSON Intl arguments require module console window document any number boolean string void Promise"
        },
        a = {
            cN: "meta",
            b: "@" + t
        },
        n = {
            b: "\\(",
            e: /\)/,
            k: r,
            c: ["self", e.QSM, e.ASM, e.NM]
        },
        i = {
            cN: "params",
            b: /\(/,
            e: /\)/,
            eB: !0,
            eE: !0,
            k: r,
            c: [e.CLCM, e.CBCM, a, n]
        };
        return {
            aliases: ["ts"],
            k: r,
            c: [{
                cN: "meta",
                b: /^\s*['"]use strict['"]/
            },
            e.ASM, e.QSM, {
                cN: "string",
                b: "`",
                e: "`",
                c: [e.BE, {
                    cN: "subst",
                    b: "\\$\\{",
                    e: "\\}"
                }]
            },
            e.CLCM, e.CBCM, {
                cN: "number",
                v: [{
                    b: "\\b(0[bB][01]+)"
                },
                {
                    b: "\\b(0[oO][0-7]+)"
                },
                {
                    b: e.CNR
                }],
                r: 0
            },
            {
                b: "(" + e.RSR + "|\\b(case|return|throw)\\b)\\s*",
                k: "return throw case",
                c: [e.CLCM, e.CBCM, e.RM, {
                    cN: "function",
                    b: "(\\(.*?\\)|" + e.IR + ")\\s*=>",
                    rB: !0,
                    e: "\\s*=>",
                    c: [{
                        cN: "params",
                        v: [{
                            b: e.IR
                        },
                        {
                            b: /\(\s*\)/
                        },
                        {
                            b: /\(/,
                            e: /\)/,
                            eB: !0,
                            eE: !0,
                            k: r,
                            c: ["self", e.CLCM, e.CBCM]
                        }]
                    }]
                }],
                r: 0
            },
            {
                cN: "function",
                b: "function",
                e: /[\{;]/,
                eE: !0,
                k: r,
                c: ["self", e.inherit(e.TM, {
                    b: t
                }), i],
                i: /%/,
                r: 0
            },
            {
                bK: "constructor",
                e: /\{/,
                eE: !0,
                c: ["self", i]
            },
            {
                b: /module\./,
                k: {
                    built_in: "module"
                },
                r: 0
            },
            {
                bK: "module",
                e: /\{/,
                eE: !0
            },
            {
                bK: "interface",
                e: /\{/,
                eE: !0,
                k: "interface extends"
            },
            {
                b: /\$[(.]/
            },
            {
                b: "\\." + e.IR,
                r: 0
            },
            a, n]
        }
    }),
    e.registerLanguage("yaml",
    function(e) {
        var t = "true false yes no null",
        r = "^[ \\-]*",
        a = "[a-zA-Z_][\\w\\-]*",
        n = {
            cN: "attr",
            v: [{
                b: r + a + ":"
            },
            {
                b: r + '"' + a + '":'
            },
            {
                b: r + "'" + a + "':"
            }]
        },
        i = {
            cN: "template-variable",
            v: [{
                b: "{{",
                e: "}}"
            },
            {
                b: "%{",
                e: "}"
            }]
        },
        s = {
            cN: "string",
            r: 0,
            v: [{
                b: /'/,
                e: /'/
            },
            {
                b: /"/,
                e: /"/
            },
            {
                b: /\S+/
            }],
            c: [e.BE, i]
        };
        return {
            cI: !0,
            aliases: ["yml", "YAML", "yaml"],
            c: [n, {
                cN: "meta",
                b: "^---s*$",
                r: 10
            },
            {
                cN: "string",
                b: "[\\|>] *$",
                rE: !0,
                c: s.c,
                e: n.v[0].b
            },
            {
                b: "<%[%=-]?",
                e: "[%-]?%>",
                sL: "ruby",
                eB: !0,
                eE: !0,
                r: 0
            },
            {
                cN: "type",
                b: "!" + e.UIR
            },
            {
                cN: "type",
                b: "!!" + e.UIR
            },
            {
                cN: "meta",
                b: "&" + e.UIR + "$"
            },
            {
                cN: "meta",
                b: "\\*" + e.UIR + "$"
            },
            {
                cN: "bullet",
                b: "^ *-",
                r: 0
            },
            e.HCM, {
                bK: t,
                k: {
                    literal: t
                }
            },
            e.CNM, s]
        }
    }),
    e
});