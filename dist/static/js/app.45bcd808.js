(function(t){function e(e){for(var a,r,i=e[0],c=e[1],l=e[2],d=0,p=[];d<i.length;d++)r=i[d],Object.prototype.hasOwnProperty.call(n,r)&&n[r]&&p.push(n[r][0]),n[r]=0;for(a in c)Object.prototype.hasOwnProperty.call(c,a)&&(t[a]=c[a]);u&&u(e);while(p.length)p.shift()();return o.push.apply(o,l||[]),s()}function s(){for(var t,e=0;e<o.length;e++){for(var s=o[e],a=!0,i=1;i<s.length;i++){var c=s[i];0!==n[c]&&(a=!1)}a&&(o.splice(e--,1),t=r(r.s=s[0]))}return t}var a={},n={app:0},o=[];function r(e){if(a[e])return a[e].exports;var s=a[e]={i:e,l:!1,exports:{}};return t[e].call(s.exports,s,s.exports,r),s.l=!0,s.exports}r.m=t,r.c=a,r.d=function(t,e,s){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:s})},r.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var s=Object.create(null);if(r.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var a in t)r.d(s,a,function(e){return t[e]}.bind(null,a));return s},r.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],c=i.push.bind(i);i.push=e,i=i.slice();for(var l=0;l<i.length;l++)e(i[l]);var u=c;o.push([0,"chunk-vendors"]),s()})({0:function(t,e,s){t.exports=s("56d7")},"0745":function(t,e,s){"use strict";var a=s("b9dd"),n=s.n(a);n.a},"2bb6":function(t,e,s){},"405e":function(t,e,s){},"409b":function(t,e,s){"use strict";var a=s("6767"),n=s.n(a);n.a},"513c":function(t,e,s){"use strict";var a=s("e18f"),n=s.n(a);n.a},"56d7":function(t,e,s){"use strict";s.r(e);s("e260"),s("e6cf"),s("cca6"),s("a79d"),s("f9e3");var a=s("2b0e"),n=s("5f5b"),o=s("b1e0"),r=s("0756"),i=s("f13c"),c=s.n(i),l=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"app"}},[s("ais-instant-search",{attrs:{"index-name":"prod_THEOFFICEQUOTES","search-client":t.searchClient}},[s("b-container",{staticClass:"py-3 px-lg-5 px-md-4",attrs:{fluid:!0}},[s("b-row",{staticClass:"my-3 pl-1"},[s("b-col",{attrs:{lg:"3",xl:"2",md:"12"}},[s("ais-search-box",{ref:"searchbox",attrs:{placeholder:"Search here…"},nativeOn:{keydown:function(e){return t.showResults(e)}}})],1)],1),s("b-row",[s("b-col",{attrs:{lg:"3",xl:"2",md:"12"}},[s("SeasonList")],1),s("b-col",{staticClass:"pt-md-2 pt-lg-0"},[s("router-view")],1),s("b-col",{attrs:{md:"0",lg:"0",xl:"2"}})],1)],1)],1)],1)},u=[],d=s("1320"),p=s.n(d),h=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"accordion",attrs:{role:"tablist"}},t._l(t.seasons,(function(e){return s("b-card",{key:e.season_id,staticClass:"season-card"},[s("b-card-header",{attrs:{"header-tag":"header",role:"tab"}},[s("a",{directives:[{name:"b-toggle",rawName:"v-b-toggle",value:"accordion-"+e.season_id,expression:"'accordion-' + season.season_id"}],staticClass:"no-link align-items-center justify-content-between d-flex"},[s("h5",{staticClass:"mb-0 pu-0 mu-0 season-title"},[t._v(" Season "+t._s(e.season_id)+" ")]),s("b-icon",{attrs:{icon:"chevron-down"}})],1)]),s("b-collapse",{attrs:{id:"accordion-"+e.season_id,accordion:"accordion-season-list"}},[s("b-card-body",{staticClass:"h-100 px-0"},[s("b-list-group",[t._l(e.episodes,(function(a){return[s("b-list-group-item",{key:"rl-"+a.episode_id,attrs:{id:"s-"+e.season_id+"-ep-"+a.episode_id}},[s("router-link",{staticClass:"no-link",attrs:{to:"/"+e.season_id+"/"+a.episode_id}},[t._v(" Episode "+t._s(a.episode_id)+' - "'+t._s(a.title)+'" ')])],1),s("b-popover",{key:"bpop-"+a.episode_id,attrs:{show:"",variant:"secondary",delay:"25",target:"s-"+e.season_id+"-ep-"+a.episode_id,triggers:"hover",placement:"right"},scopedSlots:t._u([{key:"title",fn:function(){return[t._v(t._s(a.title))]},proxy:!0}],null,!0)},[t._v(" "+t._s(a.description)+" ")])]}))],2)],1)],1)],1)})),1)},f=[],b=(s("99af"),s("bc3a")),_=s.n(b),m={name:"SeasonList",data:function(){return{seasons:[]}},methods:{getSeasons:function(){var t=this,e="http://".concat("192.168.2.35",":").concat("5000","/api/episodes/");_.a.get(e).then((function(e){t.seasons=e.data})).catch((function(t){console.error(t)}))}},created:function(){this.getSeasons()}},v=m,x=(s("513c"),s("2877")),g=Object(x["a"])(v,h,f,!1,null,null,null),y=g.exports,C=(s("c2ca"),{name:"App",components:{SeasonList:y},data:function(){return{searchClient:p()("W6VCX4QD3K","b71249cd1a242dc10b8dee9d285d7d0b")}},methods:{showResults:function(){""!==this.$refs.searchbox.currentRefinement&&"/search_results"!==this.$route.path&&this.$router.push({name:"SearchResults"})}}}),w=C,k=(s("5c0b"),Object(x["a"])(w,l,u,!1,null,null,null)),q=k.exports,S=s("8c4f"),E=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("b-card",{attrs:{title:"The Office Quotes"}},[s("b-card-text",[t._v(" A Vue.js application serving you "+t._s(t.stats.totals.quote)+" quotes from your favorite show - The Office. "),s("br"),t._v(" Click on a Season and Episode on the left-hand sidebar to view quotes. Search for quotes with the instant searchbox. ")])],1)},O=[],j={name:"Home",data:function(){return{stats:null}},methods:{getStats:function(){var t=this,e="http://".concat("192.168.2.35",":").concat("5000","/api/stats/");_.a.get(e).then((function(e){t.stats=e.data})).catch((function(t){console.error(t)}))}},created:function(){this.getStats()}},$=j,L=(s("8b71"),Object(x["a"])($,E,O,!1,null,null,null)),R=L.exports,T=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("b-card",{staticClass:"mb-4",attrs:{title:"Season "+this.$route.params.season+" Episode "+this.$route.params.episode+"         - "+(null!=t.episode?t.episode.title:"")}},[t.episode?s("span",[t._v(" "+t._s(t.episode.description)+" ")]):t._e(),t.episode&&t.episode.characters?s("CharacterList",{attrs:{characters:t.episode.characters}}):t._e()],1),null!=t.episode?s("div",t._l(t.episode.scenes,(function(t,e){return s("b-card",{key:"scene-"+e,staticClass:"mb-1",attrs:{id:e,"body-class":"p-0"}},[s("b-card-text",{staticClass:"my-2"},[s("QuoteList",{attrs:{quotes:t.quotes}})],1)],1)})),1):t._e()],1)},P=[],M=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("table",{staticClass:"quote-list px-3 w-100"},t._l(t.quotes,(function(e,a){return s("tr",{key:"quote-"+a},[e.speaker?s("td",{staticClass:"quote-speaker pl-3"},[s("span",{staticClass:"my-3"},[t._v(" "+t._s(e.speaker)+" ")])]):t._e(),s("td",{staticClass:"quote-text w-100 pr-3"},[t._v(t._s(e.text))])])})),0)},Q=[],H={props:["quotes"]},A=H,D=(s("0745"),Object(x["a"])(A,M,Q,!1,null,null,null)),F=D.exports,I=function(){var t=this,e=t.$createElement,s=t._self._c||e;return t.characters?s("div",{staticClass:"pt-2",attrs:{fluid:!0}},t._l(t.characters,(function(e){return s("b-button",{key:e.name,staticClass:"mx-2 my-1 character-button",attrs:{squared:"",size:"sm",id:"character-"+e.id,title:e.appearances+" Quote"+(e.appearances>1?"s":"")}},[t._v(" "+t._s(e.name)+" "),s("b-badge",{staticClass:"ml-1"},[t._v(t._s(e.appearances))])],1)})),1):t._e()},J=[],V={name:"CharacterList",props:["characters"]},z=V,B=(s("409b"),Object(x["a"])(z,I,J,!1,null,null,null)),K=B.exports,N={name:"Episode",components:{QuoteList:F,CharacterList:K},data:function(){return{episode:null}},methods:{getEpisode:function(){var t=this,e="http://".concat("192.168.2.35",":").concat("5000","/api/episode/").concat(this.$route.params.season,"/").concat(this.$route.params.episode,"/");_.a.get(e).then((function(e){t.episode=e.data})).catch((function(t){console.error(t)}))}},created:function(){this.getEpisode()},watch:{$route:function(){this.getEpisode(),console.log(this.$route.params.hash),this.$scrollTo("".concat(this.$route.hash),500,{easing:"ease-in-out"})}}},U=N,W=(s("5e68"),Object(x["a"])(U,T,P,!1,null,null,null)),X=W.exports,G=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("ais-hits",{scopedSlots:t._u([{key:"default",fn:function(e){var a=e.items;return s("div",{},t._l(a,(function(t){return s("SearchResult",{key:t.objectID,attrs:{item:t}})})),1)}}])})],1)},Y=[],Z=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("b-card",{staticClass:"mb-1",attrs:{"body-class":"p-0 expandable-result","footer-class":"my-1"},on:{click:function(e){return t.toggleExpansion()}}},[s("b-card-text",{staticClass:"mu-2 py-1 mb-1"},[t.expanded?s("table",{staticClass:"quote-list px-3 py-1 w-100"},[t._l(t.above,(function(e,a){return s("tr",{key:"quote-a-"+a},[s("td",{staticClass:"quote-speaker my-3 pl-3"},[t._v(t._s(e.speaker))]),s("td",{staticClass:"quote-text w-100 pr-3"},[t._v(t._s(e.text))])])})),s("tr",[s("td",{staticClass:"quote-speaker my-3 pl-3",domProps:{innerHTML:t._s(t.item._highlightResult.speaker.value)}}),s("td",{staticClass:"quote-text w-100 pr-3",domProps:{innerHTML:t._s(t.item._highlightResult.text.value)}})]),t._l(t.below,(function(e,a){return s("tr",{key:"quote-b-"+a},[s("td",{staticClass:"quote-speaker my-3 pl-3"},[t._v(t._s(e.speaker))]),s("td",{staticClass:"quote-text w-100 pr-3"},[t._v(t._s(e.text))])])}))],2):s("table",{staticClass:"quote-list px-3 py-1 w-100"},[t._l(t.above,(function(t,e){return s("tr",{key:"quote-a-"+e})})),s("tr",[s("td",{staticClass:"quote-speaker my-3 pl-3",domProps:{innerHTML:t._s(t.item._highlightResult.speaker.value)}}),s("td",{staticClass:"quote-text w-100 pr-3",domProps:{innerHTML:t._s(t.item._highlightResult.text.value)}})])],2),t.expanded?s("router-link",{staticClass:"no-link search-result-link w-100 text-muted mb-2 ml-2",attrs:{to:"/"+t.item.season+"/"+t.item.episode_rel+"#"+t.item.section_rel}},[t._v(" Season "+t._s(t.item.season)+" Episode "+t._s(t.item.episode_rel)+" Scene "+t._s(t.item.section_rel)+" ")]):t._e()],1)],1)},tt=[],et={props:["item"],data:function(){return{expanded:!1,hasExpanded:!1,above:null,below:null}},methods:{toggleExpansion:function(){this.expanded=!this.expanded,!this.hasExpanded&&this.expanded&&(this.hasExpanded=!0,this.fetchQuotes())},fetchQuotes:function(){var t=this,e="http://".concat("192.168.2.35",":").concat("5000","/api/quote_surround?season=").concat(this.item.season,"&episode=").concat(this.item.episode_rel,"&scene=").concat(this.item.section_rel,"&quote=").concat(this.item.quote_rel);_.a.get(e).then((function(e){t.above=e.data.above,t.below=e.data.below})).catch((function(t){console.error(t)}))}}},st=et,at=(s("a219"),Object(x["a"])(st,Z,tt,!1,null,null,null)),nt=at.exports,ot={name:"SearchResults",components:{SearchResult:nt}},rt=ot,it=(s("ad06"),Object(x["a"])(rt,G,Y,!1,null,null,null)),ct=it.exports;a["default"].use(S["a"]);var lt=new S["a"]({mode:"history",base:"/",routes:[{path:"/",name:"Home",component:R},{path:"/:season/:episode",name:"Episode",component:X},{path:"/search_results",name:"SearchResults",component:ct}],scrollBehavior:function(t,e,s){return t.hash?{selector:t.hash}:s||{x:0,y:0}}});a["default"].use(c.a),a["default"].use(n["a"]),a["default"].use(o["a"]),a["default"].use(r["a"]),a["default"].config.productionTip=!1,new a["default"]({router:lt,render:function(t){return t(q)}}).$mount("#app")},"5c0b":function(t,e,s){"use strict";var a=s("9c0c"),n=s.n(a);n.a},"5e68":function(t,e,s){"use strict";var a=s("405e"),n=s.n(a);n.a},6767:function(t,e,s){},"88d7":function(t,e,s){},"8b71":function(t,e,s){"use strict";var a=s("88d7"),n=s.n(a);n.a},"9c0c":function(t,e,s){},a219:function(t,e,s){"use strict";var a=s("b6f6"),n=s.n(a);n.a},ad06:function(t,e,s){"use strict";var a=s("2bb6"),n=s.n(a);n.a},b6f6:function(t,e,s){},b9dd:function(t,e,s){},e18f:function(t,e,s){}});
//# sourceMappingURL=app.45bcd808.js.map