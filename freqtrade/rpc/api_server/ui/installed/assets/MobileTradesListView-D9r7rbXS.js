import{_ as I}from"./TradeDetail-D2NK4zQT.js";import{V as S,o as r,c as l,a as n,f as B,M as v,b as c,_ as C,O as $,r as w,n as g,v as k,I as F,J as q,A as t,s as m,y as i,W as h,a6 as j,a8 as z,ag as E,d as M,S as O}from"./index-BNCVPFy5.js";import{a as P,_ as A,d as G}from"./InfoBox.vue_vue_type_script_setup_true_lang-5y6r1Rhw.js";import"./event-a_bi5ysw-CCMJ8JbX.js";const R={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"};function U(a,e){return r(),l("svg",R,e[0]||(e[0]=[n("path",{fill:"currentColor",d:"M20 11v2H8l5.5 5.5l-1.42 1.42L4.16 12l7.92-7.92L13.5 5.5L8 11z"},null,-1)]))}const H=S({name:"mdi-arrow-left",render:U}),J={class:"d-flex"},W={class:"px-1 d-flex flex-row flex-fill text-start justify-content-between align-items-center"},Z={class:"me-1 fw-bold"},K={class:"text-secondary"},Q=B({__name:"CustomTradeListEntry",props:{trade:{type:Object,required:!0},stakeCurrencyDecimals:{type:Number,required:!0},showDetails:{type:Boolean,default:!1}},setup(a){return(e,p)=>{const s=A;return r(),l("div",J,[n("div",W,[n("span",null,[n("span",Z,v(a.trade.pair),1),n("small",K,"(#"+v(a.trade.trade_id)+")",1)]),n("small",null,[c(s,{date:a.trade.open_timestamp,"date-only":!0},null,8,["date"])])]),c(P,{class:"col-5",trade:a.trade},null,8,["trade"])])}}}),X=C(Q,[["__scopeId","data-v-bd4ea2df"]]),Y={class:"h-100 overflow-auto p-1"},ee={key:0,class:"mt-5"},te={class:"w-100 d-flex justify-content-between mt-1"},ae=B({__name:"CustomTradeList",props:{trades:{required:!0,type:Array},title:{default:"Trades",type:String},stakeCurrency:{required:!1,default:"",type:String},activeTrades:{default:!1,type:Boolean},showFilter:{default:!1,type:Boolean},multiBotView:{default:!1,type:Boolean},emptyText:{default:"No Trades to show.",type:String},stakeCurrencyDecimals:{default:3,type:Number}},setup(a){const e=a,p=$(),s=w(1),d=w(""),u=e.activeTrades?200:25,f=g(()=>e.trades.length),y=g(()=>e.trades.slice((s.value-1)*u,s.value*u)),T=x=>{p.activeBot.setDetailTrade(x)};return(x,_)=>{const b=X,D=j,L=z,V=G,N=E;return r(),l("div",Y,[c(L,{id:"tradeList"},{default:k(()=>[(r(!0),l(F,null,q(t(y),o=>(r(),m(D,{key:o.trade_id,class:"border border-secondary rounded my-05 px-1",onClick:oe=>T(o)},{default:k(()=>[c(b,{trade:o,"stake-currency-decimals":a.stakeCurrencyDecimals},null,8,["trade","stake-currency-decimals"])]),_:2},1032,["onClick"]))),128))]),_:1}),a.trades.length==0?(r(),l("span",ee,v(a.emptyText),1)):i("",!0),n("div",te,[a.activeTrades?i("",!0):(r(),m(V,{key:0,modelValue:t(s),"onUpdate:modelValue":_[0]||(_[0]=o=>h(s)?s.value=o:null),"total-rows":t(f),"per-page":t(u),"aria-controls":"tradeList"},null,8,["modelValue","total-rows","per-page"])),a.showFilter?(r(),m(N,{key:1,modelValue:t(d),"onUpdate:modelValue":_[1]||(_[1]=o=>h(d)?d.value=o:null),type:"text",placeholder:"Filter",size:"sm",style:{width:"unset"}},null,8,["modelValue"])):i("",!0)])])}}}),se=C(ae,[["__scopeId","data-v-0134679c"]]),re={key:2,class:"d-flex flex-column"},ie=B({__name:"MobileTradesListView",props:{history:{default:!1,type:Boolean}},setup(a){const e=$();return(p,s)=>{const d=se,u=H,f=O,y=I;return r(),l("div",null,[!a.history&&!t(e).activeBot.detailTradeId?(r(),m(d,{key:0,trades:t(e).activeBot.openTrades,title:"Open trades","active-trades":!0,"stake-currency-decimals":t(e).activeBot.stakeCurrencyDecimals,"empty-text":"No open Trades."},null,8,["trades","stake-currency-decimals"])):i("",!0),a.history&&!t(e).activeBot.detailTradeId?(r(),m(d,{key:1,trades:t(e).activeBot.closedTrades,title:"Trade history","stake-currency-decimals":t(e).activeBot.stakeCurrencyDecimals,"empty-text":"No closed trades so far."},null,8,["trades","stake-currency-decimals"])):i("",!0),t(e).activeBot.detailTradeId&&t(e).activeBot.tradeDetail?(r(),l("div",re,[c(f,{size:"sm",class:"align-self-start my-1 ms-1",onClick:s[0]||(s[0]=T=>t(e).activeBot.setDetailTrade(null))},{default:k(()=>[c(u),s[1]||(s[1]=M(" Back"))]),_:1}),c(y,{trade:t(e).activeBot.tradeDetail,"stake-currency":t(e).activeBot.stakeCurrency},null,8,["trade","stake-currency"])])):i("",!0)])}}});export{ie as default};
//# sourceMappingURL=MobileTradesListView-D9r7rbXS.js.map
