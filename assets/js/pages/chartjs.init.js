function getChartColorsArray(r){if(null!==document.getElementById(r)){r=document.getElementById(r).getAttribute("data-colors");if(r)return(r=JSON.parse(r)).map(function(r){var o=r.replace(" ","");return-1===o.indexOf(",")?getComputedStyle(document.documentElement).getPropertyValue(o)||o:2==(r=r.split(",")).length?"rgba("+getComputedStyle(document.documentElement).getPropertyValue(r[0])+","+r[1]+")":o})}}!function(i){"use strict";function r(){}r.prototype.respChart=function(r,o,e,t){Chart.defaults.global.defaultFontColor="#9295a4",Chart.defaults.scale.gridLines.color="rgba(166, 176, 207, 0.1)";var a=r.get(0).getContext("2d"),n=i(r).parent();function l(){r.attr("width",i(n).width());switch(o){case"Line":new Chart(a,{type:"line",data:e,options:t});break;case"Doughnut":new Chart(a,{type:"doughnut",data:e,options:t});break;case"Pie":new Chart(a,{type:"pie",data:e,options:t});break;case"Bar":new Chart(a,{type:"bar",data:e,options:t});break;case"Radar":new Chart(a,{type:"radar",data:e,options:t});break;case"PolarArea":new Chart(a,{data:e,type:"polarArea",options:t})}}i(window).resize(l),l()},r.prototype.init=function(){var r=getChartColorsArray("lineChart"),r=(r&&(r={labels:["January","February","March","April","May","June","July","August","September","October"],datasets:[{label:"Sales Analytics",fill:!0,lineTension:.5,backgroundColor:r[0],borderColor:r[1],borderCapStyle:"butt",borderDash:[],borderDashOffset:0,borderJoinStyle:"miter",pointBorderColor:r[1],pointBackgroundColor:"#fff",pointBorderWidth:1,pointHoverRadius:5,pointHoverBackgroundColor:r[1],pointHoverBorderColor:"#fff",pointHoverBorderWidth:2,pointRadius:1,pointHitRadius:10,data:[65,59,80,81,56,55,40,55,30,80]},{label:"Monthly Earnings",fill:!0,lineTension:.5,backgroundColor:r[2],borderColor:r[3],borderCapStyle:"butt",borderDash:[],borderDashOffset:0,borderJoinStyle:"miter",pointBorderColor:r[3],pointBackgroundColor:"#fff",pointBorderWidth:1,pointHoverRadius:5,pointHoverBackgroundColor:r[3],pointHoverBorderColor:"#eef0f2",pointHoverBorderWidth:2,pointRadius:1,pointHitRadius:10,data:[80,23,56,65,23,35,85,25,92,36]}]},this.respChart(i("#lineChart"),"Line",r,{scales:{yAxes:[{ticks:{max:100,min:20,stepSize:10}}]}})),getChartColorsArray("doughnut")),r=(r&&(r={labels:["Desktops","Tablets"],datasets:[{data:[300,210],backgroundColor:r,hoverBackgroundColor:r,hoverBorderColor:"#fff"}]},this.respChart(i("#doughnut"),"Doughnut",r)),getChartColorsArray("pie")),r=(r&&(r={labels:["Desktops","Tablets"],datasets:[{data:[300,180],backgroundColor:r,hoverBackgroundColor:r,hoverBorderColor:"#fff"}]},this.respChart(i("#pie"),"Pie",r)),getChartColorsArray("bar")),r=(r&&(r={labels:["January","February","March","April","May","June","July"],datasets:[{label:"Sales Analytics",backgroundColor:r[0],borderColor:r[0],borderWidth:1,hoverBackgroundColor:r[1],hoverBorderColor:r[1],data:[65,59,81,45,56,80,50,20]}]},this.respChart(i("#bar"),"Bar",r,{scales:{xAxes:[{barPercentage:.4}]}})),getChartColorsArray("radar")),r=(r&&(r={labels:["Eating","Drinking","Sleeping","Designing","Coding","Cycling","Running"],datasets:[{label:"Desktops",backgroundColor:r[0],borderColor:r[1],pointBackgroundColor:r[1],pointBorderColor:"#fff",pointHoverBackgroundColor:"#fff",pointHoverBorderColor:r[1],data:[65,59,90,81,56,55,40]},{label:"Tablets",backgroundColor:r[2],borderColor:r[3],pointBackgroundColor:r[3],pointBorderColor:"#fff",pointHoverBackgroundColor:"#fff",pointHoverBorderColor:r[3],data:[28,48,40,19,96,27,100]}]},this.respChart(i("#radar"),"Radar",r)),getChartColorsArray("polarArea"));r&&(r={datasets:[{data:[11,16,7,18],backgroundColor:r,label:"My dataset",hoverBorderColor:"#fff"}],labels:["Series 1","Series 2","Series 3","Series 4"]},this.respChart(i("#polarArea"),"PolarArea",r))},i.ChartJs=new r,i.ChartJs.Constructor=r}(window.jQuery),function(){"use strict";window.jQuery.ChartJs.init()}();