// This code is adapted from here: http://bl.ocks.org/nbremer/6506614
// I changed it to accept user input for changing axis values
// Also some adjustments were made with coloring and positioning

var d = [
		  [
           {axis:"Strength", value:0.2},
           {axis:"Extraction", value:0.2},
           {axis:"Acidity", value:0.2},
           {axis:"Overall Score", value:0.2},
           {axis:"Aftertaste", value:0.2},
           {axis:"Body", value:0.2}
		  ]
		];

var RadarChart = {
  draw: function(id, d, options){
  var cfg = {
	 radius: 5,
	 w: 600,
	 h: 600,
	 factor: 1,
	 factorLegend: .85,
	 levels: 3,
	 maxValue: 0,
	 radians: 2 * Math.PI,
	 opacityArea: 0.5,
	 ToRight: 5,
	 TranslateX: 150,
	 TranslateY: 30,
	 ExtraWidthX: 00,
	 ExtraWidthY: 00,
	 color: d3.scale.category10()
	};

	if('undefined' !== typeof options){
	  for(var i in options){
		if('undefined' !== typeof options[i]){
		  cfg[i] = options[i];
		}
	  }
	}
	cfg.maxValue = Math.max(cfg.maxValue, d3.max(d, function(i){return d3.max(i.map(function(o){return o.value;}))}));
	var allAxis = (d[0].map(function(i, j){return i.axis}));
	var total = allAxis.length;
	var radius = cfg.factor*Math.min(cfg.w/2, cfg.h/2);
	var Format = d3.format('%');
	d3.select(id).select("svg").remove();

   series = 0;

	var g = d3.select(id)
			.append("svg")
			.attr("width", cfg.w+cfg.ExtraWidthX)
			.attr("height", cfg.h+cfg.ExtraWidthY)
			.append("g")
			.attr("transform", "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")");

         // builds the polygon inside the graph
      	d.forEach(function(y, x){
      	  dataValues = [];
      	  g.selectAll(".nodes")
      		.data(y, function(j, i){
      		  dataValues.push([
      			cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)),
      			cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
      		  ]);
      		});
      	  dataValues.push(dataValues[0]);
      	  g.selectAll(".area")
      					 .data([dataValues])
      					 .enter()
      					 .append("polygon")
      					 .attr("class", "radar-chart-serie"+series)
      					 .style("stroke-width", "2px")
      					 .style("stroke", cfg.color(series))
      					 .attr("points",function(d) {
      						 var str="";
      						 for(var pti=0;pti<d.length;pti++){
      							 str=str+d[pti][0]+","+d[pti][1]+" ";
      						 }
      						 return str;
      					  })
      					 .style("fill", function() { return cfg.color(0)})
                      .style("fill-opacity", 0.2)
      	  series++;
      	});
      	series=0;

	//Circular segments
	for(var j=0; j<cfg.levels-1; j++){
	  var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
	  g.selectAll(".levels")
	   .data(allAxis)
	   .enter()
	   .append("svg:line")
	   .attr("x1", function(d, i){return levelFactor*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
	   .attr("y1", function(d, i){return levelFactor*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
	   .attr("x2", function(d, i){return levelFactor*(1-cfg.factor*Math.sin((i+1)*cfg.radians/total));})
	   .attr("y2", function(d, i){return levelFactor*(1-cfg.factor*Math.cos((i+1)*cfg.radians/total));})
	   .attr("class", "line")
	   .style("stroke", "grey")
	   .style("stroke-opacity", "0.75")
	   .style("stroke-width", "3px")
	   .attr("transform", "translate(" + (cfg.w/2-levelFactor) + ", " + (cfg.h/2-levelFactor) + ")")
      .attr("class", "level" + (cfg.w/2-levelFactor))
      .on("mouseenter", function(d) {
         d3.selectAll("." + d3.select(this).attr("class"))
            .style("stroke", "black")
            .style("opacity", "0.75")
            .style("stroke-width", "4px")
      })
      .on("mouseleave", function(d) {
         d3.selectAll("." + d3.select(this).attr("class"))
         .style("stroke", "grey")
         .style("stroke-opacity", "0.75")
         .style("stroke-width", "3px")
      });
	}


	var axis = g.selectAll(".axis")
			.data(allAxis)
			.enter()
			.append("g")
			.attr("class", "axis");

	axis.append("line")
		.attr("x1", cfg.w/2)
		.attr("y1", cfg.h/2)
		.attr("x2", function(d, i){return cfg.w/2*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
		.attr("y2", function(d, i){return cfg.h/2*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
		.attr("class", "line")
		.style("stroke", "grey")
		.style("stroke-width", "1px");

	axis.append("text")
		.attr("class", "legend")
		.text(function(d){return d})
		.style("font-family", "sans-serif")
		.style("font-size", "11px")
		.attr("text-anchor", "middle")
		.attr("dy", "1.5em")
		.attr("transform", function(d, i){return "translate(0, -10)"})
		.attr("x", function(d, i){return cfg.w/2*(1-cfg.factorLegend*Math.sin(i*cfg.radians/total))-60*Math.sin(i*cfg.radians/total);})
		.attr("y", function(d, i){return cfg.h/2*(1-Math.cos(i*cfg.radians/total))-20*Math.cos(i*cfg.radians/total);});


   // builds the nodes at each vertex of the polygon
	d.forEach(function(y){
	  g.selectAll(".nodes")
		.data(y).enter()
		.append("svg:circle")
		.attr("class", "radar-chart-serie"+series)
		.attr('r', cfg.radius)
		.attr("alt", function(j){return Math.max(j.value, 0)})
		.attr("cx", function(j, i){
		  dataValues.push([
			cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)),
			cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
		    ]);
		return cfg.w/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total));
		})
		.attr("cy", function(j, i){
		  return cfg.h/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total));
		})
		.attr("data-id", function(j){return j.axis})
		.style("fill", cfg.color(series)).style("fill-opacity", .9)
		.append("svg:title")
		.text(function(j){return Math.max(j.value, 0)});

	  series++;
	});

   // build the secret hidden buttons!
   buttonArr = [d[0].length * 5]
   posInd = 0;
   for (i = 0; i < d[0].length * 5; i++) {
      buttonArr[i] = {axis:i % d[0].length, value:posInd}
      posInd = (posInd + 0.2) % 1
   }

   g.selectAll(".changeButton")
      .data(buttonArr).enter()
      .append("svg:circle")
      .attr('r', cfg.radius * 2.5)
      .attr("cx", function(j, i){
		  dataValues.push([
			cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(j.axis*cfg.radians/total)),
			cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(j.axis*cfg.radians/total))
		    ]);
		return cfg.w/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.sin(j.axis*cfg.radians/total));
		})
		.attr("cy", function(j, i){
		  return cfg.h/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.cos(j.axis*cfg.radians/total));
		})
      .style("fill", "black")
      .style("fill-opacity", "0")
      //.style("stroke", "black")
      .on("click", function(data) {
         var newD = d.slice()
         newD[0][data.axis].value = data.value
         d[0][data.axis].value = data.value
         //d[0].push({"axis":d[0][data.axis].axis, "value":data.value})
         update(newD, cfg, total)
      })
  }
};


// redraw the graph
function update(newD, cfg, total) {
   console.log("updating")
   // move the polygon
   dataValues = [];
   d3.selectAll(".nodes")
    .data(newD[0], function(j, i){
      console.log(j)
     dataValues.push([
      cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)),
      cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
     ]);
    });
   dataValues.push(dataValues[0]);
   d3.selectAll("polygon").data([dataValues])
      .transition().duration(500)
    .attr("points",function(d) {
        var str="";
        for(var pti=0;pti<d.length;pti++){
           str=str+d[pti][0]+","+d[pti][1]+" ";
        }
        return str;
      })

   // move the dots
   d3.selectAll("circle").filter(".radar-chart-serie0").data(newD[0])
      .transition().duration(500)
      .attr("cx", function(j, i){
         dataValues.push([
            cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)),
            cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
        ]);
        return cfg.w/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total));
      })
      .attr("cy", function(j, i){
         return cfg.h/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total));
      })

}

function getData() {
	console.log("we out here bruh")
   var descriptors = [];
   var elem = document.getElementsByClassName("stayActive");
   for (var i = 0; i < elem.length; i++) {
      descriptors.push(elem[i].id)
      console.log(elem[i].id)
   }
   console.log(descriptors);
   console.log(d[0][0]);
	attributes = []

	for (obj in d[0]) {
		attributes.push({axis:obj.axis, value:obj.value})
	}
	console.log(attributes)

	var form = document.getElementsByClassName("tastingData")[0];
	console.log(form)

	var hidden = document.createElement("input");
	hidden.setAttribute("type", "hidden");
	hidden.setAttribute("name", "descriptors")
	hidden.setAttribute("value", descriptors)
	form.appendChild(hidden);

	for (var i = 0; i < d[0].length; i++) {
		hidden = document.createElement("input");
		hidden.setAttribute("type", "hidden");
		hidden.setAttribute("name", d[0][i].axis)
		hidden.setAttribute("value", d[0][i].value)
		form.appendChild(hidden);
	}




	return false;
}
